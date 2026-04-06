import { useQuery } from '@tanstack/react-query'

import { api } from '@/lib/api'
import type { Article } from '@/types/news'

export function useTrending(topic?: string) {
	return useQuery({
		queryKey: ['trending', topic],
		queryFn: () => api.get<Article[]>('/news/trending', { params: { topic } }).then((r) => r.data),
		staleTime: 1000 * 60 * 5,
	})
}
