from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pymongo.database import Database

from app.core.security import decode_access_token
from app.database.session import get_db

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_operator(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Database = Depends(get_db),
) -> dict:
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

    operator = db["operators"].find_one({"email": email}, {"_id": 0})
    if not operator:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Operator not found")

    return operator


def get_optional_current_operator(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Database = Depends(get_db),
) -> dict | None:
    if not credentials:
        return None
    try:
        email = decode_access_token(credentials.credentials)
    except ValueError:
        return None
    return db["operators"].find_one({"email": email}, {"_id": 0})
