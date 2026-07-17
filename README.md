# PDF to E-Course Learning Platform

Full-stack AI app that turns any PDF into a structured, interactive course with
an AI tutor chatbot and auto-generated quizzes — built for the In2Peta
Generative AI Internship assignment.

> **📋 Preparing for Submission?** Start with **[START_HERE.md](./START_HERE.md)** for a complete submission guide!

## Features implemented

- **Auth**: Supabase Auth (Google OAuth + email/password), protected routes via middleware
- **PDF upload**: extraction via PyMuPDF (pdfplumber fallback), stored + chunked for RAG
- **AI course generation**: Groq (Llama 3.3 70B) turns extracted text into title, description,
  objectives, prerequisites, difficulty, chapters, lessons — each lesson has explanation,
  key takeaways, examples, and a summary
- **Learning progress**: mark lessons complete, per-course completion %, persists in Postgres
- **AI chatbot (RAG)**: ChromaDB vector search over the source PDF + Groq for grounded,
  context-aware answers; keeps short conversation history per course
- **Quiz generation**: Groq generates 10 MCQs per chapter from that chapter's actual lesson
  content; answers are graded server-side, explanations shown after submission
- **Dashboard**: total courses, lessons completed, completion %, average quiz score, recent courses
- **Search**: keyword search across your chapters/lessons, jumps straight to the lesson
- **Responsive UI**: Next.js + Tailwind, works on mobile and desktop

