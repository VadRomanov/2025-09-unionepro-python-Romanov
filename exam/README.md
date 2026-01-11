# Exam Service

Сервис для планирования и управления поездками.

## Стек

- Python (основная логика в `src/`)
- PostgreSQL (база данных, настройки в `database.py` и docker-compose)
- MinIO (объектное хранилище, клиент в `minio_client.py` / `minio_service.py` и docker-compose)

## Структура проекта

- `src/main.py` — точка входа приложения / запуск веб‑сервиса.
- `src/auth_service.py` — авторизация и работа с пользователями (логин/токены и т.п.).
- `src/trip_service.py` — бизнес‑логика для сущности поездок (создание, получение, обновление).
- `src/minio_client.py`, `src/minio_service.py` — интеграция с MinIO (создание бакетов, загрузка и чтение объектов).
- `src/models.py` — Pydantic/ORM‑модели домена (пользователи, поездки, файлы и т.д.).
- `src/database.py` — подключение к БД и вспомогательные функции работы с ней.
- `src/storage.py` — абстракция над файловым хранилищем.
- `docker/docker-compose.yml` — описание сервисов (приложение, PostgreSQL, MinIO).
- `docker/volumes/minio/policy/` — политика доступа для MinIO.

## Запуск через Docker

1. Перейти в директорию проекта:
   ```bash
   cd exam
   ```
2. Поднять инфраструктуру:
   ```bash
   docker compose -f docker/docker-compose.yml up --build
   ```
3. Старт сервиса
4. После старта:
   - Приложение будет доступно по адресу `http://localhost:<PORT>`.
   - MinIO консоль — `http://localhost:<MINIO_PORT>`, креды указаны в `docker-compose.yml`.

## Переменные окружения

Основные параметры:

- `DATABASE_URL` — строка подключения к PostgreSQL.  
или
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` - настройки БД.
- `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_SECURE`, `MINIO_BUCKET` — настройки MinIO.
- `APP_PORT` — порт веб‑приложения.

## Основные возможности

- Регистрация/авторизация пользователя.
- Создание и просмотр поездок.
- Загрузка и хранение файлов поездок в MinIO.
- Получение загруженных объектов.