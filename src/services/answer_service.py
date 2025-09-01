from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models import Question
from src.models.answer import Answer
from src.schemas import answer as answer_schema
from src.repositories import answer as answer_repository
from src.schemas.answer import AnswerRetrieve


def show_answer(session: Session, answer_id: int) -> AnswerRetrieve:
    answer = answer_repository.show(session, answer_id)

    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    return AnswerRetrieve.model_validate(answer, from_attributes=True)


def create_answer(session: Session, answer: answer_schema.AnswerCreate, question_id: int) -> Answer:
    try:
        query = select(Question).where(Question.id == question_id)
        question = session.execute(query).scalars().first()

        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        q = Answer(
            text=answer.text,
            user_id=answer.user_id,
            question_id=question.id,
        )
        session.add(q)
        session.commit()
        session.refresh(q)

        return q
    except Exception as e:
        session.rollback()

        raise e


def delete_answer(session: Session, answer_id: int) -> bool:
   answer = answer_repository.show(session, answer_id)

   if not answer:
       raise HTTPException(status_code=404, detail="Answer not found")

   session.delete(answer)
   session.commit()

   return True