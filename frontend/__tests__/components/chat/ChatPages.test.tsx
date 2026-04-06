import { fireEvent, render, screen, waitFor } from '@testing-library/react'

import ChatPage from '@/app/(dashboard)/chat/page'
import ChatDetailPage from '@/app/(dashboard)/chat/[id]/page'

const mockMutate = jest.fn()
const mockReplace = jest.fn()
const mockUseParams = jest.fn()

jest.mock('next/navigation', () => ({
  useRouter: () => ({ replace: mockReplace }),
  useParams: () => mockUseParams(),
  useSearchParams: () => new URLSearchParams(),
}))

jest.mock('@/hooks/useConversations', () => ({
  useCreateConversation: () => ({ mutate: mockMutate, isPending: false }),
}))

const mockUseMessages = jest.fn()
const mockUseSendMessage = jest.fn()

jest.mock('@/hooks/useMessages', () => ({
  useMessages: (...args: unknown[]) => mockUseMessages(...args),
  useSendMessage: (...args: unknown[]) => mockUseSendMessage(...args),
}))

jest.mock('@/components/chat/MessageList', () => ({
  MessageList: ({ messages, displayName }: { messages: Array<{ id: string }>; displayName: string }) => (
    <div>
      <span>messages:{messages.length}</span>
      <span>display:{displayName}</span>
    </div>
  ),
}))

jest.mock('@/components/chat/MessageInput', () => ({
  MessageInput: ({ disabled, onSend }: { disabled: boolean; onSend: (content: string) => void }) => (
    <button type="button" data-disabled={String(disabled)} onClick={() => onSend('hello')}>
      MessageInput
    </button>
  ),
}))

jest.mock('@/stores/authStore', () => ({
  useAuthStore: (selector: (state: { user: { display_name: string } | null }) => unknown) =>
    selector({
      user: {
        display_name: 'Ada',
      },
    }),
}))

beforeEach(() => {
  jest.clearAllMocks()
  mockUseParams.mockReturnValue({ id: 'conversation-1' })
})

test('chat page creates a conversation on send', () => {
  render(<ChatPage />)

  expect(screen.getByText(/Welcome to News AI/i)).toBeInTheDocument()

  fireEvent.click(screen.getByRole('button', { name: /messageinput/i }))

  expect(mockMutate).toHaveBeenCalledWith({
    title: 'hello',
    initialMessage: 'hello',
  })
})

test('chat detail page renders messages and message input', () => {
  mockUseMessages.mockReturnValue({
    data: {
      id: 'conversation-1',
      title: 'Test Chat',
      updated_at: '2024-01-01T00:00:00Z',
      messages: [{ id: '1', role: 'user', content: 'Hello', sources: null, created_at: '2024-01-01T00:00:00Z' }],
    },
    error: null,
    isLoading: false,
    isPending: false,
  })
  mockUseSendMessage.mockReturnValue({ mutate: jest.fn(), isPending: false })

  render(<ChatDetailPage />)

  expect(screen.getByText('messages:1')).toBeInTheDocument()
  expect(screen.getByText('display:Ada')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: /messageinput/i })).toHaveAttribute('data-disabled', 'false')
})

test('chat detail page redirects to chat when conversation is not found', async () => {
  mockUseMessages.mockReturnValue({
    data: undefined,
    error: { response: { status: 404 } },
    isLoading: false,
    isPending: false,
  })
  mockUseSendMessage.mockReturnValue({ mutate: jest.fn(), isPending: false })

  render(<ChatDetailPage />)

  await waitFor(() => expect(mockReplace).toHaveBeenCalledWith('/chat'))
})