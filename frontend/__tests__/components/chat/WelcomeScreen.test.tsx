import { render, screen, fireEvent } from '@testing-library/react'

import { WelcomeScreen } from '@/components/chat/WelcomeScreen'

test('renders welcome heading', () => {
  render(<WelcomeScreen onSuggestClick={jest.fn()} />)

  expect(screen.getByText(/Welcome to News AI/i)).toBeInTheDocument()
})

test('renders 3 suggested questions', () => {
  render(<WelcomeScreen onSuggestClick={jest.fn()} />)

  const cards = screen.getAllByRole('button')

  expect(cards.length).toBeGreaterThanOrEqual(3)
})

test('clicking suggested question calls onSuggestClick', () => {
  const onSuggestClick = jest.fn()

  render(<WelcomeScreen onSuggestClick={onSuggestClick} />)

  fireEvent.click(screen.getAllByRole('button')[0])

  expect(onSuggestClick).toHaveBeenCalledWith(expect.any(String))
})