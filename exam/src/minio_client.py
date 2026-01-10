"""Клиент для работы с MinIO"""
from minio import Minio
from minio.error import S3Error
import os
from typing import Optional
import uuid


class MinIOClient:
    """Класс для работы с MinIO объектным хранилищем"""
    
    def __init__(self):
        """
        Инициализация клиента MinIO
        """
        # Получаем настройки из переменных окружения или используем значения по умолчанию
        self.endpoint = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
        self.access_key = os.getenv('MINIO_ACCESS_KEY', 'root')
        self.secret_key = os.getenv('MINIO_SECRET_KEY', 'password')
        self.secure = os.getenv('MINIO_SECURE', 'false').lower() == 'true'
        self.bucket_name = os.getenv('MINIO_BUCKET', 'plan-your-trip-file-bucket')
        
        # Инициализация клиента MinIO
        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )
        
        # Создание бакета, если его нет
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Проверить существование бакета и создать его, если нужно"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            print(f"Ошибка при создании бакета: {e}")
    
    def upload_file(self, file_data: bytes, file_name: str, content_type: str = 'application/octet-stream') -> Optional[str]:
        """
        Загрузить файл в MinIO
        
        Args:
            file_data: Данные файла в виде bytes
            file_name: Имя файла
            content_type: MIME-тип файла
            
        Returns:
            str: URL файла или None в случае ошибки
        """
        try:
            # Генерируем уникальное имя файла
            file_extension = os.path.splitext(file_name)[1]
            unique_file_name = f"{uuid.uuid4()}{file_extension}"
            object_name = f"uploads/{unique_file_name}"
            
            # Загружаем файл
            from io import BytesIO
            file_stream = BytesIO(file_data)
            
            self.client.put_object(
                self.bucket_name,
                object_name,
                file_stream,
                length=len(file_data),
                content_type=content_type
            )
            
            # Возвращаем URL файла
            # Для публичного доступа используем прямую ссылку
            if self.secure:
                protocol = 'https'
            else:
                protocol = 'http'
            
            url = f"{protocol}://{self.endpoint}/{self.bucket_name}/{object_name}"
            return url
            
        except S3Error as e:
            print(f"Ошибка при загрузке файла в MinIO: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка при загрузке файла: {e}")
            return None
    
    def delete_file(self, file_url: str) -> bool:
        """
        Удалить файл из MinIO по URL
        
        Args:
            file_url: URL файла
            
        Returns:
            bool: True, если файл удален успешно, False в случае ошибки
        """
        try:
            # Извлекаем имя объекта из URL
            # Формат URL: http://endpoint/bucket/object_name
            parts = file_url.split(f'/{self.bucket_name}/')
            if len(parts) != 2:
                return False
            
            object_name = parts[1]
            
            # Удаляем объект
            self.client.remove_object(self.bucket_name, object_name)
            return True
            
        except S3Error as e:
            print(f"Ошибка при удалении файла из MinIO: {e}")
            return False
        except Exception as e:
            print(f"Неожиданная ошибка при удалении файла: {e}")
            return False
