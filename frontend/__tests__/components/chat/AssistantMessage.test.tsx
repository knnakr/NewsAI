import { render, screen } from '@testing-library/react'

import { AssistantMessage } from '@/components/chat/AssistantMessage'

jest.mock('react-markdown', () => ({
  __esModule: true,
  default: ({ children }: { children: string }) => <span>{children}</span>,
}))

test('renders AI response content', () => {
  render(<AssistantMessage content="Here is your news summary" sources={null} />)

  expect(screen.getByText(/Here is your news summary/)).toBeInTheDocument()
})

test('renders sources when provided', () => {
  const sources = [{ title: 'BBC News', url: 'http://bbc.com', snippet: 'snippet' }]

  render(<AssistantMessage content="News" sources={sources} />)

  expect(screen.getByText('BBC News')).toBeInTheDocument()
  expect(screen.getByRole('link', { name: 'BBC News' })).toHaveAttribute('href', 'http://bbc.com')
})

test('does not render sources section when sources is null', () => {
  render(<AssistantMessage content="News" sources={null} />)

  expect(screen.queryByText(/Sources/i)).not.toBeInTheDocument()
})

test('sources links open in new tab', () => {
  const sources = [{ title: 'CNN', url: 'http://cnn.com', snippet: '' }]

  render(<AssistantMessage content="News" sources={sources} />)

  expect(screen.getByRole('link', { name: 'CNN' })).toHaveAttribute('target', '_blank')
})