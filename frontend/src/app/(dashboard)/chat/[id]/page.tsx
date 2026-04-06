'use client'

import { useEffect, useRef, useState } from 'react'
import { useParams, useRouter, useSearchParams } from 'next/navigation'

import { ErrorState } from '@/components/ErrorState'
import { MessageInput } from '@/components/chat/MessageInput'
import { MessageList } from '@/components/chat/MessageList'
import { WelcomeScreen } from '@/components/chat/WelcomeScreen'
import { useMessages, useSendMessage } from '@/hooks/useMessages'
import { useAuthStore } from '@/stores/authStore'

export default function ChatDetailPage() {
  const router = useRouter()
  const params = useParams()
  const searchParams = useSearchParams()
  const conversationId = typeof params.id === 'string' ? params.id : Array.isArray(params.id) ? params.id[0] : undefined
  const [draftMessage, setDraftMessage] = useState('')
  const hasSentInitialMessage = useRef(false)
  const initialMessage = searchParams.get('message')?.trim() ?? ''

  const { data: conversation, error, isLoading, isError, refetch } = useMessages(conversationId)
  const sendMessage = useSendMessage(conversationId)
  const displayName = useAuthStore((state) => state.user?.display_name ?? 'You')

  useEffect(() => {
    const status = (error as { response?: { status?: number } } | null)?.response?.status
    if (status === 404) {
      router.replace('/chat')
    }
  }, [error, router])

  useEffect(() => {
    if (!initialMessage || hasSentInitialMessage.current) {
      return
    }

    if (!conversation || conversation.messages.length > 0 || sendMessage.isPending) {
      return
    }

    hasSentInitialMessage.current = true
    sendMessage.mutate(initialMessage)
  }, [conversation, initialMessage, sendMessage])

  const status = (error as { response?: { status?: number } } | null)?.response?.status

  if (isError && status !== 404) {
    return <ErrorState message="Yüklenemedi. Tekrar dene" onRetry={() => void refetch()} />
  }

  if (isLoading || !conversation) {
    return (
      <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4 py-12 text-slate-300">
        Loading conversation...
      </div>
    )
  }

  return (
    <div className="flex min-h-[calc(100vh-4rem)] flex-col gap-6 px-4 py-6 sm:px-6 lg:px-8">
      <WelcomeScreen
        visible={conversation.messages.length === 0}
        onSuggestClick={(question) => setDraftMessage(question)}
      />
      <MessageList messages={conversation.messages} displayName={displayName} />

      <div className="mt-auto">
        <MessageInput
          onSend={(content) => {
            sendMessage.mutate(content)
            setDraftMessage('')
          }}
          disabled={sendMessage.isPending}
          draftMessage={draftMessage}
        />
      </div>
    </div>
  )
}
