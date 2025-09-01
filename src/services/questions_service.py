from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.question import Question
from src.repositories import question as question_repository
from src.schemas import question as question_schema
from src.schemas.pagination import PaginationModel
from src.schemas.question import QuestionRetrieve, QuestionDetail


def list_questions(session: Session, pagination: PaginationModel) -> list[QuestionRetrieve]:
    raw_sequence = question_repository.list_questions(
        session=session,
        limit=pagination.limit,
        offset=pagination.offset
    )
    valid_list = [QuestionRetrieve.model_validate(obj) for obj in raw_sequence]

    return valid_list


def show_question(session: Session, question_id: int) -> QuestionDetail:
    question = question_repository.show(session, question_id)

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return QuestionDetail.model_validate(question, from_attributes=True)


def create_question(session: Session, question: question_schema.QuestionCreate) -> Question:
    try:
        q = Question(
            text=question.text,
        )
        session.add(q)
        session.commit()
        session.refresh(q)

        return q
    except Exception as e:
        session.rollback()

        raise e


def delete_question(session: Session, question_id: int) -> bool:
    question = question_repository.show(session, question_id)

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    session.delete(question)
    session.commit()

    return True
