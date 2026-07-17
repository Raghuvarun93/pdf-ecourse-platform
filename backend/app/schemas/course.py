from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentOut(BaseModel):
    id: str
    filename: str
    page_count: Optional[int] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LessonOut(BaseModel):
    id: str
    title: str
    order_index: int
    content: Optional[str] = None
    key_takeaways: Optional[list] = None
    examples: Optional[list] = None
    summary: Optional[str] = None
    completed: bool = False

    class Config:
        from_attributes = True


class ChapterOut(BaseModel):
    id: str
    title: str
    order_index: int
    lessons: list[LessonOut] = []

    class Config:
        from_attributes = True


class CourseOut(BaseModel):
    id: str
    document_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    difficulty: Optional[str] = None
    estimated_duration: Optional[str] = None
    objectives: Optional[list] = None
    prerequisites: Optional[list] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class CourseDetailOut(CourseOut):
    chapters: list[ChapterOut] = []


class GenerateCourseRequest(BaseModel):
    document_id: str
