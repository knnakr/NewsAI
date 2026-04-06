'use client'

import { useState } from 'react'
import { useNewsFeed, useSaveArticle } from '@/hooks/useNews'
import { ErrorState } from '@/components/ErrorState'
import { NewsCard } from '@/components/news/NewsCard'
import { NewsCardSkeleton } from '@/components/news/NewsCardSkeleton'
import { PeriodFilter } from '@/components/news/PeriodFilter'
import type { FeedPeriod, Article } from '@/types/news'

const categories = ['world', 'technology', 'business', 'sports', 'entertainment']

export default function FeedPage() {
  const [activePeriod, setActivePeriod] = useState<FeedPeriod>('today')
  const [activeCategory, setActiveCategory] = useState('world')

  const { data: articles = [], isLoading, isError, refetch } = useNewsFeed(activeCategory, activePeriod)
  const saveArticle = useSaveArticle()

  const handleSaveArticle = (article: Article) => {
    saveArticle.mutate(article)
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
