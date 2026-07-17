# Pre-Launch Checklist

Complete this checklist before submitting your project for the internship evaluation.

---

## Code Quality

### Backend
- [ ] No debug `print()` statements in production code
- [ ] All routes have proper error handling with HTTPException
- [ ] Environment variables are loaded from `.env` (not hardcoded)
- [ ] `.env.example` file is complete with all required variables
- [ ] No sensitive keys/tokens committed to git (check git history)
- [ ] All API endpoints return appropriate HTTP status codes
- [ ] CORS is configured correctly for your frontend domain
- [ ] Database connection uses pooling (check `database.py`)
- [ ] All imports are used (no unused imports)

### Frontend
- [ ] No `console.log()` statements (or only intentional ones)
- [ ] `.env.local.example` file is complete
- [ ] No hardcoded API URLs (use environment variables)
- [ ] All TypeScript errors are resolved (`npm run build` succeeds)
- [ ] No unused imports or variables
- [ ] All components have proper error boundaries
- [ ] Loading states are shown for all async operations
- [ ] Error messages are user-friendly (not raw API errors)

---

## Testing

- [ ] Completed full user flow test (see `TESTING_CHECKLIST.md`)
- [ ] Tested with different PDF sizes and types
- [ ] Tested all error scenarios (invalid PDF, network errors, etc.)
- [ ] Tested on Chrome/Edge
- [ ] Tested on Firefox
- [ ] Tested on Safari (if available)
- [ ] Tested mobile responsiveness (use DevTools device mode)
- [ ] No console errors in browser DevTools
- [ ] No errors in backend logs

---

## Deployment

### Backend (Render)
- [ ] Backend is deployed and accessible
- [ ] All environment variables are set in Render dashboard
- [ ] Health check endpoint works: `GET /health`
- [ ] API docs are accessible: `GET /docs`
- [ ] CORS_ORIGINS includes your Vercel frontend URL
- [ ] Database connection works (test by uploading a PDF)
- [ ] ChromaDB directory is writable (check logs)
- [ ] Free tier disk space warning is acknowledged

### Frontend (Vercel)
- [ ] Frontend is deployed and accessible
- [ ] All environment variables are set in Vercel dashboard
- [ ] `NEXT_PUBLIC_API_URL` points to Render backend
- [ ] Supabase environment variables are correct
- [ ] Build succeeds without errors
- [ ] All pages load correctly on production URL

### Supabase
- [ ] Database schema is applied (from `database/schema.sql`)
- [ ] RLS policies are enabled and working
- [ ] Authentication providers are enabled (Google OAuth + Email)
- [ ] Redirect URLs include both localhost and Vercel URLs
- [ ] `auth/callback` route is in allowed redirect list
- [ ] Test authentication on deployed app

---

## Documentation

### README.md
- [ ] Project title and description are clear
- [ ] Features list is complete and accurate
- [ ] "Not implemented" section honestly lists missing features
- [ ] Setup instructions are step-by-step and clear
- [ ] All environment variables are documented
- [ ] API reference table is complete
- [ ] Deployment section has instructions for Render + Vercel
- [ ] Screenshots section is populated with actual images
- [ ] Technical decisions section explains key choices
- [ ] Known limitations are clearly stated
- [ ] Demo script is included
- [ ] Project structure diagram is accurate

### Additional Docs
- [ ] `.env.example` files exist for both backend and frontend
- [ ] `requirements.txt` has all Python dependencies with versions
- [ ] `package.json` has all Node dependencies
- [ ] `render.yaml` is configured correctly
- [ ] `database/schema.sql` is the latest version

---

## Screenshots

- [ ] All 7 screenshots are captured (see `SCREENSHOT_GUIDE.md`)
- [ ] Screenshots are high quality and readable
- [ ] Screenshots show the app with realistic data (not empty/test data)
- [ ] Images are committed to git in `screenshots/` folder
- [ ] README references the correct screenshot paths
- [ ] Screenshots display correctly in GitHub README

