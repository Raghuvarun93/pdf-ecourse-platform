"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";

type Document = { id: string; filename: string; status: string; page_count: number | null };

const UPLOAD_STEPS = ["📄 Uploading PDF...", "📖 Extracting text..."];
const GENERATE_STEPS = [
  "🤖 Designing course structure...",
  "📝 Writing lessons...",
  "🧠 Almost there...",
];

export default function UploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [stage, setStage] = useState<"idle" | "uploading" | "generating" | "error">("idle");
  const [stepIndex, setStepIndex] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const stepTimer = useRef<ReturnType<typeof setInterval> | null>(null);

  function startStepCycle(steps: string[]) {
    setStepIndex(0);
    stepTimer.current = setInterval(() => {
      setStepIndex((i) => Math.min(i + 1, steps.length - 1));
    }, 2500);
  }

  function stopStepCycle() {
    if (stepTimer.current) clearInterval(stepTimer.current);
  }

  useEffect(() => () => stopStepCycle(), []);

  function friendlyError(err: any): string {
    if (!err?.response) {
      return "Network error — check your connection and try again.";
    }
    const status = err.response.status;
    const detail = err.response.data?.detail;
    if (status === 400) return detail || "This file isn't a supported PDF.";
    if (status === 422)
      return (
        detail ||
        "Couldn't read this PDF — it may be scanned/image-only, empty, or corrupted."
      );
    if (status === 502) return "The AI is temporarily unavailable. Please try again in a moment.";
    if (status === 413) return "This PDF is too large. Try a smaller file.";
    if (status === 401) return "Your session expired — please log in again.";
    return detail || "Something went wrong. Please try again.";
  }

  async function handleUpload() {
    if (!file) return;
    setError(null);

    if (file.size > 30 * 1024 * 1024) {
      setError("This PDF is larger than 30MB — try a smaller file for faster processing.");
      setStage("error");
      return;
    }

    setStage("uploading");
    startStepCycle(UPLOAD_STEPS);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const uploadRes = await api.post<Document>("/documents", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      stopStepCycle();
      setStage("generating");
      startStepCycle(GENERATE_STEPS);

      const courseRes = await api.post("/courses/generate", {
        document_id: uploadRes.data.id,
      });

      stopStepCycle();
      router.push(`/course/${courseRes.data.id}`);
    } catch (err: any) {
      stopStepCycle();
      setStage("error");
      setError(friendlyError(err));
    }
  }

  const isBusy = stage === "uploading" || stage === "generating";
  const currentSteps = stage === "uploading" ? UPLOAD_STEPS : GENERATE_STEPS;

  return (
    <div className="min-h-screen bg-slate-50 p-8 flex items-center justify-center">
      <div className="w-full max-w-md bg-white border border-slate-200 rounded-xl p-8">
        <h1 className="text-xl font-semibold text-slate-900 mb-1">Upload a PDF</h1>
        <p className="text-sm text-slate-500 mb-6">
          We'll turn it into a structured course with chapters, lessons, quizzes, and an AI tutor.
        </p>

        <label className="block border-2 border-dashed border-slate-300 rounded-lg p-6 text-center cursor-pointer hover:border-slate-400 mb-4">
          <input
            type="file"
            accept="application/pdf"
            className="hidden"
            disabled={isBusy}
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
          <span className="text-sm text-slate-600">
            {file ? file.name : "Click to choose a PDF"}
          </span>
        </label>

        {isBusy && (
          <div className="mb-4 space-y-2">
            {currentSteps.map((label, i) => (
              <div
                key={label}
                className={`text-sm flex items-center gap-2 transition-opacity ${
                  i <= stepIndex ? "opacity-100 text-slate-700" : "opacity-30 text-slate-400"
                }`}
              >
                {i < stepIndex ? "✅" : i === stepIndex ? label.slice(0, 2) : "⏳"}
                <span>{i === stepIndex ? label.slice(2) : label.slice(2)}</span>
              </div>
            ))}
          </div>
        )}

        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || isBusy}
          className="w-full bg-slate-900 text-white rounded-lg py-2 text-sm font-medium hover:bg-slate-800 disabled:opacity-50"
        >
          {isBusy ? "Processing..." : "Generate Course"}
        </button>
      </div>
    </div>
  );
}
