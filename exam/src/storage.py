"""Репозитории для работы с данными"""
from sqlalchemy.orm import Session
from datetime import datetime

from exam.src.models import trips_id_seq
from models import Trip, Ticket, Accommodation, Note, User
from typing import List, Optional, Dict, Any


class TripRepository:
    """Репозиторий для работы с путешествиями"""

    def __init__(self, session: Session):
        """
        Инициализация репозитория
        
        Args:
            session: SQLAlchemy сессия
        """
        self.session = session

    @staticmethod
    def _parse_datetime(date_string: str | None) -> datetime | None:
        """
        Преобразовать строку даты в datetime объект
        
        Args:
            date_string: Строка даты в формате ISO или datetime-local
            
        Returns:
            datetime объект или None
        """
        if not date_string:
            return None
        try:
            # Пробуем разные форматы
            if 'T' in date_string:
                # Формат datetime-local: YYYY-MM-DDTHH:mm
                return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            else:
                # Формат date: YYYY-MM-DD
                return datetime.fromisoformat(date_string)
        except (ValueError, AttributeError):
            return None

    def get_all(self) -> list[type[Trip]]:
        """
        Получить все путешествия
        
        Returns:
            List[Trip]: Список всех путешествий
        """
        return self.session.query(Trip).all()

    def get_by_id(self, trip_id: int) -> Optional[Trip]:
        """
        Получить путешествие по ID
        
        Args:
            trip_id: ID путешествия
            
        Returns:
            Optional[Trip]: Путешествие или None, если не найдено
        """
        return self.session.query(Trip).filter(Trip.id == trip_id).first()

    def create(self, trip_data: Dict[str, Any]) -> Trip:
        """
        Создать новое путешествие
        
        Args:
            trip_data: Данные путешествия
            
        Returns:
            Trip: Созданное путешествие
        """
        # Создание основного объекта путешествия
        trip = Trip(
            id=trip_data.get('id', ''),
            name=trip_data.get('name', ''),
            start_date=self._parse_datetime(trip_data.get('startDate')),
            end_date=self._parse_datetime(trip_data.get('endDate'))
        )

        # Добавление билетов (используем relationship, trip_id установится автоматически)
        for ticket_data in trip_data.get('tickets', []):
            ticket = Ticket(
                type=ticket_data.get('type'),
                departure=ticket_data.get('departure'),
                arrival=ticket_data.get('arrival'),
                departure_time=self._parse_datetime(ticket_data.get('departureTime')),
                arrival_time=self._parse_datetime(ticket_data.get('arrivalTime')),
                file_url=ticket_data.get('fileUrl')
            )
            trip.tickets.append(ticket)

        # Добавление размещений (используем relationship, trip_id установится автоматически)
        for accommodation_data in trip_data.get('accommodations', []):
            accommodation = Accommodation(
                type=accommodation_data.get('type'),
                name=accommodation_data.get('name'),
                address=accommodation_data.get('address'),
                check_in_date=self._parse_datetime(accommodation_data.get('checkInDate')),
                check_out_date=self._parse_datetime(accommodation_data.get('checkOutDate')),
                file_url=accommodation_data.get('fileUrl')
            )
            trip.accommodations.append(accommodation)

        # Добавление заметок (используем relationship, trip_id установится автоматически)
        for note_data in trip_data.get('notes', []):
            note = Note(
                title=note_data.get('title'),
                content=note_data.get('content')
            )
            trip.notes.append(note)

        self.session.add(trip)
        self.session.commit()
        self.session.refresh(trip)
        return trip

    def update(self, trip_id: int, trip_data: Dict[str, Any]) -> Optional[Trip]:
        """
        Обновить путешествие
        
        Args:
            trip_id: ID путешествия
            trip_data: Новые данные путешествия
            
        Returns:
            Optional[Trip]: Обновленное путешествие или None, если не найдено
        """
        trip = self.get_by_id(trip_id)
        if not trip:
            return None

        # Обновление основных полей
        if 'name' in trip_data:
            trip.name = trip_data.get('name')
        if 'startDate' in trip_data:
            trip.start_date = self._parse_datetime(trip_data.get('startDate'))
        if 'endDate' in trip_data:
            trip.end_date = self._parse_datetime(trip_data.get('endDate'))

        # Удаление старых связанных объектов
        self.session.query(Ticket).filter(Ticket.trip_id == trip_id).delete()
        self.session.query(Accommodation).filter(Accommodation.trip_id == trip_id).delete()
        self.session.query(Note).filter(Note.trip_id == trip_id).delete()

        # Добавление новых билетов
        for ticket_data in trip_data.get('tickets', []):
            ticket = Ticket(
                trip_id=trip_id,
                type=ticket_data.get('type'),
                departure=ticket_data.get('departure'),
                arrival=ticket_data.get('arrival'),
                departure_time=self._parse_datetime(ticket_data.get('departureTime')),
                arrival_time=self._parse_datetime(ticket_data.get('arrivalTime')),
                file_url=ticket_data.get('fileUrl')
            )
            trip.tickets.append(ticket)

        # Добавление новых размещений
        for accommodation_data in trip_data.get('accommodations', []):
            accommodation = Accommodation(
                trip_id=trip_id,
                type=accommodation_data.get('type'),
                name=accommodation_data.get('name'),
                address=accommodation_data.get('address'),
                check_in_date=self._parse_datetime(accommodation_data.get('checkInDate')),
                check_out_date=self._parse_datetime(accommodation_data.get('checkOutDate')),
                file_url=accommodation_data.get('fileUrl')
            )
            trip.accommodations.append(accommodation)

        # Добавление новых заметок
        for note_data in trip_data.get('notes', []):
            note = Note(
                trip_id=trip_id,
                title=note_data.get('title'),
                content=note_data.get('content')
            )
            trip.notes.append(note)

        self.session.commit()
        self.session.refresh(trip)
        return trip

    def delete(self, trip_id: int) -> bool:
        """
        Удалить путешествие
        
        Args:
            trip_id: ID путешествия
            
        Returns:
            bool: True, если удалено успешно, False если не найдено
        """
        trip = self.get_by_id(trip_id)
        if not trip:
            return False

        self.session.delete(trip)
        self.session.commit()
        return True

    def get_next_trip_id(self):
        next_id = self.session.query(trips_id_seq.next_value()).scalar()
        return next_id


