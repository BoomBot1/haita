from typing import Generator
from src.core.db import SessionLocal
from typing import Annotated
from fastapi import Depends
from src.schemas.pagination import PaginationModel

def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def pagination_dep():
    return Annotated[PaginationModel, Depends(PaginationModel)]


PaginationDep = Annotated[PaginationModel, Depends(PaginationModel)]