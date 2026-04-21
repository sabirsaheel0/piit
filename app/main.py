from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.session import Base, engine
from app.routes.auth_routes import router as auth_router
from app.routes.operator_routes import router as operator_router
from app.routes.page_routes import router as page_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Admin Panel Dashboard")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(page_router)
app.include_router(auth_router)
app.include_router(operator_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
