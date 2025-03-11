# Система управления курсами

Проект представляет собой API для управления образовательными курсами с возможностью регистрации преподавателей и студентов, создания курсов и управления записью студентов на курсы.

## Технологии

- Python 3.12
- Django 5.0.2
- Django REST Framework
- PostgreSQL
- Bootstrap 5

## Установка и настройка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd Outpeer_HW-main
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
# или
.venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте базу данных PostgreSQL:
```sql
CREATE USER monituser WITH PASSWORD 'u_pass';
CREATE DATABASE op_hw OWNER monituser;
```

5. Примените миграции:
```bash
python manage.py migrate
```

6. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Структура проекта

- `users/` - приложение для управления пользователями
- `courses/` - приложение для управления курсами
- `config/` - основные настройки проекта

## API Endpoints

### Курсы

- `GET /courses/api/` - получить список всех курсов
- `POST /courses/api/` - создать новый курс
- `GET /courses/api/{id}/` - получить детали курса
- `PUT /courses/api/{id}/` - обновить курс
- `DELETE /courses/api/{id}/` - удалить курс
- `POST /courses/api/{id}/add_student/` - добавить студента на курс
- `POST /courses/api/{id}/remove_student/` - удалить студента с курса

### Примеры использования API

#### Создание курса
```bash
curl -X POST http://localhost:8000/courses/api/ \
-H "Content-Type: application/json" \
-d '{
    "title": "Python для начинающих",
    "description": "Базовый курс Python",
    "start_date": "2025-04-01",
    "end_date": "2025-05-01",
    "max_students": 20,
    "is_active": true
}'
```

#### Добавление студента на курс
```bash
curl -X POST http://localhost:8000/courses/api/{course_id}/add_student/ \
-H "Content-Type: application/json" \
-d '{"student_id": 1}'
```

## Модели данных

### User
- email (уникальный)
- username
- role (student/teacher)
- is_verified (статус верификации email)

### Course
- title (название курса)
- description (описание)
- teacher (преподаватель)
- students (список студентов)
- start_date (дата начала)
- end_date (дата окончания)
- max_students (максимальное количество студентов)
- is_active (статус курса)

## Веб-интерфейс

Проект также включает веб-интерфейс для:
- Просмотра списка курсов
- Просмотра деталей курса
- Управления студентами курса
- Административной панели Django

