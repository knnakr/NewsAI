'use client'

import { useMemo, useState } from 'react'

import { ErrorState } from '@/components/ErrorState'
import { CategoryChips } from '@/components/news/CategoryChips'
import { NewsCardSkeleton } from '@/components/news/NewsCardSkeleton'
import { TrendingCard } from '@/components/news/TrendingCard'
import { useSummarizeArticle } from '@/hooks/useNews'
import { useTrending } from '@/hooks/useTrending'
import type { Article } from '@/types/news'

const chipToTopicMap: Record<string, string> = {
  World: 'world',
  Technology: 'technology',
  Finance: 'economy',
  Sports: 'sports',
  Science: 'science',
  Health: 'health',
  Entertainment: 'entertainment',
}

export default function TrendingPage() {
  const [activeChip, setActiveChip] = useState<string | null>(null)
  const [summarizingUrl, setSummarizingUrl] = useState<string | null>(null)
  const [summaryErrors, setSummaryErrors] = useState<Record<string, string>>({})
  const summarizeArticle = useSummarizeArticle()

  const selectedTopic = useMemo(() => {
    if (!activeChip) return undefined
    return chipToTopicMap[activeChip]
  }, [activeChip])

  const { data: articles = [], isLoading, isError, refetch } = useTrending(selectedTopic)

  const handleSummarizeArticle = async (article: Article) => {
    setSummarizingUrl(article.url)
    setSummaryErrors((prev) => {
      const next = { ...prev }
      delete next[article.url]
      return next
    })

    try {
      await summarizeArticle.mutateAsync({
        title: article.title,
        url: article.url,
        source_name: article.source_name,
        published_at: article.published_at,
        category: article.category,
      })
    } catch {
      setSummaryErrors((prev) => ({
        ...prev,
        [article.url]: 'Summary olusturulamadi. Tekrar deneyin.',
      }))
    } finally {
      setSummarizingUrl(null)
    }
  }

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="mb-2 text-4xl font-bold text-text-primary">Global Pulse</h1>
        <p className="text-text-secondary">Top stories shaping the global conversation right now.</p>
      </div>

      <CategoryChips activeChip={activeChip} onSelect={setActiveChip} />

      {isError ? <ErrorState message="Yüklenemedi. Tekrar dene" onRetry={() => void refetch()} /> : null}

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
        {isLoading
          ? Array.from({ length: 6 }).map((_, index) => <NewsCardSkeleton key={index} />)
          : !isError &&
            articles.map((article) => (
              <TrendingCard
                key={`${article.url}-${article.published_at}`}
                article={article}
                onSummarize={handleSummarizeArticle}
                isSummarizing={summarizingUrl === article.url && summarizeArticle.isPending}
                summaryError={summaryErrors[article.url] ?? null}
              />
            ))}
      </div>

      {!isLoading && !isError && articles.length === 0 && (
        <div className="flex items-center justify-center rounded-lg border border-dashed border-navy-600 py-12">
          <p className="text-text-muted">No trending stories found for this category.</p>
        </div>
      )}
    </div>
  )
}
