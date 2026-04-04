import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ClaimInput } from '@/components/fact-check/ClaimInput'

describe('ClaimInput', () => {
  test('renders textarea with correct placeholder', () => {
    render(<ClaimInput onSubmit={jest.fn()} isLoading={false} />)
    const textarea = screen.getByRole('textbox')
    expect(textarea).toHaveAttribute('placeholder', expect.stringMatching(/paste a claim|paste a headline|paste a url/i))
  })

  test('renders Verify Claim button', () => {
    render(<ClaimInput onSubmit={jest.fn()} isLoading={false} />)
    expect(screen.getByRole('button', { name: /verify claim/i })).toBeInTheDocument()
  })

  test('does not submit empty claim', async () => {
    const onSubmit = jest.fn()
    render(<ClaimInput onSubmit={onSubmit} isLoading={false} />)
    fireEvent.click(screen.getByRole('button', { name: /verify claim/i }))
    expect(onSubmit).not.toHaveBeenCalled()
  })

  test('submits claim when button clicked', async () => {
    const onSubmit = jest.fn()
    render(<ClaimInput onSubmit={onSubmit} isLoading={false} />)
    const textarea = screen.getByRole('textbox')
    await userEvent.type(textarea, 'Test claim')
    fireEvent.click(screen.getByRole('button', { name: /verify claim/i }))
    expect(onSubmit).toHaveBeenCalledWith('Test claim')
  })

  test('shows Verifying text when loading', () => {
    render(<ClaimInput onSubmit={jest.fn()} isLoading={true} />)
    expect(screen.getByRole('button', { name: /verifying/i })).toBeInTheDocument()
  })

  test('button is disabled when loading', () => {
    render(<ClaimInput onSubmit={jest.fn()} isLoading={true} />)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  test('clears textarea after submission', async () => {
    const onSubmit = jest.fn()
    const { rerender } = render(<ClaimInput onSubmit={onSubmit} isLoading={false} />)
    const textarea = screen.getByRole('textbox') as HTMLTextAreaElement
    await userEvent.type(textarea, 'Test claim')
    fireEvent.click(screen.getByRole('button', { name: /verify claim/i }))

    rerender(<ClaimInput onSubmit={onSubmit} isLoading={false} />)
    expect((screen.getByRole('textbox') as HTMLTextAreaElement).value).toBe('')
  })
})
