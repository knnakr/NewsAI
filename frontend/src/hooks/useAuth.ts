import { useMutation, useQuery } from '@tanstack/react-query'
import { toast } from 'sonner'

import { api } from '@/lib/api'
import { queryClient } from '@/lib/queryClient'
import { useAuthStore } from '@/stores/authStore'
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '@/types/auth'

function getApiErrorMessage(error: unknown, fallback: string) {
  const responseData = (error as { response?: { data?: unknown } })?.response?.data

  if (typeof responseData === 'string' && responseData.trim()) {
    return responseData
  }

  if (responseData && typeof responseData === 'object') {
    const detail = (responseData as { detail?: unknown }).detail
    const message = (responseData as { message?: unknown }).message

    if (typeof detail === 'string' && detail.trim()) {
      return detail
    }
    if (typeof message === 'string' && message.trim()) {
      return message
    }
  }

  return fallback
}

export function useLogin() {
  return useMutation({
    mutationFn: async (data: LoginRequest) => {
      const response = await api.post<TokenResponse>('/auth/login', data)
      return response.data
    },
    onSuccess: (data) => {
      const currentUser = useAuthStore.getState().user
      useAuthStore.getState().setAccessToken(data.access_token)
      queryClient.invalidateQueries({ queryKey: ['me'] })

      toast.success(`Tekrar hoş geldin, ${currentUser?.display_name ?? 'kullanıcı'}!`)
    },
    onError: (error) => {
      toast.error(getApiErrorMessage(error, 'Giriş işlemi başarısız oldu'))
    },
  })
}

export function useRegister() {
  return useMutation({
    mutationFn: async (data: RegisterRequest) => {
      const response = await api.post('/auth/register', data)
      return response.data
    },
    onError: (error) => {
      toast.error(getApiErrorMessage(error, 'Kayıt işlemi başarısız oldu'))
    },
  })
}

export function useLogout() {
  return useMutation({
    mutationFn: async () => {
      const response = await api.post('/auth/logout')
      return response.data
    },
    onSuccess: () => {
      useAuthStore.getState().logout()
      queryClient.invalidateQueries({ queryKey: ['me'] })
      toast.success('Güvenli çıkış yapıldı.')
    },
    onError: (error) => {
      toast.error(getApiErrorMessage(error, 'Çıkış işlemi başarısız oldu'))
    },
  })
}

export function useMe() {
  const accessToken = useAuthStore((state) => state.accessToken)

  return useQuery({
    queryKey: ['me'],
    queryFn: () => api.get<User>('/users/me').then((response) => response.data),
    enabled: !!accessToken,
  })
}
