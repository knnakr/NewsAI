'use client'

import { useMemo, useState } from 'react'

import { NewsCard } from '@/components/news/NewsCard'
import { NewsCardSkeleton } from '@/components/news/NewsCardSkeleton'
import { ErrorState } from '@/components/ErrorState'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { useSavedArticles } from '@/hooks/useNews'
import type { SavedArticle } from '@/types/news'

const getCategories = (articles: SavedArticle[]) => {
	return ['all', ...Array.from(new Set(articles.map((article) => article.category)))].filter(Boolean)
}

export default function SavedPage() {
	const { data: savedArticles = [], isLoading, isError, refetch, deleteSavedArticle } = useSavedArticles()
	const [activeCategory, setActiveCategory] = useState('all')

	const categories = useMemo(() => getCategories(savedArticles), [savedArticles])
	const filteredArticles = useMemo(() => {
		if (activeCategory === 'all') return savedArticles
		return savedArticles.filter((article) => article.category === activeCategory)
	}, [activeCategory, savedArticles])

	const handleDelete = (articleId: string) => {
		deleteSavedArticle.mutate(articleId)
	}

	return (
		<div className="space-y-6 p-6">
			<div>
				<h1 className="mb-2 text-4xl font-bold text-text-primary">Saved Articles</h1>
				<p className="text-text-secondary">Makale arşivini yönet, kategorilere göre filtrele ve istemediklerini sil.</p>
			</div>

			<div className="flex flex-wrap gap-2">
				{categories.map((category) => {
					const isActive = activeCategory === category
					const label = category === 'all' ? 'All' : category.charAt(0).toUpperCase() + category.slice(1)

					return (
						<button
							key={category}
							type="button"
							onClick={() => setActiveCategory(category)}
							className={`rounded-full border px-4 py-2 text-sm font-medium transition-colors ${
								isActive
									? 'border-accent-blue bg-accent-blue text-white'
									: 'border-navy-600 text-text-secondary hover:border-navy-500 hover:text-text-primary'
							}`}
						>
							{label}
						</button>
					)
				})}
			</div>

				{isError ? <ErrorState message="Yüklenemedi. Tekrar dene" onRetry={() => void refetch()} /> : null}

			{isLoading ? (
				<div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
					{Array.from({ length: 6 }).map((_, index) => (
						<NewsCardSkeleton key={index} />
					))}
				</div>
			) : null}

			{!isLoading && !isError && filteredArticles.length > 0 ? (
				<div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
					{filteredArticles.map((article) => (
						<Card key={article.id} className="relative p-0">
							<div className="absolute right-3 top-3 z-10">
								<Button
									type="button"
									variant="danger"
									size="sm"
									onClick={() => handleDelete(article.id)}
									loading={deleteSavedArticle.isPending}
									aria-label="Delete article"
								>
									Sil
								</Button>
								</div>
							<div className="p-4">
									<NewsCard article={article} showSaveButton={false} />
							</div>
						</Card>
					))}
				</div>
			) : null}

			{!isLoading && !isError && filteredArticles.length === 0 ? (
				<div className="flex items-center justify-center rounded-lg border border-dashed border-navy-600 py-12">
					<p className="text-text-muted">Henüz makale kaydetmediniz.</p>
				</div>
			) : null}
		</div>
	)
}
