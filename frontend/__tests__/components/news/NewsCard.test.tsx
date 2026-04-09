import { render, screen, fireEvent } from '@testing-library/react'
import { NewsCard } from '@/components/news/NewsCard'
import type { Article } from '@/types/news'

describe('NewsCard', () => {
  const mockArticle: Article = {
    title: 'Big News',
    url: 'http://news.com',
    source_name: 'BBC',
    published_at: '2024-01-01',
    ai_summary: 'Summary text',
    category: 'technology',
  }

  test('renders article title and source', () => {
    render(<NewsCard article={mockArticle} />)
    expect(screen.getByText('Big News')).toBeInTheDocument()
    expect(screen.getByText('BBC')).toBeInTheDocument()
  })

  test('shows Summarize button when ai_summary is null', () => {
    const articleWithoutSummary: Article = {
      ...mockArticle,
      ai_summary: null,
    }
    render(<NewsCard article={articleWithoutSummary} />)
    expect(screen.getByRole('button', { name: /summarize/i })).toBeInTheDocument()
  })

  test('calls onSummarize when summarize button is clicked', () => {
    const articleWithoutSummary: Article = {
      ...mockArticle,
      ai_summary: null,
    }
    const onSummarize = jest.fn()

    render(<NewsCard article={articleWithoutSummary} onSummarize={onSummarize} />)
    fireEvent.click(screen.getByRole('button', { name: /summarize/i }))

    expect(onSummarize).toHaveBeenCalledWith(articleWithoutSummary)
  })

  test('does not show Summarize button when ai_summary exists', () => {
    render(<NewsCard article={mockArticle} />)
    expect(screen.queryByRole('button', { name: /summarize/i })).not.toBeInTheDocument()
  })

  test('bookmark button toggles saved state', async () => {
    const onSave = jest.fn()
    render(<NewsCard article={mockArticle} onSave={onSave} />)
    fireEvent.click(screen.getByRole('button', { name: /bookmark|kaydet/i }))
    expect(onSave).toHaveBeenCalled()
  })

  test('Read Full Article link opens in new tab', () => {
    render(<NewsCard article={mockArticle} />)
    const link = screen.getByRole('link', { name: /read full/i })
    expect(link).toHaveAttribute('target', '_blank')
    expect(link).toHaveAttribute('href', mockArticle.url)
  })

  test('renders AI summary when available', () => {
    render(<NewsCard article={mockArticle} />)
    expect(screen.getByText('Summary text')).toBeInTheDocument()
  })

  test('toggles summary panel visibility', () => {
    render(<NewsCard article={mockArticle} />)
    expect(screen.getByText('Summary text')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: /hide summary/i }))
    expect(screen.queryByText('Summary text')).not.toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: /show summary/i }))
    expect(screen.getByText('Summary text')).toBeInTheDocument()
  })
})
