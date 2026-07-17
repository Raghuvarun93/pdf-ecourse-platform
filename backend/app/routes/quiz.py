import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.models import Quiz, QuizAttempt, Chapter, Course
from app.schemas.misc import QuizGenerateRequest, QuizOut, QuizAttemptIn, QuizAttemptOut
from app.services.quiz_generator import generate_quiz_for_chapter
from app.services.groq_client import GroqServiceError

router = APIRouter(prefix="/quiz", tags=["quiz"])


def _assert_chapter_ownership(db: Session, chapter_id: str, user_id: str) -> Chapter:
    chapter = (
        db.query(Chapter)
        .join(Course, Course.id == Chapter.course_id)
        .filter(Chapter.id == chapter_id, Course.user_id == user_id)
        .first()
    )
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


@router.post("/chapters/{chapter_id}/generate", response_model=list[QuizOut])
def generate_quiz(
    chapter_id: str,
    body: QuizGenerateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chapter = _assert_chapter_ownership(db, chapter_id, current_user.id)
    try:
        quizzes = generate_quiz_for_chapter(db, str(chapter.id), chapter.title, body.count)
    except GroqServiceError as e:
        raise HTTPException(status_code=429 if e.is_rate_limit else 502, detail=e.message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return [QuizOut(id=str(q.id), question=q.question, options=q.options) for q in quizzes]


@router.get("/chapters/{chapter_id}", response_model=list[QuizOut])
def get_quiz(
    chapter_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _assert_chapter_ownership(db, chapter_id, current_user.id)
    quizzes = db.query(Quiz).filter(Quiz.chapter_id == chapter_id).all()
    return [QuizOut(id=str(q.id), question=q.question, options=q.options) for q in quizzes]


@router.post("/attempt", response_model=QuizAttemptOut)
def submit_attempt(
    body: QuizAttemptIn,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    quiz = db.query(Quiz).filter(Quiz.id == body.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz question not found")

    is_correct = body.selected_answer.strip() == quiz.correct_answer.strip()

    attempt = QuizAttempt(
        id=uuid.uuid4(),
        user_id=current_user.id,
        quiz_id=quiz.id,
        selected_answer=body.selected_answer,
        is_correct=is_correct,
    )
    db.add(attempt)
    db.commit()

    return QuizAttemptOut(
        quiz_id=str(quiz.id),
        is_correct=is_correct,
        correct_answer=quiz.correct_answer,
        explanation=quiz.explanation,
    )
