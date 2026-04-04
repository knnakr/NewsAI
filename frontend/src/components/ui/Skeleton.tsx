import { cn } from "@/lib/utils";

type SkeletonProps = {
	className?: string;
};

export function Skeleton({ className }: SkeletonProps) {
	return (
		<div
			data-testid="skeleton"
			aria-hidden="true"
			className={cn("animate-pulse rounded-md bg-navy-700/80", className)}
		/>
	);
}
