import "@testing-library/jest-dom";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import SettingsPage from "@/app/(dashboard)/settings/page";
import { api } from "@/lib/api";

jest.mock("@/lib/api", () => ({
	api: {
		get: jest.fn(),
		patch: jest.fn(),
	},
}));

jest.mock("sonner", () => ({
	toast: {
		success: jest.fn(),
		error: jest.fn(),
	},
}));

describe("PreferencesForm", () => {
	beforeEach(() => {
		(api.get as jest.Mock).mockReset();
		(api.patch as jest.Mock).mockReset();
		(api.get as jest.Mock).mockResolvedValue({
			data: {
				language: "Turkish",
				ai_tone: "neutral",
				orchestrator: "crewai",
				news_categories: ["world"],
				email_digest: false,
			},
		});
		(api.patch as jest.Mock).mockResolvedValue({ data: {} });
	});

	test("renders language selector", async () => {
		render(<SettingsPage />);
		await waitFor(() => {
			expect(api.get).toHaveBeenCalledWith("/users/me/preferences");
		});
		expect(screen.getByLabelText(/language/i)).toBeInTheDocument();
	});

	test("renders AI tone selector", async () => {
		render(<SettingsPage />);
		await waitFor(() => {
			expect(api.get).toHaveBeenCalledWith("/users/me/preferences");
		});
		expect(screen.getByLabelText(/ai tone/i)).toBeInTheDocument();
	});

	test("renders orchestrator selector", async () => {
		render(<SettingsPage />);
		await waitFor(() => {
			expect(api.get).toHaveBeenCalledWith("/users/me/preferences");
		});
		expect(screen.getByLabelText(/ai orchestrator/i)).toBeInTheDocument();
	});

	test("save button calls PATCH preferences API", async () => {
		render(<SettingsPage />);

		await waitFor(() => {
			expect(api.get).toHaveBeenCalledWith("/users/me/preferences");
		});

		fireEvent.click(screen.getByRole("button", { name: /kaydet/i }));

		await waitFor(() => {
			expect(api.patch).toHaveBeenCalledWith("/users/me/preferences", expect.any(Object));
		});
	});

	test("sends orchestrator and normalized preference payload", async () => {
		render(<SettingsPage />);

		await waitFor(() => {
			expect(api.get).toHaveBeenCalledWith("/users/me/preferences");
		});

		fireEvent.change(screen.getByLabelText(/language/i), { target: { value: "English" } });
		fireEvent.change(screen.getByLabelText(/ai tone/i), { target: { value: "Formal" } });
		fireEvent.change(screen.getByLabelText(/ai orchestrator/i), { target: { value: "langgraph" } });
		fireEvent.click(screen.getByRole("button", { name: /kaydet/i }));

		await waitFor(() => {
			expect(api.patch).toHaveBeenCalledWith("/users/me/preferences", {
				news_categories: ["world"],
				language: "English",
				ai_tone: "formal",
				orchestrator: "langgraph",
				email_digest: false,
			});
		});
	});
});