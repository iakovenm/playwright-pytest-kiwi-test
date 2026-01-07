pytest_bdd_features_path = "tests/features"

import pytest
import allure
from playwright.sync_api import Page
from config import config


# Store page reference for screenshot capture
_test_failed_page = None


@pytest.fixture(scope="function")
def page(page: Page):
    """Override page fixture to store reference for screenshot capture."""
    global _test_failed_page
    _test_failed_page = page
    yield page
    _test_failed_page = None


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Configure browser launch arguments from environment variables.

    Note: Do not depend on the base fixture of the same name to avoid recursion issues
    when plugin versions differ. Return a standalone mapping.
    """
    launch_args = {
        "headless": config.HEADLESS,
        # Additional args to avoid bot detection
        "args": [
            "--disable-blink-features=AutomationControlled",  # Hide automation
            "--disable-dev-shm-usage",  # Avoid small /dev/shm in containers causing renderer crashes/hangs
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-background-networking",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-breakpad",
            "--disable-client-side-phishing-detection",
            "--disable-default-apps",
            "--disable-extensions",
            "--disable-features=IsolateOrigins,site-per-process,Translate,AudioServiceOutOfProcess",
            "--disable-hang-monitor",
            "--disable-ipc-flooding-protection",
            "--disable-popup-blocking",
            "--disable-prompt-on-repost",
            "--disable-renderer-backgrounding",
            "--force-color-profile=srgb",
            "--metrics-recording-only",
            "--no-sandbox",  # Playwright image supports sandbox, but this improves compatibility on some hosts
            "--password-store=basic",
            "--use-mock-keychain",
        ],
        # A small slow_mo can help with flakiness against heavily dynamic UIs
        "slow_mo": 25,
    }
    return launch_args


@pytest.fixture(scope="session")
def browser_context_args():
    """Configure browser context to appear more like a real user. To avoid bot detection that blocks headless browsers.
    Return a standalone mapping rather than merging with a base fixture to avoid None merges.
    """
    return {
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "locale": "en-US",
        "timezone_id": "America/New_York",
        # Subtle realism tweaks
        "has_touch": False,
        "is_mobile": False,
        "device_scale_factor": 1.0,
        "bypass_csp": True,
        "java_script_enabled": True,
        "extra_http_headers": {
            "Accept-Language": "en-US,en;q=0.9",
        },
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item, call
):  # noqa: ARG001 - item and call required by pytest hook spec
    """
    Hook to capture screenshot on test failure and attach to Allure report.

    This hook runs after each test phase (setup, call, teardown) and captures
    a screenshot if the test failed, attaching it to the Allure report.

    Args:
        item: Test item (required by pytest hook spec, not used directly)
        call: Call info (required by pytest hook spec, not used directly)
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # Only capture screenshot on failure during the 'call' phase
    if report.when == "call" and report.failed:
        global _test_failed_page

        # Try to get page from the stored reference
        page = _test_failed_page

        if page:
            try:
                # Capture screenshot as bytes
                screenshot_bytes = page.screenshot(full_page=True)

                # Attach to Allure report
                allure.attach(
                    screenshot_bytes,
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )

                print("\n✓ Screenshot captured and attached to Allure report")
            except Exception as e:
                print(f"\n✗ Failed to capture screenshot: {e}")
        else:
            print("\n✗ Page object not available for screenshot capture")
