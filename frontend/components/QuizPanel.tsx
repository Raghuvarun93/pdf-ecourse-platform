"use client";

import { useState } from "react";
import api from "@/lib/api";

type Quiz = { id: string; question: string; options: string[] };
type AttemptResult = { quiz_id: string; is_correct: boolean; correct_answer: string; explanation: string };

export default function QuizPanel({ chapterId }: { chapterId: string }) {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [results, setResults] = useState<Record<string, AttemptResult>>({});
  const [loading, setLoading] = useState(false);

  async function generate() {
    setLoading(true);
    setResults({});
    setAnswers({});
    try {
      const res = await api.post<Quiz[]>(`/quiz/chapters/${chapterId}/generate`, { count: 10 });
      setQuizzes(res.data);
    } finally {
      setLoading(false);
    }
  }

  async function submit(quizId: string) {
    const selected = answers[quizId];
    if (!selected) return;
    const res = await api.post<AttemptResult>("/quiz/attempt", {
      quiz_id: quizId,
      selected_answer: selected,
    });
    setResults((prev) => ({ ...prev, [quizId]: res.data }));
  }

  const allAnswered = quizzes.length > 0 && Object.keys(results).length === quizzes.length;
  const score = quizzes.length
    ? Math.round(
        (Object.values(results).filter((r) => r.is_correct).length / quizzes.length) * 100
      )
    : null;

  return (
    <div>
      {quizzes.length === 0 ? (
        <button
          onClick={generate}
          disabled={loading}
          className="text-sm bg-slate-900 text-white rounded-lg px-4 py-2 disabled:opacity-50"
        >
          {loading ? "Generating quiz..." : "Generate Quiz for this Chapter"}
        </button>
      ) : (
        <div className="space-y-6">
          {allAnswered && (
            <div className="bg-white border border-slate-200 rounded-xl p-5">
              <p className="text-lg font-semibold text-slate-900 mb-1">
                You scored {score}%
              </p>
              <p className="text-sm text-slate-500 mb-4">
                {Object.values(results).filter((r) => r.is_correct).length} of {quizzes.length} correct
              </p>
              <div className="space-y-2">
                {quizzes.map((q, i) => {
                  const r = results[q.id];
                  return (
                    <div key={q.id} className="flex items-start gap-2 text-sm">
                      <span>{r.is_correct ? "✅" : "❌"}</span>
                      <div>
                        <p className={r.is_correct ? "text-slate-700" : "text-slate-900 font-medium"}>
                          {i + 1}. {q.question}
                        </p>
                        {!r.is_correct && (
                          <p className="text-xs text-slate-500">
                            Correct answer: {r.correct_answer}
                          </p>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
          {quizzes.map((q, i) => {
            const result = results[q.id];
            return (
              <div key={q.id} className="border border-slate-200 rounded-lg p-4">
                <p className="text-sm font-medium text-slate-900 mb-3">
                  {i + 1}. {q.question}
                </p>
                <div className="space-y-2">
                  {q.options.map((opt) => (
                    <label
                      key={opt}
                      className={`flex items-center gap-2 text-sm rounded-lg border px-3 py-2 cursor-pointer ${
                        result
                          ? opt === result.correct_answer
                            ? "border-green-400 bg-green-50"
                            : opt === answers[q.id]
                            ? "border-red-400 bg-red-50"
                            : "border-slate-200"
                          : answers[q.id] === opt
                          ? "border-slate-900"
                          : "border-slate-200"
                      }`}
                    >
                      <input
                        type="radio"
                        name={q.id}
                        disabled={!!result}
                        checked={answers[q.id] === opt}
                        onChange={() => setAnswers((prev) => ({ ...prev, [q.id]: opt }))}
                      />
                      {opt}
                    </label>
                  ))}
                </div>
                {result && (
                  <p className="text-xs text-slate-500 mt-2">{result.explanation}</p>
                )}
                {!result && (
                  <button
                    onClick={() => submit(q.id)}
                    disabled={!answers[q.id]}
                    className="mt-3 text-xs font-medium text-slate-900 underline disabled:opacity-40"
                  >
                    Submit answer
                  </button>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
