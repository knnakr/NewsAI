import "@testing-library/jest-dom";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import SettingsPage from "@/app/(dashboard)/settings/page";
import { api } from "@/lib/api";

jest.mock("@/lib/api", () => ({
	api: {
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
		(api.patch as jest.Mock).mockReset();
		(api.patch as jest.Mock).mockResolvedValue({ data: {} });
	});

	test("renders language selector", () => {
		render(<SettingsPage />);
		expect(screen.getByLabelText(/language/i)).toBeInTheDocument();
	});

	test("renders AI tone selector", () => {
		render(<SettingsPage />);
		expect(screen.getByLabelText(/ai tone/i)).toBeInTheDocument();
	});

	test("save button calls PATCH preferences API", async () => {
		render(<SettingsPage />);

		fireEvent.click(screen.getByRole("button", { name: /kaydet/i }));

		await waitFor(() => {
			expect(api.patch).toHaveBeenCalledWith("/users/me/preferences", expect.any(Object));
		});
	});
});