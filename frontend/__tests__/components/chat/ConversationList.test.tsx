import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ConversationList from '@/components/chat/ConversationList'

describe('ConversationList', () => {
  test('renders conversation titles', () => {
    const conversations = [
      { id: '1', title: 'Conv 1', updated_at: '2024-01-01' },
      { id: '2', title: 'Conv 2', updated_at: '2024-01-02' }
    ]
    render(<ConversationList conversations={conversations} activeId={null} onDelete={jest.fn()} />)
    expect(screen.getByText('Conv 1')).toBeInTheDocument()
    expect(screen.getByText('Conv 2')).toBeInTheDocument()
  })

  test('shows delete button on hover', async () => {
    const conversations = [{ id: '1', title: 'Conv 1', updated_at: '2024-01-01' }]
    render(<ConversationList conversations={conversations} activeId={null} onDelete={jest.fn()} />)
    await userEvent.hover(screen.getByText('Conv 1'))
    expect(screen.getByRole('button', { name: /delete|sil/i })).toBeInTheDocument()
  })

  test('calls onDelete when delete button clicked', async () => {
    const onDelete = jest.fn()
    const conversations = [{ id: '1', title: 'Conv 1', updated_at: '2024-01-01' }]
    render(<ConversationList conversations={conversations} activeId={null} onDelete={onDelete} />)
    await userEvent.hover(screen.getByText('Conv 1'))
    fireEvent.click(screen.getByRole('button', { name: /delete|sil/i }))
    
    // Dialog appears, find and click the confirm delete button
    const buttons = screen.getAllByRole('button')
    const deleteConfirmButton = buttons.find((btn) => btn.textContent?.includes('Delete (Sil)'))
    fireEvent.click(deleteConfirmButton!)
    
    expect(onDelete).toHaveBeenCalledWith('1')
  })
})
