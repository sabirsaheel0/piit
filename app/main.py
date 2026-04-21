from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.session import ensure_indexes
from app.routes.auth_routes import router as auth_router
from app.routes.operator_routes import router as operator_router
from app.routes.page_routes import router as page_router

app = FastAPI(title="Admin Panel Dashboard")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def startup() -> None:
    ensure_indexes()


app.include_router(page_router)
app.include_router(auth_router)
app.include_router(operator_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
