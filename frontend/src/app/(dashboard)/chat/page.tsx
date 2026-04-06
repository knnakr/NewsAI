'use client'

import { useState } from 'react'

import { MessageInput } from '@/components/chat/MessageInput'
import { WelcomeScreen } from '@/components/chat/WelcomeScreen'
import { useCreateConversation } from '@/hooks/useConversations'

export default function ChatPage() {
  const [draftMessage, setDraftMessage] = useState('')
  const createConversation = useCreateConversation()

  const handleSend = (content: string) => {
    createConversation.mutate({
      title: content.slice(0, 80),
      initialMessage: content,
    })
    setDraftMessage('')
  }

  return (
    <div className="flex min-h-[calc(100vh-4rem)] flex-col gap-6 px-4 py-6 sm:px-6 lg:px-8">
      <WelcomeScreen visible onSuggestClick={(question) => setDraftMessage(question)} />

      <div className="mt-auto">
        <MessageInput onSend={handleSend} disabled={createConversation.isPending} draftMessage={draftMessage} />
      </div>
    </div>
  )
}
