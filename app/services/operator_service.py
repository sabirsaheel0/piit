from datetime import datetime, timezone

from fastapi import HTTPException, status
from pymongo import ASCENDING, DESCENDING, ReturnDocument
from pymongo.database import Database

from app.core.security import hash_password
from app.schemas.operator import OperatorCreate, OperatorUpdate

ALLOWED_SORT_FIELDS = {"id", "full_name", "email", "status", "created_at"}


def _next_operator_id(db: Database) -> int:
    counter = db["counters"].find_one_and_update(
        {"_id": "operator_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(counter["seq"])


def _serialize_operator(operator: dict) -> dict:
    operator.pop("_id", None)
    return operator


def create_operator(db: Database, payload: OperatorCreate) -> dict:
    email = payload.email.lower()
    if db["operators"].find_one({"email": email}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    is_first_operator = db["operators"].count_documents({}) == 0
    now = datetime.now(timezone.utc)

    document = {
        "id": _next_operator_id(db),
        "full_name": payload.full_name.strip(),
        "email": email,
        "password_hash": hash_password(payload.password),
        "role": payload.role.strip() if payload.role else None,
        "status": payload.status,
        "is_master": is_first_operator,
        "created_at": now,
        "updated_at": now,
    }
    db["operators"].insert_one(document)
    return _serialize_operator(document)


def list_operators(
    db: Database,
    page: int,
    page_size: int,
    search: str | None,
    sort_by: str,
    sort_order: str,
) -> tuple[list[dict], int]:
    filters: dict = {}
    if search:
        term = search.strip()
        filters["$or"] = [
            {"full_name": {"$regex": term, "$options": "i"}},
            {"email": {"$regex": term, "$options": "i"}},
        ]

    total = db["operators"].count_documents(filters)
    sort_field = sort_by if sort_by in ALLOWED_SORT_FIELDS else "created_at"
    direction = DESCENDING if sort_order.lower() == "desc" else ASCENDING

    cursor = (
        db["operators"]
        .find(filters, {"_id": 0, "password_hash": 0})
        .sort(sort_field, direction)
        .skip((page - 1) * page_size)
        .limit(page_size)
    )
    return list(cursor), total


def get_operator_or_404(db: Database, operator_id: int) -> dict:
    operator = db["operators"].find_one({"id": operator_id}, {"_id": 0, "password_hash": 0})
    if not operator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found")
    return operator


def update_operator(db: Database, operator_id: int, payload: OperatorUpdate, current_operator: dict) -> dict:
    target = db["operators"].find_one({"id": operator_id})
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found")

    if target.get("is_master") and current_operator["id"] != target["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Master operator cannot be edited by other users",
        )

    email = payload.email.lower()
    email_owner = db["operators"].find_one({"email": email, "id": {"$ne": target["id"]}})
    if email_owner:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    updates: dict = {
        "full_name": payload.full_name.strip(),
        "email": email,
        "status": payload.status,
        "updated_at": datetime.now(timezone.utc),
    }
    if payload.password:
        updates["password_hash"] = hash_password(payload.password)

    db["operators"].update_one({"id": operator_id}, {"$set": updates})
    updated = db["operators"].find_one({"id": operator_id}, {"_id": 0, "password_hash": 0})
    return updated
