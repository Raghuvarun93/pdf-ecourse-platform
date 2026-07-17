"use client";

import { useEffect, useState, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import api from "@/lib/api";

type Message = { question: string; answer: string; created_at?: string };

const SUGGESTED_QUESTIONS = [
  "Summarize this chapter.",
  "Explain this simply.",
  "Give me an example.",
  "Quiz me on this chapter.",
];

function formatTime(iso?: string) {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  } catch {
    return "";
  }
}

export default function ChatPanel({
  courseId,
  documentId,
}: {
  courseId: string;
  documentId: string;
}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api
      .get<Message[]>(`/chat/${courseId}/history`)
      .then((res) => setMessages(res.data))
      .catch(() => setError("Couldn't load chat history."));
  }, [courseId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function send(override?: string) {
    const question = (override ?? input).trim();
    if (!question || loading) return;
    setInput("");
    setError(null);
    setLoading(true);

    try {
      const res = await api.post<Message>("/chat", {
        course_id: courseId,
        document_id: documentId,
        question,
      });
      setMessages((prev) => [...prev, { ...res.data, created_at: new Date().toISOString() }]);
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      setError(detail || "The AI tutor couldn't respond. Please try again in a moment.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 max-h-96 pr-1">
        {messages.length === 0 && (
          <div>
            <p className="text-sm text-slate-400 mb-3">
              Ask me anything about this document — I can explain concepts, summarize
              chapters, or quiz you.
            </p>
            <div className="flex flex-wrap gap-2">
              {SUGGESTED_QUESTIONS.map((q) => (
                <button
                  key={q}
                  onClick={() => send(q)}
                  disabled={loading}
                  className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-full px-3 py-1.5 disabled:opacity-50"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className="space-y-2">
            {/* User message — right aligned */}
            <div className="flex justify-end">
              <div className="max-w-[80%] bg-slate-900 text-white rounded-2xl rounded-br-sm px-4 py-2">
                <p className="text-sm">{m.question}</p>
                {m.created_at && (
                  <p className="text-[10px] text-slate-300 mt-1 text-right">
                    {formatTime(m.created_at)}
                  </p>
                )}
              </div>
            </div>
            {/* AI message — left aligned */}
            <div className="flex justify-start">
              <div className="max-w-[80%] bg-slate-100 text-slate-800 rounded-2xl rounded-bl-sm px-4 py-2">
                <div className="text-sm prose prose-sm prose-slate max-w-none prose-p:my-1">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.answer}</ReactMarkdown>
                </div>
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-100 rounded-2xl rounded-bl-sm px-4 py-3 flex gap-1">
              <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
              <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
              <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" />
            </div>
          </div>
        )}

        {error && <p className="text-xs text-red-600">{error}</p>}
        <div ref={bottomRef} />
      </div>

      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Ask the AI tutor..."
          className="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm"
        />
        <button
          onClick={() => send()}
          disabled={loading}
          className="bg-slate-900 text-white rounded-lg px-4 py-2 text-sm font-medium disabled:opacity-50"
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}
