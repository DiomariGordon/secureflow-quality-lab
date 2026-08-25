from __future__ import annotations

import os
import shutil

import pytest
from playwright.sync_api import Browser, Page, sync_playwright


@pytest.fixture(scope="session")
def browser() -> Browser:
    with sync_playwright() as playwright:
        launch_options: dict[str, object] = {"headless": True}
        explicit_executable = os.getenv("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
        system_chromium = shutil.which("chromium") or shutil.which("chromium-browser")
        if explicit_executable:
            launch_options["executable_path"] = explicit_executable
        elif system_chromium:
            launch_options["executable_path"] = system_chromium
        browser = playwright.chromium.launch(**launch_options)
        yield browser
        browser.close()


@pytest.fixture()
def page(browser: Browser) -> Page:
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
