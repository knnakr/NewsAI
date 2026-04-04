'use client'

import { useState } from 'react'
import { useRunFactCheck, useFactCheckHistory } from '@/hooks/useFactCheck'
import { ClaimInput } from '@/components/fact-check/ClaimInput'
import { VerdictCard } from '@/components/fact-check/VerdictCard'
import { RecentVerifications } from '@/components/fact-check/RecentVerifications'
import { useAuthStore } from '@/stores/authStore'
import type { FactCheck } from '@/types/factCheck'

export default function FactCheckPage() {
  const [lastVerdict, setLastVerdict] = useState<FactCheck | null>(null)
  const runFactCheck = useRunFactCheck()
  const history = useFactCheckHistory()
  const isAuthenticated = useAuthStore().isAuthenticated?.()

  const handleVerify = (claim: string) => {
    runFactCheck.mutate(claim, {
      onSuccess: (data) => {
        setLastVerdict(data)
      },
    })
  }

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="mb-2 text-4xl font-bold text-text-primary">Fact Check Engine</h1>
        <p className="text-text-secondary">Verify claims, headlines, and statements powered by AI research</p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Left: Input and Verdict */}
        <div className="space-y-6 lg:col-span-2">
          <ClaimInput onSubmit={handleVerify} isLoading={runFactCheck.isPending} />

          {/* Result or Last Verdict */}
          {lastVerdict && (
            <VerdictCard
              verdict={lastVerdict.verdict}
              explanation={lastVerdict.explanation}
              confidence_score={lastVerdict.confidence_score}
              sources={lastVerdict.sources}
            />
          )}
        </div>

        {/* Right: Recent Verifications (only if authenticated) */}
        {isAuthenticated && (
          <div className="lg:col-span-1">
            <RecentVerifications
              verifications={history.data || []}
              isLoading={history.isLoading}
            />
          </div>
        )}
      </div>
    </div>
  )
}
