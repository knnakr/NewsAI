import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Skeleton } from "@/components/ui/Skeleton";
import { Spinner } from "@/components/ui/Spinner";

describe("UI primitives", () => {
	test("Input renders label and error state", () => {
		render(<Input id="email" label="Email" error="Required" />);

		expect(screen.getByLabelText("Email")).toBeInTheDocument();
		expect(screen.getByText("Required")).toBeInTheDocument();
		expect(screen.getByLabelText("Email")).toHaveAttribute("aria-invalid", "true");
	});

	test("Badge success variant renders", () => {
		render(<Badge variant="success">Verified</Badge>);
		expect(screen.getByText("Verified")).toBeInTheDocument();
	});

	test("Card wraps content", () => {
		render(
			<Card>
				<div>Card content</div>
			</Card>,
		);
		expect(screen.getByText("Card content")).toBeInTheDocument();
	});

	test("Spinner has status role", () => {
		render(<Spinner />);
		expect(screen.getByRole("status")).toBeInTheDocument();
	});

	test("Skeleton is hidden from assistive tech", () => {
		render(<Skeleton />);
		expect(screen.getByTestId("skeleton")).toHaveAttribute("aria-hidden", "true");
	});
});
