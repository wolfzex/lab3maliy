Лабораторна робота №3

Тема: Валідація, обробка помилок, ORM
Дисципліна: Технології серверного програмного забезпечення
Варіант: 35 → (35 % 3 = 2) → Користувацькі категорії витрат

Мета

Реалізувати бекенд застосунку з:

валідацією даних і обробкою помилок;

ORM (Flask-SQLAlchemy) та міграціями (Flask-Migrate);

базою PostgreSQL;

REST-API (Flask-Smorest, Swagger /docs);

деплоєм на Render.com.

Технології

Python 3.11 · Flask · Flask-SQLAlchemy · Flask-Migrate · Marshmallow · Flask-Smorest · PostgreSQL · Gunicorn

Варіант 2 — Користувацькі категорії витрат

Загальні категорії (is_global=true) видимі всім

Користувацькі (user_id) — лише власнику

Перевірка прав і валідація при створенні записів

Локальний запуск
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

set FLASK_APP=app.py
set DATABASE_URL=postgresql://postgres:1234@localhost:5432/lab3_db

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python app.py


Основні ендпоінти
Метод	Шлях
GET /user	Отримати всіх користувачів	
POST /user	Створити користувача	
GET /category	Список категорій	
POST /category	Додати категорію	
GET /record	Список записів	
POST /record	Додати запис витрат