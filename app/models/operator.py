from datetime import datetime
from typing import TypedDict


class OperatorDocument(TypedDict):
    id: int
    full_name: str
    email: str
    password_hash: str
    role: str | None
    status: str
    is_master: bool
    created_at: datetime
    updated_at: datetime
