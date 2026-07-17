from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.models import Course, Chapter, Lesson, Document, Progress
from app.schemas.course import CourseOut, CourseDetailOut, ChapterOut, LessonOut, GenerateCourseRequest
from app.services.course_generator import generate_course_for_document
from app.services.groq_client import GroqServiceError

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/generate", response_model=CourseOut)
def generate_course(
    body: GenerateCourseRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(Document.id == body.document_id, Document.user_id == current_user.id)
        .first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.status != "ready" or not document.extracted_text:
        raise HTTPException(status_code=400, detail="Document is not ready for course generation yet")

    try:
        course = generate_course_for_document(
            db, current_user.id, str(document.id), document.extracted_text
        )
    except GroqServiceError as e:
        raise HTTPException(status_code=429 if e.is_rate_limit else 502, detail=e.message)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"AI course generation failed: {e}")

    return course


@router.get("", response_model=list[CourseOut])
def list_courses(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Course)
        .filter(Course.user_id == current_user.id)
        .order_by(Course.created_at.desc())
        .all()
    )


@router.get("/{course_id}", response_model=CourseDetailOut)
def get_course(
    course_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    course = (
        db.query(Course)
        .filter(Course.id == course_id, Course.user_id == current_user.id)
        .first()
    )
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    chapters = (
        db.query(Chapter)
        .filter(Chapter.course_id == course.id)
        .order_by(Chapter.order_index)
        .all()
    )

    completed_lesson_ids = {
        p.lesson_id
        for p in db.query(Progress).filter(Progress.user_id == current_user.id, Progress.completed == True)
    }

    chapter_outs = []
    for ch in chapters:
        lessons = (
            db.query(Lesson)
            .filter(Lesson.chapter_id == ch.id)
            .order_by(Lesson.order_index)
            .all()
        )
        lesson_outs = [
            LessonOut(
                id=str(l.id),
                title=l.title,
                order_index=l.order_index,
                content=l.content,
                key_takeaways=l.key_takeaways,
                examples=l.examples,
                summary=l.summary,
                completed=l.id in completed_lesson_ids,
            )
            for l in lessons
        ]
        chapter_outs.append(
            ChapterOut(id=str(ch.id), title=ch.title, order_index=ch.order_index, lessons=lesson_outs)
        )

    return CourseDetailOut(
        id=str(course.id),
        document_id=str(course.document_id) if course.document_id else None,
        title=course.title,
        description=course.description,
        difficulty=course.difficulty,
        estimated_duration=course.estimated_duration,
        objectives=course.objectives,
        prerequisites=course.prerequisites,
        status=course.status,
        created_at=course.created_at,
        chapters=chapter_outs,
    )
