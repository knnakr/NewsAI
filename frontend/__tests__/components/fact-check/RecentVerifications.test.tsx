import { render, screen } from '@testing-library/react'
import { RecentVerifications } from '@/components/fact-check/RecentVerifications'
import type { FactCheck } from '@/types/factCheck'

describe('RecentVerifications', () => {
  test('renders verifications list', () => {
    const verifications: FactCheck[] = [
      {
        id: '1',
        claim: 'Test claim 1',
        verdict: 'TRUE',
        explanation: 'True.',
        sources: [],
        confidence_score: 0.9,
        created_at: '2024-01-01T12:00:00Z',
      },
      {
        id: '2',
        claim: 'Test claim 2',
        verdict: 'FALSE',
        explanation: 'False.',
        sources: [],
        confidence_score: 0.8,
        created_at: '2024-01-02T12:00:00Z',
      },
    ]
    render(<RecentVerifications verifications={verifications} isLoading={false} />)
    expect(screen.getByText(/Test claim 1/)).toBeInTheDocument()
    expect(screen.getByText(/Test claim 2/)).toBeInTheDocument()
  })

  test('shows verdict badge for each verification', () => {
    const verifications: FactCheck[] = [
      {
        id: '1',
        claim: 'Claim',
        verdict: 'TRUE',
        explanation: 'True.',
        sources: [],
        confidence_score: 0.9,
        created_at: '2024-01-01T12:00:00Z',
      },
    ]
    render(<RecentVerifications verifications={verifications} isLoading={false} />)
    expect(screen.getByText('TRUE')).toBeInTheDocument()
  })

  test('shows loading skeleton when isLoading is true', () => {
    render(<RecentVerifications verifications={[]} isLoading={true} />)
    expect(screen.getByTestId('verification-skeleton')).toBeInTheDocument()
  })

  test('shows empty message when no verifications', () => {
    render(<RecentVerifications verifications={[]} isLoading={false} />)
    expect(screen.getByText(/no verifications|empty/i)).toBeInTheDocument()
  })

  test('truncates long claims', () => {
    const verifications: FactCheck[] = [
      {
        id: '1',
        claim: 'This is a very long claim that should be truncated because it is way too long to fit in the card without taking up too much space on the screen',
        verdict: 'TRUE',
        explanation: 'True.',
        sources: [],
        confidence_score: 0.9,
        created_at: '2024-01-01T12:00:00Z',
      },
    ]
    render(<RecentVerifications verifications={verifications} isLoading={false} />)
    const claimText = screen.getByText(/This is a very long claim/)
    expect(claimText.textContent!.length).toBeLessThan(verifications[0].claim.length)
  })
})
