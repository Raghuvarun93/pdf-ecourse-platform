# Pre-Submission Testing Checklist

## Full User Flow Test

### 1. Authentication
- [ ] Sign up with email/password
- [ ] Sign up with Google OAuth
- [ ] Log out and log back in
- [ ] Verify protected routes redirect to `/login` when not authenticated
- [ ] Verify dashboard loads after successful login

### 2. PDF Upload
- [ ] Upload a valid text-based PDF (5-10 pages)
- [ ] Verify loading indicators show correct steps:
  - [ ] "📄 Uploading PDF..."
  - [ ] "📖 Extracting text..."
  - [ ] "🤖 Designing course structure..."
  - [ ] "📝 Writing lessons..."
  - [ ] "🧠 Almost there..."
- [ ] Verify redirect to course page after generation completes
- [ ] Test error cases:
  - [ ] Upload a non-PDF file (should reject)
  - [ ] Upload an empty PDF (should show error)
  - [ ] Upload a file >30MB (should show error)
  - [ ] Upload a scanned/image-only PDF (should fail gracefully with explanation)
  - [ ] Test with slow/interrupted network (check error message quality)

### 3. Course Viewer
- [ ] Verify course title, description, difficulty, duration display correctly
- [ ] Verify progress bar shows 0% initially
- [ ] Click through all lessons in all chapters
- [ ] Verify lesson content renders properly (text, code blocks, lists)
- [ ] Verify "Key Takeaways" section displays
- [ ] Verify "Examples" section displays
- [ ] Verify "Summary" displays at bottom
- [ ] Mark a lesson complete → verify checkmark appears in sidebar
- [ ] Mark a lesson complete → verify progress bar updates
- [ ] Verify "Continue →" button navigates to next lesson
- [ ] Complete all lessons → verify "Take Quiz →" appears at the end

### 4. AI Tutor Chat
- [ ] Switch to "AI Tutor" tab
- [ ] Ask a question clearly answered in the PDF
  - [ ] Verify response is grounded in the document
  - [ ] Verify response doesn't hallucinate information
- [ ] Ask a question NOT covered in the PDF
  - [ ] Verify chatbot honestly says "not in the source material"
- [ ] Ask 3-5 follow-up questions
  - [ ] Verify conversation history is maintained
- [ ] Refresh the page
  - [ ] Verify chat history persists (loads from backend)
- [ ] Test error cases:
  - [ ] Submit an empty message (should be disabled/ignored)
  - [ ] Test with very long question (>500 words)

