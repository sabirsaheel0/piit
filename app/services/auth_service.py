from fastapi import HTTPException, status
from pymongo.database import Database

from app.core.security import create_access_token, verify_password


def login_operator(db: Database, email: str, password: str) -> str:
    operator = db["operators"].find_one({"email": email.lower()})
    if not operator or not verify_password(password, operator["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if operator["status"] != "Active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operator is inactive",
        )

    return create_access_token(subject=operator["email"])
