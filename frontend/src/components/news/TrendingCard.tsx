import { useEffect, useState } from 'react'
import { ExternalLink, Flame, Zap } from 'lucide-react'

import { Button } from '@/components/ui/Button'
import type { Article } from '@/types/news'

interface TrendingCardProps {
  article: Article
  onSummarize?: (article: Article) => void
  isSummarizing?: boolean
  summaryError?: string | null
}

const formatDate = (dateString: string | null): string => {
  if (!dateString) return 'Unknown date'

  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function TrendingCard({ article, onSummarize, isSummarizing = false, summaryError = null }: TrendingCardProps) {
  const [isSummaryOpen, setIsSummaryOpen] = useState(Boolean(article.ai_summary))

  useEffect(() => {
    if (article.ai_summary) {
      setIsSummaryOpen(true)
    }
  }, [article.ai_summary])

  return (
    <article className="group relative flex h-full flex-col overflow-hidden rounded-xl border border-navy-700 bg-gradient-to-b from-navy-800 to-navy-900 p-5 transition-all hover:border-accent-blue/60 hover:shadow-lg hover:shadow-accent-blue/10">
      <div className="mb-3 flex items-center justify-between">
        <span className="inline-flex items-center gap-1 rounded-full border border-accent-blue/30 bg-accent-blue/10 px-2 py-1 text-xs font-semibold uppercase tracking-wide text-accent-blue">
          <Flame className="h-3 w-3" />
          Trending
        </span>
      </div>

      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-text-secondary">{article.source_name}</p>
      <h3 className="mb-3 line-clamp-3 text-xl font-bold text-text-primary">{article.title}</h3>

      {article.ai_summary && isSummaryOpen && (
        <div className="mb-4 rounded-md border border-navy-600 bg-navy-900/60 p-3">
          <p className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-accent-blue">AI Summary</p>
          <p className="text-sm text-text-secondary">{article.ai_summary}</p>
        </div>
      )}

      {!article.ai_summary && summaryError ? <p className="mb-4 text-xs text-red-400">{summaryError}</p> : null}

      <div className="mt-auto flex items-end justify-between gap-2">
        <span className="text-xs text-text-muted">{formatDate(article.published_at)}</span>

        <div className="flex gap-2">
          {article.ai_summary ? (
            <Button
              size="sm"
              variant="secondary"
              className="flex items-center gap-1"
              onClick={() => setIsSummaryOpen((prev) => !prev)}
            >
              <Zap className="h-3 w-3" />
              {isSummaryOpen ? 'Hide Summary' : 'Show Summary'}
            </Button>
          ) : (
            <Button
              size="sm"
              variant="secondary"
              className="flex items-center gap-1"
              onClick={() => onSummarize?.(article)}
              loading={isSummarizing}
              disabled={!onSummarize && !isSummarizing}
            >
              <Zap className="h-3 w-3" />
              Summarize
            </Button>
          )}

          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 rounded-md bg-navy-700 px-3 py-2 text-xs font-medium text-accent-blue transition-colors hover:bg-navy-600"
          >
            Read Full
            <ExternalLink className="h-3 w-3" />
          </a>
        </div>
      </div>
    </article>
  )
}