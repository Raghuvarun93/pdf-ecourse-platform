from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.models import Course, Lesson, Chapter, Progress, QuizAttempt
from app.schemas.misc import DashboardOut

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardOut)
def get_dashboard(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    courses = (
        db.query(Course)
        .filter(Course.user_id == current_user.id)
        .order_by(Course.created_at.desc())
        .all()
    )

    course_ids = [c.id for c in courses]

    total_lessons = (
        db.query(Lesson)
        .join(Chapter, Chapter.id == Lesson.chapter_id)
        .filter(Chapter.course_id.in_(course_ids))
        .count()
        if course_ids
        else 0
    )

    completed_lessons = (
        db.query(Progress)
        .filter(Progress.user_id == current_user.id, Progress.completed == True)
        .count()
    )

    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id).all()
    avg_score = None
    if attempts:
        avg_score = round(sum(1 for a in attempts if a.is_correct) / len(attempts) * 100, 1)

    return DashboardOut(
        total_courses=len(courses),
        completed_lessons=completed_lessons,
        total_lessons=total_lessons,
        completion_percentage=round((completed_lessons / total_lessons) * 100, 1) if total_lessons else 0.0,
        avg_quiz_score=avg_score,
        recent_courses=[
            {
                "id": str(c.id),
                "title": c.title,
                "difficulty": c.difficulty,
                "status": c.status,
                "created_at": c.created_at.isoformat(),
            }
            for c in courses[:5]
        ],
    )
