"""Сервис для работы с путешествиями"""
from flask import jsonify

from exam.src.minio_service import FileType
from storage import TripRepository, UserRepository
import json


class TripService:
    """Класс для работы с путешествиями"""

    def __init__(self, db, minio_service):
        self.db = db
        self.minio_service = minio_service

    def get_trip_repository(self):
        """Получить репозиторий для работы с данными"""
        session = self.db.get_session()
        return TripRepository(session), session

    def get_user_repository(self):
        """Получить репозиторий для работы с пользователями"""
        session = self.db.get_session()
        return UserRepository(session), session

    @staticmethod
    def check_if_trip_belongs_to_user(trip, user_id):
        trip_users_id = []
        for user in trip.users:
            trip_users_id.append(user.id)

        return user_id in trip_users_id

    def get_user_trips(self, user_id):
        """Получить все путешествия пользователя"""
        user_repository, user_session = self.get_user_repository()
        try:
            trips = user_repository.get_user_trips(user_id)
            return jsonify([trip.to_dict() for trip in trips]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            user_session.close()

    def get_trip(self, user_id, trip_id):
        """Получить путешествие по ID (только если принадлежит пользователю)"""
        repository, session = self.get_trip_repository()
        try:
            trip = repository.get_by_id(int(trip_id))
            if not trip:
                return jsonify({'error': 'Путешествие не найдено'}), 404

            if not self.check_if_trip_belongs_to_user(trip, user_id):
                return jsonify({'error': 'Доступ запрещен'}), 403

            return jsonify(trip.to_dict()), 200
        except ValueError as e:
            print(f'Error: {e}')
            return jsonify({'error': 'Неверный формат ID'}), 400
        except Exception as e:
            print(f'Error: {e}')
            return jsonify({'error': str(e)}), 500
        finally:
            session.close()

    def create_trip(self, user_id, content_type, form, files, get_json_func):
        """Создать новое путешествие"""
        repository, session = self.get_trip_repository()
        user_repository, user_session = self.get_user_repository()
        try:
            # Получаем следующий trip_id
            next_trip_id = repository.get_next_trip_id()

            # Проверяем, есть ли файлы в запросе
            if content_type and 'multipart/form-data' in content_type:
                # Обработка multipart/form-data
                data = json.loads(form['trip'])

                # Обработка файлов для билетов
                for i, ticket in enumerate(data.get('tickets', [])):
                    file_key = f'ticket_file_{i}'
                    if file_key in files:
                        file = files[file_key]
                        file_url = self.minio_service.upload_file_to_minio(file, next_trip_id, FileType.TICKET)
                        if file_url:
                            ticket['fileUrl'] = file_url

                # Обработка файлов для размещений
                for i, accommodation in enumerate(data.get('accommodations', [])):
                    file_key = f'accommodation_file_{i}'
                    if file_key in files:
                        file = files[file_key]
                        file_url = self.minio_service.upload_file_to_minio(file, next_trip_id, FileType.ACCOMMODATION)
                        if file_url:
                            accommodation['fileUrl'] = file_url
            else:
                # Обычный JSON запрос
                data = get_json_func()

            # Валидация обязательных полей
            if not data.get('name'):
                return jsonify({'error': 'Название путешествия обязательно'}), 400

            # Создание нового путешествия через репозиторий
            data['id'] = next_trip_id
            new_trip = repository.create(data)

            # Связываем путешествие с пользователем
            user = user_repository.get_by_id(user_id)
            if user:
                user_repository.add_trip_to_user(user_id, new_trip.id)

            return jsonify(new_trip.to_dict()), 201

        except Exception as e:
            session.rollback()
            user_session.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            session.close()
            user_session.close()

    def update_trip(self, user_id, trip_id, content_type, form, files, get_json_func):
        """Обновить путешествие"""
        repository, session = self.get_trip_repository()
        try:
            # Проверка прав доступа
            trip = repository.get_by_id(int(trip_id))
            if not trip:
                return jsonify({'error': 'Путешествие не найдено'}), 404

            if not self.check_if_trip_belongs_to_user(trip, user_id):
                return jsonify({'error': 'Доступ запрещен'}), 403

            # Проверяем, есть ли файлы в запросе
            if content_type and 'multipart/form-data' in content_type:
                # Обработка multipart/form-data
                if 'trip' in form:
                    data = json.loads(form['trip'])
                else:
                    # Если данные не в JSON, собираем из form
                    data = {
                        'name': form.get('name'),
                        'startDate': form.get('startDate'),
                        'endDate': form.get('endDate'),
                        'tickets': json.loads(form.get('tickets', '[]')) if form.get('tickets') else [],
                        'accommodations': json.loads(form.get('accommodations', '[]')) if form.get(
                            'accommodations') else [],
                        'notes': json.loads(form.get('notes', '[]')) if form.get('notes') else []
                    }

                # Обработка файлов для билетов
                for i, ticket in enumerate(data.get('tickets', [])):
                    file_key = f'ticket_file_{i}'
                    if file_key in files:
                        file = files[file_key]
                        # Удаляем старый файл, если есть
                        if ticket.get('fileUrl'):
                            self.minio_service.delete_file(ticket['fileUrl'])
                        # Загружаем новый файл
                        file_url = self.minio_service.upload_file_to_minio(file, trip_id, FileType.TICKET)
                        if file_url:
                            ticket['fileUrl'] = file_url

                # Обработка файлов для размещений
                for i, accommodation in enumerate(data.get('accommodations', [])):
                    file_key = f'accommodation_file_{i}'
                    if file_key in files:
                        file = files[file_key]
                        # Удаляем старый файл, если есть
                        if accommodation.get('fileUrl'):
                            self.minio_service.delete_file(accommodation['fileUrl'])
                        # Загружаем новый файл
                        file_url = self.minio_service.upload_file_to_minio(file, trip_id, FileType.ACCOMMODATION)
                        if file_url:
                            accommodation['fileUrl'] = file_url
            else:
                # Обычный JSON запрос
                data = get_json_func()

            # Обновление путешествия через репозиторий
            updated_trip = repository.update(int(trip_id), data)
            if not updated_trip:
                return jsonify({'error': 'Путешествие не найдено'}), 404

            return jsonify(updated_trip.to_dict()), 200

        except ValueError:
            return jsonify({'error': 'Неверный формат ID'}), 400
        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            session.close()

    def delete_trip(self, user_id, trip_id):
        """Удалить путешествие"""
        repository, session = self.get_trip_repository()
        user_repository, user_session = self.get_user_repository()
        try:
            # Получаем путешествие перед удалением, чтобы удалить файлы
            trip = repository.get_by_id(int(trip_id))
            if not trip:
                return jsonify({'error': 'Путешествие не найдено'}), 404

            # Проверка прав доступа
            user = user_repository.get_by_id(user_id)
            if user and trip not in user.trips:
                return jsonify({'error': 'Доступ запрещен'}), 403

            # Удаляем файлы из MinIO
            for ticket in trip.tickets:
                if ticket.file_url:
                    self.minio_service.delete_file(ticket.file_url)

            for accommodation in trip.accommodations:
                if accommodation.file_url:
                    self.minio_service.delete_file(accommodation.file_url)

            # Удаляем путешествие из БД
            success = repository.delete(int(trip_id))
            if not success:
                return jsonify({'error': 'Ошибка при удалении путешествия'}), 500

            return jsonify({'message': 'Путешествие удалено'}), 200
        except ValueError:
            return jsonify({'error': 'Неверный формат ID'}), 400
        except Exception as e:
            session.rollback()
            user_session.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            session.close()
            user_session.close()
