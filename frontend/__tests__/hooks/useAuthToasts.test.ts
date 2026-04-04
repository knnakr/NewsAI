import { renderHook, waitFor } from '@testing-library/react'

import { useLogin, useLogout } from '@/hooks/useAuth'
import { api } from '@/lib/api'
import { useAuthStore } from '@/stores/authStore'

import { createWrapper } from '../test-utils'

const mockToastSuccess = jest.fn()
const mockToastError = jest.fn()

jest.mock('sonner', () => ({
  toast: {
    success: (...args: unknown[]) => mockToastSuccess(...args),
    error: (...args: unknown[]) => mockToastError(...args),
  },
}))

jest.mock('@/lib/api', () => ({
  api: {
    post: jest.fn(),
    get: jest.fn(),
  },
}))

beforeEach(() => {
  useAuthStore.setState({
    accessToken: null,
    user: {
      id: '1',
      email: 'ada@test.com',
      display_name: 'Ada',
      role: 'user',
      email_verified_at: null,
      created_at: '2026-03-31T00:00:00Z',
    },
  })
  jest.clearAllMocks()
})

test('shows success toast on login success', async () => {
  ;(api.post as jest.Mock).mockResolvedValueOnce({
    data: { access_token: 'token', token_type: 'bearer', expires_in: 900 },
  })

  const { result } = renderHook(() => useLogin(), { wrapper: createWrapper() })

  result.current.mutate({ email: 'ada@test.com', password: 'password123' })

  await waitFor(() => expect(result.current.isSuccess).toBe(true))
  expect(mockToastSuccess).toHaveBeenCalledWith('Tekrar hoş geldin, Ada!')
})

test('shows success toast on logout', async () => {
  ;(api.post as jest.Mock).mockResolvedValueOnce({ data: { ok: true } })

  const { result } = renderHook(() => useLogout(), { wrapper: createWrapper() })

  result.current.mutate()

  await waitFor(() => expect(result.current.isSuccess).toBe(true))
  expect(mockToastSuccess).toHaveBeenCalledWith('Güvenli çıkış yapıldı.')
})

test('shows API error message toast on login error', async () => {
  ;(api.post as jest.Mock).mockRejectedValueOnce({
    response: { data: { detail: 'Geçersiz kimlik bilgileri' } },
  })

  const { result } = renderHook(() => useLogin(), { wrapper: createWrapper() })

  result.current.mutate({ email: 'ada@test.com', password: 'wrong-password' })

  await waitFor(() => expect(result.current.isError).toBe(true))
  expect(mockToastError).toHaveBeenCalledWith('Geçersiz kimlik bilgileri')
})