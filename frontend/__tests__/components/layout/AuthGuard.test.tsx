import "@testing-library/jest-dom";
import { render, screen, waitFor } from "@testing-library/react";

import { AuthGuard } from "@/components/layout/AuthGuard";
import { useAuthStore } from "@/stores/authStore";

const mockReplace = jest.fn();

jest.mock("next/navigation", () => ({
	useRouter: () => ({ replace: mockReplace }),
}));

jest.mock("@/stores/authStore", () => ({
	useAuthStore: jest.fn(),
}));

const mockUseAuthStore = useAuthStore as unknown as jest.Mock;

describe("AuthGuard", () => {
	beforeEach(() => {
		jest.clearAllMocks();
	});

	test("redirects to login when not authenticated", async () => {
		mockUseAuthStore.mockImplementation((selector) =>
			selector({
				isAuthenticated: () => false,
			}),
		);

		render(
			<AuthGuard>
				<div>Protected</div>
			</AuthGuard>,
		);

		await waitFor(() => {
			expect(mockReplace).toHaveBeenCalledWith("/login");
		});
	});

	test("renders children when authenticated", async () => {
		mockUseAuthStore.mockImplementation((selector) =>
			selector({
				isAuthenticated: () => true,
			}),
		);

		render(
			<AuthGuard>
				<div>Protected Content</div>
			</AuthGuard>,
		);

		await waitFor(() => {
			expect(screen.getByText("Protected Content")).toBeInTheDocument();
		});
		expect(mockReplace).not.toHaveBeenCalled();
	});

	test("shows spinner while checking auth", () => {
		mockUseAuthStore.mockImplementation((selector) =>
			selector({
				isAuthenticated: () => true,
			}),
		);

		render(
			<AuthGuard>
				<div>Content</div>
			</AuthGuard>,
		);

		expect(screen.getByRole("status")).toBeInTheDocument();
	});
});