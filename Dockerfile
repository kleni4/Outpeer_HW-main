# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем .env файл
COPY .env .

# Копируем проект
COPY . .

# Устанавливаем python-dotenv для работы с .env
RUN pip install python-dotenv

# Выполняем миграции и запускаем сервер
CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
