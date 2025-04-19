# models.py
from pydantic import BaseModel
from typing import Optional, List

class UserQuery(BaseModel):
    subject: str
    year: int
    need_solutions: bool = False

class Question(BaseModel):
    number: int
    text: str
    marks: int
    type: Optional[str] = None
    chapter: Optional[str] = None
    answer: Optional[str] = None  # from GitHub memory

class Paper(BaseModel):
    subject: str
    year: int
    questions: List[Question]

class Answer(BaseModel):
    question_number: int
    answer_text: str

class Output(BaseModel):
    paper: Paper
    answers: Optional[List[Answer]] = None
