from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.models import Flashcard, Chapter, Course
from app.schemas.misc import FlashcardGenerateRequest, FlashcardOut
from app.services.flashcard_generator import generate_flashcards_for_chapter
from app.services.groq_client import GroqServiceError

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


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


@router.post("/chapters/{chapter_id}/generate", response_model=list[FlashcardOut])
def generate_flashcards(
    chapter_id: str,
    body: FlashcardGenerateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chapter = _assert_chapter_ownership(db, chapter_id, current_user.id)
    try:
        cards = generate_flashcards_for_chapter(db, str(chapter.id), chapter.title, body.count)
    except GroqServiceError as e:
        raise HTTPException(status_code=429 if e.is_rate_limit else 502, detail=e.message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return [FlashcardOut(id=str(c.id), front=c.front, back=c.back) for c in cards]


@router.get("/chapters/{chapter_id}", response_model=list[FlashcardOut])
def get_flashcards(
    chapter_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _assert_chapter_ownership(db, chapter_id, current_user.id)
    cards = db.query(Flashcard).filter(Flashcard.chapter_id == chapter_id).all()
    return [FlashcardOut(id=str(c.id), front=c.front, back=c.back) for c in cards]
