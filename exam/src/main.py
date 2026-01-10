from flask import Flask, request
from flask_cors import CORS
from database import Database
from exam.src.minio_service import MinIOService
from exam.src.trip_service import TripService
from minio_client import MinIOClient

# Настройки для загрузки файлов
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для взаимодействия с фронтендом

# Инициализация базы данных
db = Database()

# Инициализация MinIO клиента
minio_client = MinIOClient()

# Инициализация сервисов
minio_service = MinIOService(minio_client, MAX_FILE_SIZE)
trip_service = TripService(db, minio_service)


@app.route('/api/trips', methods=['GET'])
def get_trips():
    """Получить все путешествия"""
    return trip_service.get_trips()


@app.route('/api/trips/<trip_id>', methods=['GET'])
def get_trip(trip_id):
    """Получить путешествие по ID"""
    return trip_service.get_trip(trip_id)


@app.route('/api/trips', methods=['POST'])
def create_trip():
    """Создать новое путешествие"""
    return trip_service.create_trip(request.content_type, request.form, request.files, lambda: request.get_json())


@app.route('/api/trips/<trip_id>', methods=['PUT'])
def update_trip(trip_id):
    """Обновить путешествие"""
    return trip_service.update_trip(trip_id, request.content_type, request.form, request.files,
                                    lambda: request.get_json())


@app.route('/api/trips/<trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    """Удалить путешествие"""
    return trip_service.delete_trip(trip_id)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