## Not implemented (call this out honestly in your demo)
- OCR for scanned/image-only PDFs (only text-based PDFs are supported)
- Flashcards, mind maps, TTS narration, course export, multi-language (bonus features — pick 1-2
  if you have spare time before the demo, they're the easiest to bolt on)
- Supabase Storage isn't used for PDFs (stored on local disk / Render disk instead) — fine for a
  demo/free-tier deployment, but call this out as a known limitation if asked

---

## Setup

### 1. Supabase project
1. Create a project at supabase.com (free tier).
2. **SQL Editor** → paste `database/schema.sql` → Run.
3. **Authentication → Providers** → enable Google (OAuth client ID/secret from Google Cloud
   Console) and confirm Email is enabled.
4. **Authentication → URL Configuration** → add `http://localhost:3000/auth/callback` and your
   future Vercel URL's `/auth/callback`.
5. **Project Settings → API** → copy Project URL, anon public key, and JWT Secret.
6. **Project Settings → Database** → copy the connection string (use the pooled one, port 6543).

### 2. Groq (free)
Sign up at console.groq.com → API Keys → create one.

### 3. Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # fill in SUPABASE_URL, SUPABASE_JWT_SECRET, DATABASE_URL, GROQ_API_KEY
uvicorn app.main:app --reload --port 8000
```
Check `http://localhost:8000/docs` — full interactive API docs (FastAPI auto-generates this).

### 4. Frontend
```bash
cd frontend
npm install
cp .env.local.example .env.local   # fill in Supabase URL/anon key + NEXT_PUBLIC_API_URL
npm run dev
```
Visit `http://localhost:3000` → sign up → Upload PDF → watch the course generate → explore
lessons, take a quiz, chat with the AI tutor.

---

## API reference (all routes require `Authorization: Bearer <supabase_access_token>`)

| Method | Path | Purpose |
|---|---|---|
| GET | `/auth/me` | current user profile |
| POST | `/documents` | upload a PDF (multipart `file`), extracts + indexes text |
| GET | `/documents` | list your uploaded documents |
| POST | `/courses/generate` | `{document_id}` → generates full course structure |
| GET | `/courses` | list your courses |
| GET | `/courses/{id}` | course + chapters + lessons + your progress |
| POST | `/chat` | `{course_id, document_id, question}` → RAG answer |
| GET | `/chat/{course_id}/history` | past chat turns for a course |
| POST | `/quiz/chapters/{chapter_id}/generate` | `{count}` → generates MCQs |
| GET | `/quiz/chapters/{chapter_id}` | fetch existing quiz (answers hidden) |
| POST | `/quiz/attempt` | `{quiz_id, selected_answer}` → grades + explains |
| POST | `/progress` | `{lesson_id, completed}` → marks a lesson done |
| GET | `/progress/course/{course_id}` | completion % for one course |
| GET | `/dashboard` | aggregate stats for the dashboard |
| GET | `/search?q=` | keyword search across your lessons |

---

## Deployment

### Backend → Render
1. Push this repo to GitHub.
2. Render → New → Blueprint → point at your repo (`render.yaml` is already set up).
3. Fill in the env vars it prompts for (Supabase URL/secret, DATABASE_URL, GROQ_API_KEY,
   CORS_ORIGINS = your Vercel URL).
4. Note: ChromaDB's `chroma_data` folder resets on redeploy on Render's free tier (no second
   disk) — documents will need re-uploading after a redeploy. Fine for a demo; mention it as a
   known limitation if asked, and as a next step point to a hosted vector DB (Pinecone free tier).

### Frontend → Vercel
1. Import the repo, set root directory to `frontend`.
2. Add env vars: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`,
   `NEXT_PUBLIC_API_URL` (your Render backend URL).
3. Deploy. Add the Vercel URL's `/auth/callback` to Supabase's redirect URL allowlist.

---

## Screenshots

### Landing Page
![Landing Page](./screenshots/landing.png)

### Dashboard
![Dashboard](./screenshots/dashboard.png)

### PDF Upload & Generation
![Upload Flow](./screenshots/upload.png)

### Course Viewer
![Course View](./screenshots/course-view.png)

### AI Tutor Chat
![AI Tutor](./screenshots/chatbot.png)

### Quiz
![Quiz](./screenshots/quiz.png)

### Flashcards
![Flashcards](./screenshots/flashcards.png)

---

## Demo script (for your live walkthrough)
1. Sign up with Google → land on dashboard (empty state)
2. Upload a PDF → show extraction + AI generation happening (20-40s)
3. Redirects into course viewer → walk a lesson, show key takeaways/examples
4. Mark a lesson complete → show progress bar move
5. Switch to Quiz tab → generate quiz → answer a few, show grading + explanations
6. Switch to AI Tutor tab → ask a question that's clearly answered in the PDF → show it's
   grounded (not hallucinated) → ask something not in the PDF → show it says so honestly
7. Back to dashboard → show stats updated, use search to jump to a lesson

## Technical Decisions & Interview Prep

Be ready to explain these key architectural choices:

### Why FastAPI?
- **Async support** for handling multiple AI generation requests concurrently
- **Auto-generated API docs** (OpenAPI/Swagger) at `/docs` — makes testing and integration easier
- **Pydantic validation** for request/response type safety
- **Fast performance** with minimal overhead compared to Flask/Django

### Why ChromaDB for RAG?
- **Embeddings-based search** — semantic similarity, not just keyword matching
- **Lightweight & local** — no external service needed for demo/free deployment
- **Simple Python API** — quick to integrate, minimal configuration
- **Persistence** — stores vectors on disk, no complex setup
- Next step: migrate to Pinecone/Weaviate for production persistence across deploys

### Why Groq?
- **Ultra-fast inference** (Llama 3.3 70B at 800+ tokens/sec on their LPU hardware)
- **Free tier** suitable for demo/development
- **JSON mode** for structured outputs (course structure, quiz generation)
- **OpenAI-compatible API** — easy to swap for GPT-4 if needed

### How does RAG improve chatbot responses?
1. User asks a question
2. Question is embedded and searched in ChromaDB against PDF chunks
3. Top 3-5 most relevant chunks are retrieved
4. Chunks + question are passed to Groq as context
5. Groq generates a grounded answer based on the source material
6. Result: **fewer hallucinations**, answers cite the actual document

### How is learning progress stored?
- **Progress table** with `(user_id, lesson_id, completed)` rows
- Updated via `/progress` endpoint when user marks a lesson complete
- **Dashboard aggregates** total lessons, completed count, completion %, quiz scores
- **RLS policies** ensure users only see their own progress

### How does authentication work?
- **Supabase Auth** handles OAuth (Google) + email/password
- **JWT tokens** issued by Supabase, verified in FastAPI via `get_current_user` dependency
- **Middleware.ts** in Next.js protects routes — redirects to `/login` if no session
- **RLS policies** in Postgres enforce row-level security (users can't access others' data)

### Known Limitations & Next Steps
- **ChromaDB resets on Render redeploy** (free tier has no persistent disk) → migrate to hosted vector DB
- **No OCR support** for scanned/image-only PDFs → add Tesseract or cloud OCR service
- **Single-language** (English) → add multi-language support with i18n
- **No export** — add PDF/Markdown export for generated courses

---

## Project structure
```
backend/
  app/
    main.py                # FastAPI app, CORS, router registration
    config.py                # env var loading
    database.py               # SQLAlchemy engine/session
    core/security.py           # Supabase JWT verification
    models/models.py            # SQLAlchemy models
    schemas/                     # Pydantic request/response models
    routes/                       # auth, documents, courses, chat, quiz, progress, dashboard, search
    services/
      pdf_extractor.py            # PyMuPDF + pdfplumber + chunking
      vector_store.py               # ChromaDB wrapper
      groq_client.py                  # Groq chat completion wrapper (+ JSON mode)
      course_generator.py               # prompt + persistence for course generation
      quiz_generator.py                   # prompt + persistence for quiz generation
      chatbot.py                            # RAG pipeline for the AI tutor
  requirements.txt / .env.example / Dockerfile

frontend/
  app/
    page.tsx, login/, dashboard/, upload/, course/[id]/, auth/callback/
  components/
    ChatPanel.tsx, QuizPanel.tsx
  lib/
    supabaseClient.ts, supabaseServer.ts, api.ts
  middleware.ts

database/schema.sql   # full Postgres schema + RLS policies
render.yaml            # Render deployment blueprint
```
