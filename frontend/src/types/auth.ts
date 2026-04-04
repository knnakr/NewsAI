export interface LoginRequest {
	email: string;
	password: string;
}

export interface RegisterRequest {
	email: string;
	password: string;
	display_name: string;
}

export interface TokenResponse {
	access_token: string;
	token_type: string;
	expires_in: number;
}

export interface User {
	id: string;
	email: string;
	display_name: string;
	role: 'user' | 'admin';
	email_verified_at: string | null;
	created_at: string;
}
