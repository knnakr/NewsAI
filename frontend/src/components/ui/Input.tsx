import type { InputHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  error?: string;
};

export function Input({ label, error, id, className, ...props }: InputProps) {
  const inputId = id ?? props.name;

  return (
    <div className="w-full space-y-1.5">
      {label ? (
        <label htmlFor={inputId} className="text-sm font-medium text-slate-200">
          {label}
        </label>
      ) : null}
      <input
        id={inputId}
        aria-invalid={!!error}
        className={cn(
          "w-full rounded-lg border bg-navy-800 px-3 py-2 text-slate-100 outline-none placeholder:text-slate-400 focus:ring-2 focus:ring-accent-blue",
          error ? "border-red-500" : "border-navy-600",
          className,
        )}
        {...props}
      />
      {error ? <p className="text-xs text-red-400">{error}</p> : null}
    </div>
  );
}
