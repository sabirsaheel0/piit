import os
from collections.abc import Generator

from pymongo import ASCENDING, MongoClient
from pymongo.database import Database

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "admin_dashboard")

mongo_client = MongoClient(MONGODB_URI)
database = mongo_client[MONGODB_DB]


def ensure_indexes() -> None:
    operators = database["operators"]
    operators.create_index([("id", ASCENDING)], unique=True)
    operators.create_index([("email", ASCENDING)], unique=True)


def get_db() -> Generator[Database, None, None]:
    yield database
