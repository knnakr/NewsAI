import { useMutation, useQuery } from '@tanstack/react-query'
import type { AxiosError } from 'axios'
import { toast } from 'sonner'
import { api } from '@/lib/api'
import { queryClient } from '@/lib/queryClient'
import type { Article, SavedArticle, FeedPeriod } from '@/types/news'

type ApiErrorResponse = {
  status?: number
}

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

export function useCategoryNews(category: string, subcategory?: string, page = 1) {
  return useQuery({
    queryKey: ['category-news', category, subcategory, page],
    queryFn: () =>
      api
        .get<Article[]>(`/news/category/${category}`, {
          params: { subcategory, page, page_size: 12 },
        })
        .then((r) => r.data),
    staleTime: 1000 * 60 * 10,
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
    onError: (error: unknown) => {
      const statusCode = (error as AxiosError<ApiErrorResponse>)?.response?.status

      if (statusCode === 409) {
        toast.error('Bu makale zaten kaydedilmiş!')
      } else {
        toast.error('Makale kaydedilirken bir hata oluştu.')
      }
    },
  })
}

export function useSavedArticles() {
  const savedArticlesQuery = useQuery({
    queryKey: ['saved-articles'],
    queryFn: () => api.get<SavedArticle[]>('/news/saved').then((response) => response.data),
  })

  const deleteSavedArticle = useMutation({
    mutationFn: async (articleId: string) => {
      await api.delete(`/news/saved/${articleId}`)
      return articleId
    },
    onSuccess: () => {
      toast.success('Saved article deleted successfully!')
      queryClient.invalidateQueries({ queryKey: ['saved-articles'] })
    },
    onError: () => {
      toast.error('Makale silinirken bir hata oluştu.')
    },
  })

  return {
    ...savedArticlesQuery,
    deleteSavedArticle,
  }
}
