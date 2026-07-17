# Screenshot Guide

## How to Capture Professional Screenshots

### Required Screenshots
1. **Landing Page** (`screenshots/landing.png`)
2. **Dashboard** (`screenshots/dashboard.png`)
3. **Upload Flow** (`screenshots/upload.png`)
4. **Course View** (`screenshots/course-view.png`)
5. **AI Tutor Chat** (`screenshots/chatbot.png`)
6. **Quiz** (`screenshots/quiz.png`)
7. **Flashcards** (`screenshots/flashcards.png`)

---

## Setup

### 1. Create screenshots folder
```bash
mkdir screenshots
```

### 2. Prepare your environment
- Use Chrome or Edge (best rendering)
- Set browser zoom to 100%
- Use a clean browser window (no bookmarks bar, close dev tools)
- Use a resolution of 1920x1080 or 1440x900

### 3. Use sample data
- Upload a professional-looking PDF (not random test documents)
- Use a PDF with clean formatting and interesting content
- Complete a few lessons and quizzes before taking screenshots
- Have 2-3 courses in dashboard for better visuals

---

## Screenshot Checklist

### Landing Page
**What to capture:**
- Full page from nav to footer
- Show hero section prominently
- Include feature cards

**How to capture:**
1. Go to `http://localhost:3000` (or your deployed URL)
2. Log out if logged in
3. Use full-page screenshot tool or browser extension
4. Save as `screenshots/landing.png`

**Tool suggestion:** Use browser's built-in screenshot or [Full Page Screen Capture extension](https://chrome.google.com/webstore/detail/full-page-screen-capture/)

---

### Dashboard
**What to capture:**
- Stats cards (total courses, lessons completed, completion %, quiz scores)
- Recent courses list with course cards

**Preparation:**
- Have at least 2-3 courses created
- Complete a few lessons to show progress
- Take at least one quiz to show scores

**How to capture:**
1. Go to `/dashboard`
2. Screenshot the main content area
3. Save as `screenshots/dashboard.png`

---

### Upload Flow
**What to capture:**
- Upload form with "Choose PDF" button
- Loading indicators showing progress steps
- Can be a composite of 2 screenshots side-by-side

**How to capture:**
1. Go to `/upload`
2. Take screenshot of initial state
3. Upload a PDF and immediately take screenshot showing loading steps
4. Use image editor to combine both or choose the loading state screenshot
5. Save as `screenshots/upload.png`

**Alternative:** Record video and extract a frame showing the loading indicators

---

### Course View
**What to capture:**
- Sidebar with chapters and lessons
- Main content area with a lesson open
- Progress bar visible
- Tabs (Lesson, Quiz, Flashcards, AI Tutor) visible

**Preparation:**
- Open a course with well-formatted content
- Choose a lesson with key takeaways and examples
- Show progress bar partially filled (not 0% or 100%)

**How to capture:**
1. Go to `/course/[id]`
2. Select a lesson in the middle of the course
3. Scroll to show content + key takeaways
4. Screenshot full window or main content area
5. Save as `screenshots/course-view.png`

---

### AI Tutor Chat
**What to capture:**
- Chat interface with 3-4 messages
- Show both user questions and AI responses
- Responses should look grounded (not generic)

**Preparation:**
- Ask 2-3 relevant questions about the PDF content
- Make sure responses reference the document

**Example questions:**
- "What are the main concepts covered in this document?"
- "Can you explain [specific topic from PDF]?"
- "What examples are provided for [concept]?"

**How to capture:**
1. Go to course and switch to "AI Tutor" tab
2. Have a short conversation (3-4 exchanges)
3. Scroll to show conversation flow
4. Screenshot the chat panel
5. Save as `screenshots/chatbot.png`

---

### Quiz
**What to capture:**
- Generated quiz questions (2-3 visible)
- One or more questions answered
- Ideally show the graded state with explanations

**Preparation:**
- Generate a quiz for a chapter
- Answer 2-3 questions
- Submit and get grading + explanations

**How to capture:**
1. Go to course and switch to "Quiz" tab
2. Generate quiz if not already done
3. Answer questions and submit
4. Screenshot showing questions + grading + explanations
5. Save as `screenshots/quiz.png`

---

### Flashcards
**What to capture:**
- Flashcard interface showing front or back
- Navigation controls
- Counter showing "1 / 10" or similar

**Preparation:**
- Generate flashcards for a chapter

**How to capture:**
1. Go to course and switch to "Flashcards" tab
2. Generate flashcards
3. Screenshot showing a card (either front or flipped to back)
4. Save as `screenshots/flashcards.png`

---

## Tips for Professional Screenshots

### Visual Polish
- **Clean up:** Close unnecessary browser tabs
- **Consistent theme:** Use light mode or dark mode consistently
- **High resolution:** Capture at actual size, don't downscale excessively
- **No sensitive data:** Use dummy data, not real personal information

### Composition
- **Center the important content:** Main feature should be in focus
- **Show context:** Include enough UI to understand the feature
- **Avoid clutter:** Don't show too many open panels or dialogs

### Annotations (Optional)
- Use image editor to add arrows or highlights for key features
- Add subtle shadows or borders to make screenshots pop
- Keep annotations minimal and professional

### File Management
- Save as PNG (better quality than JPG for screenshots)
- Name files consistently (lowercase, hyphens not underscores)
- Compress if needed but maintain readability

---

## Tools

### Screenshot Capture
- **Windows:** Win + Shift + S (Snipping Tool)
- **Mac:** Cmd + Shift + 4
- **Chrome:** DevTools → Cmd/Ctrl + Shift + P → "Capture screenshot"
- **Extensions:** 
  - [Awesome Screenshot](https://www.awesomescreenshot.com/)
  - [Nimbus Screenshot](https://chrome.google.com/webstore/detail/nimbus-screenshot-screen/)

### Image Editing (Optional)
- **Online:** [Photopea](https://www.photopea.com/) (free, Photoshop-like)
- **Desktop:** Paint, Preview (Mac), GIMP (free, advanced)
- **Quick edits:** Windows Paint, Mac Preview

### Optimization
- [TinyPNG](https://tinypng.com/) — compress PNG files without visible quality loss
- [Squoosh](https://squoosh.app/) — image compression tool by Google

---

## After Taking Screenshots

1. **Review each screenshot:**
   - Is the content clear and readable?
   - Is the resolution appropriate?
   - Does it show the intended feature?

2. **Add to README:**
   - Replace placeholder paths with actual images
   - Ensure all images are committed to git

3. **Test in README:**
   - View README in GitHub to ensure images display correctly
   - Check that paths are relative and correct

4. **Commit to git:**
```bash
git add screenshots/*.png
git commit -m "Add application screenshots for README"
git push
```

---

## Checklist

- [ ] Created `screenshots/` folder
- [ ] Captured landing page
- [ ] Captured dashboard with populated data
- [ ] Captured upload flow with loading states
- [ ] Captured course view with lesson content
- [ ] Captured AI tutor chat with conversation
- [ ] Captured quiz with questions and grading
- [ ] Captured flashcards interface
- [ ] Reviewed all screenshots for quality
- [ ] Updated README.md with correct image paths
- [ ] Committed screenshots to git repository
- [ ] Verified screenshots display correctly in GitHub README
