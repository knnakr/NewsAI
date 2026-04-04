import { render, screen } from '@testing-library/react'

import { TypingIndicator } from '@/components/chat/TypingIndicator'

test('renders typing indicator with status role', () => {
  render(<TypingIndicator />)

  expect(screen.getByRole('status')).toBeInTheDocument()
})