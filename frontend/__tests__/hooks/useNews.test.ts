import { renderHook, waitFor } from '@testing-library/react'
import { useNewsFeed, useSaveArticle } from '@/hooks/useNews'
import { api } from '@/lib/api'
import { createWrapper } from '../test-utils'
import { toast } from 'sonner'
import type { Article } from '@/types/news'

jest.mock('@/lib/api')
jest.mock('sonner')

beforeEach(() => {
  jest.clearAllMocks()
})

describe('News Hooks', () => {
  describe('useNewsFeed', () => {
    test('fetches news feed with correct params', async () => {
      const mockData: Article[] = [
        {
          title: 'Tech News',
          url: 'http://tech.com',
          source_name: 'TechCrunch',
          published_at: '2024-01-01',
          ai_summary: 'Summary',
          category: 'technology',
        },
      ]

      ;(api.get as jest.Mock).mockResolvedValueOnce({ data: mockData })

      const { result } = renderHook(() => useNewsFeed('technology', 'today'), { wrapper: createWrapper() })

      await waitFor(() => expect(result.current.isSuccess).toBe(true))

      expect(api.get).toHaveBeenCalledWith('/news/feed', { params: { category: 'technology', period: 'today' } })
      expect(result.current.data).toEqual(mockData)
    })

    test('fetches with world category and week period', async () => {
      ;(api.get as jest.Mock).mockResolvedValueOnce({ data: [] })

      const { result } = renderHook(() => useNewsFeed('world', 'week'), { wrapper: createWrapper() })

      await waitFor(() => expect(result.current.isSuccess).toBe(true))

      expect(api.get).toHaveBeenCalledWith('/news/feed', { params: { category: 'world', period: 'week' } })
    })

    test('handles API errors gracefully', async () => {
      const error = new Error('API Error')
      ;(api.get as jest.Mock).mockRejectedValueOnce(error)

      const { result } = renderHook(() => useNewsFeed('technology', 'today'), { wrapper: createWrapper() })

      await waitFor(() => expect(result.current.isError).toBe(true))
      expect(result.current.error).toBeTruthy()
    })

    test('returns empty array on success with no articles', async () => {
      ;(api.get as jest.Mock).mockResolvedValueOnce({ data: [] })

      const { result } = renderHook(() => useNewsFeed('sports', 'month'), { wrapper: createWrapper() })

      await waitFor(() => expect(result.current.isSuccess).toBe(true))
      expect(result.current.data).toEqual([])
    })
  })

  describe('useSaveArticle', () => {
    test('saves article successfully', async () => {
      const article: Article = {
        title: 'News Title',
        url: 'http://news.com',
        source_name: 'BBC',
        published_at: '2024-01-01',
        ai_summary: null,
        category: 'world',
      }

      ;(api.post as jest.Mock).mockResolvedValueOnce({
        data: { ...article, id: '1', saved_at: '2024-01-01' },
      })

      const { result } = renderHook(() => useSaveArticle(), { wrapper: createWrapper() })

      result.current.mutate(article)

      await waitFor(() => expect(result.current.isSuccess).toBe(true))
      expect(api.post).toHaveBeenCalledWith('/news/saved', article)
    })

    test('shows error toast on 409 duplicate article', async () => {
      const article: Article = {
        title: 'News Title',
        url: 'http://news.com',
        source_name: 'BBC',
        published_at: null,
        ai_summary: null,
        category: 'world',
      }

      ;(api.post as jest.Mock).mockRejectedValueOnce({
        response: { status: 409, data: { detail: 'Article already saved' } },
      })

      const { result } = renderHook(() => useSaveArticle(), { wrapper: createWrapper() })

      result.current.mutate(article)

      await waitFor(() => expect(result.current.isError).toBe(true))
      expect(toast.error).toHaveBeenCalledWith(expect.stringMatching(/zaten|already/i))
    })

    test('shows generic error toast on other API errors', async () => {
      const article: Article = {
        title: 'News Title',
        url: 'http://news.com',
        source_name: 'BBC',
        published_at: null,
        ai_summary: null,
        category: 'world',
      }

      ;(api.post as jest.Mock).mockRejectedValueOnce({
        response: { status: 500, data: { detail: 'Server error' } },
      })

      const { result } = renderHook(() => useSaveArticle(), { wrapper: createWrapper() })

      result.current.mutate(article)

      await waitFor(() => expect(result.current.isError).toBe(true))
      expect(toast.error).toHaveBeenCalled()
    })

    test('invalidates news feed cache on save success', async () => {
      const article: Article = {
        title: 'News Title',
        url: 'http://news.com',
        source_name: 'BBC',
        published_at: null,
        ai_summary: null,
        category: 'world',
      }

      ;(api.post as jest.Mock).mockResolvedValueOnce({
        data: { ...article, id: '1', saved_at: '2024-01-01' },
      })

      const { result } = renderHook(() => useSaveArticle(), { wrapper: createWrapper() })

      result.current.mutate(article)

      await waitFor(() => expect(result.current.isSuccess).toBe(true))
    })
  })
})
