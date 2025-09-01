from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from src.schemas.answer import AnswerRetrieve


class QuestionBase(BaseModel):
    id: int
    text: str = Field(min_length=1)


class QuestionCreate(BaseModel):
    text: str = Field(min_length=1)


class QuestionRetrieve(QuestionBase):
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionDetail(QuestionBase):
    answers: List[AnswerRetrieve] = []
