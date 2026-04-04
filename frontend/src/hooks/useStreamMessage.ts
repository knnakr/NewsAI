'use client'

import { useState } from 'react'
import { useAuthStore } from '@/stores/authStore'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8001'

export function useStreamMessage(conversationId: string) {
  const [streamContent, setStreamContent] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const accessToken = useAuthStore((state) => state.accessToken)

  const sendStreaming = async (content: string) => {
    setIsStreaming(true)
    setStreamContent('')

    try {
      const response = await fetch(
        `${API_BASE_URL}/conversations/${conversationId}/messages/stream`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify({ content }),
        }
      )

      const reader = response.body?.getReader()
      if (!reader) {
        setIsStreaming(false)
        return
      }

      const decoder = new TextDecoder()
      let accumulator = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        accumulator += chunk
        setStreamContent(accumulator)
      }

      // Final flush
      const finalChunk = decoder.decode()
      if (finalChunk) {
        accumulator += finalChunk
        setStreamContent(accumulator)
      }
    } catch (error) {
      console.error('Streaming error:', error)
    } finally {
      setIsStreaming(false)
    }
  }

  return { sendStreaming, streamContent, isStreaming }
}
