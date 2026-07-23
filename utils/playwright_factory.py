from playwright.sync_api import sync_playwright
from config.env_config import HEADLESS


class PlaywrightFactory:

    def start(self):
        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(
            headless=HEADLESS,
            slow_mo=500,  # ms delay between actions so you can watch execution; lower/remove later
            args=[
                "--start-maximized",
                "--force-device-scale-factor=1",
                "--high-dpi-support=1",
                "--use-fake-ui-for-media-stream",
                "--use-fake-device-for-media-stream"
            ]
        )

        context = browser.new_context(
            permissions=[],
            no_viewport=True
        )

        page = context.new_page()

        # Optional: Set a default timeout for all actions
        page.set_default_timeout(30000)

        return playwright, browser, context, page