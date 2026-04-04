import { useEffect, useRef } from 'react'

import { AssistantMessage } from '@/components/chat/AssistantMessage'
import { TypingIndicator } from '@/components/chat/TypingIndicator'
import { UserMessage } from '@/components/chat/UserMessage'
import type { Message } from '@/types/conversation'

type MessageListProps = {
  messages: Message[]
  displayName: string
  isTyping?: boolean
}

export function MessageList({ messages, displayName, isTyping = false }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView?.({ behavior: 'smooth', block: 'end' })
  }, [messages, isTyping])

  return (
    <div className="space-y-5">
      {messages.map((message) => {
        if (message.role === 'user') {
          return <UserMessage key={message.id} content={message.content} displayName={displayName} />
        }

        if (message.role === 'assistant') {
          return <AssistantMessage key={message.id} content={message.content} sources={message.sources} />
        }

        return (
          <div key={message.id} className="rounded-lg border border-navy-600 bg-navy-800 px-4 py-3 text-sm text-slate-300">
            {message.content}
          </div>
        )
      })}

      {isTyping ? <TypingIndicator /> : null}
      <div ref={bottomRef} />
    </div>
  )
}