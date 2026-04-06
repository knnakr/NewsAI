import ReactMarkdown from 'react-markdown'
import { Bot } from 'lucide-react'

import { Card } from '@/components/ui/Card'
import type { Source } from '@/types/conversation'

type AssistantMessageProps = {
  content: string
  sources: Source[] | null
  isStreaming?: boolean
}

export function AssistantMessage({ content, sources, isStreaming = false }: AssistantMessageProps) {
  return (
    <div className="flex items-start gap-3" data-testid="assistant-message">
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-accent-blue/30 bg-navy-800 text-accent-blue">
        <Bot className="h-4 w-4" aria-hidden="true" />
      </div>

      <Card className="max-w-3xl flex-1 space-y-4 bg-navy-800/80">
        <div className="text-sm leading-7 text-slate-100">
          <ReactMarkdown>{content}</ReactMarkdown>
          {isStreaming && (
            <span
              data-testid="streaming-cursor"
              className="animate-pulse inline-block ml-1 w-1 h-5 bg-accent-blue"
              aria-hidden="true"
            />
          )}
        </div>

        {sources && sources.length > 0 ? (
          <div className="space-y-2 border-t border-navy-600 pt-3">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">Sources</p>
            <div className="flex flex-wrap gap-2">
              {sources.map((source) => (
                <a
                  key={`${source.title}-${source.url}`}
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="rounded-full border border-navy-600 bg-navy-700 px-3 py-1 text-xs text-slate-200 transition-colors hover:border-accent-blue hover:text-white"
                >
                  {source.title}
                </a>
              ))}
            </div>
          </div>
        ) : null}
      </Card>
    </div>
  )
}