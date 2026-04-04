import { useMutation, useQuery } from '@tanstack/react-query'
import { toast } from 'sonner'
import { api } from '@/lib/api'
import { queryClient } from '@/lib/queryClient'
import type { Article, SavedArticle, FeedPeriod } from '@/types/news'

export function useNewsFeed(category: string, period: FeedPeriod) {
  return useQuery({
    queryKey: ['news-feed', category, period],
    queryFn: async () => {
      const { data } = await api.get<Article[]>('/news/feed', {
        params: { category, period },
      })
      return data
    },
  })
}

export function useSaveArticle() {
  return useMutation({
    mutationFn: async (article: Article) => {
      const { data } = await api.post<SavedArticle>('/news/saved', article)
      return data
    },
    onSuccess: () => {
      toast.success('Article saved successfully!')
      queryClient.invalidateQueries({ queryKey: ['news-feed'] })
      queryClient.invalidateQueries({ queryKey: ['saved-articles'] })
    },
    onError: (error: any) => {
      if (error.response?.status === 409) {
        toast.error('Bu makale zaten kaydedilmiş!')
      } else {
        toast.error('Makale kaydedilirken bir hata oluştu.')
      }
    },
  })
}
