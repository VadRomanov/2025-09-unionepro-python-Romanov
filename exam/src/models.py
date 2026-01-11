"""Модели данных для приложения планировщика путешествий"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, BigInteger, Table, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import hashlib

Base = declarative_base()

# Последовательность для trips id
trips_id_seq = Sequence('trips_id_seq', Base.metadata)

# Таблица связи многие-ко-многим между пользователями и путешествиями
trip_users = Table(
    'trip_users',
    Base.metadata,
    Column('trip_id', BigInteger, ForeignKey('trips.id', ondelete='CASCADE'), primary_key=True),
    Column('user_id', BigInteger, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
)


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    language_code = Column(String(10))
    password_hash = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    
    # Связь с путешествиями
    trips = relationship("Trip", secondary=trip_users, back_populates="users")
    
    def set_password(self, password: str):
        """Установить пароль (хэширование)"""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password: str) -> bool:
        """Проверить пароль"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.password_hash == password_hash

    def to_dict(self):
        """Преобразование объекта в словарь для JSON"""
        return {
            'id': self.id,
            'telegramId': self.telegram_id,
            'username': self.username,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'languageCode': self.language_code,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class Trip(Base):
    """Модель путешествия"""
    __tablename__ = 'trips'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    # Связи с дочерними таблицами
    tickets = relationship("Ticket", back_populates="trip", cascade="all, delete-orphan")
    accommodations = relationship("Accommodation", back_populates="trip", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="trip", cascade="all, delete-orphan")
    
    # Связь с пользователями
    users = relationship("User", secondary=trip_users, back_populates="trips")
    
    def to_dict(self):
        """Преобразование объекта в словарь для JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'tickets': [ticket.to_dict() for ticket in self.tickets],
            'accommodations': [accommodation.to_dict() for accommodation in self.accommodations],
            'notes': [note.to_dict() for note in self.notes]
        }
    
    def __repr__(self):
        return f"<Trip(id={self.id}, trip_name={self.name})>"


class Ticket(Base):
    """Модель билета"""
    __tablename__ = 'tickets'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey('trips.id', ondelete='CASCADE'), nullable=False)
    type = Column(String(50))
    departure = Column(String(255))
    arrival = Column(String(255))
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    file_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    
    # Связь с путешествием
    trip = relationship("Trip", back_populates="tickets")
    
    def to_dict(self):
        """Преобразование объекта в словарь для JSON"""
        return {
            'id': self.id,
            'tripId': self.trip_id,
            'type': self.type,
            'departure': self.departure,
            'arrival': self.arrival,
            'departureTime': self.departure_time,
            'arrivalTime': self.arrival_time,
            'fileUrl': self.file_url,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Ticket(id={self.id}, type={self.type})>"


class Accommodation(Base):
    """Модель размещения"""
    __tablename__ = 'accommodations'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey('trips.id', ondelete='CASCADE'), nullable=False)
    type = Column(String(50))
    name = Column(String(255))
    address = Column(String(500))
    check_in_date = Column(DateTime)
    check_out_date = Column(DateTime)
    file_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    
    # Связь с путешествием
    trip = relationship("Trip", back_populates="accommodations")
    
    def to_dict(self):
        """Преобразование объекта в словарь для JSON"""
        return {
            'id': self.id,
            'tripId': self.trip_id,
            'type': self.type,
            'name': self.name,
            'address': self.address,
            'checkInDate': self.check_in_date,
            'checkOutDate': self.check_out_date,
            'fileUrl': self.file_url,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Accommodation(id={self.id}, name={self.name})>"


class Note(Base):
    """Модель заметки"""
    __tablename__ = 'notes'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trip_id = Column(BigInteger, ForeignKey('trips.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    # Связь с путешествием
    trip = relationship("Trip", back_populates="notes")
    
    def to_dict(self):
        """Преобразование объекта в словарь для JSON"""
        return {
            'id': self.id,
            'tripId': self.trip_id,
            'title': self.title,
            'content': self.content,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Note(id={self.id}, title={self.title})>"

