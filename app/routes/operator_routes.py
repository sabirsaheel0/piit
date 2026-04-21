from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_operator, get_optional_current_operator
from app.database.session import get_db
from app.models import Operator
from app.schemas.operator import OperatorCreate, OperatorListResponse, OperatorOut, OperatorUpdate
from app.services.operator_service import create_operator, get_operator_or_404, list_operators, update_operator

router = APIRouter(prefix="/api/operators", tags=["operators"])


@router.post("", response_model=OperatorOut)
def create_operator_endpoint(
    payload: OperatorCreate,
    db: Session = Depends(get_db),
    current_operator: Operator | None = Depends(get_optional_current_operator),
): 
    if db.query(Operator).count() > 0 and not current_operator:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return create_operator(db, payload)


@router.get("", response_model=OperatorListResponse)
def list_operators_endpoint(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    _: Operator = Depends(get_current_operator),
):
    items, total = list_operators(db, page, page_size, search, sort_by, sort_order)
    return OperatorListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{operator_id}", response_model=OperatorOut)
def get_operator_endpoint(
    operator_id: int,
    db: Session = Depends(get_db),
    _: Operator = Depends(get_current_operator),
):
    return get_operator_or_404(db, operator_id)


@router.put("/{operator_id}", response_model=OperatorOut)
def update_operator_endpoint(
    operator_id: int,
    payload: OperatorUpdate,
    db: Session = Depends(get_db),
    current_operator: Operator = Depends(get_current_operator),
):
    return update_operator(db, operator_id, payload, current_operator)
