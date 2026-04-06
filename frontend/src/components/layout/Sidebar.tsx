"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import {
	ChevronLeft,
	ChevronRight,
	Bookmark,
	LogOut,
	Menu,
	MessageSquare,
	Newspaper,
	Settings,
	ShieldCheck,
	TrendingUp,
} from "lucide-react";

import { cn } from "@/lib/utils";
import { useLogout } from "@/hooks/useAuth";
import { useAuthStore } from "@/stores/authStore";
import { useUIStore } from "@/stores/uiStore";

const NAV_LINKS = [
	{ label: "Chat", href: "/chat", icon: MessageSquare },
	{ label: "Fact Check", href: "/fact-check", icon: ShieldCheck },
	{ label: "News Feed", href: "/feed", icon: Newspaper },
	{ label: "Trending", href: "/trending", icon: TrendingUp },
];

const CATEGORY_LINKS = [
	{ label: "World", href: "/category/world" },
	{ label: "Economy", href: "/category/economy" },
	{ label: "Sports", href: "/category/sports" },
	{ label: "Technology", href: "/category/technology" },
];

export function Sidebar() {
	const [isMobileOpen, setIsMobileOpen] = useState(false);
	const pathname = usePathname();
	const router = useRouter();
	const sidebarCollapsed = useUIStore((state) => state.sidebarCollapsed);
	const toggleSidebar = useUIStore((state) => state.toggleSidebar);
	const user = useAuthStore((state) => state.user);
	const logout = useLogout();

	const handleLogout = () => {
		logout.mutate(undefined, {
			onSuccess: () => {
				setIsMobileOpen(false);
				router.push("/login");
			},
		});
	};

	const handleMobileToggle = () => {
		setIsMobileOpen((prev) => !prev);
	};

	const closeMobileSidebar = () => {
		setIsMobileOpen(false);
	};

	return (
		<>
			<button
				type="button"
				onClick={handleMobileToggle}
				aria-label="Toggle sidebar"
				className="fixed left-4 top-4 z-40 rounded-lg border border-navy-600 bg-navy-800 p-2 text-slate-200 md:hidden"
			>
				<Menu className="h-5 w-5" />
			</button>

			{isMobileOpen && (
				<button
					type="button"
					onClick={closeMobileSidebar}
					aria-label="Close sidebar overlay"
					className="fixed inset-0 z-30 bg-black/50 md:hidden"
				/>
			)}

			<aside
				className={cn(
					"fixed left-0 top-0 z-40 flex h-screen -translate-x-full flex-col border-r border-navy-600 bg-navy-900 transition-all duration-200 md:sticky md:translate-x-0",
					isMobileOpen && "translate-x-0",
					sidebarCollapsed ? "md:w-20" : "md:w-72",
				)}
			>
				<div className="flex items-center justify-between border-b border-navy-600 px-4 py-4">
					<div className="flex items-center gap-3">
						<div className="rounded-md bg-accent-blue/20 p-2 text-accent-blue">
							<Newspaper className="h-5 w-5" />
						</div>
						{!sidebarCollapsed && <span className="text-lg font-semibold">News AI</span>}
					</div>
					<button
						type="button"
						onClick={toggleSidebar}
						aria-label="Collapse sidebar"
						className="hidden rounded-md p-1.5 text-slate-300 hover:bg-navy-800 md:block"
					>
						{sidebarCollapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
					</button>
				</div>

				<nav className="flex-1 overflow-y-auto p-3">
					<ul className="space-y-1">
						{NAV_LINKS.map((item) => {
							const isActive = pathname === item.href;
							const Icon = item.icon;
							return (
								<li key={item.href}>
									<Link
										href={item.href}
										className={cn(
											"flex items-center gap-3 rounded-md border-l-2 px-3 py-2 text-sm text-slate-200 transition-colors",
											isActive
												? "border-accent-blue bg-navy-600"
												: "border-transparent hover:bg-navy-800",
											sidebarCollapsed && "justify-center px-2",
										)}
										onClick={closeMobileSidebar}
									>
										<Icon className="h-4 w-4 shrink-0" />
										{!sidebarCollapsed && <span>{item.label}</span>}
									</Link>
								</li>
							);
						})}
					</ul>

					{!sidebarCollapsed && (
						<div className="mt-6">
							<p className="px-3 text-xs font-semibold uppercase tracking-wide text-slate-400">Categories</p>
							<ul className="mt-2 space-y-1">
								{CATEGORY_LINKS.map((item) => {
									const isActive = pathname === item.href;
									return (
										<li key={item.href}>
											<Link
												href={item.href}
												className={cn(
													"block rounded-md border-l-2 px-3 py-2 text-sm text-slate-300 transition-colors",
													isActive
														? "border-accent-blue bg-navy-600"
														: "border-transparent hover:bg-navy-800",
												)}
												onClick={closeMobileSidebar}
											>
												{item.label}
											</Link>
										</li>
									);
								})}
							</ul>
						</div>
					)}
				</nav>

				<div className="border-t border-navy-600 p-3">
					{!sidebarCollapsed && (
						<div className="mb-3 flex items-center gap-2 rounded-md bg-navy-800 px-3 py-2 text-sm text-slate-200">
							<Settings className="h-4 w-4 text-slate-400" />
							<span className="truncate">{user?.display_name || "Guest User"}</span>
						</div>
					)}
					<Link
						href="/saved"
						className={cn(
							"mb-2 flex w-full items-center gap-2 rounded-md border-l-2 px-3 py-2 text-sm text-slate-200 transition-colors",
							pathname === "/saved"
								? "border-accent-blue bg-navy-600"
								: "border-transparent hover:bg-navy-800",
							sidebarCollapsed && "justify-center px-2",
						)}
						onClick={closeMobileSidebar}
					>
						<Bookmark className="h-4 w-4" />
						{!sidebarCollapsed && <span>Saved</span>}
					</Link>
					<Link
						href="/settings"
						className={cn(
							"mb-2 flex w-full items-center gap-2 rounded-md border-l-2 px-3 py-2 text-sm text-slate-200 transition-colors",
							pathname === "/settings"
								? "border-accent-blue bg-navy-600"
								: "border-transparent hover:bg-navy-800",
							sidebarCollapsed && "justify-center px-2",
						)}
						onClick={closeMobileSidebar}
					>
						<Settings className="h-4 w-4" />
						{!sidebarCollapsed && <span>Settings</span>}
					</Link>
					<button
						type="button"
						data-testid="logout-button"
						onClick={handleLogout}
						disabled={logout.isPending}
						className={cn(
							"flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-slate-200 hover:bg-navy-800",
							logout.isPending && "cursor-not-allowed opacity-60",
							sidebarCollapsed && "justify-center px-2",
						)}
					>
						<LogOut className="h-4 w-4" />
						{!sidebarCollapsed && <span>Logout</span>}
					</button>
				</div>
			</aside>
		</>
	);
}
