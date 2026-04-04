import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
	id: string;
	email: string;
	display_name: string;
	role: 'user' | 'admin';
	email_verified_at: string | null;
	created_at: string;
}

interface AuthStore {
	accessToken: string | null;
	user: User | null;
	setAccessToken: (token: string) => void;
	setUser: (user: User) => void;
	logout: () => void;
	isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthStore>()(
	persist(
		(set, get) => ({
			accessToken: null,
			user: null,
			setAccessToken: (token) => set({ accessToken: token }),
			setUser: (user) => set({ user }),
			logout: () => set({ accessToken: null, user: null }),
			isAuthenticated: () => !!get().accessToken,
		}),
		{ name: 'newsai-auth', partialize: (s) => ({ user: s.user }) },
	),
);
