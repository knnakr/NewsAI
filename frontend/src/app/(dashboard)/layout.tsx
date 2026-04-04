import { AuthGuard } from "@/components/layout/AuthGuard";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopBar } from "@/components/layout/TopBar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
	return (
		<AuthGuard>
			<div className="flex h-screen bg-navy-900">
				<Sidebar />
				<main className="flex-1 overflow-auto">
					<TopBar />
					{children}
				</main>
			</div>
		</AuthGuard>
	);
}
