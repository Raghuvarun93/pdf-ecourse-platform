"use client";

import { useState } from "react";
import api from "@/lib/api";

type Flashcard = { id: string; front: string; back: string };

export default function FlashcardsPanel({ chapterId }: { chapterId: string }) {
  const [cards, setCards] = useState<Flashcard[]>([]);
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function generate() {
    setLoading(true);
    setError(null);
    try {
      const res = await api.post<Flashcard[]>(`/flashcards/chapters/${chapterId}/generate`, {
        count: 10,
      });
      setCards(res.data);
      setIndex(0);
      setFlipped(false);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Couldn't generate flashcards. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  function next() {
    setFlipped(false);
    setIndex((i) => (i + 1) % cards.length);
  }

  function prev() {
    setFlipped(false);
    setIndex((i) => (i - 1 + cards.length) % cards.length);
  }

  if (cards.length === 0) {
    return (
      <div>
        <button
          onClick={generate}
          disabled={loading}
          className="text-sm bg-slate-900 text-white rounded-lg px-4 py-2 disabled:opacity-50"
        >
          {loading ? "Generating flashcards..." : "Generate Flashcards for this Chapter"}
        </button>
        {error && <p className="text-sm text-red-600 mt-2">{error}</p>}
      </div>
    );
  }

  const card = cards[index];

  return (
    <div className="max-w-md">
      <p className="text-xs text-slate-400 mb-2">
        Card {index + 1} of {cards.length}
      </p>

      <div
        onClick={() => setFlipped(!flipped)}
        className="cursor-pointer h-56 bg-white border border-slate-200 rounded-xl flex items-center justify-center p-6 text-center shadow-sm hover:shadow-md transition-shadow"
      >
        <p className="text-base text-slate-900">
          {flipped ? card.back : card.front}
        </p>
      </div>
      <p className="text-xs text-slate-400 text-center mt-2">
        {flipped ? "Answer — click to see question" : "Question — click to reveal answer"}
      </p>

      <div className="flex justify-between mt-4">
        <button onClick={prev} className="text-sm text-slate-500 hover:underline">
          ← Previous
        </button>
        <button onClick={next} className="text-sm text-slate-500 hover:underline">
          Next →
        </button>
      </div>
    </div>
  );
}
