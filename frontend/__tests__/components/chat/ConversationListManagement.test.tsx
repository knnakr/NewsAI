import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ConversationList from '@/components/chat/ConversationList'

describe('ConversationList Management', () => {
  describe('Delete Conversation', () => {
    test('shows confirm dialog before deleting conversation', async () => {
      const onDelete = jest.fn()
      const conversations = [{ id: '1', title: 'Conv 1', updated_at: '2024-01-01' }]
      render(
        <ConversationList conversations={conversations} activeId={null} onDelete={onDelete} />
      )
      
      await userEvent.hover(screen.getByText('Conv 1'))
      fireEvent.click(screen.getByRole('button', { name: /delete|sil/i }))
      
      expect(screen.getByText(/emin misiniz|are you sure/i)).toBeInTheDocument()
    })

    test('cancelling delete dialog does not call delete mutation', async () => {
      const onDelete = jest.fn()
      const conversations = [{ id: '1', title: 'Conv 1', updated_at: '2024-01-01' }]
      render(
        <ConversationList conversations={conversations} activeId={null} onDelete={onDelete} />
      )
      
      await userEvent.hover(screen.getByText('Conv 1'))
      fireEvent.click(screen.getByRole('button', { name: /delete|sil/i }))
      
      const cancelButton = screen.getByRole('button', { name: /iptal|cancel/i })
      fireEvent.click(cancelButton)
      
      expect(onDelete).not.toHaveBeenCalled()
    })

    test('confirming delete calls delete mutation', async () => {
      const onDelete = jest.fn()
      const conversations = [{ id: '1', title: 'Conv 1', updated_at: '2024-01-01' }]
      render(
        <ConversationList conversations={conversations} activeId={null} onDelete={onDelete} />
      )
      
      await userEvent.hover(screen.getByText('Conv 1'))
      fireEvent.click(screen.getByRole('button', { name: /delete|sil/i }))
      
      // After clicking delete, the dialog appears with Cancel and Delete buttons
      // We need to find the Delete button in the dialog (the one with text matching /Delete \(Sil\)/)
      const buttons = screen.getAllByRole('button')
      const deleteConfirmButton = buttons.find((btn) => btn.textContent?.includes('Delete (Sil)'))
      
      fireEvent.click(deleteConfirmButton!)
      
      expect(onDelete).toHaveBeenCalledWith('1')
    })
  })

  describe('Edit Conversation Title', () => {
    test('double-click enters edit mode', async () => {
      const onUpdate = jest.fn()
      const conversations = [{ id: '1', title: 'Conv 1', updated_at: '2024-01-01' }]
      render(
        <ConversationList
          conversations={conversations}
          activeId={null}
          onDelete={jest.fn()}
          onUpdate={onUpdate}
        />
      )
      
      const title = screen.getByText('Conv 1')
      fireEvent.doubleClick(title)
      
      expect(screen.getByRole('textbox')).toBeInTheDocument()
    })

    test('enter key saves new title', async () => {
      const onUpdate = jest.fn()
      const conversations = [{ id: '1', title: 'Conv 1', updated_at: '2024-01-01' }]
      render(
        <ConversationList
          conversations={conversations}
          activeId={null}
          onDelete={jest.fn()}
          onUpdate={onUpdate}
        />
      )
      
      const title = screen.getByText('Conv 1')
      fireEvent.doubleClick(title)
      
      const input = screen.getByRole('textbox') as HTMLInputElement
      await userEvent.clear(input)
      await userEvent.type(input, 'New Title')
      fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' })
      
      expect(onUpdate).toHaveBeenCalledWith('1', 'New Title')
    })

    test('escape key cancels edit', async () => {
      const onUpdate = jest.fn()
      const conversations = [{ id: '1', title: 'Conv 1', updated_at: '2024-01-01' }]
      render(
        <ConversationList
          conversations={conversations}
          activeId={null}
          onDelete={jest.fn()}
          onUpdate={onUpdate}
        />
      )
      
      const title = screen.getByText('Conv 1')
      fireEvent.doubleClick(title)
      
      const input = screen.getByRole('textbox')
      await userEvent.type(input, 'New Title')
      fireEvent.keyDown(input, { key: 'Escape', code: 'Escape' })
      
      expect(onUpdate).not.toHaveBeenCalled()
      expect(screen.getByText('Conv 1')).toBeInTheDocument()
    })
  })
})
