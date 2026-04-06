import { fireEvent, render, screen } from '@testing-library/react'

import { SubCategoryChips } from '@/components/news/SubCategoryChips'

const mockPush = jest.fn()

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush }),
  useSearchParams: () => new URLSearchParams(),
  usePathname: () => '/category/sports',
}))

describe('SubCategoryChips', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  test('renders sports subcategories for sports category', () => {
    render(<SubCategoryChips category="sports" activeSubcategory={null} onSelect={jest.fn()} />)

    expect(screen.getByText(/Football/i)).toBeInTheDocument()
    expect(screen.getByText(/Basketball/i)).toBeInTheDocument()
  })

  test('renders technology subcategories for technology category', () => {
    render(<SubCategoryChips category="technology" activeSubcategory={null} onSelect={jest.fn()} />)

    expect(screen.getByText(/AI/i)).toBeInTheDocument()
    expect(screen.getByText(/Semiconductors/i)).toBeInTheDocument()
  })

  test('clicking subcategory updates URL query param', async () => {
    render(<SubCategoryChips category="sports" activeSubcategory={null} onSelect={jest.fn()} />)

    fireEvent.click(screen.getByText(/Football/i))

    expect(mockPush).toHaveBeenCalledWith(expect.stringContaining('football'))
  })
})