import { cn } from "@/lib/utils";

type SpinnerProps = {
  className?: string;
};

export function Spinner({ className }: SpinnerProps) {
  return (
    <span
      role="status"
      aria-live="polite"
      className={cn(
        "inline-block h-4 w-4 animate-spin rounded-full border-2 border-slate-400 border-t-accent-blue",
        className,
      )}
    />
  );
}
