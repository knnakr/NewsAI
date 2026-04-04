"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { useAuthStore } from "@/stores/authStore";
import { Spinner } from "@/components/ui/Spinner";

export function AuthGuard({ children }: { children: React.ReactNode }) {
	const router = useRouter();
	const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
	const [isChecking, setIsChecking] = useState(true);

	useEffect(() => {
		const timer = window.setTimeout(() => {
			if (!isAuthenticated()) {
				router.replace("/login");
			}
			setIsChecking(false);
		}, 0);

		return () => {
			window.clearTimeout(timer);
		};
	}, [isAuthenticated, router]);

	if (isChecking) {
		return (
			<div className="flex min-h-screen items-center justify-center bg-navy-900">
				<Spinner />
			</div>
		);
	}

	if (!isAuthenticated()) {
		return null;
	}

	return <>{children}</>;
}
