import { useMutation, useQuery } from '@tanstack/react-query'
import { toast } from 'sonner'

import { api } from '@/lib/api'
import { queryClient } from '@/lib/queryClient'
import { useAuthStore } from '@/stores/authStore'
import type { FactCheck } from '@/types/factCheck'

function getApiErrorMessage(error: unknown, fallback: string) {
  const responseData = (error as { response?: { data?: unknown } })?.response?.data

  if (typeof responseData === 'string' && responseData.trim()) {
    return responseData
  }

  if (responseData && typeof responseData === 'object') {
    const detail = (responseData as { detail?: unknown }).detail
    const message = (responseData as { message?: unknown }).message

    if (typeof detail === 'string' && detail.trim()) {
      return detail
    }
    if (typeof message === 'string' && message.trim()) {
      return message
    }
  }

  return fallback
}

function isRateLimitError(error: unknown): boolean {
  const status = (error as { response?: { status?: number } })?.response?.status
  return status === 429
}

function getRetryDelayMs(error: unknown, defaultMs: number): number {
  const headers = (error as { response?: { headers?: Record<string, string | number | undefined> } })?.response?.headers
  const retryAfter = headers?.['retry-after']

  if (typeof retryAfter === 'string') {
    const asNumber = Number(retryAfter)
    if (!Number.isNaN(asNumber) && asNumber > 0) {
      return Math.min(asNumber * 1000, 10000)
    }
  }

  if (typeof retryAfter === 'number' && retryAfter > 0) {
    return Math.min(retryAfter * 1000, 10000)
  }

  return defaultMs
}

export function useRunFactCheck() {
  return useMutation({
    mutationFn: (claim: string) =>
      api.post<FactCheck>('/fact-check', { claim }).then((r) => r.data),
    retry: (failureCount, error) => isRateLimitError(error) && failureCount < 2,
    retryDelay: (attempt, error) => getRetryDelayMs(error, Math.min(1000 * 2 ** attempt, 8000)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fact-check-history'] })
    },
    onError: (error) => {
      toast.error(getApiErrorMessage(error, 'Dogrulama su anda tamamlanamadi. Lutfen tekrar deneyin.'))
    }
  })
}

export function useFactCheckHistory() {
  return useQuery({
    queryKey: ['fact-check-history'],
    queryFn: () => api.get<FactCheck[]>('/fact-check/history').then((r) => r.data),
    enabled: !!useAuthStore.getState().accessToken
  })
}
