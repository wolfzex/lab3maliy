Лабораторна робота №3  
**Тема:** Валідація, обробка помилок, ORM  
**Дисципліна:** Технології серверного програмного забезпечення  
**Варіант:** 35 → (35 % 3 = 2) → **Користувацькі категорії витрат**

## Мета

Реалізувати бекенд-застосунок, який містить:

- валідацію вхідних даних та обробку помилок;
- роботу з ORM (Flask-SQLAlchemy) та міграціями (Flask-Migrate);
- зберігання даних у базі PostgreSQL;
- REST-API з документацією (Flask-Smorest, Swagger `/docs`);
- підготовку до деплою на Render.com.

## Використані технології

Python 3.11 · Flask · Flask-SQLAlchemy · Flask-Migrate · Marshmallow · Flask-Smorest · PostgreSQL · Gunicorn

## Варіант 2 — Користувацькі категорії витрат

У межах варіанту реалізовано розширену логіку роботи з категоріями витрат:

- **Загальні категорії** (`is_global = true`) — доступні всім користувачам.
- **Користувацькі категорії** (`user_id`) — видимі та доступні лише власнику.
- При створенні записів витрат виконується перевірка:
  - що категорія існує;
  - що користувач має право використовувати цю категорію (не може використовувати чужу персональну категорію);
  - валідація вхідних даних виконується через Marshmallow-схеми.

Таким чином виконано додаткове завдання відповідно до методичних вказівок для варіанту 2.

## Локальний запуск

```bash
python -m venv venv
venv\Scripts\activate  # або source venv/bin/activate на Linux/macOS
pip install -r requirements.txt

set FLASK_APP=app.py
set DATABASE_URL=postgresql://postgres:1234@localhost:5432/lab3_db

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

python app.py
```

Бекенд буде доступний за адресою `http://localhost:5000`, документація — на `http://localhost:5000/docs`.

## Основні ендпоінти (стан після ЛР3)

| Метод | Шлях      | Опис                        |
|-------|-----------|-----------------------------|
| GET   | `/user`   | Отримати всіх користувачів |
| POST  | `/user`   | Створити користувача       |
| GET   | `/category` | Список категорій (загальних і користувацьких) |
| POST  | `/category` | Додати нову категорію витрат |
| GET   | `/record`   | Список записів витрат      |
| POST  | `/record`   | Додати запис витрат        |

Валідація параметрів та обробка помилок реалізовані за допомогою Flask-Smorest і Marshmallow-схем, а зберігання даних — через ORM-моделі Flask-SQLAlchemy з міграціями Flask-Migrate.

Лабораторна робота №4  
**Тема:** Аутентифікація (JWT)  
**Дисципліна:** Технології серверного програмного забезпечення  

## Мета

Додати до застосунку повноцінну систему аутентифікації за допомогою JWT-токенів, захистити доступ до приватних ресурсів та протестувати роботу з токенами у Postman.

## Використані технології

Python 3.11 · Flask · Flask-Smorest · Flask-JWT-Extended · Marshmallow · PostgreSQL · Flask-Migrate · Docker · Docker Compose

## Реалізований функціонал

### 1. Реєстрація користувача (`POST /register`)
- приймає `username` та `password`
- пароль хешується через `pbkdf2_sha256`
- перевіряє унікальність імені користувача
- повертає створеного користувача

### 2. Логін користувача (`POST /login`)
- перевіряє правильність пароля
- повертає JWT токен через `create_access_token(identity=user.id)`
- токен використовується для доступу до захищених ендпоінтів

### 3. Захист API через @jwt_required
Усі критичні ендпоінти (`/user`, `/category`, `/record`) тепер доступні **лише з валідним JWT**.

### 4. Обробники помилок JWT
Додано кастомні хендлери:

- прострочений токен  
- неправильний токен  
- відсутність токена  

Відповідь у форматі JSON.

### 5. Postman Flow
Створено тестовий flow для:
- реєстрації
- логіну
- автоматичного підстановлення токена
- перевірки приватних ендпоінтів

## Docker-запуск проекту

### 1. Запуск у Docker Compose

```bash
docker compose up --build -d
```

Після старту буде два контейнери:
- `flask_db` — PostgreSQL
- `flask_api` — Flask backend

API працює за адресою:

👉 http://localhost:5001  
Документація Swagger:

👉 http://localhost:5001/docs

### 2. Зміна порту (якщо 5000 зайнятий macOS ControlCenter)

У `docker-compose.yaml`:

```yaml
ports:
  - "5001:5000"
```

## Локальний запуск без Docker

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=app.py
export JWT_SECRET_KEY="your-secret"
export DATABASE_URL="postgresql://postgres:1234@localhost:5432/lab3_db"

flask db upgrade
python app.py
```

## Перевірка функціоналу у Postman

### 1. Реєстрація

POST `/register`

```json
{
  "username": "testuser",
  "password": "secret123"
}
```

### 2. Логін

POST `/login`

```json
{
  "username": "testuser",
  "password": "secret123"
}
```

У відповідь повертається:

```json
{
  "access_token": "JWT_TOKEN",
  "user_id": 1
}
```

### 3. Використання токена

У Headers:

```
Authorization: Bearer JWT_TOKEN
```

### 4. Доступ до захищених ендпоінтів:

- `GET /user`
- `GET /category`
- `POST /category`
- `GET /record`
- `POST /record`

---

Лабораторна робота №4 виконана відповідно до методичних вимог:  
- реалізована аутентифікація;  
- захищені ендпоінти;  
- додано Postman flow;  
- присутній .gitignore;  
- є інструкції запуску та документація.  
