from fastapi import HTTPException, status
from sqlalchemy import asc, desc, func, or_
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models import Operator
from app.schemas.operator import OperatorCreate, OperatorUpdate

SORT_FIELDS = {
    "id": Operator.id,
    "full_name": Operator.full_name,
    "email": Operator.email,
    "status": Operator.status,
    "created_at": Operator.created_at,
}


def create_operator(db: Session, payload: OperatorCreate) -> Operator:
    existing = db.query(Operator).filter(func.lower(Operator.email) == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    is_first_operator = db.query(Operator).count() == 0
    operator = Operator(
        full_name=payload.full_name.strip(),
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        role=payload.role.strip() if payload.role else None,
        status=payload.status,
        is_master=is_first_operator,
    )
    db.add(operator)
    db.commit()
    db.refresh(operator)
    return operator


def list_operators(
    db: Session,
    page: int,
    page_size: int,
    search: str | None,
    sort_by: str,
    sort_order: str,
) -> tuple[list[Operator], int]:
    query = db.query(Operator)

    if search:
        like_term = f"%{search.strip()}%"
        query = query.filter(
            or_(Operator.full_name.ilike(like_term), Operator.email.ilike(like_term))
        )

    total = query.count()
    sort_field = SORT_FIELDS.get(sort_by, Operator.created_at)
    order_clause = desc(sort_field) if sort_order.lower() == "desc" else asc(sort_field)

    records = (
        query.order_by(order_clause)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return records, total


def get_operator_or_404(db: Session, operator_id: int) -> Operator:
    operator = db.query(Operator).filter(Operator.id == operator_id).first()
    if not operator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operator not found")
    return operator


def update_operator(
    db: Session,
    operator_id: int,
    payload: OperatorUpdate,
    current_operator: Operator,
) -> Operator:
    target = get_operator_or_404(db, operator_id)

    if target.is_master and current_operator.id != target.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Master operator cannot be edited by other users",
        )

    email_owner = (
        db.query(Operator)
        .filter(func.lower(Operator.email) == payload.email.lower(), Operator.id != target.id)
        .first()
    )
    if email_owner:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    target.full_name = payload.full_name.strip()
    target.email = payload.email.lower()
    target.status = payload.status
    if payload.password:
        target.password_hash = hash_password(payload.password)

    db.add(target)
    db.commit()
    db.refresh(target)
    return target
