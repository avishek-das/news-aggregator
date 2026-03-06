import { render, screen } from "@testing-library/react";
import Page from "../app/page";

// TDD RED: this test fails until app/page.tsx renders "AI News Aggregator"
describe("Home page", () => {
  it("renders the app heading", () => {
    render(<Page />);
    expect(screen.getByText(/AI News Aggregator/i)).toBeInTheDocument();
  });
});
