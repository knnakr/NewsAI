import { renderHook, waitFor } from '@testing-library/react'

import { useConversations, useCreateConversation, useDeleteConversation } from '@/hooks/useConversations'
import { api } from '@/lib/api'
import { queryClient } from '@/lib/queryClient'

import { createWrapper } from '../test-utils'

const mockPush = jest.fn()

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush }),
}))

jest.mock('@/lib/api', () => ({
  api: {
    get: jest.fn(),
    post: jest.fn(),
    delete: jest.fn(),
  },
}))

beforeEach(() => {
  jest.clearAllMocks()
})

test('useConversations fetches conversation list', async () => {
  ;(api.get as jest.Mock).mockResolvedValueOnce({
    data: [{ id: '1', title: 'Test Conv', updated_at: '2024-01-01T00:00:00Z' }],
  })

  const { result } = renderHook(() => useConversations(), { wrapper: createWrapper() })

  await waitFor(() => expect(result.current.isSuccess).toBe(true))

  expect(api.get).toHaveBeenCalledWith('/conversations')
  expect(result.current.data).toHaveLength(1)
})

test('useCreateConversation posts payload and navigates to the new conversation', async () => {
  ;(api.post as jest.Mock).mockResolvedValueOnce({
    data: { id: 'conv-1', title: 'New Chat', updated_at: '2024-01-01T00:00:00Z' },
  })

  const invalidateSpy = jest.spyOn(queryClient, 'invalidateQueries')
  const { result } = renderHook(() => useCreateConversation(), { wrapper: createWrapper() })

  result.current.mutate({ title: 'New Chat' })

  await waitFor(() => expect(result.current.isSuccess).toBe(true))

  expect(api.post).toHaveBeenCalledWith('/conversations', { title: 'New Chat' })
  expect(invalidateSpy).toHaveBeenCalledWith({ queryKey: ['conversations'] })
  expect(mockPush).toHaveBeenCalledWith('/chat/conv-1')
})

test('useDeleteConversation deletes conversation and invalidates list cache', async () => {
  ;(api.delete as jest.Mock).mockResolvedValueOnce({ data: { detail: 'Konuşma silindi' } })

  const invalidateSpy = jest.spyOn(queryClient, 'invalidateQueries')
  const { result } = renderHook(() => useDeleteConversation(), { wrapper: createWrapper() })

  result.current.mutate('conv-1')

  await waitFor(() => expect(result.current.isSuccess).toBe(true))

  expect(api.delete).toHaveBeenCalledWith('/conversations/conv-1')
  expect(invalidateSpy).toHaveBeenCalledWith({ queryKey: ['conversations'] })
})