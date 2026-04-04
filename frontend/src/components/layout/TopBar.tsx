"use client";

import { Bell, Search } from "lucide-react";
import { usePathname } from "next/navigation";

const TITLE_MAP: Record<string, string> = {
  "/chat": "Chat",
  "/fact-check": "Fact Check",
  "/feed": "News Feed",
  "/trending": "Trending",
};

function resolveTitle(pathname: string) {
  if (TITLE_MAP[pathname]) {
    return TITLE_MAP[pathname];
  }

  if (pathname.startsWith("/category/")) {
    const category = pathname.replace("/category/", "");
    return category.charAt(0).toUpperCase() + category.slice(1);
  }

  return "Dashboard";
}

export function TopBar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-navy-600 bg-navy-900/95 px-4 backdrop-blur md:px-6">
      <h1 className="text-lg font-semibold text-slate-100">{resolveTitle(pathname)}</h1>
      <div className="flex items-center gap-2">
        <button
          type="button"
          aria-label="Search"
          className="rounded-md p-2 text-slate-300 transition-colors hover:bg-navy-800"
        >
          <Search className="h-5 w-5" />
        </button>
        <button
          type="button"
          aria-label="Notifications"
          className="rounded-md p-2 text-slate-300 transition-colors hover:bg-navy-800"
        >
          <Bell className="h-5 w-5" />
        </button>
      </div>
    </header>
  );
}
