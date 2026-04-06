import { useMutation, useQuery } from '@tanstack/react-query'
import { useRouter } from 'next/navigation'

import { api } from '@/lib/api'
import { queryClient } from '@/lib/queryClient'
import type { Conversation } from '@/types/conversation'

type ConversationCreateInput = {
	title?: string
	initialMessage?: string
}

export function useConversations() {
	return useQuery({
		queryKey: ['conversations'],
		queryFn: () => api.get<Conversation[]>('/conversations').then((response) => response.data),
	})
}

export function useCreateConversation() {
	const router = useRouter()

	return useMutation({
		mutationFn: async (data?: ConversationCreateInput) => {
			const response = await api.post<Conversation>('/conversations', data)
			return response.data
		},
		onSuccess: (conversation, variables) => {
			queryClient.invalidateQueries({ queryKey: ['conversations'] })
			const initialMessage = variables?.initialMessage?.trim()
			router.push(
				initialMessage ? `/chat/${conversation.id}?message=${encodeURIComponent(initialMessage)}` : `/chat/${conversation.id}`,
			)
		},
	})
}

export function useDeleteConversation() {
	return useMutation({
		mutationFn: async (conversationId: string) => {
			const response = await api.delete(`/conversations/${conversationId}`)
			return response.data
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['conversations'] })
		},
	})
}

export function useUpdateConversation() {
	return useMutation({
		mutationFn: async (data: { conversationId: string; title: string }) => {
			const response = await api.patch<Conversation>(`/conversations/${data.conversationId}`, {
				title: data.title,
			})
			return response.data
		},
		onSuccess: () => {
			queryClient.invalidateQueries({ queryKey: ['conversations'] })
		},
	})
}
