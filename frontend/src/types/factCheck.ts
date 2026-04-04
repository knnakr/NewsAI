import type { Source } from './conversation';

export type Verdict = 'TRUE' | 'FALSE' | 'UNVERIFIED';

export interface FactCheck {
	id: string;
	claim: string;
	verdict: Verdict;
	explanation: string;
	sources: Source[];
	confidence_score: number;
	created_at: string;
}
