import { ExternalLink } from 'lucide-react'
import { Skeleton } from '@/components/ui/Skeleton'
import type { Verdict } from '@/types/factCheck'
import type { Source } from '@/types/conversation'

interface VerdictCardProps {
  verdict?: Verdict
  explanation?: string
  confidence_score?: number
  sources?: Source[]
  loading?: boolean
}

const verdictColors = {
  TRUE: 'bg-verdict-true text-white',
  FALSE: 'bg-verdict-false text-white',
  UNVERIFIED: 'bg-verdict-unverified text-gray-900',
}

export function VerdictCard({
  verdict,
  explanation,
  confidence_score,
  sources = [],
  loading = false,
}: VerdictCardProps) {
  if (loading) {
    return (
      <div data-testid="verdict-skeleton" className="rounded-lg border border-navy-700 bg-navy-800 p-6">
        <Skeleton className="mb-4 h-10 w-32" />
        <Skeleton className="mb-6 h-20 w-full" />
        <Skeleton className="h-10 w-full" />
      </div>
    )
  }

  if (!verdict) return null

  const confidencePercent = Math.round((confidence_score || 0) * 100)

  return (
    <div data-testid="verdict-card" className="rounded-lg border border-navy-700 bg-navy-800 p-6">
      {/* Verdict Badge */}
      <div className="mb-4 flex items-center gap-3">
        <span
          data-testid="verdict-badge"
          className={`rounded-full px-4 py-2 text-sm font-bold ${verdictColors[verdict]} verdict-${verdict.toLowerCase()}`}
        >
          {verdict}
        </span>
        <span className="text-lg font-semibold text-text-primary">{confidencePercent}% Confidence</span>
      </div>

      {/* Confidence Bar */}
      <div className="mb-6">
        <div className="h-2 rounded-full bg-navy-700">
          <div
            className={`h-2 rounded-full transition-all ${
              verdict === 'TRUE'
                ? 'bg-verdict-true'
                : verdict === 'FALSE'
                  ? 'bg-verdict-false'
                  : 'bg-verdict-unverified'
            }`}
            style={{ width: `${confidencePercent}%` }}
          />
        </div>
      </div>

      {/* Explanation */}
      {explanation && <p className="mb-6 text-base text-text-secondary">{explanation}</p>}

      {/* Sources */}
      {sources && sources.length > 0 && (
        <div>
          <p className="mb-3 text-sm font-semibold text-text-secondary">Sources</p>
          <div className="flex flex-wrap gap-2">
            {sources.map((source, idx) => (
              <a
                key={idx}
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1 rounded-md bg-navy-700 px-3 py-2 text-sm text-accent-blue hover:bg-navy-600"
              >
                {source.title}
                <ExternalLink className="h-3 w-3" />
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
