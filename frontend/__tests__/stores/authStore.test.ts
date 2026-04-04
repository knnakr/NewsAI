import { renderHook, act } from '@testing-library/react';
import { useAuthStore } from '@/stores/authStore';

beforeEach(() => {
  useAuthStore.setState({ accessToken: null, user: null });
});

test('initial state has no accessToken', () => {
  const { result } = renderHook(() => useAuthStore());
  expect(result.current.accessToken).toBeNull();
});

test('setAccessToken updates state', () => {
  const { result } = renderHook(() => useAuthStore());
  act(() => result.current.setAccessToken('test-token'));
  expect(result.current.accessToken).toBe('test-token');
});

test('logout clears accessToken and user', () => {
  const { result } = renderHook(() => useAuthStore());
  act(() => {
    result.current.setAccessToken('token');
    result.current.setUser({
      id: '1',
      email: 'a@b.com',
      display_name: 'Test',
      role: 'user',
      email_verified_at: null,
      created_at: '',
    });
    result.current.logout();
  });
  expect(result.current.accessToken).toBeNull();
  expect(result.current.user).toBeNull();
});

test('isAuthenticated returns true when token exists', () => {
  const { result } = renderHook(() => useAuthStore());
  act(() => result.current.setAccessToken('some-token'));
  expect(result.current.isAuthenticated()).toBe(true);
});

test('isAuthenticated returns false when no token', () => {
  const { result } = renderHook(() => useAuthStore());
  expect(result.current.isAuthenticated()).toBe(false);
});
