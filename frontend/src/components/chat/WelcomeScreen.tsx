import { Rocket } from 'lucide-react'

import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

type WelcomeScreenProps = {
  onSuggestClick: (question: string) => void
  visible?: boolean
}

const suggestedQuestions = [
  'What are the biggest headlines today?',
  'Summarize the latest technology news.',
  'What is trending in world politics right now?',
]

export function WelcomeScreen({ onSuggestClick, visible = true }: WelcomeScreenProps) {
  if (!visible) {
    return null
  }

  return (
    <div className="flex min-h-[60vh] items-center justify-center px-4 py-10">
      <Card className="w-full max-w-3xl border-navy-600 bg-navy-800/80 text-center shadow-xl shadow-navy-950/30">
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full border border-accent-blue/30 bg-accent-blue/10 text-accent-blue">
          <Rocket className="h-6 w-6" aria-hidden="true" />
        </div>

        <div className="mt-5 space-y-2">
          <h1 className="text-2xl font-semibold text-slate-100 sm:text-3xl">Welcome to News AI</h1>
          <p className="text-sm leading-6 text-slate-400 sm:text-base">
            Ask for summaries, breaking news, or a quick explanation of what is happening right now.
          </p>
        </div>

        <div className="mt-8 grid gap-3 sm:grid-cols-3">
          {suggestedQuestions.map((question) => (
            <Button
              key={question}
              type="button"
              variant="secondary"
              onClick={() => onSuggestClick(question)}
              className="h-auto min-h-24 flex-col items-start justify-start whitespace-normal rounded-xl border border-navy-600 bg-navy-700 p-4 text-left text-sm font-normal text-slate-100 hover:border-accent-blue hover:bg-navy-600"
            >
              <span>{question}</span>
            </Button>
          ))}
        </div>
      </Card>
    </div>
  )
}