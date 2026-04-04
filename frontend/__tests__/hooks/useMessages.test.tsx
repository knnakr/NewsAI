import type { ReactNode } from 'react'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { act, renderHook, waitFor } from '@testing-library/react'

import { useMessages, useSendMessage } from '@/hooks/useMessages'
import { api } from '@/lib/api'

jest.mock('@/lib/api', () => ({
  api: {
    get: jest.fn(),
    post: jest.fn(),
  },
}))

function createClientWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
      mutations: {
        retry: false,
      },
    },
  })

  function Wrapper({ children }: { children: ReactNode }) {
    return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  }

  return { queryClient, Wrapper }
}

beforeEach(() => {
  jest.clearAllMocks()
})

test('useMessages fetches conversation detail', async () => {
  ;(api.get as jest.Mock).mockResolvedValueOnce({
    data: {
      id: 'conv-1',
      title: 'Test Chat',
      updated_at: '2024-01-01T00:00:00Z',
      created_at: '2024-01-01T00:00:00Z',
      messages: [
        {
          id: 'msg-1',
          role: 'user',
          content: 'Hello',
          sources: null,
          created_at: '2024-01-01T00:00:00Z',
        },
      ],
    },
  })

  const { Wrapper } = createClientWrapper()
  const { result } = renderHook(() => useMessages('conv-1'), { wrapper: Wrapper })

  await waitFor(() => expect(result.current.isSuccess).toBe(true))

  expect(api.get).toHaveBeenCalledWith('/conversations/conv-1')
  expect(result.current.data?.messages).toHaveLength(1)
})

test('useSendMessage adds optimistic user message', async () => {
  let resolvePost: (value: {
    data: {
      id: string
      role: 'assistant'
      content: string
      sources: null
      created_at: string
    }
  }) => void = () => {}

  const postPromise = new Promise<{
    data: {
      id: string
      role: 'assistant'
      content: string
      sources: null
      created_at: string
    }
  }>((resolve) => {
    resolvePost = resolve
  })

  ;(api.post as jest.Mock).mockImplementationOnce(() => postPromise)

  const { queryClient, Wrapper } = createClientWrapper()
  queryClient.setQueryData(['conversation', 'conv-1'], {
    id: 'conv-1',
    title: 'Test Chat',
    updated_at: '2024-01-01T00:00:00Z',
    created_at: '2024-01-01T00:00:00Z',
    messages: [],
  })

  const { result } = renderHook(() => useSendMessage('conv-1'), { wrapper: Wrapper })

  act(() => {
    result.current.mutate('What is happening?')
  })

  await waitFor(() => {
    const optimisticConversation = queryClient.getQueryData<{
      messages: Array<{ role: string; content: string }>
    }>(['conversation', 'conv-1'])

    expect(optimisticConversation?.messages).toHaveLength(1)
    expect(optimisticConversation?.messages[0]).toMatchObject({
      role: 'user',
      content: 'What is happening?',
    })
  })

  resolvePost({
    data: {
      id: 'msg-assistant-1',
      role: 'assistant',
      content: 'AI response',
      sources: null,
      created_at: '2024-01-01T00:00:01Z',
    },
  })

  await waitFor(() => expect(result.current.isSuccess).toBe(true))

  expect(api.post).toHaveBeenCalledWith('/conversations/conv-1/messages', {
    content: 'What is happening?',
  })

  const finalConversation = queryClient.getQueryData<{
    messages: Array<{ role: string; content: string }>
  }>(['conversation', 'conv-1'])

  expect(finalConversation?.messages).toHaveLength(2)
  expect(finalConversation?.messages[1]).toMatchObject({
    role: 'assistant',
    content: 'AI response',
  })
})