import { render, screen } from '@testing-library/react'

import { TrendingCard } from '@/components/news/TrendingCard'
import type { Article } from '@/types/news'

describe('TrendingCard', () => {
  const article: Article = {
    title: 'Global markets react to AI surge',
    url: 'https://example.com/markets-ai',
    source_name: 'Reuters',
    published_at: '2026-04-05T10:00:00Z',
    ai_summary: 'Markets climb as AI spending rises.',
    category: 'technology',
  }

  test('renders title and source', () => {
    render(<TrendingCard article={article} />)

    expect(screen.getByText(article.title)).toBeInTheDocument()
    expect(screen.getByText(article.source_name)).toBeInTheDocument()
  })

  test('read link opens in new tab', () => {
    render(<TrendingCard article={article} />)

    const link = screen.getByRole('link', { name: /read full/i })
    expect(link).toHaveAttribute('href', article.url)
    expect(link).toHaveAttribute('target', '_blank')
  })
})