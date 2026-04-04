import { Skeleton } from '@/components/ui/Skeleton'

export function NewsCardSkeleton() {
  return (
    <div className="flex flex-col rounded-lg border border-navy-700 bg-navy-800 p-4">
      {/* Header */}
      <div className="mb-3 flex justify-between">
        <Skeleton className="h-4 w-20" />
        <Skeleton className="h-5 w-5" />
      </div>

      {/* Title */}
      <Skeleton className="mb-2 h-6 w-full" />
      <Skeleton className="mb-3 h-4 w-4/5" />

      {/* Summary */}
      <Skeleton className="mb-3 h-4 w-full" />
      <Skeleton className="mb-4 h-4 w-3/4" />

      {/* Footer */}
      <div className="mt-auto flex justify-between">
        <Skeleton className="h-4 w-16" />
        <div className="flex gap-2">
          <Skeleton className="h-8 w-24" />
          <Skeleton className="h-8 w-24" />
        </div>
      </div>
    </div>
  )
}
