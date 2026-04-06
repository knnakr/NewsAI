import { fireEvent, render, screen } from '@testing-library/react'

import SavedPage from '@/app/(dashboard)/saved/page'
import { useSavedArticles } from '@/hooks/useNews'

jest.mock('@/hooks/useNews', () => ({
  useSavedArticles: jest.fn(),
}))

const savedArticles = [
  {
    id: 'saved-1',
    title: 'AI chip demand surges',
    url: 'https://example.com/ai-chip-demand',
    source_name: 'Reuters',
    published_at: '2026-04-05T10:00:00Z',
    ai_summary: 'Demand for AI chips keeps climbing.',
    category: 'technology',
    saved_at: '2026-04-05T11:00:00Z',
  },
  {
    id: 'saved-2',
    title: 'Election updates from Europe',
    url: 'https://example.com/election-updates',
    source_name: 'AP',
    published_at: '2026-04-04T09:00:00Z',
    ai_summary: null,
    category: 'world',
    saved_at: '2026-04-05T12:00:00Z',
  },
]

describe('SavedPage', () => {
  const mockedUseSavedArticles = useSavedArticles as unknown as jest.Mock
  const createHookResult = (deleteMutate: jest.Mock = jest.fn()) =>
    ({
      data: savedArticles,
      isLoading: false,
      deleteSavedArticle: { mutate: deleteMutate, isPending: false },
    } as unknown as ReturnType<typeof useSavedArticles>)

  beforeEach(() => {
    jest.clearAllMocks()
  })

  test('renders saved articles and category filters', () => {
    mockedUseSavedArticles.mockReturnValue(createHookResult())

    render(<SavedPage />)

    expect(screen.getByText(/Saved Articles/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /all/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /technology/i })).toBeInTheDocument()
    expect(screen.getByText('AI chip demand surges')).toBeInTheDocument()
    expect(screen.getByText('Election updates from Europe')).toBeInTheDocument()
    expect(screen.getAllByRole('button', { name: /delete article/i })).toHaveLength(2)
  })

  test('filters articles by category and calls delete mutation', () => {
    const deleteMutate = jest.fn()

    mockedUseSavedArticles.mockReturnValue(createHookResult(deleteMutate))

    render(<SavedPage />)

    fireEvent.click(screen.getByRole('button', { name: /technology/i }))

    expect(screen.getByText('AI chip demand surges')).toBeInTheDocument()
    expect(screen.queryByText('Election updates from Europe')).not.toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: /delete article/i }))
    expect(deleteMutate).toHaveBeenCalledWith('saved-1')
  })

  test('shows empty state when no saved articles exist', () => {
    mockedUseSavedArticles.mockReturnValue(
      ({
        data: [],
        isLoading: false,
        deleteSavedArticle: { mutate: jest.fn(), isPending: false },
      } as unknown as ReturnType<typeof useSavedArticles>),
    )

    render(<SavedPage />)

    expect(screen.getByText(/Henüz makale kaydetmediniz/i)).toBeInTheDocument()
  })
})
