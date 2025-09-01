from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models.answer import Answer

def show(session: Session, answer_id: int) -> Answer:
    stmt = (
        select(Answer)
        .where(Answer.id == answer_id)
    )

    return session.execute(stmt).scalars().first()