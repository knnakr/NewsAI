import { User } from 'lucide-react'

import { Card } from '@/components/ui/Card'

type UserMessageProps = {
  content: string
  displayName: string
}

export function UserMessage({ content, displayName }: UserMessageProps) {
  const avatarInitial = displayName.trim().charAt(0).toUpperCase() || '?'

  return (
    <div className="flex justify-end gap-3">
      <Card className="max-w-3xl space-y-3 bg-navy-700 text-right">
        <p className="whitespace-pre-wrap text-sm leading-7 text-slate-100">{content}</p>
      </Card>

      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-navy-600 bg-navy-800 text-slate-100">
        <span className="sr-only">{displayName}</span>
        <span aria-hidden="true" className="text-sm font-semibold">
          {avatarInitial}
        </span>
      </div>
    </div>
  )
}