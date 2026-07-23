"""
environment.py

Behave hooks that start/stop Playwright around the whole test run, and
open/close a fresh browser context+page around every scenario. Each
scenario starts already logged in (phone number + OTP) and landed on
the Home page, so feature files don't need explicit login steps.

Install:
    pip install playwright behave
    playwright install

Run:
    behave

Credentials/URL come from Config (utils/config.py), which reads ENV,
PHONE_NUMBER, and OTP from environment variables (with dev defaults).
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from pages.expert_connect_page import ExpertConnectPage

from utils.config import Config
from pages.login_page import LoginPage

HEADLESS = False  # set True to run without a visible browser window
LOGIN_RETRY_ATTEMPTS = 2  # first page load can be slow/flaky; retry once before failing


def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=HEADLESS)


def _navigate_and_start_login(login_page, context):
    # goto() may navigate using its own internal URL config, or may accept
    # a URL argument - handle both without guessing wrong.
    try:
        login_page.goto(Config.BASE_URL)
    except TypeError:
        login_page.goto()

    # Ensure the SPA has actually finished loading before looking for the
    # phone number field - a bare goto() can return before rendering
    # completes, which is what caused the first-run timeout.
    context.page.wait_for_load_state("networkidle")

    login_page.enter_phone_number(Config.PHONE_NUMBER)


def before_scenario(context, scenario):
    context.browser_context = context.browser.new_context()
    context.page = context.browser_context.new_page()

    login_page = LoginPage(context.page)

    last_error = None
    for attempt in range(1, LOGIN_RETRY_ATTEMPTS + 1):
        try:
            _navigate_and_start_login(login_page, context)
            break
        except PlaywrightTimeoutError as err:
            last_error = err
            print(f"[before_scenario] login attempt {attempt} failed, retrying: {err}")
    else:
        raise last_error

    login_page.check_terms_checkbox()
    login_page.click_send_otp()
    login_page.enter_otp(Config.OTP)
    login_page.click_verify_otp()

    assert login_page.is_login_successful(), "Login failed in before_scenario hook"


def after_scenario(context, scenario):
    context.browser_context.close()


def after_all(context):
    context.browser.close()
    context.playwright.stop()