from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_analyst_creates_and_submits_record(page: Page, live_server_url: str):
    # This broad test proves the layers are wired together. Detailed business
    # and security rules stay in faster API/unit tests for clearer diagnosis.
    page.goto(live_server_url)
    page.get_by_role("button", name="Sign in").click()
    expect(page.get_by_text("Analyst One — analyst")).to_be_visible()

    page.get_by_label("Title").fill("Browser release readiness")
    page.get_by_label("Description").fill("End-to-end user workflow with evidence.")
    page.get_by_label("Risk score").fill("72")
    page.get_by_role("button", name="Create record").click()

    expect(page.get_by_text("Created record")).to_be_visible()
    row = page.get_by_role("row").filter(has_text="Browser release readiness")
    expect(row).to_contain_text("HIGH")
    expect(row).to_contain_text("DRAFT")

    row.get_by_role("button", name="Submit").click()
    expect(page.get_by_text("is now SUBMITTED")).to_be_visible()
    expect(page.get_by_role("row").filter(has_text="Browser release readiness")).to_contain_text("SUBMITTED")
