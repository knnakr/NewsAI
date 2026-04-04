export function TypingIndicator() {
  return (
    <div
      role="status"
      aria-label="Assistant is typing"
      className="inline-flex items-center gap-1 rounded-full border border-navy-600 bg-navy-800 px-3 py-2"
    >
      <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.2s]" />
      <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.1s]" />
      <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400" />
    </div>
  )
}