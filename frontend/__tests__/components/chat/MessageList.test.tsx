import { render, screen } from '@testing-library/react'

import { MessageList } from '@/components/chat/MessageList'

jest.mock('@/components/chat/AssistantMessage', () => ({
  AssistantMessage: ({ content }: { content: string }) => <div>{content}</div>,
}))

jest.mock('@/components/chat/UserMessage', () => ({
  UserMessage: ({ content }: { content: string }) => <div>{content}</div>,
}))

test('renders conversation messages in order', () => {
  render(
    <MessageList
      messages={[
        {
          id: '1',
          role: 'user',
          content: 'Hello',
          sources: null,
          created_at: '2024-01-01T00:00:00Z',
        },
        {
          id: '2',
          role: 'assistant',
          content: 'Hi there',
          sources: null,
          created_at: '2024-01-01T00:00:01Z',
        },
      ]}
      displayName="Ada"
    />
  )

  expect(screen.getByText('Hello')).toBeInTheDocument()
  expect(screen.getByText('Hi there')).toBeInTheDocument()
})