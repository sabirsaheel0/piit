# Admin Panel Dashboard (Phase 1)

Production-ready FastAPI admin panel starter with JWT auth, secure operator management, and Bootstrap UI.

## 1) Project Structure

```bash
app/
  core/            # security + shared dependencies
  database/        # MongoDB connection and indexes
  models/          # typed document models
  routes/          # API + page routes
  schemas/         # Pydantic request/response schemas
  services/        # business logic layer
  static/          # CSS/JS assets
  templates/       # Jinja HTML templates
```

## 2) Prerequisites

- Python 3.11+ (for local run)
- Docker (recommended)
- MongoDB Atlas cluster or local MongoDB

## 3) Quick Start (Docker Compose)

```bash
cp .env.example .env
# set MONGODB_URI if using Atlas, otherwise local mongo is auto-provisioned

docker compose up --build
```

Open:
- Login: http://127.0.0.1:8000/
- Dashboard: http://127.0.0.1:8000/dashboard

## 4) Atlas Configuration

Set these in `.env`:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=<app-name>
MONGODB_DB=admin_dashboard
```

> Ensure your Atlas network access list allows your Docker host IP.

## 5) Local Python Run (optional)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export $(cat .env | xargs)
uvicorn app.main:app --reload
```

## 6) Data Model

`operators` collection fields:
- id (numeric auto-increment via `counters` collection)
- full_name (required)
- email (unique, required)
- password_hash (required)
- role (optional)
- status (Active/Inactive)
- is_master (default false; first operator is true)
- created_at
- updated_at

## 7) API Endpoints

### Auth
- `POST /api/auth/login`
- `GET /api/auth/me`

### Operators
- `POST /api/operators`
- `GET /api/operators`
- `GET /api/operators/{operator_id}`
- `PUT /api/operators/{operator_id}`

## 8) Example API Requests (curl)

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

## 9) Security Notes

- Passwords are hashed using bcrypt (`passlib`).
- JWT Bearer token is required on all operator APIs.
- Validation enforced with Pydantic schemas.
- Master operator protection is enforced in service layer.
- Proper 401/403/404/409 responses are returned.
