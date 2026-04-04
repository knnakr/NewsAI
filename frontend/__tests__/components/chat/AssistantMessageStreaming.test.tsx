import React from 'react'
import { render, screen } from '@testing-library/react'
import { AssistantMessage } from '@/components/chat/AssistantMessage'

jest.mock('react-markdown', () => ({
  __esModule: true,
  default: ({ children }: { children: string }) => <span>{children}</span>,
}))

describe('AssistantMessage - Streaming Cursor Animation', () => {
  test('shows cursor animation when isStreaming is true', () => {
    const { container } = render(
      <AssistantMessage
        content="Hello world"
        sources={null}
        isStreaming={true}
      />
    )
    
    // Check if the cursor/blinking element is rendered
    const cursorElement = container.querySelector('[data-testid="streaming-cursor"]')
    expect(cursorElement).toBeInTheDocument()
  })

  test('hides cursor animation when isStreaming is false', () => {
    const { container } = render(
      <AssistantMessage
        content="Hello world"
        sources={null}
        isStreaming={false}
      />
    )
    
    const cursorElement = container.querySelector('[data-testid="streaming-cursor"]')
    expect(cursorElement).not.toBeInTheDocument()
  })

  test('renders content normally when not streaming', () => {
    render(
      <AssistantMessage
        content="This is my response"
        sources={null}
        isStreaming={false}
      />
    )
    
    expect(screen.getByText(/This is my response/)).toBeInTheDocument()
  })

  test('renders content and cursor when streaming', () => {
    const { container } = render(
      <AssistantMessage
        content="Streaming response"
        sources={null}
        isStreaming={true}
      />
    )
    
    expect(screen.getByText(/Streaming response/)).toBeInTheDocument()
    expect(container.querySelector('[data-testid="streaming-cursor"]')).toBeInTheDocument()
  })

  test('renders sources with content when isStreaming is false', () => {
    const sources = [
      { title: 'Source 1', url: 'http://example.com', snippet: 'snippet' },
      { title: 'Source 2', url: 'http://example2.com', snippet: 'snippet2' }
    ]
    
    render(
      <AssistantMessage
        content="Response"
        sources={sources}
        isStreaming={false}
      />
    )
    
    expect(screen.getByText('Source 1')).toBeInTheDocument()
    expect(screen.getByText('Source 2')).toBeInTheDocument()
  })

  test('applies streaming animation class when isStreaming is true', () => {
    const { container } = render(
      <AssistantMessage
        content="Streaming"
        sources={null}
        isStreaming={true}
      />
    )
    
    const cursor = container.querySelector('[data-testid="streaming-cursor"]')
    expect(cursor).toHaveClass('animate-pulse')
  })
})
