# Система управления пользователями

Веб-приложение на Django для управления пользователями с разными ролями (студенты, менеджеры, администраторы) и системой верификации email.

## Функциональность

- **Регистрация и аутентификация**
  - Регистрация пользователей с разными ролями
  - Вход по email и паролю
  - Обязательная верификация email через 6-значный код

- **Управление пользователями**
  - Просмотр списка пользователей с фильтрацией
  - Экспорт данных в Excel
  - Отображение статистики по студентам

- **Роли пользователей** (в разработке)
  - **Студент**: имеет доступ к своим данным (посещаемость, количество уроков, баллы) - не готово в процессе
  - **Менеджер**: управляет данными студентов (в процессе...)
  - **Администратор**: полный доступ к системе

## Технологии

- **Backend**: Django 5.0
- **База данных**: PostgreSQL
- **Frontend**: Bootstrap 5
- **Дополнительно**:
  - django-crispy-forms для стилизации форм
  - openpyxl для экспорта в Excel
  - python-dotenv для управления переменными окружения

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ ...
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   venv\Scripts\activate  # для Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` в корневой директории проекта или в settings:
   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=postgres://user:password@localhost:5432/dbname
   ```

5. Выполните миграции:
   ```bash
   python manage.py migrate
   ```

6. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

7. Запустите сервер:
   ```bash
   python manage.py runserver
   ```


## Процесс верификации email

1. При регистрации пользователя генерируется 6-значный код
2. Код отправляется на указанный email (в данном контексте в консоль)
3. Пользователь вводит код на странице верификации
4. После успешной верификации пользователь получает доступ к функционалу


Система позволяет экспортировать список пользователей в Excel с учетом примененных фильтров. Экспорт включает следующие данные:
.