---

## Security & Best Practices

- [ ] No API keys or secrets in frontend code
- [ ] No API keys or secrets committed to git
- [ ] JWT tokens are verified on every protected backend route
- [ ] Database queries use parameterization (SQLAlchemy ORM)
- [ ] User data is isolated (RLS policies working)
- [ ] CORS is restricted to known origins (not `*` in production)
- [ ] File upload size limits are enforced (30MB max)
- [ ] Uploaded files are validated (PDF mime type check)
- [ ] Error messages don't expose internal implementation details

---

## Performance

- [ ] PDF extraction completes in reasonable time (<30s for 10-page PDF)
- [ ] Course generation completes in reasonable time (<40s)
- [ ] Chat responses return in <5 seconds
- [ ] Quiz generation completes in <20 seconds
- [ ] Dashboard loads quickly (<2s)
- [ ] Images/assets are optimized (if using custom images)
- [ ] No memory leaks in long-running sessions

---

## User Experience

- [ ] All forms have clear labels and placeholders
- [ ] All buttons have hover states
- [ ] All loading states have spinners or progress indicators
- [ ] All error states have helpful messages
- [ ] Navigation is intuitive (no dead ends)
- [ ] Mobile experience is usable (responsive design works)
- [ ] Text is readable (good contrast, font sizes)
- [ ] No layout shifts during loading
- [ ] Success feedback is shown (e.g., "Lesson marked complete")

---

## Demo Preparation

- [ ] Practiced the full demo script (see `DEMO_SCRIPT.md`)
- [ ] Demo completes in 5-7 minutes
- [ ] Prepared answers to anticipated questions
- [ ] Backup plan ready if something fails during demo
- [ ] Sample PDF is professional and appropriate
- [ ] Can explain technical decisions confidently
- [ ] Can explain RAG architecture simply
- [ ] Can discuss what you'd improve with more time

---

## Git & GitHub

- [ ] All changes are committed
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts in main branch
- [ ] `.gitignore` excludes `.env`, `node_modules/`, `venv/`, etc.
- [ ] Repository is public (or accessible to reviewers)
- [ ] README is the first thing visible in repo
- [ ] No large files committed (PDFs, videos, etc.)
- [ ] Git history is clean (no sensitive data in past commits)

---

## Final Checks

- [ ] Deployed app URL is accessible from any browser
- [ ] Can complete full user flow on deployed app (not just localhost)
- [ ] All links in README are working
- [ ] No "TODO" or "FIXME" comments in production code
- [ ] Project name and branding are consistent everywhere
- [ ] Contact information or GitHub profile is included
- [ ] License file is included (if required)

---

## Submission

- [ ] GitHub repository URL is ready to share
- [ ] Deployed frontend URL is ready to share
- [ ] Deployed backend URL is ready to share (if needed)
- [ ] Demo video is recorded (if required by assignment)
- [ ] Assignment submission form is filled out
- [ ] Submitted before the deadline

---

## Optional Enhancements (If Time Permits)

- [ ] Add loading skeleton screens instead of spinners
- [ ] Add toast notifications for success/error feedback
- [ ] Add keyboard shortcuts for navigation
- [ ] Add accessibility improvements (ARIA labels, focus management)
- [ ] Add analytics tracking (Google Analytics, Mixpanel, etc.)
- [ ] Add a tutorial/onboarding flow for first-time users
- [ ] Add PDF preview before upload
- [ ] Add course sharing functionality
- [ ] Add export course to PDF/Markdown
- [ ] Add dark mode toggle

---

## Sign-Off

**I confirm that:**
- [ ] I have completed all items in this checklist
- [ ] I have tested the application thoroughly
- [ ] I am confident in the quality and stability of my submission
- [ ] I am prepared to demo and defend my technical decisions

**Name:** ___________________  
**Date:** ___________________  
**Time to submission:** ___________________
