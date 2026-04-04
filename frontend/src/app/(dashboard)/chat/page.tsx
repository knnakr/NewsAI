'use client'

import { useEffect, useRef } from 'react'

import { useCreateConversation } from '@/hooks/useConversations'

export default function ChatPage() {
  const { mutate, isPending } = useCreateConversation()
  const hasRequestedConversation = useRef(false)

  useEffect(() => {
    if (hasRequestedConversation.current) {
      return
    }

    hasRequestedConversation.current = true
    mutate({})
  }, [mutate])

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4 py-12">
      <div className="text-center">
        <p className="text-lg font-medium text-slate-100">
          {isPending ? 'Creating your conversation...' : 'Starting a new conversation...'}
        </p>
      </div>
    </div>
  )
}
