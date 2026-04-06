'use client'

import { cn } from '@/lib/utils'

interface CategoryChipsProps {
  activeChip: string | null
  onSelect: (chip: string) => void
}

const CATEGORIES = ['World', 'Technology', 'Finance', 'Sports', 'Science', 'Health', 'Entertainment']

export function CategoryChips({ activeChip, onSelect }: CategoryChipsProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {CATEGORIES.map((chip) => {
        const isActive = activeChip === chip

        return (
          <button
            key={chip}
            type="button"
            onClick={() => onSelect(chip)}
            className={cn(
              'rounded-full border px-4 py-2 text-sm font-medium transition-colors',
              isActive
                ? 'border-accent-blue bg-accent-blue text-white'
                : 'border-navy-600 text-text-secondary hover:border-navy-500 hover:text-text-primary'
            )}
          >
            {chip}
          </button>
        )
      })}
    </div>
  )
}