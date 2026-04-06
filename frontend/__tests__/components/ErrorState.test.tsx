import { fireEvent, render, screen } from '@testing-library/react'

import { ErrorState } from '@/components/ErrorState'

describe('ErrorState', () => {
  test('error state shows retry button', () => {
    const onRetry = jest.fn()

    render(<ErrorState message="Yuklenemedi" onRetry={onRetry} />)

    expect(screen.getByRole('button', { name: /tekrar dene/i })).toBeInTheDocument()
  })

  test('retry button calls onRetry', () => {
    const onRetry = jest.fn()

    render(<ErrorState message="Yuklenemedi" onRetry={onRetry} />)
    fireEvent.click(screen.getByRole('button', { name: /tekrar dene/i }))

    expect(onRetry).toHaveBeenCalledTimes(1)
  })
})
