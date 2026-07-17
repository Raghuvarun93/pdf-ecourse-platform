"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import api from "@/lib/api";
import ChatPanel from "@/components/ChatPanel";
import QuizPanel from "@/components/QuizPanel";
import FlashcardsPanel from "@/components/FlashcardsPanel";

type Lesson = {
  id: string;
  title: string;
  content: string;
  key_takeaways: string[];
  examples: string[];
  summary: string;
  completed: boolean;
};

type Chapter = { id: string; title: string; lessons: Lesson[] };

type CourseDetail = {
  id: string;
  document_id: string | null;
  title: string;
  description: string;
  difficulty: string;
  estimated_duration: string;
  objectives: string[];
  prerequisites: string[];
  chapters: Chapter[];
};

export default function CoursePage() {
  const { id } = useParams<{ id: string }>();
  const [course, setCourse] = useState<CourseDetail | null>(null);
  const [activeLessonId, setActiveLessonId] = useState<string | null>(null);
  const [tab, setTab] = useState<"lesson" | "quiz" | "flashcards" | "chat">("lesson");
  const [activeChapterId, setActiveChapterId] = useState<string | null>(null);

  useEffect(() => {
    api.get<CourseDetail>(`/courses/${id}`).then((res) => {
      setCourse(res.data);
      const firstChapter = res.data.chapters[0];
      if (firstChapter) {
        setActiveChapterId(firstChapter.id);
        setActiveLessonId(firstChapter.lessons[0]?.id ?? null);
      }
    });
  }, [id]);

  async function toggleComplete(lessonId: string, completed: boolean) {
    await api.post("/progress", { lesson_id: lessonId, completed: !completed });
    setCourse((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        chapters: prev.chapters.map((ch) => ({
          ...ch,
          lessons: ch.lessons.map((l) =>
            l.id === lessonId ? { ...l, completed: !completed } : l
          ),
        })),
      };
    });
  }

  if (!course) return <div className="p-8 text-sm text-slate-500">Loading course...</div>;

  const activeChapter = course.chapters.find((c) => c.id === activeChapterId);
  const activeLesson = activeChapter?.lessons.find((l) => l.id === activeLessonId);

  const totalLessons = course.chapters.reduce((sum, c) => sum + c.lessons.length, 0);
  const completedLessons = course.chapters.reduce(
    (sum, c) => sum + c.lessons.filter((l) => l.completed).length,
    0
  );
  const percent = totalLessons ? Math.round((completedLessons / totalLessons) * 100) : 0;

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar: chapters + lessons */}
      <aside className="w-72 bg-white border-r border-slate-200 p-4 overflow-y-auto">
        <h2 className="font-semibold text-slate-900 mb-1">{course.title}</h2>
        <p className="text-xs text-slate-500 mb-3">{course.difficulty} · {course.estimated_duration}</p>
        <div className="h-1.5 bg-slate-100 rounded-full mb-4">
          <div
            className="h-1.5 bg-slate-900 rounded-full"
            style={{ width: `${percent}%` }}
          />
        </div>
        <p className="text-xs text-slate-500 mb-4">{percent}% complete</p>

        {course.chapters.map((chapter) => (
          <div key={chapter.id} className="mb-4">
            <button
              onClick={() => setActiveChapterId(chapter.id)}
              className="text-sm font-medium text-slate-900 mb-1 text-left"
            >
              {chapter.title}
            </button>
            <div className="space-y-1 pl-2">
              {chapter.lessons.map((lesson) => (
                <button
                  key={lesson.id}
                  onClick={() => {
                    setActiveChapterId(chapter.id);
                    setActiveLessonId(lesson.id);
                    setTab("lesson");
                  }}
                  className={`w-full text-left text-xs rounded px-2 py-1.5 flex items-center gap-2 ${
                    lesson.id === activeLessonId ? "bg-slate-100 text-slate-900" : "text-slate-500"
                  }`}
                >
                  <span>{lesson.completed ? "✓" : "○"}</span>
                  {lesson.title}
                </button>
              ))}
            </div>
          </div>
        ))}
      </aside>

      {/* Main content */}
      <main className="flex-1 p-8 max-w-3xl">
        <div className="flex gap-4 border-b border-slate-200 mb-6">
          {(["lesson", "quiz", "flashcards", "chat"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`pb-2 text-sm font-medium capitalize ${
                tab === t ? "border-b-2 border-slate-900 text-slate-900" : "text-slate-400"
              }`}
            >
              {t === "chat" ? "AI Tutor" : t}
            </button>
          ))}
        </div>

        {tab === "lesson" && activeLesson && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h1 className="text-xl font-semibold text-slate-900">{activeLesson.title}</h1>
              <button
                onClick={() => toggleComplete(activeLesson.id, activeLesson.completed)}
                className={`text-xs font-medium rounded-lg px-3 py-1.5 ${
                  activeLesson.completed
                    ? "bg-green-100 text-green-700"
                    : "bg-slate-900 text-white"
                }`}
              >
                {activeLesson.completed ? "Completed ✓" : "Mark Complete"}
              </button>
            </div>

            <div className="prose prose-sm prose-slate max-w-none mb-6 prose-headings:font-semibold prose-table:text-sm prose-pre:bg-slate-900 prose-pre:text-slate-100">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {activeLesson.content}
              </ReactMarkdown>
            </div>

            {activeLesson.key_takeaways?.length > 0 && (
              <div className="bg-white border border-slate-200 rounded-xl p-4 mb-4">
                <p className="text-xs font-semibold text-slate-900 mb-2">Key Takeaways</p>
                <ul className="text-sm text-slate-600 list-disc pl-5 space-y-1">
                  {activeLesson.key_takeaways.map((k, i) => (
                    <li key={i}>{k}</li>
                  ))}
                </ul>
              </div>
            )}

            {activeLesson.examples?.length > 0 && (
              <div className="bg-white border border-slate-200 rounded-xl p-4 mb-4">
                <p className="text-xs font-semibold text-slate-900 mb-2">Examples</p>
                <ul className="text-sm text-slate-600 list-disc pl-5 space-y-1">
                  {activeLesson.examples.map((ex, i) => (
                    <li key={i}>{ex}</li>
                  ))}
                </ul>
              </div>
            )}

            {activeLesson.summary && (
              <p className="text-sm text-slate-500 italic mb-6">{activeLesson.summary}</p>
            )}

            {/* AI guidance nudge — suggests the next lesson or a quiz check */}
            {(() => {
              const chIdx = course.chapters.findIndex((c) => c.id === activeChapter?.id);
              const lIdx = activeChapter?.lessons.findIndex((l) => l.id === activeLesson.id) ?? -1;
              const nextInChapter = activeChapter?.lessons[lIdx + 1];
              const nextChapter = course.chapters[chIdx + 1];
              const nextTarget = nextInChapter
                ? { chapterId: activeChapter!.id, lessonId: nextInChapter.id, label: nextInChapter.title }
                : nextChapter?.lessons[0]
                ? { chapterId: nextChapter.id, lessonId: nextChapter.lessons[0].id, label: nextChapter.lessons[0].title }
                : null;

              return (
                <div className="bg-slate-100 rounded-xl p-4 flex items-center justify-between gap-4">
                  {nextTarget ? (
                    <>
                      <div>
                        <p className="text-xs text-slate-500">Suggested next lesson</p>
                        <p className="text-sm font-medium text-slate-900">{nextTarget.label}</p>
                      </div>
                      <button
                        onClick={() => {
                          setActiveChapterId(nextTarget.chapterId);
                          setActiveLessonId(nextTarget.lessonId);
                        }}
                        className="text-sm bg-slate-900 text-white rounded-lg px-4 py-2 whitespace-nowrap"
                      >
                        Continue →
                      </button>
                    </>
                  ) : (
                    <>
                      <div>
                        <p className="text-xs text-slate-500">You've reached the end</p>
                        <p className="text-sm font-medium text-slate-900">Test what you've learned</p>
                      </div>
                      <button
                        onClick={() => setTab("quiz")}
                        className="text-sm bg-slate-900 text-white rounded-lg px-4 py-2 whitespace-nowrap"
                      >
                        Take Quiz →
                      </button>
                    </>
                  )}
                </div>
              );
            })()}
          </div>
        )}

        {tab === "quiz" && activeChapter && (
          <div>
            <h1 className="text-lg font-semibold text-slate-900 mb-4">
              Quiz: {activeChapter.title}
            </h1>
            <QuizPanel chapterId={activeChapter.id} />
          </div>
        )}

        {tab === "flashcards" && activeChapter && (
          <div>
            <h1 className="text-lg font-semibold text-slate-900 mb-4">
              Flashcards: {activeChapter.title}
            </h1>
            <FlashcardsPanel chapterId={activeChapter.id} />
          </div>
        )}

        {tab === "chat" && course.document_id && (
          <div className="bg-white border border-slate-200 rounded-xl p-4 h-[32rem]">
            <ChatPanel courseId={course.id} documentId={course.document_id} />
          </div>
        )}
      </main>
    </div>
  );
}