class UserRepository:
    """Репозиторий для работы с пользователями"""

    def __init__(self, session: Session):
        """
        Инициализация репозитория
        
        Args:
            session: SQLAlchemy сессия
        """
        self.session = session

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Получить пользователя по username
        
        Args:
            username: Username пользователя
            
        Returns:
            Optional[User]: Пользователь или None, если не найден
        """
        return self.session.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Получить пользователя по ID
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Optional[User]: Пользователь или None, если не найден
        """
        return self.session.query(User).filter(User.id == user_id).first()

    def create(self, username: str, password: str) -> User:
        """
        Создать нового пользователя
        
        Args:
            username: username пользователя
            password: Пароль пользователя
            
        Returns:
            User: Созданный пользователь
        """
        user = User(username=username)
        user.set_password(password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def add_trip_to_user(self, user_id: int, trip_id: int) -> bool:
        """
        Добавить путешествие пользователю
        
        Args:
            user_id: ID пользователя
            trip_id: ID путешествия
            
        Returns:
            bool: True, если успешно добавлено
        """
        user = self.get_by_id(user_id)
        trip = self.session.query(Trip).filter(Trip.id == trip_id).first()

        if not user or not trip:
            return False

        if trip not in user.trips:
            user.trips.append(trip)
            self.session.commit()

        return True

    def get_user_trips(self, user_id: int) -> List[Trip]:
        """
        Получить все путешествия пользователя
        
        Args:
            user_id: ID пользователя
            
        Returns:
            List[Trip]: Список путешествий пользователя
        """
        user = self.get_by_id(user_id)
        if not user:
            return []
        return user.trips
