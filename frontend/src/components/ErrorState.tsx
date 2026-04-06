import { AlertTriangle } from 'lucide-react'

import { Button } from '@/components/ui/Button'

type ErrorStateProps = {
  message: string
  onRetry: () => void
}

export function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="flex items-center justify-center rounded-lg border border-red-500/30 bg-red-500/10 px-6 py-10">
      <div className="max-w-xl text-center">
        <div className="mb-4 inline-flex rounded-full border border-red-500/30 bg-red-500/10 p-3 text-red-300">
          <AlertTriangle className="h-5 w-5" aria-hidden="true" />
        </div>
        <p className="mb-4 text-sm text-red-100">{message}</p>
        <Button type="button" variant="secondary" onClick={onRetry}>
          Tekrar dene
        </Button>
      </div>
    </div>
  )
}
