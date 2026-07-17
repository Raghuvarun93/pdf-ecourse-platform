# Demo Script (5-7 Minutes)

## Preparation (Before Demo)
- [ ] Have the deployed app open in browser (Vercel URL)
- [ ] Have a fresh incognito/private window ready
- [ ] Prepare a PDF (5-10 pages, interesting content like "Introduction to Python" or similar)
- [ ] Test the full flow once before the demo
- [ ] Close unnecessary browser tabs to avoid distractions

---

## Script

### Introduction (30 seconds)
> "Hi! Today I'm presenting my PDF to E-Course Learning Platform — a full-stack AI application that transforms any PDF into an interactive course with structured lessons, an AI tutor, and auto-generated quizzes. Let me walk you through it."

---

### 1. Landing Page (30 seconds)
**Action:** Show the landing page  
**Say:**
> "This is the landing page. The platform turns static PDFs into engaging learning experiences. Users can upload documents, get AI-generated courses, chat with an intelligent tutor, and test their knowledge with quizzes."

**Action:** Click "Get Started" or "Log in"

---

### 2. Authentication (30 seconds)
**Action:** Sign up with Google or email/password  
**Say:**
> "Authentication is handled through Supabase — supporting both Google OAuth and email/password. All routes are protected with JWT tokens and row-level security."

**Action:** Complete sign-in → land on Dashboard

---

### 3. Dashboard (30 seconds)
**Action:** Show empty or populated dashboard  
**Say:**
> "This is the dashboard. It shows total courses, lessons completed, overall completion percentage, and average quiz scores. Let's create a new course."

**Action:** Click "Upload PDF" or navigate to upload page

---

### 4. Upload & Generation (1-1.5 minutes)
**Action:** Select and upload PDF  
**Say:**
> "I'm uploading a PDF here. The backend extracts text using PyMuPDF, chunks it for vector search, and then sends it to Groq's Llama 3.3 70B model."

**Action:** Click "Generate Course"  
**Point out the loading indicators:**
> "Notice the step-by-step progress indicators: uploading, extracting text, designing the course structure, writing lessons. This typically takes 20-40 seconds depending on PDF size and API speed."

**Wait for generation to complete** (if demo time is tight, have a pre-generated course ready as backup)

---

### 5. Course Viewer (1.5 minutes)
**Action:** Navigate through a lesson  
**Say:**
> "Here's the generated course. It has a title, description, difficulty level, estimated duration, and structured chapters. The AI broke down the PDF into digestible lessons."

**Action:** Open a lesson and scroll through  
**Say:**
> "Each lesson includes detailed explanations, key takeaways, practical examples, and a summary. The content is generated from the PDF text."

**Action:** Mark a lesson complete  
**Say:**
> "I can mark lessons complete, and the progress bar updates in real-time. All progress is persisted in Postgres."

**Action:** Click "Continue" to next lesson

---

### 6. AI Tutor Chat (1.5 minutes)
**Action:** Switch to "AI Tutor" tab  
**Say:**
> "This is the RAG-powered chatbot. When I ask a question, it searches the indexed PDF chunks in ChromaDB, retrieves the most relevant sections, and uses Groq to generate a grounded answer."

**Action:** Ask a question clearly answered in the PDF (e.g., "What is a variable?")  
**Say:**
> "Notice it's answering based on the source material — it's not just pulling from general knowledge. This reduces hallucinations."

**Action:** Ask a question NOT in the PDF (e.g., "What is quantum computing?")  
**Say:**
> "And when I ask something outside the document's scope, it honestly tells me it's not covered in the source material rather than making something up."

---

### 7. Quiz (1.5 minutes)
**Action:** Switch to "Quiz" tab  
**Say:**
> "Let's test what we've learned. I'll generate a quiz for this chapter."

**Action:** Click "Generate Quiz" and show loading state  
**Say:**
> "The AI reads the chapter's lessons and creates 10 multiple-choice questions specifically about this content."

**Action:** Answer 2-3 questions quickly (mix correct and incorrect)  
**Say:**
> "I'll answer a few questions here..."

**Action:** Submit quiz  
**Say:**
> "After submission, it grades the answers server-side and provides explanations for each question. This helps reinforce learning."

---

### 8. Dashboard Return (30 seconds)
**Action:** Navigate back to Dashboard  
**Say:**
> "Back on the dashboard, we can see the stats have updated — lessons completed, quiz scores, everything is tracked."

**Action:** (Optional) Demo search feature  
**Say:**
> "There's also a search feature to jump directly to specific lessons by keyword."

---

### Technical Highlights (30 seconds)
**Say:**
> "Under the hood, this uses:
> - **FastAPI** for the backend with async support and auto-generated API docs
> - **Next.js + Tailwind** for the responsive frontend
> - **Supabase** for authentication and Postgres database with row-level security
> - **ChromaDB** for vector search and RAG
> - **Groq** for ultra-fast LLM inference with Llama 3.3 70B
> - **Deployed on Render and Vercel** for free-tier cloud hosting"

---

### Closing (15 seconds)
**Say:**
> "That's the full flow. I built this to demonstrate practical AI integration in a real-world learning application. Happy to answer any questions about the architecture, design decisions, or implementation details. Thank you!"

---

## Backup Plan
If something breaks during the demo:
- **PDF upload fails:** Have a pre-generated course ready to demonstrate
- **AI generation is slow:** Mention Groq free tier rate limits and show the pre-generated course
- **Chat doesn't work:** Explain the RAG architecture verbally and show the code
- **Quiz generation fails:** Show a pre-generated quiz or explain the prompting strategy

---

## Anticipated Questions & Answers

### "Why did you choose FastAPI over Flask/Django?"
> "FastAPI has native async support, which is crucial for handling concurrent AI requests. It also auto-generates OpenAPI documentation at `/docs`, has built-in Pydantic validation, and offers better performance with minimal overhead."

### "How does RAG work in your chatbot?"
> "When a user asks a question, I embed it and search ChromaDB for the most relevant PDF chunks using cosine similarity. I retrieve the top 3-5 chunks and pass them as context to Groq along with the question. This grounds the answer in the actual document, reducing hallucinations."

### "Why Groq instead of OpenAI?"
> "Groq offers ultra-fast inference — 800+ tokens per second on their custom LPU hardware. They have a free tier that's suitable for demos, and their API is OpenAI-compatible, so I can swap to GPT-4 if needed."

### "What are the limitations?"
> "The main limitations are: no OCR support for scanned PDFs, ChromaDB storage resets on Render's free tier redeployments, and it's currently English-only. With more time, I'd add Tesseract for OCR, migrate to a hosted vector DB like Pinecone, and add multi-language support."

### "How do you handle authentication and security?"
> "Supabase handles OAuth and JWT tokens. Every API request verifies the JWT in the `get_current_user` dependency. The Postgres database uses row-level security policies to ensure users can only access their own data. Next.js middleware protects frontend routes."

### "What would you improve with more time?"
> "I'd add: OCR for scanned PDFs, flashcards with spaced repetition algorithms, course export to PDF/Markdown, real-time collaboration features, admin analytics dashboard, and migrate to a production-grade vector database."

### "How do you ensure the AI doesn't hallucinate?"
> "By using RAG — every answer is grounded in retrieved PDF chunks. I also prompt the model to say 'I don't know' if the information isn't in the context. Additionally, I store conversation history to maintain coherence across turns."

---

## Post-Demo Checklist
- [ ] Share the deployed app link
- [ ] Share the GitHub repo link
- [ ] Offer to walk through code if they want
- [ ] Thank the reviewers for their time
