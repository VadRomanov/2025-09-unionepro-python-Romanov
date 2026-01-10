"""Сервис для работы с аутентификацией"""
from flask import jsonify, session as flask_session
from storage import UserRepository
from typing import Optional, Tuple
import json


class AuthService:
    """Класс для работы с аутентификацией"""

    def __init__(self, db):
        self.db = db

    def get_user_repository(self):
        """Получить репозиторий для работы с пользователями"""
        db_session = self.db.get_session()
        return UserRepository(db_session), db_session

    def register(self, credentials: json) -> Tuple[dict, int]:
        """
        Регистрация нового пользователя
        
        Args:
            credentials: реквизиты для входа
            
        Returns:
            Tuple[dict, int]: Ответ и статус код
        """
        username = credentials.get('username')
        password = credentials.get('password')

        if not username or not password:
            return {'error': 'username и пароль обязательны'}, 400

        repository, db_session = self.get_user_repository()
        try:
            # Проверка, существует ли пользователь
            existing_user = repository.get_by_username(username)
            if existing_user:
                return jsonify({'error': 'Пользователь с таким username уже существует'}), 400

            # Создание нового пользователя
            user = repository.create(username, password)
            return jsonify({
                'message': 'Пользователь успешно зарегистрирован',
                'user': user.to_dict()
            }), 201

        except Exception as e:
            db_session.rollback()
            print(f'Error: {e}')
            return jsonify({'error': 'registration failed'}), 500
        finally:
            db_session.close()

    def login(self, credentials: json) -> Tuple[dict, int]:
        """
        Вход пользователя
        
        Args:
            credentials: реквизиты для входа

        Returns:
            Tuple[dict, int]: Ответ и статус код
        """
        username = credentials.get('username')
        password = credentials.get('password')

        if not username or not password:
            return {'error': 'username и пароль обязательны'}, 400

        repository, db_session = self.get_user_repository()
        try:
            # Поиск пользователя по username
            user = repository.get_by_username(username)
            if not user:
                return jsonify({'error': 'Пользователь с данными именем не зарегестрирован'}), 401

            # Проверка пароля
            if not user.check_password(password):
                return jsonify({'error': 'Неверный пароль'}), 401

            # Сохранение ID пользователя в сессии
            flask_session['user_id'] = user.id
            flask_session['user_username'] = user.username

            return jsonify({
                'message': 'Успешный вход',
                'user': user.to_dict()
            }), 200

        except Exception as e:
            print(f'Error: {e}')
            return jsonify({'error': 'authentication failed'}), 500
        finally:
            db_session.close()

    def logout(self) -> Tuple[dict, int]:
        """
        Выход пользователя
        
        Returns:
            Tuple[dict, int]: Ответ и статус код
        """
        flask_session.clear()
        return jsonify({'message': 'Успешный выход'}), 200

    def get_current_user(self) -> Optional[dict]:
        """
        Получить текущего пользователя из сессии
        
        Returns:
            Optional[dict]: Данные пользователя или None
        """
        user_id = flask_session.get('user_id')
        if not user_id:
            return None

        repository, db_session = self.get_user_repository()
        try:
            user = repository.get_by_id(user_id)
            if user:
                return user.to_dict()
            return None
        finally:
            db_session.close()

    def require_auth(self):
        """
        Проверить, аутентифицирован ли пользователь
        
        Returns:
            Tuple[dict, int] или None: Ошибка, если не аутентифицирован
        """
        user_id = flask_session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Требуется аутентификация'}), 401
        return None

