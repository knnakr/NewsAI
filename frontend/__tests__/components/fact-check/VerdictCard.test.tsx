import { render, screen } from '@testing-library/react'
import { VerdictCard } from '@/components/fact-check/VerdictCard'

describe('VerdictCard', () => {
  test('renders TRUE verdict with green color', () => {
    render(<VerdictCard verdict="TRUE" explanation="This is true." confidence_score={0.92} sources={[]} />)
    const badge = screen.getByText('TRUE')
    expect(badge.className).toMatch(/green|verdict-true/)
  })

  test('renders FALSE verdict with red color', () => {
    render(<VerdictCard verdict="FALSE" explanation="This is false." confidence_score={0.95} sources={[]} />)
    const badge = screen.getByText('FALSE')
    expect(badge.className).toMatch(/red|verdict-false/)
  })

  test('renders UNVERIFIED verdict with yellow color', () => {
    render(<VerdictCard verdict="UNVERIFIED" explanation="Cannot verify." confidence_score={0.3} sources={[]} />)
    const badge = screen.getByText('UNVERIFIED')
    expect(badge.className).toMatch(/yellow|amber|verdict-unverified/)
  })

  test('renders confidence score as percentage', () => {
    render(<VerdictCard verdict="TRUE" explanation="True." confidence_score={0.87} sources={[]} />)
    expect(screen.getByText(/87%/)).toBeInTheDocument()
  })

  test('renders sources list', () => {
    const sources = [{ title: 'Reuters', url: 'http://reuters.com', snippet: 'snippet' }]
    render(<VerdictCard verdict="TRUE" explanation="True." confidence_score={0.9} sources={sources} />)
    expect(screen.getByText('Reuters')).toBeInTheDocument()
  })

  test('shows loading skeleton when loading prop is true', () => {
    render(<VerdictCard loading />)
    expect(screen.getByTestId('verdict-skeleton')).toBeInTheDocument()
  })
})
