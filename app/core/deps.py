from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.session import get_db
from app.models import Operator

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_operator(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Operator:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        email = decode_access_token(credentials.credentials)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from None

    operator = db.query(Operator).filter(Operator.email == email).first()
    if not operator:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Operator not found")

    return operator


def get_optional_current_operator(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Operator | None:
    if not credentials:
        return None
    try:
        email = decode_access_token(credentials.credentials)
    except ValueError:
        return None
    return db.query(Operator).filter(Operator.email == email).first()
