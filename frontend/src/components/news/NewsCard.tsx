'use client'

import { useEffect, useState } from 'react'
import { Bookmark, BookmarkCheck, Zap, ExternalLink } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import type { Article } from '@/types/news'

interface NewsCardProps {
  article: Article
  onSave?: (article: Article) => void
  onSummarize?: (article: Article) => void
  isSummarizing?: boolean
  summaryError?: string | null
}

const formatDate = (dateString: string | null): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

export function NewsCard({ article, onSave, onSummarize, isSummarizing = false, summaryError = null }: NewsCardProps) {
  const [isSaved, setIsSaved] = useState(false)
  const [isSummaryOpen, setIsSummaryOpen] = useState(Boolean(article.ai_summary))

  useEffect(() => {
    if (article.ai_summary) {
      setIsSummaryOpen(true)
    }
  }, [article.ai_summary])

  const handleSave = () => {
    onSave?.(article)
    setIsSaved(!isSaved)
  }

  const handleSummarize = () => {
    onSummarize?.(article)
  }

  return (
    <div className="flex flex-col rounded-lg border border-navy-700 bg-navy-800 p-4 transition-all hover:border-navy-600 hover:shadow-lg">
      {/* Header: Source and Bookmark */}
      <div className="mb-3 flex items-start justify-between">
        <span className="text-xs font-medium uppercase tracking-wider text-accent-blue">{article.source_name}</span>
        <button
          onClick={handleSave}
          className="text-text-muted transition-colors hover:text-accent-blue"
          aria-label={isSaved ? 'Remove bookmark' : 'Bookmark article'}
        >
          {isSaved ? <BookmarkCheck className="h-5 w-5" /> : <Bookmark className="h-5 w-5" />}
        </button>
      </div>

      {/* Title */}
      <h3 className="mb-2 line-clamp-2 text-lg font-bold text-text-primary hover:text-accent-blue">{article.title}</h3>

      {article.ai_summary && isSummaryOpen && (
        <div className="mb-3 rounded-md border border-navy-600 bg-navy-900/60 p-3">
          <p className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-accent-blue">AI Summary</p>
          <p className="text-sm text-text-secondary">{article.ai_summary}</p>
        </div>
      )}

      {!article.ai_summary && summaryError ? (
        <p className="mb-3 text-xs text-red-400">{summaryError}</p>
      ) : null}

      {/* Footer: Date and Buttons */}
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
              onClick={handleSummarize}
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
    </div>
  )
}
