'use client'

import { useState } from 'react'
import { useNewsFeed, useSaveArticle, useSummarizeArticle } from '@/hooks/useNews'
import { ErrorState } from '@/components/ErrorState'
import { NewsCard } from '@/components/news/NewsCard'
import { NewsCardSkeleton } from '@/components/news/NewsCardSkeleton'
import { PeriodFilter } from '@/components/news/PeriodFilter'
import type { FeedPeriod, Article } from '@/types/news'

const categories = ['world', 'technology', 'sports', 'entertainment']

export default function FeedPage() {
  const [activePeriod, setActivePeriod] = useState<FeedPeriod>('today')
  const [activeCategory, setActiveCategory] = useState('world')
  const [summarizingUrl, setSummarizingUrl] = useState<string | null>(null)
  const [summaryErrors, setSummaryErrors] = useState<Record<string, string>>({})

  const { data: articles = [], isLoading, isError, refetch } = useNewsFeed(activeCategory, activePeriod)
  const saveArticle = useSaveArticle()
  const summarizeArticle = useSummarizeArticle()

  const handleSaveArticle = (article: Article) => {
    saveArticle.mutate(article)
  }

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
      {/* Header */}
      <div>
        <h1 className="mb-2 text-4xl font-bold text-text-primary">News Feed</h1>
        <p className="text-text-secondary">Stay updated with the latest news from around the world</p>
      </div>

      {/* Period Filter */}
      <PeriodFilter activePeriod={activePeriod} onPeriodChange={setActivePeriod} />

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => setActiveCategory(category)}
            className={`rounded-full px-4 py-2 text-sm font-medium transition-colors ${
              activeCategory === category
                ? 'bg-accent-blue text-white'
                : 'border border-navy-600 text-text-secondary hover:border-navy-500'
            }`}
          >
            {category.charAt(0).toUpperCase() + category.slice(1)}
          </button>
        ))}
      </div>

      {/* Articles Grid */}
      {isError && <ErrorState message="Yüklenemedi. Tekrar dene" onRetry={() => void refetch()} />}

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {isLoading
          ? Array.from({ length: 6 }).map((_, i) => <NewsCardSkeleton key={i} />)
          : !isError && articles.map((article) => (
              <NewsCard
                key={`${article.url}-${article.published_at}`}
                article={article}
                onSave={handleSaveArticle}
                onSummarize={handleSummarizeArticle}
                isSummarizing={summarizingUrl === article.url && summarizeArticle.isPending}
                summaryError={summaryErrors[article.url] ?? null}
              />
            ))}
      </div>

      {/* Empty State */}
      {!isLoading && !isError && articles.length === 0 && (
        <div className="flex items-center justify-center rounded-lg border border-dashed border-navy-600 py-12">
          <p className="text-text-muted">No articles found for this period and category.</p>
        </div>
      )}
    </div>
  )
}
