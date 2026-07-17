from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routes import auth, documents, courses, chat, quiz, progress, dashboard, search, flashcards

settings = get_settings()

app = FastAPI(title="PDF to E-Course API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(courses.router)
app.include_router(chat.router)
app.include_router(quiz.router)
app.include_router(progress.router)
app.include_router(dashboard.router)
app.include_router(search.router)
app.include_router(flashcards.router)


@app.get("/health")
def health():
    return {"status": "ok"}
