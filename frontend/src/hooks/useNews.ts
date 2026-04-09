import { useMutation, useQuery } from '@tanstack/react-query'
import type { AxiosError } from 'axios'
import { toast } from 'sonner'
import { api } from '@/lib/api'
import { queryClient } from '@/lib/queryClient'
import type {
  Article,
  SavedArticle,
  FeedPeriod,
  SummarizeArticleRequest,
  SummarizeArticleResponse,
} from '@/types/news'

type ApiErrorResponse = {
  status?: number
  detail?:
    | string
    | {
        error_type?: string
        message?: string
        provider_detail?: string
      }
}

function updateArticleSummaryInList(data: unknown, url: string, summary: string) {
  if (!Array.isArray(data)) return data
  return data.map((item) => {
    if (!item || typeof item !== 'object') return item

    const article = item as Article
    if (article.url !== url) return article

    return {
      ...article,
      ai_summary: summary,
    }
  })
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

export function useSummarizeArticle() {
  return useMutation({
    mutationFn: async (article: SummarizeArticleRequest) => {
      const { data } = await api.post<SummarizeArticleResponse>('/news/summarize', article)
      return data
    },
    onSuccess: (data, variables) => {
      const url = variables.url
      const summary = data.ai_summary

      queryClient.setQueriesData({ queryKey: ['news-feed'] }, (oldData) =>
        updateArticleSummaryInList(oldData, url, summary)
      )
      queryClient.setQueriesData({ queryKey: ['category-news'] }, (oldData) =>
        updateArticleSummaryInList(oldData, url, summary)
      )
      queryClient.setQueriesData({ queryKey: ['trending'] }, (oldData) =>
        updateArticleSummaryInList(oldData, url, summary)
      )

      toast.success(data.cached ? 'Summary loaded from cache.' : 'Summary generated successfully!')
    },
    onError: (error: unknown) => {
      const axiosError = error as AxiosError<ApiErrorResponse>
      const detail = axiosError.response?.data?.detail

      if (detail && typeof detail === 'object') {
        const errorType = detail.error_type

        if (detail.provider_detail) {
          console.warn('Summarize provider error:', detail.provider_detail)
        }

        if (errorType === 'rate_limit' || errorType === 'too_many_requests') {
          toast.error('Ozet servisi yogun (429). Lutfen biraz sonra tekrar deneyin.')
          return
        }

        if (errorType === 'timeout') {
          toast.error('Ozet olusturma zaman asimina ugradi (504). Lutfen tekrar deneyin.')
          return
        }

        if (errorType === 'bad_gateway') {
          toast.error('Saglayici gecici hata verdi (502). Lutfen tekrar deneyin.')
          return
        }
      }

      toast.error('Makale ozeti olusturulamadi.')
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
