import axios from 'axios'

import { useAuthStore } from '@/stores/authStore'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8001'

export const api = axios.create({
	baseURL: API_BASE_URL,
	withCredentials: true,
})

api.interceptors.request.use((config) => {
	const token = useAuthStore.getState().accessToken
	if (token) {
		config.headers.Authorization = `Bearer ${token}`
	}
	return config
})

api.interceptors.response.use(
	(res) => res,
	async (error) => {
		if (error.response?.status === 401) {
			try {
				const { data } = await axios.post(
					`${API_BASE_URL}/auth/refresh`,
					{},
					{ withCredentials: true }
				)

				const authState = useAuthStore.getState() as {
					setAccessToken?: (token: string) => void
					logout?: () => void
				}

				authState.setAccessToken?.(data.access_token)

				if (error.config?.headers) {
					error.config.headers.Authorization = `Bearer ${data.access_token}`
				}

				return axios(error.config)
			} catch {
				const authState = useAuthStore.getState() as {
					logout?: () => void
				}

				authState.logout?.()

				if (typeof window !== 'undefined') {
					window.location.href = '/login'
				}
			}
		}

		return Promise.reject(error)
	}
)
