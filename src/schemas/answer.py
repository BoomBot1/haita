from pydantic import BaseModel, Field
from datetime import datetime


class AnswerBase(BaseModel):
    id: int
    user_id: str
    text: str = Field(min_length=1)


class AnswerCreate(BaseModel):
    user_id: str
    text: str = Field(min_length=1)


class AnswerRetrieve(AnswerBase):
    question_id: int
    created_at: datetime

    class Config:
        from_attributes = True