import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.models import Progress
from app.schemas.misc import ProgressUpdateIn, ProgressOut

router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("", response_model=ProgressOut)
def update_progress(
    body: ProgressUpdateIn,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(Progress)
        .filter(Progress.user_id == current_user.id, Progress.lesson_id == body.lesson_id)
        .first()
    )
    if not record:
        record = Progress(id=uuid.uuid4(), user_id=current_user.id, lesson_id=body.lesson_id)
        db.add(record)

    record.completed = body.completed
    record.completed_at = datetime.now(timezone.utc) if body.completed else None
    db.commit()

    return ProgressOut(lesson_id=body.lesson_id, completed=body.completed)


@router.get("/course/{course_id}", response_model=dict)
def get_course_progress(
    course_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns completion percentage for a specific course."""
    from app.models.models import Chapter, Lesson

    lesson_ids = [
        l.id
        for l in db.query(Lesson)
        .join(Chapter, Chapter.id == Lesson.chapter_id)
        .filter(Chapter.course_id == course_id)
        .all()
    ]
    total = len(lesson_ids)
    if total == 0:
        return {"completion_percentage": 0, "completed": 0, "total": 0}

    completed = (
        db.query(Progress)
        .filter(
            Progress.user_id == current_user.id,
            Progress.lesson_id.in_(lesson_ids),
            Progress.completed == True,
        )
        .count()
    )
    return {
        "completion_percentage": round((completed / total) * 100, 1),
        "completed": completed,
        "total": total,
    }
