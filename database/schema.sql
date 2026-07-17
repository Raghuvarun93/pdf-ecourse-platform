-- ============================================================
-- PDF to E-Course Learning Platform — Supabase Postgres Schema
-- Run this in Supabase SQL Editor (Project > SQL Editor > New query)
-- ============================================================

-- Supabase already provides auth.users. We reference it via UUID.

create extension if not exists "uuid-ossp";

-- ---------------------------------------------------------------
-- 1. Profiles (mirrors auth.users, holds app-specific user data)
-- ---------------------------------------------------------------
create table if not exists public.profiles (
    id uuid primary key references auth.users(id) on delete cascade,
    name text,
    avatar_url text,
    created_at timestamptz default now()
);

-- Auto-create a profile row whenever a new auth user signs up
create or replace function public.handle_new_user()
returns trigger as $$
begin
    insert into public.profiles (id, name, avatar_url)
    values (new.id, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'avatar_url');
    return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
    after insert on auth.users
    for each row execute procedure public.handle_new_user();

-- ---------------------------------------------------------------
-- 2. Documents (uploaded PDFs)
-- ---------------------------------------------------------------
create table if not exists public.documents (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references public.profiles(id) on delete cascade,
    filename text not null,
    storage_path text not null,       -- path in Supabase Storage bucket
    page_count int,
    extracted_text text,              -- full extracted PDF text (used for course generation + RAG)
    status text default 'uploaded',   -- uploaded | processing | ready | failed
    created_at timestamptz default now()
);

-- ---------------------------------------------------------------
-- 3. Courses
-- ---------------------------------------------------------------
create table if not exists public.courses (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references public.profiles(id) on delete cascade,
    document_id uuid references public.documents(id) on delete set null,
    title text not null,
    description text,
    difficulty text,                  -- beginner | intermediate | advanced
    estimated_duration text,
    objectives jsonb,                 -- array of strings
    prerequisites jsonb,              -- array of strings
    status text default 'generating', -- generating | ready | failed
    created_at timestamptz default now()
);

-- ---------------------------------------------------------------
-- 4. Chapters
-- ---------------------------------------------------------------
create table if not exists public.chapters (
    id uuid primary key default uuid_generate_v4(),
    course_id uuid references public.courses(id) on delete cascade,
    title text not null,
    order_index int not null default 0,
    created_at timestamptz default now()
);

-- ---------------------------------------------------------------
-- 5. Lessons (topics/subtopics live inside a lesson's content as structured JSON)
-- ---------------------------------------------------------------
create table if not exists public.lessons (
    id uuid primary key default uuid_generate_v4(),
    chapter_id uuid references public.chapters(id) on delete cascade,
    title text not null,
    order_index int not null default 0,
    content text,               -- markdown explanation
    key_takeaways jsonb,        -- array of strings
    examples jsonb,             -- array of strings
    summary text,
    created_at timestamptz default now()
);

-- ---------------------------------------------------------------
-- 6. Progress tracking
-- ---------------------------------------------------------------
create table if not exists public.progress (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references public.profiles(id) on delete cascade,
    lesson_id uuid references public.lessons(id) on delete cascade,
    completed boolean default false,
    completed_at timestamptz,
    unique(user_id, lesson_id)
);

-- ---------------------------------------------------------------
-- 7. Chat history (AI companion)
-- ---------------------------------------------------------------
create table if not exists public.chat_history (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references public.profiles(id) on delete cascade,
    course_id uuid references public.courses(id) on delete cascade,
    question text not null,
    answer text not null,
    created_at timestamptz default now()
);

-- ---------------------------------------------------------------
-- 8. Quizzes
-- ---------------------------------------------------------------
create table if not exists public.quizzes (
    id uuid primary key default uuid_generate_v4(),
    chapter_id uuid references public.chapters(id) on delete cascade,
    question text not null,
    options jsonb not null,      -- array of 4 strings
    correct_answer text not null,
    explanation text,
    created_at timestamptz default now()
);

-- ---------------------------------------------------------------
-- 9. Quiz attempts
-- ---------------------------------------------------------------
create table if not exists public.quiz_attempts (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references public.profiles(id) on delete cascade,
    quiz_id uuid references public.quizzes(id) on delete cascade,
    selected_answer text,
    is_correct boolean,
    created_at timestamptz default now()
);

-- ---------------------------------------------------------------
-- Row Level Security (RLS) — users can only see their own data
-- ---------------------------------------------------------------
alter table public.documents enable row level security;
alter table public.courses enable row level security;
alter table public.chapters enable row level security;
alter table public.lessons enable row level security;
alter table public.progress enable row level security;
alter table public.chat_history enable row level security;
alter table public.quiz_attempts enable row level security;

create policy "own documents" on public.documents
    for all using (auth.uid() = user_id);

create policy "own courses" on public.courses
    for all using (auth.uid() = user_id);

create policy "chapters via course ownership" on public.chapters
    for all using (
        exists (select 1 from public.courses c where c.id = course_id and c.user_id = auth.uid())
    );

create policy "lessons via chapter ownership" on public.lessons
    for all using (
        exists (
            select 1 from public.chapters ch
            join public.courses c on c.id = ch.course_id
            where ch.id = chapter_id and c.user_id = auth.uid()
        )
    );

create policy "own progress" on public.progress
    for all using (auth.uid() = user_id);

create policy "own chat history" on public.chat_history
    for all using (auth.uid() = user_id);

create policy "own quiz attempts" on public.quiz_attempts
    for all using (auth.uid() = user_id);

-- quizzes are readable if you own the parent course
alter table public.quizzes enable row level security;
create policy "quizzes via chapter ownership" on public.quizzes
    for all using (
        exists (
            select 1 from public.chapters ch
            join public.courses c on c.id = ch.course_id
            where ch.id = chapter_id and c.user_id = auth.uid()
        )
    );

-- ---------------------------------------------------------------
-- 10. Flashcards (bonus feature)
-- ---------------------------------------------------------------
create table if not exists public.flashcards (
    id uuid primary key default uuid_generate_v4(),
    chapter_id uuid references public.chapters(id) on delete cascade,
    front text not null,
    back text not null,
    created_at timestamptz default now()
);

alter table public.flashcards enable row level security;
create policy "flashcards via chapter ownership" on public.flashcards
    for all using (
        exists (
            select 1 from public.chapters ch
            join public.courses c on c.id = ch.course_id
            where ch.id = chapter_id and c.user_id = auth.uid()
        )
    );

-- ---------------------------------------------------------------
-- Migration: if you already ran the schema before this table
-- existed, this whole block is safe to re-run (uses IF NOT EXISTS).
-- ---------------------------------------------------------------
alter table public.documents add column if not exists extracted_text text;
