import type { HTMLAttributes, ReactNode } from "react";

import { cn } from "@/lib/utils";

type CardProps = HTMLAttributes<HTMLDivElement> & {
	children: ReactNode;
};

export function Card({ children, className, ...props }: CardProps) {
	return (
		<div
			className={cn("rounded-lg border border-navy-600 bg-navy-700 p-4", className)}
			{...props}
		>
			{children}
		</div>
	);
}
