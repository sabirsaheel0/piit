from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/operators/create", response_class=HTMLResponse)
def create_operator_page(request: Request):
    return templates.TemplateResponse("operator_create.html", {"request": request})


@router.get("/operators", response_class=HTMLResponse)
def operators_page(request: Request):
    return templates.TemplateResponse("operator_list.html", {"request": request})


@router.get("/operators/{operator_id}/edit", response_class=HTMLResponse)
def operator_edit_page(request: Request, operator_id: int):
    return templates.TemplateResponse(
        "operator_edit.html", {"request": request, "operator_id": operator_id}
    )
