import { fireEvent, render, screen } from '@testing-library/react'

import { CategoryChips } from '@/components/news/CategoryChips'

describe('CategoryChips', () => {
  test('renders all category chips', () => {
    render(<CategoryChips activeChip={null} onSelect={jest.fn()} />)

    expect(screen.getByText(/Technology/i)).toBeInTheDocument()
    expect(screen.getByText(/Finance/i)).toBeInTheDocument()
  })

  test('active chip has accent styling', () => {
    render(<CategoryChips activeChip="Technology" onSelect={jest.fn()} />)

    const chip = screen.getByText('Technology').closest('button')
    expect(chip?.className).toMatch(/accent|active|bg-accent/)
  })

  test('clicking chip calls onSelect with chip name', () => {
    const onSelect = jest.fn()
    render(<CategoryChips activeChip={null} onSelect={onSelect} />)

    fireEvent.click(screen.getByText(/Technology/i))

    expect(onSelect).toHaveBeenCalledWith('Technology')
  })
})