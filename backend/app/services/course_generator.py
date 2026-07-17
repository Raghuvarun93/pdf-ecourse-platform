import uuid
from sqlalchemy.orm import Session
from app.services.groq_client import chat_completion_json
from app.models.models import Course, Chapter, Lesson

SYSTEM_PROMPT = """You are an expert curriculum designer and educator.
Given raw text extracted from a document, design a structured, engaging learning course from it.
Always respond with valid JSON only — no markdown, no commentary, no code fences."""

# Groq's context window comfortably fits large inputs, but we cap it to keep
# generation fast and reliable within a single request.
MAX_INPUT_CHARS = 18000


def _build_prompt(document_text: str) -> str:
    truncated = document_text[:MAX_INPUT_CHARS]
    return f"""Create a structured course from the following document content.

Return ONLY JSON matching exactly this shape:
{{
  "title": "string",
  "description": "string (2-3 sentences)",
  "difficulty": "beginner | intermediate | advanced",
  "estimated_duration": "string, e.g. '3 hours'",
  "objectives": ["string", "..."],
  "prerequisites": ["string", "..."],
  "chapters": [
    {{
      "title": "string",
      "lessons": [
        {{
          "title": "string",
          "content": "markdown-formatted explanation, 200-400 words",
          "key_takeaways": ["string", "..."],
          "examples": ["string", "..."],
          "summary": "string, 1-2 sentences"
        }}
      ]
    }}
  ]
}}

Guidelines:
- Produce 3-6 chapters, each with 2-5 lessons.
- Lessons should build progressively from foundational to advanced.
- Base every lesson strictly on the document content below — do not invent facts not supported by it.

DOCUMENT CONTENT:
\"\"\"
{truncated}
\"\"\"
"""


def generate_course_for_document(db: Session, user_id: str, document_id: str, document_text: str) -> Course:
    """
    Calls Groq to design a full course structure, then persists Course > Chapters > Lessons.
    Returns the created Course row (chapters/lessons are committed separately below).
    """
    data = chat_completion_json(SYSTEM_PROMPT, _build_prompt(document_text))

    course = Course(
        id=uuid.uuid4(),
        user_id=user_id,
        document_id=document_id,
        title=data.get("title", "Untitled Course"),
        description=data.get("description", ""),
        difficulty=data.get("difficulty", "beginner"),
        estimated_duration=data.get("estimated_duration", ""),
        objectives=data.get("objectives", []),
        prerequisites=data.get("prerequisites", []),
        status="ready",
    )
    db.add(course)
    db.flush()  # get course.id populated before creating children

    for chapter_index, chapter_data in enumerate(data.get("chapters", [])):
        chapter = Chapter(
            id=uuid.uuid4(),
            course_id=course.id,
            title=chapter_data.get("title", f"Chapter {chapter_index + 1}"),
            order_index=chapter_index,
        )
        db.add(chapter)
        db.flush()

        for lesson_index, lesson_data in enumerate(chapter_data.get("lessons", [])):
            lesson = Lesson(
                id=uuid.uuid4(),
                chapter_id=chapter.id,
                title=lesson_data.get("title", f"Lesson {lesson_index + 1}"),
                order_index=lesson_index,
                content=lesson_data.get("content", ""),
                key_takeaways=lesson_data.get("key_takeaways", []),
                examples=lesson_data.get("examples", []),
                summary=lesson_data.get("summary", ""),
            )
            db.add(lesson)

    db.commit()
    db.refresh(course)
    return course
