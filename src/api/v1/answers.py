from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from src.api.deps import get_db
from src.schemas.answer import AnswerRetrieve, AnswerCreate
from src.services import answer_service

router = APIRouter(prefix="/answers", tags=["answers"])


@router.get('/{id}', response_model=AnswerRetrieve)
def show_answer(
        id: int,
        session: Session = Depends(get_db)
):
    q = answer_service.show_answer(session, id)

    return q


@router.delete('/{id}')
def delete_answer(
        id: int,
        session: Session = Depends(get_db)
):
    answer_service.delete_answer(session, id)

    return JSONResponse({'message': 'Completed'}, status_code=204)