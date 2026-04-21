# Admin Panel Dashboard (Phase 1)

Production-ready FastAPI admin panel starter with JWT auth, secure operator management, and Bootstrap UI.

## 1) Project Structure

```bash
app/
  core/            # security + shared dependencies
  database/        # DB connection/session
  models/          # SQLAlchemy models
  routes/          # API + page routes
  schemas/         # Pydantic request/response schemas
  services/        # business logic layer
  static/          # CSS/JS assets
  templates/       # Jinja HTML templates
```

## 2) Prerequisites

- Python 3.11+
- MySQL 8+

## 3) Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your MySQL credentials.

## 4) Run

```bash
export $(cat .env | xargs)
uvicorn app.main:app --reload
```

Open:
- Login: http://127.0.0.1:8000/
- Dashboard: http://127.0.0.1:8000/dashboard

## 5) Database Schema

`operators` table is created by SQLAlchemy on startup.

Columns:
- id (PK, auto-increment)
- full_name (required)
- email (unique, required)
- password_hash (required)
- role (optional)
- status (Active/Inactive)
- is_master (default false; first operator is true)
- created_at
- updated_at

## 6) API Endpoints

### Auth
- `POST /api/auth/login`

### Operators (JWT required)
- `POST /api/operators`
- `GET /api/operators`
- `GET /api/operators/{operator_id}`
- `PUT /api/operators/{operator_id}`

## 7) Example API Requests (curl)

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"master@example.com","password":"StrongPass123"}'
```

### Create operator
```bash
curl -X POST http://127.0.0.1:8000/api/operators \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"full_name":"Jane Doe","email":"jane@example.com","password":"StrongPass123","role":"Supervisor","status":"Active"}'
```

### List operators
```bash
curl "http://127.0.0.1:8000/api/operators?page=1&page_size=10&search=jane&sort_by=created_at&sort_order=desc" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### Update operator
```bash
curl -X PUT http://127.0.0.1:8000/api/operators/2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"full_name":"Jane Updated","email":"jane.updated@example.com","status":"Active","password":null}'
```

## 8) Security Notes

- Passwords are hashed using bcrypt (`passlib`).
- JWT Bearer token is required on all operator APIs.
- Validation enforced with Pydantic schemas.
- Master operator protection is enforced in service layer.
- Proper 401/403/404/409 responses are returned.

## 9) Phase 1 Scope

Included:
- Auth, Dashboard shell, operator create/list/edit

Not included:
- Delete operator
- Advanced RBAC
- Audit logs
