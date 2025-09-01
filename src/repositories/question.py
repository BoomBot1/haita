from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from src.models.question import Question


def list_questions(session: Session, limit: int, offset: int) -> Sequence[Question]:
    stmt = (
        select(Question)
        .limit(limit)
        .offset(offset)
    )

    return session.execute(stmt).scalars().all()


def show(session: Session, question_id) -> Question:
    stmt = (
        select(Question)
        .options(selectinload(Question.answers))
        .where(Question.id == question_id)
    )

    return session.execute(stmt).scalars().first()
