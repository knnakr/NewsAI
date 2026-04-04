import { render, screen } from '@testing-library/react'

import { WelcomeScreen } from '@/components/chat/WelcomeScreen'

test('does not render when visible is false', () => {
  const { container } = render(<WelcomeScreen onSuggestClick={jest.fn()} visible={false} />)

  expect(container).toBeEmptyDOMElement()
  expect(screen.queryByText(/Welcome to News AI/i)).not.toBeInTheDocument()
})