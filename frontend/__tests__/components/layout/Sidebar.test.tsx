import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

import { Sidebar } from "@/components/layout/Sidebar";

jest.mock("@/hooks/useAuth", () => ({
	useLogout: () => ({
		mutate: jest.fn(),
		isPending: false,
		isSuccess: false,
	}),
}));

jest.mock("next/navigation", () => ({
	usePathname: () => "/chat",
	useRouter: () => ({ push: jest.fn() }),
}));

describe("Sidebar", () => {
	test("renders News AI logo", () => {
		render(<Sidebar />);
		expect(screen.getByText(/News AI/i)).toBeInTheDocument();
	});

	test("renders all navigation links", () => {
		render(<Sidebar />);
		expect(screen.getByText(/Chat/i)).toBeInTheDocument();
		expect(screen.getByText(/Fact Check/i)).toBeInTheDocument();
		expect(screen.getByText(/News Feed/i)).toBeInTheDocument();
		expect(screen.getByText(/Trending/i)).toBeInTheDocument();
	});

	test("renders category links", () => {
		render(<Sidebar />);
		expect(screen.getByText(/World/i)).toBeInTheDocument();
		expect(screen.getByText(/Technology/i)).toBeInTheDocument();
		expect(screen.getByText(/Sports/i)).toBeInTheDocument();
	});

	test("active link has highlight class", () => {
		render(<Sidebar />);
		const chatLink = screen.getByText(/Chat/i).closest("a");
		expect(chatLink).toHaveClass("bg-navy-600");
	});
});
