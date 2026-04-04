'use client'

import { useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'

import { MessageInput } from '@/components/chat/MessageInput'
import { MessageList } from '@/components/chat/MessageList'
import { useMessages, useSendMessage } from '@/hooks/useMessages'
import { useAuthStore } from '@/stores/authStore'

export default function ChatDetailPage() {
  const router = useRouter()
  const params = useParams()
  const conversationId = typeof params.id === 'string' ? params.id : Array.isArray(params.id) ? params.id[0] : undefined

  const { data: conversation, error, isLoading } = useMessages(conversationId)
  const sendMessage = useSendMessage(conversationId)
  const displayName = useAuthStore((state) => state.user?.display_name ?? 'You')

  useEffect(() => {
    const status = (error as { response?: { status?: number } } | null)?.response?.status
    if (status === 404) {
      router.replace('/chat')
    }
  }, [error, router])

  if (isLoading || !conversation) {
    return (
      <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4 py-12 text-slate-300">
        Loading conversation...
      </div>
    )
  }

  return (
    <div className="flex min-h-[calc(100vh-4rem)] flex-col gap-6 px-4 py-6 sm:px-6 lg:px-8">
      <MessageList messages={conversation.messages} displayName={displayName} />

      <div className="mt-auto">
        <MessageInput onSend={(content) => sendMessage.mutate(content)} disabled={sendMessage.isPending} />
      </div>
    </div>
  )
}
