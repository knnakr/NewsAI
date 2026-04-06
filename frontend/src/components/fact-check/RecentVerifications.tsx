import { Skeleton } from '@/components/ui/Skeleton'
import { Badge } from '@/components/ui/Badge'
import { ErrorState } from '@/components/ErrorState'
import type { FactCheck, Verdict } from '@/types/factCheck'

interface RecentVerificationsProps {
  verifications: FactCheck[]
  isLoading: boolean
  isError?: boolean
  onRetry?: () => void
}

const verdictVariants: Record<Verdict, 'success' | 'danger' | 'warning'> = {
  TRUE: 'success',
  FALSE: 'danger',
  UNVERIFIED: 'warning',
}

const truncateClaim = (claim: string, maxLength: number = 60): string => {
  if (claim.length <= maxLength) return claim
  return claim.substring(0, maxLength) + '...'
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = now.getTime() - date.getTime()
  const diffMinutes = Math.floor(diffTime / (1000 * 60))
  const diffHours = Math.floor(diffTime / (1000 * 60 * 60))
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

  if (diffMinutes < 60) return `${diffMinutes}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  return date.toLocaleDateString()
}

export function RecentVerifications({
  verifications,
  isLoading,
  isError = false,
  onRetry,
}: RecentVerificationsProps) {
  if (isLoading) {
    return (
      <div data-testid="verification-skeleton" className="rounded-lg border border-navy-700 bg-navy-800 p-4">
        <h3 className="mb-4 font-semibold text-text-primary">Recent Verifications</h3>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-16 w-full" />
          ))}
        </div>
      </div>
    )
  }

  if (isError) {
    return (
      <ErrorState
        message="Yüklenemedi. Tekrar dene"
        onRetry={onRetry ?? (() => undefined)}
      />
    )
  }

  return (
    <div className="rounded-lg border border-navy-700 bg-navy-800 p-4">
      <h3 className="mb-4 font-semibold text-text-primary">Recent Verifications</h3>

      {verifications.length === 0 ? (
        <div className="flex items-center justify-center rounded-lg border border-dashed border-navy-600 py-8">
          <p className="text-sm text-text-muted">Henüz doğrulama yapmadınız.</p>
        </div>
      ) : (
        <div className="max-h-96 space-y-2 overflow-y-auto">
          {verifications.map((verification) => (
            <div
              key={verification.id}
              className="rounded-md border border-navy-600 bg-navy-900 p-3 hover:bg-navy-800"
            >
              <div className="mb-2 flex items-start justify-between gap-2">
                <p className="line-clamp-2 flex-1 text-sm font-medium text-text-primary">
                  {truncateClaim(verification.claim)}
                </p>
                <Badge variant={verdictVariants[verification.verdict]}>{verification.verdict}</Badge>
              </div>
              <p className="text-xs text-text-muted">{formatDate(verification.created_at)}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
