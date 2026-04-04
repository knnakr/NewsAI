import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

type BadgeVariant = "default" | "success" | "danger" | "warning" | "info";

type BadgeProps = {
  children: ReactNode;
  variant?: BadgeVariant;
  className?: string;
};

const badgeVariantClasses: Record<BadgeVariant, string> = {
  default: "bg-navy-700 text-slate-200 border border-navy-600",
  success: "bg-verdict-true/20 text-verdict-true border border-verdict-true/50",
  danger: "bg-verdict-false/20 text-verdict-false border border-verdict-false/50",
  warning: "bg-verdict-unverified/20 text-verdict-unverified border border-verdict-unverified/50",
  info: "bg-accent-blue/20 text-accent-blue border border-accent-blue/50",
};

export function Badge({ children, variant = "default", className }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold",
        badgeVariantClasses[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}
