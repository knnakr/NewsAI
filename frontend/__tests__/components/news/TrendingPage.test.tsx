import { fireEvent, render, screen } from '@testing-library/react'

import TrendingPage from '@/app/(dashboard)/trending/page'
import { useSummarizeArticle } from '@/hooks/useNews'
import { useTrending } from '@/hooks/useTrending'

jest.mock('@/hooks/useTrending')
jest.mock('@/hooks/useNews')

describe('TrendingPage', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    ;(useSummarizeArticle as jest.Mock).mockReturnValue({
      mutateAsync: jest.fn(),
      isPending: false,
    })
  })

  test('renders Global Pulse heading', () => {
    ;(useTrending as jest.Mock).mockReturnValue({
      data: [],
      isLoading: false,
    })

    render(<TrendingPage />)

    expect(screen.getByText(/Global Pulse/i)).toBeInTheDocument()
  })

  test('clicking category chip updates selected topic', () => {
    ;(useTrending as jest.Mock).mockReturnValue({
      data: [],
      isLoading: false,
    })

    render(<TrendingPage />)

    fireEvent.click(screen.getByRole('button', { name: /Technology/i }))

    expect(useTrending).toHaveBeenLastCalledWith('technology')
  })
})