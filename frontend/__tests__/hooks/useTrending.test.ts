import { renderHook, waitFor } from '@testing-library/react'

import { useTrending } from '@/hooks/useTrending'
import { api } from '@/lib/api'
import { createWrapper } from '../test-utils'

jest.mock('@/lib/api')

beforeEach(() => {
  jest.clearAllMocks()
})

describe('useTrending', () => {
  test('fetches trending news with topic parameter', async () => {
    const mockData = [
      {
        title: 'AI adoption rises globally',
        url: 'https://example.com/ai-adoption',
        source_name: 'Global Tech',
        published_at: '2026-04-05T10:00:00Z',
        ai_summary: 'AI adoption increased this quarter.',
        category: 'technology',
      },
    ]

    ;(api.get as jest.Mock).mockResolvedValueOnce({ data: mockData })

    const { result } = renderHook(() => useTrending('technology'), {
      wrapper: createWrapper(),
    })

    await waitFor(() => expect(result.current.isSuccess).toBe(true))

    expect(api.get).toHaveBeenCalledWith('/news/trending', {
      params: { topic: 'technology' },
    })
    expect(result.current.data).toEqual(mockData)
  })

  test('fetches trending news without topic', async () => {
    ;(api.get as jest.Mock).mockResolvedValueOnce({ data: [] })

    const { result } = renderHook(() => useTrending(), {
      wrapper: createWrapper(),
    })

    await waitFor(() => expect(result.current.isSuccess).toBe(true))

    expect(api.get).toHaveBeenCalledWith('/news/trending', {
      params: { topic: undefined },
    })
    expect(result.current.data).toEqual([])
  })

  test('handles API errors', async () => {
    ;(api.get as jest.Mock).mockRejectedValueOnce(new Error('API Error'))

    const { result } = renderHook(() => useTrending('world'), {
      wrapper: createWrapper(),
    })

    await waitFor(() => expect(result.current.isError).toBe(true))
    expect(result.current.error).toBeTruthy()
  })
})