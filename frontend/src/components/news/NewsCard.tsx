'use client'

import { useState } from 'react'
import { Bookmark, BookmarkCheck, Zap, ExternalLink } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import type { Article } from '@/types/news'

interface NewsCardProps {
  article: Article
  onSave?: (article: Article) => void
}

const formatDate = (dateString: string | null): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

export function NewsCard({ article, onSave }: NewsCardProps) {
  const [isSaved, setIsSaved] = useState(false)

  const handleSave = () => {
    onSave?.(article)
    setIsSaved(!isSaved)
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

      {/* AI Summary */}
      {article.ai_summary && <p className="mb-3 line-clamp-2 text-sm text-text-secondary">{article.ai_summary}</p>}

      {/* Footer: Date and Buttons */}
      <div className="mt-auto flex items-end justify-between gap-2">
        <span className="text-xs text-text-muted">{formatDate(article.published_at)}</span>

        <div className="flex gap-2">
          {!article.ai_summary && (
            <Button size="sm" variant="secondary" className="flex items-center gap-1">
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
