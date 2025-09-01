from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.api.deps import PaginationDep, get_db
from src.schemas.answer import AnswerRetrieve, AnswerCreate
from src.schemas.question import QuestionRetrieve, QuestionDetail, QuestionCreate
from src.services import questions_service, answer_service

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("", response_model=list[QuestionRetrieve])
def list_questions(
        pagination: PaginationDep,
        session: Session = Depends(get_db)
):
    q = questions_service.list_questions(session, pagination)

    return q


@router.get("/{id}", response_model=QuestionDetail)
def show_question(
        id: int,
        session: Session = Depends(get_db)
):
    q = questions_service.show_question(session, id)

    return q


@router.post("/", response_model=QuestionCreate)
def create_question(
        question: QuestionCreate,
        session: Session = Depends(get_db)
):
    questions_service.create_question(session, question)

    return JSONResponse({"Message": "Completed"}, status_code=201)


@router.delete("/{id}")
def delete_question(
        id: int,
        session: Session = Depends(get_db)
):
    if questions_service.delete_question(session, id):
        return JSONResponse({"message": "Completed"}, status_code=204)


@router.post("/{question_id}/answers/")
def create_answer(
        question_id: int,
        answer: AnswerCreate,
        session: Session = Depends(get_db)
):
    answer_service.create_answer(session, answer, question_id)

    return JSONResponse({"message": "Completed"}, status_code=201)