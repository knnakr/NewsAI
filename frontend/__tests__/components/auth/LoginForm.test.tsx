import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import LoginPage from '@/app/(auth)/login/page'
import { useLogin } from '@/hooks/useAuth'

const mockPush = jest.fn()

jest.mock('next/navigation', () => ({
  useRouter: () => ({ push: mockPush }),
}))

jest.mock('@/hooks/useAuth', () => ({
  useLogin: jest.fn(),
}))

const mockUseLogin = useLogin as jest.Mock

beforeEach(() => {
  jest.clearAllMocks()
  mockUseLogin.mockReturnValue({
    mutate: jest.fn(),
    isPending: false,
    isError: false,
    error: null,
    isSuccess: false,
  })
})

test('renders email and password inputs', () => {
  render(<LoginPage />)

  expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
})

test('shows error when submitting empty form', async () => {
  render(<LoginPage />)

  fireEvent.click(screen.getByRole('button', { name: /giriş yap/i }))

  await waitFor(() => {
    expect(screen.getAllByText(/boş olamaz|gerekli/i).length).toBeGreaterThan(0)
  })
})

test('shows error for invalid email format', async () => {
  render(<LoginPage />)

  await userEvent.type(screen.getByLabelText(/email/i), 'notanemail')
  fireEvent.click(screen.getByRole('button', { name: /giriş yap/i }))

  await waitFor(() => {
    expect(screen.getByText(/geçerli.*email/i)).toBeInTheDocument()
  })
})

test('login button shows loading state during submission', async () => {
  mockUseLogin.mockReturnValue({
    mutate: jest.fn(),
    isPending: true,
    isError: false,
    error: null,
    isSuccess: false,
  })

  render(<LoginPage />)

  await userEvent.type(screen.getByLabelText(/email/i), 'test@test.com')
  await userEvent.type(screen.getByLabelText(/password/i), 'password123')
  fireEvent.click(screen.getByRole('button', { name: /giriş yap/i }))

  expect(screen.getByRole('button', { name: /giriş yap/i })).toBeDisabled()
})

test('shows locked account message on 423', async () => {
  mockUseLogin.mockReturnValue({
    mutate: jest.fn(),
    isPending: false,
    isError: true,
    error: { response: { status: 423 } },
    isSuccess: false,
  })

  render(<LoginPage />)

  await waitFor(() => {
    expect(screen.getByText(/kilitlendi/i)).toBeInTheDocument()
  })
})