### 5. Quiz
- [ ] Switch to "Quiz" tab
- [ ] Click "Generate Quiz" for a chapter
- [ ] Verify loading state shows during generation
- [ ] Verify 10 multiple-choice questions appear
- [ ] Answer all questions (mix of correct and incorrect)
- [ ] Submit quiz
- [ ] Verify grading happens (shows correct/incorrect)
- [ ] Verify explanations appear for each question
- [ ] Verify score is calculated and displayed
- [ ] Navigate away and come back
  - [ ] Verify quiz results persist (don't need to regenerate)
- [ ] Test error cases:
  - [ ] Generate quiz while AI is unavailable (check error message)
  - [ ] Submit quiz without answering all questions (should be prevented or warned)

### 6. Flashcards (if implemented)
- [ ] Switch to "Flashcards" tab
- [ ] Generate flashcards for a chapter
- [ ] Flip cards front/back
- [ ] Navigate through all cards
- [ ] Verify flashcards persist after page refresh

### 7. Dashboard
- [ ] Return to dashboard from course
- [ ] Verify stats display correctly:
  - [ ] Total courses count
  - [ ] Lessons completed count
  - [ ] Completion percentage
  - [ ] Average quiz score (if quizzes taken)
- [ ] Verify recent courses list shows uploaded courses
- [ ] Click on a course card → verify it navigates to course page

### 8. Search (if implemented)
- [ ] Use search to find a keyword from a lesson
- [ ] Verify search results list relevant lessons
- [ ] Click a search result → verify it jumps to that lesson

## Browser Compatibility
- [ ] Test in Chrome/Edge
- [ ] Test in Firefox
- [ ] Test in Safari (if on Mac)

## Mobile Responsiveness
- [ ] Open on mobile device or use Chrome DevTools device mode
- [ ] Verify landing page looks good
- [ ] Verify dashboard is usable
- [ ] Verify course sidebar collapses or stacks properly
- [ ] Verify quiz is readable and usable
- [ ] Verify chat interface works on mobile

## Performance & Edge Cases
- [ ] Upload a large PDF (20-30 pages) → verify it completes without timeout
- [ ] Upload 2-3 PDFs in sequence → verify all generate successfully
- [ ] Have 2+ browser tabs open with same course → verify progress syncs
- [ ] Test with slow 3G network throttling (Chrome DevTools)
- [ ] Check browser console for JavaScript errors (should be none)
- [ ] Check backend logs for Python errors (should be none)

## Deployment Checks
- [ ] Verify backend is deployed and accessible at your Render URL
- [ ] Verify frontend is deployed and accessible at your Vercel URL
- [ ] Verify environment variables are set correctly in both platforms
- [ ] Test the full flow on the deployed version (not just localhost)
- [ ] Verify CORS is configured correctly (frontend can call backend)
- [ ] Verify Supabase redirect URLs include your deployed frontend URL

## Documentation Review
- [ ] README has clear setup instructions
- [ ] README includes screenshots of all major features
- [ ] README explains technical decisions (FastAPI, ChromaDB, Groq)
- [ ] README lists known limitations honestly
- [ ] README has a demo script section
- [ ] All environment variable examples are provided (.env.example files)

## Final Polish
- [ ] Fix any console warnings/errors
- [ ] Remove any debug console.log statements
- [ ] Ensure all loading states have spinners or progress indicators
- [ ] Ensure all error states show user-friendly messages
- [ ] Verify no broken links or navigation issues
- [ ] Verify no typos in UI text or README
- [ ] Ensure consistent styling across all pages

## Demo Preparation
- [ ] Have a sample PDF ready (5-10 pages, interesting topic)
- [ ] Prepare 2-3 questions for the AI tutor (1 answerable, 1 not in PDF)
- [ ] Practice the full flow in 5-7 minutes
- [ ] Be ready to explain technical decisions
- [ ] Be ready to discuss what you'd improve with more time
- [ ] Be ready to explain how RAG works in simple terms

---

## Common Issues & Fixes

### "Failed to process PDF"
- PDF might be scanned/image-only (no text layer)
- PDF might be corrupted
- PDF might be too complex (lots of tables/images)
- **Fix:** Use a different test PDF with clear text content

### Chat gives wrong answers
- Vector search might not be finding relevant chunks
- **Fix:** Check chunk size in `pdf_extractor.py` (try 500-1000 chars)
- **Fix:** Increase number of retrieved chunks in `chatbot.py`

### ChromaDB data disappears after backend redeploy
- Render free tier doesn't persist disk between deploys
- **Expected behavior** — mention this as a known limitation
- **Future improvement:** migrate to Pinecone or Weaviate

### Quiz generation is slow
- Groq free tier has rate limits
- **Expected behavior** for free tier
- **Workaround:** Generate quizzes ahead of time during course generation

### Progress doesn't sync across tabs
- Frontend might be caching stale data
- **Fix:** Refetch course data when tab becomes visible (use `visibilitychange` event)

---

## Sign-off

- [ ] I have tested the full user flow end-to-end
- [ ] I have fixed all critical bugs
- [ ] I have added screenshots to the README
- [ ] I have prepared my demo script
- [ ] I am ready to submit

**Tester Name:** ___________________  
**Date:** ___________________  
**Notes:**

