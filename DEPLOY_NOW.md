# 🚀 DEPLOY NOW - Complete Guide

Your Project ID: **lwiwzytfxhmybxnxprxu**

---

## 📋 PART 1: Supabase Setup (10 minutes)

### Step 1: Run Database Schema

1. In Supabase, find **SQL Editor** in the left menu (icon looks like </>)
2. Click **"New query"** button
3. Open Notepad and copy this file path: `e:\Gen ai internship\pdf-ecourse\database\schema.sql`
4. Open that file in Notepad, press Ctrl+A to select all, Ctrl+C to copy
5. Go back to Supabase SQL Editor, paste (Ctrl+V)
6. Click **RUN** button (or press Ctrl+Enter)
7. Wait 2-3 seconds, you should see "Success"

---

### Step 2: Get API Keys

**A) Get anon key:**
1. In Supabase, click ⚙️ **Settings** (bottom left)
2. Click **API** 
3. Scroll down to "Project API keys" or "Legacy keys"
4. Find the key labeled **"anon"** or **"anon public"**
5. Click the copy icon or click to reveal the key
6. It's VERY LONG (400+ characters), starts with `eyJhbGc`
7. Paste it in Notepad, label it "ANON KEY"

**B) Get service_role key:**
1. Same page, find the key labeled **"service_role"** 
2. Click copy or reveal
3. Also VERY LONG, starts with `eyJhbGc` (different from anon)
4. Paste in Notepad, label it "SERVICE ROLE KEY"

**C) Get Database Password:**
- What password did you create when you first made this Supabase project?
- Write it down in Notepad as "DB PASSWORD"

**D) Your Project URL (already found):**
```
https://lwiwzytfxhmybxnxprxu.supabase.co
```

---

### Step 3: Build Database Connection String

Copy this and replace `YOUR_PASSWORD_HERE`:

```
postgresql://postgres.lwiwzytfxhmybxnxprxu:YOUR_PASSWORD_HERE@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

Replace `YOUR_PASSWORD_HERE` with your actual database password.

Save this as "DATABASE URL" in Notepad.

---

## 📋 PART 2: Groq API Key (3 minutes)

1. Go to: https://console.groq.com
2. Sign up or log in (use Google for fastest)
3. Click **"API Keys"** in left sidebar
4. Click **"Create API Key"** button
5. Name: `pdf-ecourse`
6. Click **Submit**
7. Copy the key (starts with `gsk_`)
8. Save in Notepad as "GROQ KEY"

---

## 📋 PART 3: Deploy to Render (15 minutes)

### Go back to your Render tab (where you were configuring)

Add these **6 Environment Variables**:

#### Variable 1: DATABASE_URL
- Key: `DATABASE_URL`
- Value: `postgresql://postgres.lwiwzytfxhmybxnxprxu:YOUR_PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres`
  - (Replace YOUR_PASSWORD with your actual password)

#### Variable 2: SUPABASE_URL
- Key: `SUPABASE_URL`
- Value: `https://lwiwzytfxhmybxnxprxu.supabase.co`

#### Variable 3: SUPABASE_JWT_SECRET
- Key: `SUPABASE_JWT_SECRET`
- Value: `[Your SERVICE ROLE key from Notepad]`
  - Paste the LONG key starting with `eyJhbGc...`

#### Variable 4: GROQ_API_KEY
- Key: `GROQ_API_KEY`
- Value: `[Your Groq key from Notepad]`
  - Starts with `gsk_...`

#### Variable 5: CORS_ORIGINS
- Key: `CORS_ORIGINS`
- Value: `http://localhost:3000`

#### Variable 6: UPLOAD_DIR
- Key: `UPLOAD_DIR`
- Value: `./uploads`

### Check These Settings:
- ✅ Name: `pdf-ecourse-backend` (or whatever you want)
- ✅ Root Directory: **`backend`** (MUST be set!)
- ✅ Branch: `main`
- ✅ Instance Type: Free

### Click "Deploy web service" at the bottom!

Wait 5-10 minutes. You'll get a URL like: `https://pdf-ecourse-backend.onrender.com`

---

## 📋 PART 4: Deploy to Vercel (10 minutes)

1. Go to: https://vercel.com
2. Sign up/login with GitHub
3. Click **"Add New..."** → **"Project"**
4. Find **`Raghuvarun93/pdf-ecourse-platform`**
5. Click **"Import"**

### Configure:
- Project Name: `pdf-ecourse-frontend`
- ⚠️ **Root Directory:** Click "Edit" → Type **`frontend`** → Save
- Framework: Next.js (auto-detected)

### Add 3 Environment Variables:

#### Variable 1:
- Key: `NEXT_PUBLIC_SUPABASE_URL`
- Value: `https://lwiwzytfxhmybxnxprxu.supabase.co`

#### Variable 2:
- Key: `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Value: `[Your ANON key from Notepad]`
  - The LONG key starting with `eyJhbGc...`

#### Variable 3:
- Key: `NEXT_PUBLIC_API_URL`
- Value: `[Your Render backend URL]`
  - Wait for Render to finish, then copy the URL
  - Like: `https://pdf-ecourse-backend.onrender.com`

### Click "Deploy"!

Wait 3-5 minutes. You'll get a URL like: `https://pdf-ecourse-frontend.vercel.app`

---

## 📋 PART 5: Final Updates (5 minutes)

### A) Update CORS in Render:
1. Go back to Render
2. Click your service
3. Click **"Environment"** in left sidebar
4. Find `CORS_ORIGINS`
5. Click "Edit"
6. Change to: `http://localhost:3000,https://YOUR-VERCEL-URL`
   - Replace YOUR-VERCEL-URL with your actual Vercel URL
7. Save (will auto-redeploy)

### B) Update Supabase Redirect URLs:
1. Go to Supabase
2. **Authentication** → **URL Configuration**
3. Under "Redirect URLs", add:
   - `https://YOUR-VERCEL-URL/auth/callback`
4. Click Save

---

## ✅ YOUR LIVE URLS:

**Frontend:** https://[your-app].vercel.app  
**Backend:** https://[your-backend].onrender.com  
**GitHub:** https://github.com/Raghuvarun93/pdf-ecourse-platform

---

## 🆘 STUCK? Tell me which step and I'll help!

**Common issues:**
- Can't find SQL Editor → Look for </> icon in left sidebar
- Can't find API keys → Settings (gear icon) → API → scroll down
- Render build fails → Make sure Root Directory is set to `backend`
- Vercel build fails → Make sure Root Directory is set to `frontend`

---

**Where are you stuck? Tell me the step number and I'll guide you through it!**
