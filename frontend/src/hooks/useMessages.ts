import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'

import { api } from '@/lib/api'
import type { ConversationDetail, Message } from '@/types/conversation'

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

export function useMessages(conversationId: string | null | undefined) {
  return useQuery({
    queryKey: ['conversation', conversationId],
    queryFn: () => api.get<ConversationDetail>(`/conversations/${conversationId}`).then((response) => response.data),
    enabled: !!conversationId,
  })
}

export function useSendMessage(conversationId: string | null | undefined) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (content: string) => {
      const response = await api.post<Message>(`/conversations/${conversationId}/messages`, {
        content,
      })
      return response.data
    },
    retry: (failureCount, error) => isRateLimitError(error) && failureCount < 2,
    retryDelay: (attempt, error) => getRetryDelayMs(error, Math.min(1000 * 2 ** attempt, 8000)),
    onMutate: async (content: string) => {
      if (!conversationId) {
        return { previousConversation: undefined as ConversationDetail | undefined }
      }

      await queryClient.cancelQueries({ queryKey: ['conversation', conversationId] })

      const previousConversation = queryClient.getQueryData<ConversationDetail>(['conversation', conversationId])

      const optimisticMessage: Message = {
        id: `optimistic-${Date.now()}`,
        role: 'user',
        content,
        sources: null,
        created_at: new Date().toISOString(),
      }

      queryClient.setQueryData<ConversationDetail>(['conversation', conversationId], (currentConversation) => {
        if (!currentConversation) {
          return currentConversation
        }

        return {
          ...currentConversation,
          messages: [...currentConversation.messages, optimisticMessage],
        }
      })

      return { previousConversation }
    },
    onError: (error, _content, context) => {
      if (!conversationId || !context?.previousConversation) {
        toast.error(getApiErrorMessage(error, 'Mesaj gonderilemedi. Lutfen tekrar deneyin.'))
        return
      }

      queryClient.setQueryData(['conversation', conversationId], context.previousConversation)
      toast.error(getApiErrorMessage(error, 'Mesaj gonderilemedi. Lutfen tekrar deneyin.'))
    },
    onSuccess: (assistantMessage) => {
      if (!conversationId) {
        return
      }

      queryClient.setQueryData<ConversationDetail>(['conversation', conversationId], (currentConversation) => {
        if (!currentConversation) {
          return currentConversation
        }

        return {
          ...currentConversation,
          messages: [...currentConversation.messages, assistantMessage],
        }
      })

      queryClient.invalidateQueries({ queryKey: ['conversations'] })
    },
  })
}
