from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.models import Operator


def login_operator(db: Session, email: str, password: str) -> str:
    operator = db.query(Operator).filter(Operator.email == email).first()
    if not operator or not verify_password(password, operator.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if operator.status != "Active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operator is inactive",
        )

    return create_access_token(subject=operator.email)
