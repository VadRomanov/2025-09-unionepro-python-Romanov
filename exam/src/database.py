"""Класс для работы с базой данных"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
import os


class Database:
    """Класс для управления подключением к базе данных"""
    
    def __init__(self, database_url: str = None):
        """
        Инициализация подключения к БД
        
        Args:
            database_url: URL подключения к БД. Если не указан, используется переменная окружения DATABASE_URL
        """
        if database_url is None:
            # Используем PostgreSQL из переменной окружения
            database_url = os.getenv('DATABASE_URL')
            if database_url is None:
                # Формируем URL из отдельных переменных окружения
                db_user = os.getenv('DB_USER', 'postgres')
                db_password = os.getenv('DB_PASSWORD', 'postgres')
                db_host = os.getenv('DB_HOST', 'localhost')
                db_port = os.getenv('DB_PORT', '5440')
                db_name = os.getenv('DB_NAME', 'plan_your_trip')
                database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._init_database()
    
    def _init_database(self):
        """Инициализация таблиц в БД"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """
        Получить новую сессию для работы с БД
        
        Returns:
            Session: SQLAlchemy сессия
        """
        return self.SessionLocal()
    
    def close(self):
        """Закрыть соединение с БД"""
        self.engine.dispose()

