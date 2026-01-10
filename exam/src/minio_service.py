"""Сервис для работы с MinIO"""
from werkzeug.utils import secure_filename


class MinIOService:
    """Класс для работы с MinIO объектным хранилищем"""

    def __init__(self, minio_client, max_file_size):
        self.minio_client = minio_client
        self.max_file_size = max_file_size

    def upload_file_to_minio(self, file) -> str:
        """
        Загрузить файл в MinIO

        Args:
            file: Файл из request.files

        Returns:
            str: URL загруженного файла или None
        """
        if file and file.filename:
            # Читаем данные файла
            file_data = file.read()

            # Проверяем размер файла
            if len(file_data) > self.max_file_size:
                return None

            # Определяем content type
            content_type = file.content_type or 'application/octet-stream'

            # Загружаем в MinIO
            file_url = self.minio_client.upload_file(
                file_data,
                secure_filename(file.filename),
                content_type
            )

            return file_url
        return None

    def delete_file(self, file_url: str) -> bool:
        """
        Удалить файл из MinIO по URL

        Args:
            file_url: URL файла

        Returns:
            bool: True, если файл удален успешно, False в случае ошибки
        """
        return self.minio_client.delete_file(file_url)
