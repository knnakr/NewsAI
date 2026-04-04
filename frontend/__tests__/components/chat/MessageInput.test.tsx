import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { MessageInput } from '@/components/chat/MessageInput'

test('renders textarea', () => {
  render(<MessageInput onSend={jest.fn()} disabled={false} />)

  expect(screen.getByRole('textbox')).toBeInTheDocument()
})

test('does not submit empty message', () => {
  const onSend = jest.fn()

  render(<MessageInput onSend={onSend} disabled={false} />)

  fireEvent.click(screen.getByRole('button', { name: /send/i }))

  expect(onSend).not.toHaveBeenCalled()
})

test('submits on Enter key', async () => {
  const onSend = jest.fn()

  render(<MessageInput onSend={onSend} disabled={false} />)

  await userEvent.type(screen.getByRole('textbox'), 'Hello{Enter}')

  expect(onSend).toHaveBeenCalledWith('Hello')
})

test('does not submit on Shift+Enter', async () => {
  const onSend = jest.fn()

  render(<MessageInput onSend={onSend} disabled={false} />)

  await userEvent.type(screen.getByRole('textbox'), 'Hello{Shift>}{Enter}')

  expect(onSend).not.toHaveBeenCalled()
})

test('send button is disabled when prop disabled=true', () => {
  render(<MessageInput onSend={jest.fn()} disabled={true} />)

  expect(screen.getByRole('button', { name: /send/i })).toBeDisabled()
})

test('shows character count', async () => {
  render(<MessageInput onSend={jest.fn()} disabled={false} />)

  await userEvent.type(screen.getByRole('textbox'), 'Test message')

  expect(screen.getByText(/12.*4000/)).toBeInTheDocument()
})