from pydantic import BaseModel
from typing import Optional


class ChatMessageIn(BaseModel):
    course_id: str
    document_id: str
    question: str


class ChatMessageOut(BaseModel):
    question: str
    answer: str


class QuizGenerateRequest(BaseModel):
    count: int = 10


class QuizOut(BaseModel):
    id: str
    question: str
    options: list
    # correct_answer intentionally omitted from the list view so the frontend
    # doesn't leak answers before the student submits.

    class Config:
        from_attributes = True


class QuizAttemptIn(BaseModel):
    quiz_id: str
    selected_answer: str


class QuizAttemptOut(BaseModel):
    quiz_id: str
    is_correct: bool
    correct_answer: str
    explanation: Optional[str] = None


class ProgressUpdateIn(BaseModel):
    lesson_id: str
    completed: bool


class ProgressOut(BaseModel):
    lesson_id: str
    completed: bool


class DashboardOut(BaseModel):
    total_courses: int
    completed_lessons: int
    total_lessons: int
    completion_percentage: float
    avg_quiz_score: Optional[float] = None
    recent_courses: list


class FlashcardGenerateRequest(BaseModel):
    count: int = 10


class FlashcardOut(BaseModel):
    id: str
    front: str
    back: str

    class Config:
        from_attributes = True
