export interface Article {
	title: string;
	url: string;
	source_name: string;
	published_at: string | null;
	ai_summary: string | null;
	category: string;
}

export interface SavedArticle extends Article {
	id: string;
	saved_at: string;
}

export interface SummarizeArticleRequest {
	title: string;
	url: string;
	source_name: string;
	published_at: string | null;
	category: string;
}

export interface SummarizeArticleResponse {
	url: string;
	ai_summary: string;
	cached: boolean;
}

export type FeedPeriod = 'today' | 'week' | 'month';
