import type { ButtonHTMLAttributes, ReactNode } from "react";

import { cn } from "@/lib/utils";

import { Spinner } from "./Spinner";

type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";
type ButtonSize = "sm" | "md" | "lg";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
	children: ReactNode;
	variant?: ButtonVariant;
	size?: ButtonSize;
	loading?: boolean;
};

const variantClasses: Record<ButtonVariant, string> = {
	primary: "bg-accent-blue text-white hover:opacity-90",
	secondary: "bg-navy-700 text-slate-100 hover:bg-navy-600",
	ghost: "bg-transparent text-slate-200 hover:bg-navy-800",
	danger: "bg-red-600 text-white hover:bg-red-500",
};

const sizeClasses: Record<ButtonSize, string> = {
	sm: "h-8 px-3 text-xs",
	md: "h-10 px-4 text-sm",
	lg: "h-12 px-5 text-base",
};

export function Button({
	children,
	variant = "primary",
	size = "md",
	loading = false,
	disabled,
	className,
	type = "button",
	...props
}: ButtonProps) {
	const isDisabled = disabled || loading;

	return (
		<button
			type={type}
			disabled={isDisabled}
			aria-busy={loading}
			className={cn(
				"inline-flex items-center justify-center gap-2 rounded-lg font-medium transition disabled:cursor-not-allowed disabled:opacity-60",
				variantClasses[variant],
				sizeClasses[size],
				className,
			)}
			{...props}
		>
			{loading ? <Spinner className="h-3.5 w-3.5 border-slate-200 border-t-white" /> : null}
			<span>{children}</span>
		</button>
	);
}
