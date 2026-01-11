from flask import Flask, request, session
from flask_cors import CORS
from database import Database
from exam.src.minio_service import MinIOService
from exam.src.trip_service import TripService
from exam.src.auth_service import AuthService
from minio_client import MinIOClient
import os
import secrets

# Настройки для загрузки файлов
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))
CORS(app, supports_credentials=True)  # Разрешаем CORS для взаимодействия с фронтендом

# Инициализация базы данных
db = Database()

# Инициализация MinIO клиента
minio_client = MinIOClient()

# Инициализация сервисов
minio_service = MinIOService(minio_client, MAX_FILE_SIZE)
trip_service = TripService(db, minio_service)
auth_service = AuthService(db)


# API для аутентификации
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    return auth_service.register(request.get_json())


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Вход пользователя"""
    return auth_service.login(request.get_json())


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Выход пользователя"""
    return auth_service.logout()


@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    """Получить текущего пользователя"""
    user = auth_service.get_current_user()
    if not user:
        return {'error': 'Не аутентифицирован'}, 401
    return {'user': user}, 200


@app.route('/api/trips', methods=['GET'])
def get_trips():
    """Получить все путешествия текущего пользователя"""
    auth_error = auth_service.require_auth()
    if auth_error:
        return auth_error
    
    user_id = session.get('user_id')
    return trip_service.get_user_trips(user_id)


@app.route('/api/trips/<trip_id>', methods=['GET'])
def get_trip(trip_id):
    """Получить путешествие по ID"""
    auth_error = auth_service.require_auth()
    if auth_error:
        return auth_error

    user_id = session.get('user_id')
    return trip_service.get_trip(user_id, trip_id)


@app.route('/api/trips', methods=['POST'])
def create_trip():
    """Создать новое путешествие"""
    auth_error = auth_service.require_auth()
    if auth_error:
        return auth_error
    
    user_id = session.get('user_id')
    return trip_service.create_trip(user_id, request.content_type, request.form, request.files, lambda: request.get_json())


@app.route('/api/trips/<trip_id>', methods=['PUT'])
def update_trip(trip_id):
    """Обновить путешествие"""
    auth_error = auth_service.require_auth()
    if auth_error:
        return auth_error
    
    user_id = session.get('user_id')
    return trip_service.update_trip(user_id, trip_id, request.content_type, request.form, request.files,
                                    lambda: request.get_json())


@app.route('/api/trips/<trip_id>', methods=['DELETE'])
def delete_trip(trip_id):
    """Удалить путешествие"""
    auth_error = auth_service.require_auth()
    if auth_error:
        return auth_error
    
    user_id = session.get('user_id')
    return trip_service.delete_trip(user_id, trip_id)


if __name__ == '__main__':
    port = os.getenv('DB_USER', 5000)
    app.run(debug=True, port=int(port))
