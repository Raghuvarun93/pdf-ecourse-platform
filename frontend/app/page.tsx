import Link from "next/link";

const FEATURES = [
  {
    icon: "📄",
    title: "Upload Any PDF",
    desc: "Books, papers, docs, study material — drop in any PDF and get started in seconds.",
  },
  {
    icon: "🤖",
    title: "AI Tutor",
    desc: "Ask questions about the material and get answers grounded in the actual document.",
  },
  {
    icon: "🧠",
    title: "Quiz Generator",
    desc: "Auto-generated multiple-choice quizzes for every chapter, graded instantly.",
  },
  {
    icon: "📊",
    title: "Learning Progress",
    desc: "Track completion, revisit lessons, and pick up right where you left off.",
  },
];

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Nav */}
      <nav className="flex items-center justify-between px-6 sm:px-12 py-5 border-b border-slate-100">
        <span className="font-semibold text-slate-900">PDF to E-Course</span>
        <Link
          href="/login"
          className="text-sm font-medium bg-slate-900 text-white rounded-lg px-4 py-2 hover:bg-slate-800"
        >
          Log in
        </Link>
      </nav>

      {/* Hero */}
      <section className="px-6 sm:px-12 py-20 sm:py-28 text-center max-w-3xl mx-auto">
        <h1 className="text-3xl sm:text-5xl font-semibold text-slate-900 mb-5 leading-tight">
          Turn any PDF into an
          <br />
          interactive AI course
        </h1>
        <p className="text-slate-500 text-base sm:text-lg mb-8 max-w-xl mx-auto">
          Upload a document and get structured chapters, lessons, an AI tutor
          that answers from the source material, and quizzes — all generated
          automatically.
        </p>
        <Link
          href="/login"
          className="inline-block bg-slate-900 text-white rounded-lg px-6 py-3 text-sm font-medium hover:bg-slate-800"
        >
          Get started — it's free
        </Link>
      </section>

      {/* Features */}
      <section className="px-6 sm:px-12 pb-24 max-w-5xl mx-auto">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {FEATURES.map((f) => (
            <div
              key={f.title}
              className="border border-slate-200 rounded-xl p-6 text-left hover:border-slate-300 transition-colors"
            >
              <span className="text-2xl">{f.icon}</span>
              <h3 className="font-medium text-slate-900 mt-3 mb-1">{f.title}</h3>
              <p className="text-sm text-slate-500">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="border-t border-slate-100 px-6 sm:px-12 py-6 text-center">
        <p className="text-xs text-slate-400">PDF to E-Course Learning Platform</p>
      </footer>
    </div>
  );
}
