'use client'

import { use, useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'next/navigation'

import { ErrorState } from '@/components/ErrorState'
import { CategoryHeader } from '@/components/news/CategoryHeader'
import { NewsCard } from '@/components/news/NewsCard'
import { NewsCardSkeleton } from '@/components/news/NewsCardSkeleton'
import { SubCategoryChips } from '@/components/news/SubCategoryChips'
import { Button } from '@/components/ui/Button'
import { useCategoryNews, useSummarizeArticle } from '@/hooks/useNews'
import type { Article } from '@/types/news'

const VALID_CATEGORIES = new Set([
  'world',
  'technology',
  'sports',
  'economy',
  'health',
  'science',
  'entertainment',
])

type CategoryPageProps = {
  params: Promise<{
    slug: string
  }>
}

export default function CategoryPage({ params }: CategoryPageProps) {
  const { slug: rawSlug } = use(params)
  const slug = rawSlug.toLowerCase()
  const searchParams = useSearchParams()
  const subcategoryFromUrl = searchParams.get('subcategory')

  const [activeSubcategory, setActiveSubcategory] = useState<string | null>(subcategoryFromUrl)
  const [page, setPage] = useState(() => Number(searchParams.get('page') ?? '1'))
  const [articles, setArticles] = useState<Article[]>([])
  const [summarizingUrl, setSummarizingUrl] = useState<string | null>(null)
  const [summaryErrors, setSummaryErrors] = useState<Record<string, string>>({})
  const summarizeArticle = useSummarizeArticle()

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- this state mirrors URL query selection.
    setActiveSubcategory(subcategoryFromUrl)
    setPage(Number(searchParams.get('page') ?? '1'))
    setArticles([])
  }, [subcategoryFromUrl, slug, searchParams])

  const { data: pageArticles = [], isLoading, isFetching, isError, refetch } = useCategoryNews(
    slug,
    activeSubcategory ?? undefined,
    page
  )

  useEffect(() => {
    if (!pageArticles.length) return

    // eslint-disable-next-line react-hooks/set-state-in-effect -- append/replace flow depends on fetched page payload.
    setArticles((prev) => {
      if (page === 1) {
        return pageArticles
      }
      return [...prev, ...pageArticles]
    })
  }, [pageArticles, page])

  const hasMore = pageArticles.length === 12

  const featuredArticle = useMemo(() => {
    if (slug !== 'sports') return null
    return articles[0] ?? null
  }, [articles, slug])

  const sportsGridArticles = useMemo(() => {
    if (slug !== 'sports') return []
    return articles.slice(1)
  }, [articles, slug])

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

  if (!VALID_CATEGORIES.has(slug)) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center p-6">
        <div className="rounded-lg border border-navy-700 bg-navy-800 p-8 text-center">
          <h1 className="mb-2 text-3xl font-bold text-text-primary">404</h1>
          <p className="text-text-secondary">Category not found.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      <CategoryHeader category={slug} />

      <SubCategoryChips
        category={slug}
        activeSubcategory={activeSubcategory}
        onSelect={(value) => {
          setActiveSubcategory(value)
          setPage(1)
          setArticles([])
        }}
      />

      {isError ? <ErrorState message="Yüklenemedi. Tekrar dene" onRetry={() => void refetch()} /> : null}

      {isLoading && !isError && page === 1 ? (
        <div
          className={
            slug === 'technology'
              ? 'grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3'
              : 'grid grid-cols-1 gap-6 md:grid-cols-2'
          }
        >
          {Array.from({ length: 6 }).map((_, index) => (
            <NewsCardSkeleton key={index} />
          ))}
        </div>
      ) : null}

      {!isLoading && !isError && slug === 'sports' && featuredArticle ? (
        <div className="rounded-xl border border-navy-700 bg-navy-800 p-6">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-accent-blue">Featured</p>
          <NewsCard
            article={featuredArticle}
            onSummarize={handleSummarizeArticle}
            isSummarizing={summarizingUrl === featuredArticle.url && summarizeArticle.isPending}
            summaryError={summaryErrors[featuredArticle.url] ?? null}
          />
        </div>
      ) : null}

      {!isLoading && !isError && slug === 'sports' ? (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          {sportsGridArticles.map((article) => (
            <NewsCard
              key={`${article.url}-${article.published_at}`}
              article={article}
              onSummarize={handleSummarizeArticle}
              isSummarizing={summarizingUrl === article.url && summarizeArticle.isPending}
              summaryError={summaryErrors[article.url] ?? null}
            />
          ))}
        </div>
      ) : null}

      {!isLoading && !isError && slug === 'technology' ? (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {articles.map((article) => (
            <NewsCard
              key={`${article.url}-${article.published_at}`}
              article={article}
              onSummarize={handleSummarizeArticle}
              isSummarizing={summarizingUrl === article.url && summarizeArticle.isPending}
              summaryError={summaryErrors[article.url] ?? null}
            />
          ))}
        </div>
      ) : null}

      {!isLoading && !isError && slug !== 'sports' && slug !== 'technology' ? (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {articles.map((article) => (
            <NewsCard
              key={`${article.url}-${article.published_at}`}
              article={article}
              onSummarize={handleSummarizeArticle}
              isSummarizing={summarizingUrl === article.url && summarizeArticle.isPending}
              summaryError={summaryErrors[article.url] ?? null}
            />
          ))}
        </div>
      ) : null}

      {!isLoading && !isError && articles.length === 0 ? (
        <div className="flex items-center justify-center rounded-lg border border-dashed border-navy-600 py-12">
          <p className="text-text-muted">No articles found for this category.</p>
        </div>
      ) : null}

      {articles.length > 0 && hasMore ? (
        <div className="flex justify-center">
          <Button
            type="button"
            variant="secondary"
            onClick={() => setPage((prev) => prev + 1)}
            loading={isFetching && page > 1}
          >
            Load More
          </Button>
        </div>
      ) : null}
    </div>
  )
}
