'use client'

import Link from 'next/link'
import { useState } from 'react'
import { Trash2 } from 'lucide-react'
import type { Conversation } from '@/types/conversation'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

interface ConversationListProps {
  conversations: Conversation[]
  activeId: string | null
  onDelete: (id: string) => void
  onUpdate?: (id: string, title: string) => void
}

function formatRelativeDate(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`

  return date.toLocaleDateString()
}

export default function ConversationList({
  conversations,
  activeId,
  onDelete,
  onUpdate
}: ConversationListProps) {
  const [hoveredId, setHoveredId] = useState<string | null>(null)
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editTitle, setEditTitle] = useState('')

  const handleDeleteClick = (id: string) => {
    setDeleteConfirmId(id)
  }

  const handleConfirmDelete = () => {
    if (deleteConfirmId) {
      onDelete(deleteConfirmId)
      setDeleteConfirmId(null)
    }
  }

  const handleCancelDelete = () => {
    setDeleteConfirmId(null)
  }

  const handleEditStart = (id: string, currentTitle: string) => {
    setEditingId(id)
    setEditTitle(currentTitle)
  }

  const handleEditSave = () => {
    if (editingId && onUpdate && editTitle.trim()) {
      onUpdate(editingId, editTitle)
      setEditingId(null)
      setEditTitle('')
    }
  }

  const handleEditCancel = () => {
    setEditingId(null)
    setEditTitle('')
  }

  const handleEditKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleEditSave()
    } else if (e.key === 'Escape') {
      handleEditCancel()
    }
  }

  // Show delete confirmation dialog
  if (deleteConfirmId) {
    return (
      <div className="flex flex-col gap-3 h-full">
        <Link href="/chat" className="w-full">
          <Button variant="secondary" className="w-full">
            New Chat
          </Button>
        </Link>

        <Card className="p-6 relative">
          <p className="text-sm font-medium mb-4">Are you sure you want to delete this conversation? (Emin misiniz?)</p>
          <div className="flex gap-2 justify-end">
            <Button
              variant="secondary"
              size="sm"
              onClick={handleCancelDelete}
            >
              Cancel (İptal)
            </Button>
            <Button
              variant="danger"
              size="sm"
              onClick={handleConfirmDelete}
            >
              Delete (Sil)
            </Button>
          </div>
        </Card>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-3 h-full">
      <Link href="/chat" className="w-full">
        <Button variant="secondary" className="w-full">
          New Chat
        </Button>
      </Link>

      <div className="flex-1 overflow-y-auto space-y-2">
        {conversations.length === 0 ? (
          <div className="rounded-lg border border-dashed border-navy-600 px-4 py-6 text-center">
            <p className="text-sm text-text-muted">Henüz sohbet yok. Yeni bir sohbet başlat.</p>
          </div>
        ) : null}

        {conversations.map((conv) => (
          <div
            key={conv.id}
            onMouseEnter={() => setHoveredId(conv.id)}
            onMouseLeave={() => setHoveredId(null)}
            className={`relative rounded-md p-3 transition-colors ${
              activeId === conv.id
                ? 'bg-accent-blue/20 border border-accent-blue'
                : 'hover:bg-navy-700/50'
            }`}
          >
            {editingId === conv.id ? (
              <input
                autoFocus
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                onKeyDown={handleEditKeyDown}
                onBlur={handleEditCancel}
                className="w-full px-2 py-1 text-sm bg-navy-600 text-white rounded border border-accent-blue focus:outline-none"
              />
            ) : (
              <Link href={`/chat/${conv.id}`} className="block pr-8">
                <p
                  className="font-medium text-sm truncate cursor-pointer hover:text-accent-blue"
                  onDoubleClick={() => handleEditStart(conv.id, conv.title)}
                >
                  {conv.title}
                </p>
                <p className="text-xs text-gray-400">
                  {formatRelativeDate(conv.updated_at)}
                </p>
              </Link>
            )}

            {hoveredId === conv.id && editingId !== conv.id && (
              <button
                onClick={(e) => {
                  e.preventDefault()
                  handleDeleteClick(conv.id)
                }}
                className="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover:bg-red-500/20 rounded transition-colors"
                aria-label="Delete conversation"
              >
                <Trash2 size={16} className="text-red-400" />
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
