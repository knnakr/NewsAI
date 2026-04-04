import { renderHook, waitFor } from '@testing-library/react'

import { useLogin, useMe, useRegister } from '@/hooks/useAuth'
import { api } from '@/lib/api'
import { useAuthStore } from '@/stores/authStore'

import { createWrapper } from '../test-utils'

jest.mock('@/lib/api', () => ({
  api: {
    post: jest.fn(),
    get: jest.fn(),
  },
}))

beforeEach(() => {
  useAuthStore.setState({ accessToken: null, user: null })
  jest.clearAllMocks()
})

test('useLogin sets access token on success', async () => {
  ;(api.post as jest.Mock).mockResolvedValueOnce({
    data: { access_token: 'mock-token', token_type: 'bearer', expires_in: 900 },
  })

  const { result } = renderHook(() => useLogin(), { wrapper: createWrapper() })

  result.current.mutate({ email: 'test@test.com', password: 'pass123' })

  await waitFor(() => expect(result.current.isSuccess).toBe(true))
  expect(useAuthStore.getState().accessToken).toBe('mock-token')
})

test('useLogin returns error on 401', async () => {
  ;(api.post as jest.Mock).mockRejectedValueOnce({ response: { status: 401 } })

  const { result } = renderHook(() => useLogin(), { wrapper: createWrapper() })

  result.current.mutate({ email: 'bad@test.com', password: 'wrong' })

  await waitFor(() => expect(result.current.isError).toBe(true))
})

test('useMe returns null when not authenticated', () => {
  const { result } = renderHook(() => useMe(), { wrapper: createWrapper() })
  expect(result.current.data).toBeUndefined()
})

test('useRegister sends register payload', async () => {
  ;(api.post as jest.Mock).mockResolvedValueOnce({ data: { ok: true } })

  const { result } = renderHook(() => useRegister(), { wrapper: createWrapper() })

  result.current.mutate({
    email: 'new@test.com',
    password: 'pass12345',
    display_name: 'New User',
  })

  await waitFor(() => expect(result.current.isSuccess).toBe(true))
  expect(api.post).toHaveBeenCalledWith('/auth/register', {
    email: 'new@test.com',
    password: 'pass12345',
    display_name: 'New User',
  })
})