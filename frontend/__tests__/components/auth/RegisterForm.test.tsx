import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import RegisterPage from '@/app/(auth)/register/page'
import { useRegister } from '@/hooks/useAuth'

const mockPush = jest.fn()
const mockToastSuccess = jest.fn()

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush }),
}))

jest.mock('sonner', () => ({
  toast: {
    success: (...args: unknown[]) => mockToastSuccess(...args),
  },
}))

jest.mock('@/hooks/useAuth', () => ({
  useRegister: jest.fn(),
}))

const mockUseRegister = useRegister as jest.Mock

beforeEach(() => {
  jest.clearAllMocks()
  mockUseRegister.mockReturnValue({
    mutate: jest.fn(),
    isPending: false,
    isError: false,
    error: null,
    isSuccess: false,
  })
})

test('renders all required fields', () => {
  render(<RegisterPage />)

  expect(screen.getByLabelText(/display name/i)).toBeInTheDocument()
  expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
})

test('shows error when password is too short', async () => {
  render(<RegisterPage />)

  await userEvent.type(screen.getByLabelText(/password/i), 'short')
  fireEvent.blur(screen.getByLabelText(/password/i))

  await waitFor(() => {
    expect(screen.getByText(/en az 8 karakter olmalı/i)).toBeInTheDocument()
  })
})

test('shows 409 error when email already exists', async () => {
  mockUseRegister.mockReturnValue({
    mutate: jest.fn(),
    isPending: false,
    isError: true,
    error: { response: { status: 409 } },
    isSuccess: false,
  })

  render(<RegisterPage />)

  await waitFor(() => {
    expect(screen.getByText(/zaten kullanılıyor/i)).toBeInTheDocument()
  })
})

test('redirects to login and shows success toast on successful register', async () => {
  mockUseRegister.mockReturnValue({
    mutate: jest.fn(),
    isPending: false,
    isError: false,
    error: null,
    isSuccess: true,
  })

  render(<RegisterPage />)

  await waitFor(() => {
    expect(mockPush).toHaveBeenCalledWith('/login')
    expect(mockToastSuccess).toHaveBeenCalledWith('Hoş geldin! Giriş yapabilirsin.')
  })
})
