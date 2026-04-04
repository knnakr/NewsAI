'use client'

import { cn } from '@/lib/utils'
import type { FeedPeriod } from '@/types/news'

interface PeriodFilterProps {
  activePeriod: FeedPeriod
  onPeriodChange: (period: FeedPeriod) => void
}

const periods: { value: FeedPeriod; label: string }[] = [
  { value: 'today', label: 'Today' },
  { value: 'week', label: 'This Week' },
  { value: 'month', label: 'This Month' },
]

export function PeriodFilter({ activePeriod, onPeriodChange }: PeriodFilterProps) {
  return (
    <div className="flex gap-6 border-b border-navy-700">
      {periods.map((period) => (
        <button
          key={period.value}
          onClick={() => onPeriodChange(period.value)}
          className={cn(
            'px-4 py-3 text-sm font-medium transition-colors',
            activePeriod === period.value
              ? 'border-b-2 border-accent-blue text-accent-blue'
              : 'border-b-2 border-transparent text-text-secondary hover:text-text-primary'
          )}
        >
          {period.label}
        </button>
      ))}
    </div>
  )
}
