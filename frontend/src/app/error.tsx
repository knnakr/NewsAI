'use client'

import { useEffect } from 'react'

import { ErrorState } from '@/components/ErrorState'

type GlobalErrorProps = {
  error: Error & { digest?: string }
  reset: () => void
}

export default function GlobalError({ error, reset }: GlobalErrorProps) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div className="min-h-screen bg-navy-900 p-6 text-text-primary">
      <div className="mx-auto max-w-3xl pt-16">
        <ErrorState message="Yüklenemedi. Tekrar dene" onRetry={reset} />
      </div>
    </div>
  )
}
