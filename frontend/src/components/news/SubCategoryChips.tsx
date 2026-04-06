'use client'

import { usePathname, useRouter, useSearchParams } from 'next/navigation'

import { cn } from '@/lib/utils'

interface SubCategoryChipsProps {
  category: string
  activeSubcategory: string | null
  onSelect: (subcategory: string | null) => void
}

const SUBCATEGORY_MAP: Record<string, string[]> = {
  sports: ['Football', 'Basketball', 'Tennis', 'Formula 1'],
  technology: ['AI', 'Semiconductors', 'Cybersecurity', 'Startups'],
}

export function SubCategoryChips({ category, activeSubcategory, onSelect }: SubCategoryChipsProps) {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  const chips = SUBCATEGORY_MAP[category] ?? []

  if (chips.length === 0) {
    return null
  }

  const handleSelect = (label: string) => {
    const value = label.toLowerCase()
    const params = new URLSearchParams(searchParams.toString())

    if (activeSubcategory === value) {
      params.delete('subcategory')
      params.delete('page')
      onSelect(null)
      router.push(params.toString() ? `${pathname}?${params.toString()}` : pathname)
      return
    }

    params.set('subcategory', value)
    params.delete('page')
    onSelect(value)
    router.push(`${pathname}?${params.toString()}`)
  }

  return (
    <div className="flex flex-wrap gap-2">
      {chips.map((chip) => {
        const normalized = chip.toLowerCase()
        const isActive = activeSubcategory === normalized

        return (
          <button
            key={chip}
            type="button"
            onClick={() => handleSelect(chip)}
            className={cn(
              'rounded-full border px-4 py-2 text-sm font-medium transition-colors',
              isActive
                ? 'border-accent-blue bg-accent-blue text-white'
                : 'border-navy-600 text-text-secondary hover:border-navy-500 hover:text-text-primary'
            )}
          >
            {chip}
          </button>
        )}
      )}
    </div>
  )
}