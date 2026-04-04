export interface Conversation {
	id: string;
	title: string;
	updated_at: string;
}

export interface Message {
	id: string;
	role: 'user' | 'assistant' | 'system';
	content: string;
	sources: Source[] | null;
	created_at: string;
}

export interface Source {
	title: string;
	url: string;
	snippet: string;
}

export interface ConversationDetail extends Conversation {
	messages: Message[];
}
