from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.deps import get_current_operator
from app.models import Operator
from app.schemas.auth import CurrentOperatorResponse, LoginRequest, TokenResponse
from app.services.auth_service import login_operator

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    token = login_operator(db, payload.email, payload.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=CurrentOperatorResponse)
def me(current_operator: Operator = Depends(get_current_operator)):
    return CurrentOperatorResponse(
        id=current_operator.id,
        full_name=current_operator.full_name,
        email=current_operator.email,
        is_master=current_operator.is_master,
    )
