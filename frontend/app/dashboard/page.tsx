"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { createClient } from "@/lib/supabaseClient";

type DashboardData = {
  total_courses: number;
  completed_lessons: number;
  total_lessons: number;
  completion_percentage: number;
  avg_quiz_score: number | null;
  recent_courses: { id: string; title: string; difficulty: string; status: string }[];
};

type SearchResult = {
  lesson_id: string;
  lesson_title: string;
  chapter_title: string;
  course_id: string;
  course_title: string;
};

const COVER_GRADIENTS = [
  "from-indigo-500 to-purple-500",
  "from-emerald-500 to-teal-500",
  "from-orange-500 to-rose-500",
  "from-sky-500 to-blue-500",
  "from-fuchsia-500 to-pink-500",
];

function coverGradient(title: string) {
  const idx = title.charCodeAt(0) % COVER_GRADIENTS.length;
  return COVER_GRADIENTS[idx];
}

function highlightMatch(text: string, query: string) {
  if (!query.trim()) return text;
  const idx = text.toLowerCase().indexOf(query.toLowerCase());
  if (idx === -1) return text;
  return (
    <>
      {text.slice(0, idx)}
      <mark className="bg-yellow-200 text-slate-900 rounded-sm px-0.5">
        {text.slice(idx, idx + query.length)}
      </mark>
      {text.slice(idx + query.length)}
    </>
  );
}

export default function DashboardPage() {
  const router = useRouter();
  const supabase = createClient();
  const [data, setData] = useState<DashboardData | null>(null);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searching, setSearching] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<DashboardData>("/dashboard")
      .then((res) => setData(res.data))
      .finally(() => setLoading(false));
  }, []);

  // Debounced instant search — fires 350ms after the user stops typing
  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }
    setSearching(true);
    const handle = setTimeout(() => {
      api
        .get<SearchResult[]>("/search", { params: { q: query } })
        .then((res) => setResults(res.data))
        .finally(() => setSearching(false));
    }, 350);
    return () => clearTimeout(handle);
  }, [query]);

  async function handleLogout() {
    await supabase.auth.signOut();
    router.push("/login");
  }

  if (loading) return <div className="p-8 text-sm text-slate-500">Loading...</div>;

  const completed = data?.completed_lessons ?? 0;

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-xl font-semibold text-slate-900">Your Dashboard</h1>
        <div className="flex gap-3">
          <Link
            href="/upload"
            className="bg-slate-900 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-slate-800"
          >
            Upload PDF
          </Link>
          <button onClick={handleLogout} className="text-sm text-slate-500 hover:underline">
            Log out
          </button>
        </div>
      </div>

      <div className="relative mb-6 max-w-md">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search your chapters and lessons..."
          className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm"
        />
        {searching && (
          <span className="absolute right-3 top-2.5 text-xs text-slate-400">searching...</span>
        )}

        {query.trim() && !searching && (
          <div className="absolute z-10 w-full bg-white border border-slate-200 rounded-xl p-2 mt-1 shadow-lg max-h-64 overflow-y-auto">
            {results.length === 0 ? (
              <p className="text-sm text-slate-400 px-2 py-2">
                No lessons matched "{query}".
              </p>
            ) : (
              results.map((r) => (
                <Link
                  key={r.lesson_id}
                  href={`/course/${r.course_id}`}
                  className="block text-sm px-2 py-1.5 rounded hover:bg-slate-50"
                >
                  <span className="font-medium text-slate-900">
                    {highlightMatch(r.lesson_title, query)}
                  </span>
                  <span className="text-slate-400"> — {r.course_title} / {r.chapter_title}</span>
                </Link>
              ))
            )}
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="grid grid-cols-2 gap-4 lg:col-span-2">
          <div className="bg-white border border-slate-200 rounded-xl p-4">
            <p className="text-xs text-slate-500">Total Courses</p>
            <p className="text-2xl font-semibold">{data?.total_courses ?? 0}</p>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl p-4">
            <p className="text-xs text-slate-500">Lessons Completed</p>
            <p className="text-2xl font-semibold">
              {completed}/{data?.total_lessons ?? 0}
            </p>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl p-4">
            <p className="text-xs text-slate-500">Overall Progress</p>
            <p className="text-2xl font-semibold">{data?.completion_percentage ?? 0}%</p>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl p-4">
            <p className="text-xs text-slate-500">Avg Quiz Score</p>
            <p className="text-2xl font-semibold">
              {data?.avg_quiz_score != null ? `${data.avg_quiz_score}%` : "—"}
            </p>
          </div>
        </div>

        {/* Progress chart - Temporarily disabled */}
        <div className="bg-white border border-slate-200 rounded-xl p-4 flex flex-col items-center justify-center">
          <p className="text-xs text-slate-500 mb-2 self-start">Learning Progress</p>
          <div className="w-full h-36 flex items-center justify-center">
            <div className="text-center">
              <p className="text-4xl font-bold text-slate-900">{data?.completion_percentage ?? 0}%</p>
              <p className="text-xs text-slate-500 mt-2">Complete</p>
            </div>
          </div>
          <p className="text-xs text-slate-500 -mt-2">
            {data?.total_lessons ? `${completed} of ${data.total_lessons} lessons` : "Upload a PDF to begin"}
          </p>
        </div>
      </div>

      <h2 className="text-sm font-semibold text-slate-900 mb-3">Recent Courses</h2>

      {data && data.recent_courses.length === 0 && (
        <div className="bg-white border border-dashed border-slate-300 rounded-xl p-8 text-center">
          <p className="text-sm text-slate-600 font-medium mb-1">No courses yet</p>
          <p className="text-sm text-slate-400 mb-4">
            Upload your first PDF to create an interactive AI-powered course.
          </p>
          <Link
            href="/upload"
            className="inline-block bg-slate-900 text-white rounded-lg px-4 py-2 text-sm font-medium"
          >
            Upload a PDF
          </Link>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {data?.recent_courses.map((c) => (
          <Link
            key={c.id}
            href={`/course/${c.id}`}
            className="bg-white border border-slate-200 rounded-xl overflow-hidden hover:border-slate-300 hover:shadow-sm transition-shadow"
          >
            <div
              className={`h-20 bg-gradient-to-br ${coverGradient(c.title)} flex items-center justify-center`}
            >
              <span className="text-white text-2xl font-semibold">{c.title.charAt(0).toUpperCase()}</span>
            </div>
            <div className="p-4">
              <p className="text-sm font-medium text-slate-900">{c.title}</p>
              <p className="text-xs text-slate-500 capitalize">
                {c.difficulty} · {c.status}
              </p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
