import { render, screen } from '@testing-library/react'

import { UserMessage } from '@/components/chat/UserMessage'

test('renders user message content and avatar initial', () => {
  render(<UserMessage content="Hello there" displayName="Ada Lovelace" />)

  expect(screen.getByText('Hello there')).toBeInTheDocument()
  expect(screen.getByText('A')).toBeInTheDocument()
})