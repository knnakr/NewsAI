import "@testing-library/jest-dom";
import { fireEvent, render, screen } from "@testing-library/react";

import { Button } from "@/components/ui/Button";

describe("Button", () => {
	test("renders with label", () => {
		render(<Button>Click me</Button>);
		expect(screen.getByText("Click me")).toBeInTheDocument();
	});

	test("calls onClick when clicked", () => {
		const handleClick = jest.fn();
		render(<Button onClick={handleClick}>Click</Button>);
		fireEvent.click(screen.getByText("Click"));
		expect(handleClick).toHaveBeenCalledTimes(1);
	});

	test("disabled button does not call onClick", () => {
		const handleClick = jest.fn();
		render(
			<Button disabled onClick={handleClick}>
				Disabled
			</Button>,
		);
		fireEvent.click(screen.getByText("Disabled"));
		expect(handleClick).not.toHaveBeenCalled();
	});

	test("shows spinner when loading", () => {
		render(<Button loading>Loading</Button>);
		expect(screen.getByRole("status")).toBeInTheDocument();
		expect(screen.getByRole("button")).toHaveAttribute("aria-busy", "true");
	});

	test("danger variant has red styling", () => {
		render(<Button variant="danger">Delete</Button>);
		const btn = screen.getByText("Delete").closest("button");
		expect(btn?.className).toMatch(/red|danger/);
	});
});
