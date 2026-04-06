import { ExternalLink, Flame } from 'lucide-react'

import type { Article } from '@/types/news'

interface TrendingCardProps {
  article: Article
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

export function TrendingCard({ article }: TrendingCardProps) {
  return (
    <article className="group relative overflow-hidden rounded-xl border border-navy-700 bg-gradient-to-b from-navy-800 to-navy-900 p-5 transition-all hover:border-accent-blue/60 hover:shadow-lg hover:shadow-accent-blue/10">
      <div className="mb-3 flex items-center justify-between">
        <span className="inline-flex items-center gap-1 rounded-full border border-accent-blue/30 bg-accent-blue/10 px-2 py-1 text-xs font-semibold uppercase tracking-wide text-accent-blue">
          <Flame className="h-3 w-3" />
          Trending
        </span>
        <span className="text-xs text-text-muted">{formatDate(article.published_at)}</span>
      </div>

      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-text-secondary">{article.source_name}</p>
      <h3 className="mb-3 line-clamp-3 text-xl font-bold text-text-primary">{article.title}</h3>

      {article.ai_summary && <p className="mb-4 line-clamp-3 text-sm text-text-secondary">{article.ai_summary}</p>}

      <a
        href={article.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-1 text-sm font-medium text-accent-blue transition-colors group-hover:text-cyan-300"
      >
        Read Full
        <ExternalLink className="h-4 w-4" />
      </a>
    </article>
  )
}