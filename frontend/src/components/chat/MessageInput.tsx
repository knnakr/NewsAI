import { useEffect, useRef, useState } from 'react'
import { Send } from 'lucide-react'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

type MessageInputProps = {
  onSend: (content: string) => void
  disabled: boolean
}

const MAX_LENGTH = 4000
const MAX_HEIGHT = 144

export function MessageInput({ onSend, disabled }: MessageInputProps) {
  const [content, setContent] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement | null>(null)

  useEffect(() => {
    const textarea = textareaRef.current
    if (!textarea) {
      return
    }

    textarea.style.height = 'auto'
    textarea.style.height = `${Math.min(textarea.scrollHeight, MAX_HEIGHT)}px`
  }, [content])

  const submitMessage = () => {
    const trimmedContent = content.trim()

    if (!trimmedContent || disabled) {
      return
    }

    onSend(trimmedContent)
    setContent('')
  }

  return (
    <Card className="border-navy-600 bg-navy-800/95 p-3">
      <div className="space-y-3">
        <textarea
          ref={textareaRef}
          role="textbox"
          value={content}
          disabled={disabled}
          placeholder="Write a message..."
          maxLength={MAX_LENGTH}
          rows={1}
          onChange={(event) => setContent(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              event.preventDefault()
              submitMessage()
            }
          }}
          className="min-h-12 w-full resize-none rounded-lg border border-navy-600 bg-navy-900 px-4 py-3 text-sm text-slate-100 outline-none placeholder:text-slate-400 focus:border-accent-blue focus:ring-2 focus:ring-accent-blue/40 disabled:cursor-not-allowed disabled:opacity-60"
        />

        <div className="flex items-center justify-between gap-3">
          <p className="text-xs text-slate-400">
            {content.length} / {MAX_LENGTH}
          </p>

          <Button
            type="button"
            onClick={submitMessage}
            disabled={disabled || !content.trim()}
            className="min-w-24"
          >
            <Send className="h-4 w-4" aria-hidden="true" />
            <span>Send</span>
          </Button>
        </div>
      </div>
    </Card>
  )
}