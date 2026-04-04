'use client'

import { useState } from 'react'
import { Search } from 'lucide-react'
import { Button } from '@/components/ui/Button'

interface ClaimInputProps {
  onSubmit: (claim: string) => void
  isLoading: boolean
}

export function ClaimInput({ onSubmit, isLoading }: ClaimInputProps) {
  const [claim, setClaim] = useState('')

  const handleSubmit = () => {
    const trimmedClaim = claim.trim()
    if (!trimmedClaim) return

    onSubmit(trimmedClaim)
    setClaim('')
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleSubmit()
    }
  }

  return (
    <div className="rounded-lg border border-navy-700 bg-navy-800 p-6">
      <h2 className="mb-4 text-2xl font-bold text-text-primary">Verify a Claim</h2>

      <div className="mb-4 flex flex-col gap-3">
        <textarea
          value={claim}
          onChange={(e) => setClaim(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Paste a claim, headline, or URL to verify..."
          className="min-h-32 rounded-lg border border-navy-600 bg-navy-900 px-4 py-3 text-text-primary placeholder-text-muted focus:border-accent-blue focus:outline-none focus:ring-1 focus:ring-accent-blue"
          disabled={isLoading}
        />
      </div>

      <Button
        onClick={handleSubmit}
        disabled={isLoading || !claim.trim()}
        loading={isLoading}
        className="w-full"
      >
        {isLoading ? 'Verifying...' : 'Verify Claim'}
      </Button>

      <p className="mt-3 text-sm text-text-muted">
        Tip: Press Ctrl+Enter to quickly verify
      </p>
    </div>
  )
}
