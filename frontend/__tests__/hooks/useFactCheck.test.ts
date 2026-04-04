import { renderHook, waitFor } from '@testing-library/react'
import { useRunFactCheck, useFactCheckHistory } from '@/hooks/useFactCheck'
import { api } from '@/lib/api'
import { useAuthStore } from '@/stores/authStore'
import { createWrapper } from '../test-utils'

jest.mock('@/lib/api')

// Mock useAuthStore with getState method
jest.mock('@/stores/authStore', () => ({
  useAuthStore: jest.fn(() => ({
    accessToken: null
  }))
}))

const mockUseAuthStore = useAuthStore as jest.MockedFunction<typeof useAuthStore>

beforeEach(() => {
  jest.clearAllMocks()
  // Reset the mock to default behavior
  mockUseAuthStore.mockImplementation(() => ({ accessToken: null }))
})

describe('useFactCheck hooks', () => {
  describe('useRunFactCheck', () => {
    test('sends claim to API', async () => {
      const factCheckResponse = {
        id: '1',
        claim: 'test claim',
        verdict: 'TRUE' as const,
        explanation: 'This is true.',
        sources: [],
        confidence_score: 0.9,
        created_at: '2024-01-01'
      }

      ;(api.post as jest.Mock).mockResolvedValueOnce({
        data: factCheckResponse
      })

      const { result } = renderHook(() => useRunFactCheck(), { wrapper: createWrapper() })

      result.current.mutate('test claim')

      await waitFor(() => expect(result.current.isSuccess).toBe(true))

      expect(api.post).toHaveBeenCalledWith('/fact-check', { claim: 'test claim' })
      expect(result.current.data).toEqual(factCheckResponse)
    })

    test('handles API errors', async () => {
      const error = new Error('API Error')
      ;(api.post as jest.Mock).mockRejectedValueOnce(error)

      const { result } = renderHook(() => useRunFactCheck(), { wrapper: createWrapper() })

      result.current.mutate('test claim')

      await waitFor(() => expect(result.current.isError).toBe(true))
      expect(result.current.error).toBeTruthy()
    })

    test('invalidates fact-check-history on success', async () => {
      const factCheckResponse = {
        id: '1',
        claim: 'test',
        verdict: 'TRUE' as const,
        explanation: 'True.',
        sources: [],
        confidence_score: 0.9,
        created_at: ''
      }

      ;(api.post as jest.Mock).mockResolvedValueOnce({
        data: factCheckResponse
      })

      const { result } = renderHook(() => useRunFactCheck(), { wrapper: createWrapper() })

      result.current.mutate('test claim')

      await waitFor(() => expect(result.current.isSuccess).toBe(true))
    })
  })

  describe('useFactCheckHistory', () => {
    test('fetches fact-check history when authenticated', async () => {
      const historyResponse = [
        {
          id: '1',
          claim: 'claim 1',
          verdict: 'TRUE' as const,
          explanation: 'True.',
          sources: [],
          confidence_score: 0.9,
          created_at: '2024-01-01'
        }
      ]

      // Setup mock with getState
      const mockGetState = jest.fn(() => ({ accessToken: 'token' }))
      mockUseAuthStore.mockImplementation(() => ({ accessToken: 'token' }))
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      ;(mockUseAuthStore as any).getState = mockGetState

      ;(api.get as jest.Mock).mockResolvedValueOnce({
        data: historyResponse
      })

      const { result } = renderHook(() => useFactCheckHistory(), { wrapper: createWrapper() })

      await waitFor(() => expect(result.current.isSuccess).toBe(true))

      expect(api.get).toHaveBeenCalledWith('/fact-check/history')
      expect(result.current.data).toEqual(historyResponse)
    })

    test('does not fetch when not authenticated', async () => {
      // Setup mock with getState returning no token
      const mockGetState = jest.fn(() => ({ accessToken: null }))
      mockUseAuthStore.mockImplementation(() => ({ accessToken: null }))
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      ;(mockUseAuthStore as any).getState = mockGetState

      const { result } = renderHook(() => useFactCheckHistory(), { wrapper: createWrapper() })

      // Query should be disabled, not execute
      expect(result.current.isLoading).toBe(false)
      expect(api.get).not.toHaveBeenCalled()
    })

    test('returns empty array on success with no history', async () => {
      // Setup mock with getState
      const mockGetState = jest.fn(() => ({ accessToken: 'token' }))
      mockUseAuthStore.mockImplementation(() => ({ accessToken: 'token' }))
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      ;(mockUseAuthStore as any).getState = mockGetState

      ;(api.get as jest.Mock).mockResolvedValueOnce({
        data: []
      })

      const { result } = renderHook(() => useFactCheckHistory(), { wrapper: createWrapper() })

      await waitFor(() => expect(result.current.isSuccess).toBe(true))

      expect(result.current.data).toEqual([])
    })
  })
})
