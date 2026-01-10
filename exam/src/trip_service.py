"""Сервис для работы с путешествиями"""
from flask import jsonify
from storage import TripRepository
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

    def get_trips(self):
        """Получить все путешествия"""
        repository, session = self.get_trip_repository()
        try:
            trips = repository.get_all()
            return jsonify([trip.to_dict() for trip in trips]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            session.close()

    def get_trip(self, trip_id):
        """Получить путешествие по ID"""
        repository, session = self.get_trip_repository()
        try:
            trip = repository.get_by_id(int(trip_id))
            if trip:
                return jsonify(trip.to_dict()), 200
            return jsonify({'error': 'Путешествие не найдено'}), 404
        except ValueError:
            return jsonify({'error': 'Неверный формат ID'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            session.close()

    def create_trip(self, content_type, form, files, get_json_func):
        """Создать новое путешествие"""
        repository, session = self.get_trip_repository()
        try:
            # Проверяем, есть ли файлы в запросе
            if content_type and 'multipart/form-data' in content_type:
                # Обработка multipart/form-data
                data = json.loads(form['trip'])

                # Обработка файлов для билетов
                for i, ticket in enumerate(data.get('tickets', [])):
                    file_key = f'ticket_file_{i}'
                    if file_key in files:
                        file = files[file_key]
                        file_url = self.minio_service.upload_file_to_minio(file)
                        if file_url:
                            ticket['fileUrl'] = file_url

                # Обработка файлов для размещений
                for i, accommodation in enumerate(data.get('accommodations', [])):
                    file_key = f'accommodation_file_{i}'
                    if file_key in files:
                        file = files[file_key]
                        file_url = self.minio_service.upload_file_to_minio(file)
                        if file_url:
                            accommodation['fileUrl'] = file_url
            else:
                # Обычный JSON запрос
                data = get_json_func()

            # Валидация обязательных полей
            if not data.get('name'):
                return jsonify({'error': 'Название путешествия обязательно'}), 400

            # Создание нового путешествия через репозиторий
            new_trip = repository.create(data)
            return jsonify(new_trip.to_dict()), 201

        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            session.close()

    def update_trip(self, trip_id, content_type, form, files, get_json_func):
        """Обновить путешествие"""
        repository, session = self.get_trip_repository()
        try:
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
                        file_url = self.minio_service.upload_file_to_minio(file)
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
                        file_url = self.minio_service.upload_file_to_minio(file)
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

    def delete_trip(self, trip_id):
        """Удалить путешествие"""
        repository, session = self.get_trip_repository()
        try:
            # Получаем путешествие перед удалением, чтобы удалить файлы
            trip = repository.get_by_id(int(trip_id))
            if not trip:
                return jsonify({'error': 'Путешествие не найдено'}), 404

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
            return jsonify({'error': str(e)}), 500
        finally:
            session.close()
