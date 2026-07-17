from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.models import Course, Chapter, Lesson

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=list[dict])
def search(
    q: str = Query(..., min_length=1),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Keyword search across the user's chapters and lessons (title + content)."""
    like = f"%{q}%"

    lessons = (
        db.query(Lesson, Chapter, Course)
        .join(Chapter, Chapter.id == Lesson.chapter_id)
        .join(Course, Course.id == Chapter.course_id)
        .filter(Course.user_id == current_user.id)
        .filter(or_(Lesson.title.ilike(like), Lesson.content.ilike(like)))
        .limit(30)
        .all()
    )

    results = [
        {
            "type": "lesson",
            "course_id": str(course.id),
            "course_title": course.title,
            "chapter_title": chapter.title,
            "lesson_id": str(lesson.id),
            "lesson_title": lesson.title,
        }
        for lesson, chapter, course in lessons
    ]
    return results
