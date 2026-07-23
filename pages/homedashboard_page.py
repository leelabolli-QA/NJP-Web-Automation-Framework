"""
Playwright Page Object for the Home Dashboard screens (Home menu + Chatbot flow).

Notes on selectors:
    All locators in home_dashboard_locators.py are raw XPath strings (some wrapped
    in parentheses, e.g. "(//span[text()='Home'])[1]"). Playwright only
    auto-detects XPath when a selector starts with "//" or "..", so anything
    that starts with "(" must be explicitly prefixed with "xpath=". The _xp()
    helper below takes care of that everywhere in this file.
"""

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

from locators.homedashboard_locators import Homedashboardlocators


class HomeDashboardPage:
    def __init__(self, page: Page, default_timeout: int = 20000):
        self.page = page
        self.default_timeout = default_timeout

    # ---------- generic helpers ----------
    @staticmethod
    def _xp(locator: str) -> str:
        return locator if locator.startswith(("//", "..")) else f"xpath={locator}"

    def _click(self, locator: str, timeout: int = None):
        self.page.locator(self._xp(locator)).click(timeout=timeout or self.default_timeout)

    def _fill(self, locator: str, text: str, timeout: int = None):
        loc = self.page.locator(self._xp(locator))
        loc.wait_for(state="visible", timeout=timeout or self.default_timeout)
        loc.fill(text)

    def _locator(self, locator: str):
        return self.page.locator(self._xp(locator))

    # ---------- Home menu navigation ----------
    def click_home_tab(self):
        self._click(Homedashboardlocators.HOME_TAB)

    def click_knowledge_library_tab(self):
        self._click(Homedashboardlocators.KNOWLEDGE_LIBRARY_TAB)

    def click_programs_tab(self):
        self._click(Homedashboardlocators.PROGRAMS_TAB)

    def click_experts_tab(self):
        self._click(Homedashboardlocators.EXPERTS_TAB)

    def click_about_us_tab(self):
        """Clicks About Us. If it opens a new tab/window, that tab is closed
        and control returns to the original (main) browser page/tab."""
        context = self.page.context
        try:
            with context.expect_page(timeout=3000) as new_page_info:
                self._click(Homedashboardlocators.ABOUT_US_TAB)
            new_page = new_page_info.value
            new_page.wait_for_load_state()
            new_page.close()
        except PlaywrightTimeoutError:
            # About Us navigated within the same tab (no popup opened) - nothing to close
            pass
        # ensure focus is back on the main page/tab
        self.page.bring_to_front()

    def click_my_profile(self):
        self._click(Homedashboardlocators.PROFILE_ICON)

    def is_on_home_page(self) -> bool:
        try:
            expect(self._locator(Homedashboardlocators.HOME_TAB)).to_be_visible(timeout=self.default_timeout)
            return True
        except AssertionError:
            return False

    # ---------- Chatbot flow ----------
    def ask_question(self, question_text: str):
        self._fill(Homedashboardlocators.ASK_QUERY_TEXTAREA, question_text)
        self._click(Homedashboardlocators.ARROW_BUTTON)
        # The button briefly enters a "submitted" state while the AI response
        # streams in, then reverts once the answer (with related questions)
        # has fully rendered. Waiting on the transient "submitted" class is a
        # race condition - by the time we check, the response may already be
        # complete and the button already back to normal. Instead, wait for
        # the related-question button, which only appears once the full
        # response (including related questions) has rendered.
        self._locator(Homedashboardlocators.RELATED_QUESTION_BUTTON).wait_for(
            state="visible", timeout=self.default_timeout * 2
        )

    def click_down_arrow_and_first_related_question(self):
        self._click(Homedashboardlocators.DOWN_ARROW_BUTTON)
        self._click(Homedashboardlocators.RELATED_QUESTION_BUTTON)

    def click_thumbs_up(self):
        self._click(Homedashboardlocators.THUMBSUP_BUTTON)

    def click_thumbs_down(self):
        self._click(Homedashboardlocators.THUMBSDOWN_BUTTON)

    def validate_profile_summary_and_request_meeting(self):
        # The expert-profile panel (Profile summary / Request meeting) loads
        # asynchronously and separately from the chat answer, and can take
        # noticeably longer to appear - especially after multiple Q&A round
        # trips have already happened in the same conversation. Waiting only
        # 20s on the button directly was racing against that load, so:
        #   1) if a "Loading profile..." indicator is present, wait for it
        #      to disappear first
        #   2) use a longer timeout for the button itself
        #   3) scroll it into view before asserting/clicking, in case it's
        #      rendered outside the current viewport
        long_timeout = self.default_timeout * 3  # e.g. 60s if default is 20s

        loading_indicator = self.page.get_by_text("Loading profile", exact=False)
        try:
            loading_indicator.first.wait_for(state="visible", timeout=3000)
            loading_indicator.first.wait_for(state="hidden", timeout=long_timeout)
        except PlaywrightTimeoutError:
            # either it never appeared (panel loaded instantly) or it's still
            # showing after the long wait - either way, fall through and let
            # the button-visibility check below give the real failure signal
            pass

        profile_summary = self._locator(Homedashboardlocators.VALIDATE_PROFILE_SUMMARY_BUTTON)
        profile_summary.wait_for(state="visible", timeout=long_timeout)
        profile_summary.scroll_into_view_if_needed()
        expect(profile_summary).to_be_visible()

        self._click(Homedashboardlocators.REQUEST_MEETING_BUTTON, timeout=long_timeout)

    # ---- Date & slot selection with "next available" fallback ----
    def select_date(self):
        """Selects today's date if available/enabled, otherwise picks the next available day."""
        today = self._locator(Homedashboardlocators.SLOT_DATE)
        try:
            today.click(timeout=3000)
            return
        except PlaywrightTimeoutError:
            pass
        # fallback: pick the first non-disabled date available
        self._click(Homedashboardlocators.AVAILABLE_DATE_ANY)

    def select_time_slot(self):
        """Selects the first time slot if available/enabled, otherwise picks the next available slot."""
        first_slot = self._locator(Homedashboardlocators.FIRST_SLOT_BUTTON)
        try:
            first_slot.click(timeout=3000)
            return
        except PlaywrightTimeoutError:
            pass
        self._click(Homedashboardlocators.AVAILABLE_SLOT_ANY)

    def select_date_time_and_proceed(self):
        self.select_date()
        self.select_time_slot()
        proceed_button = self._locator(Homedashboardlocators.CONFIRM_SLOT_AND_PROCEED_BUTTON)
        # The button stays disabled until the app's state has registered
        # both the date and slot selections - clicking as soon as it's
        # merely visible races that state update, so wait for "enabled".
        expect(proceed_button).to_be_enabled(timeout=self.default_timeout * 2)
        proceed_button.click(timeout=self.default_timeout)

    def select_company_stage_pre_revenue(self):
        """Opens the Select company stage dropdown and picks the
        Validation (Pre-revenue, prototype, or MVP stage) option. Waits
        explicitly for the option to render after opening the dropdown,
        since the dropdown can take a moment to open/animate in."""
        dropdown = self._locator(Homedashboardlocators.SELECT_COMPANY_STAGE_DROPDOWN)
        

        dropdown.click(timeout=self.default_timeout)
        option = self._locator(Homedashboardlocators.VALIDATION_PRE_REVENUE_OPTION)
        try:
            option.wait_for(state="visible", timeout=5000)
        except PlaywrightTimeoutError:
            # dropdown may not have opened on the first click (e.g. animation
            # not finished yet) - retry once
            dropdown.click(timeout=self.default_timeout)
            option.wait_for(state="visible", timeout=self.default_timeout)

        option.scroll_into_view_if_needed()
        option.click(timeout=self.default_timeout)

    def fill_required_details_and_send_request(self, description: str, company_url: str, key_decision: str):
        self._fill(Homedashboardlocators.BRIEFLY_DESCRIBE_TEXTAREA, description)
        self._fill(Homedashboardlocators.COMPANY_URL, company_url)
        self.select_company_stage_pre_revenue()
        self._fill(Homedashboardlocators.KEY_DECISION_TEXTAREA, key_decision)
        self._click(Homedashboardlocators.SEND_REQUEST_TO_EXPERT_BUTTON)

    def open_resources_tab_and_first_card(self):
        """Clicks the Resources tab and the first resource card. The card
        is expected to open its content in a new tab/window; if it does,
        the popup page is kept on self.resource_popup so it can be closed
        later via navigate_back_to_main_browser_window()."""
        self._click(Homedashboardlocators.RESOURCES_TAB)
        context = self.page.context
        self.resource_popup = None
        try:
            with context.expect_page(timeout=5000) as new_page_info:
                self._click(Homedashboardlocators.CARD_CONTENT_FIRST)
            self.resource_popup = new_page_info.value
            self.resource_popup.wait_for_load_state()
        except PlaywrightTimeoutError:
            # card opened content within the same tab - nothing to track
            pass
 
    def navigate_back_to_main_browser_window(self) -> bool:
        """Returns to the chat/dashboard view after viewing a resource card.
 
        If the card opened a popup tab, that popup is closed and the main
        page is brought to front. If the card instead navigated within the
        same tab (which turned out to be the actual behavior here), browser
        history is used to go back. Either way, this only returns True once
        the chat input is confirmed visible again - just checking which
        page/tab is "active" isn't a real confirmation that we're back on
        the right view."""
        if getattr(self, "resource_popup", None):
            self.resource_popup.close()
            self.resource_popup = None
            self.page.bring_to_front()
        else:
            # card opened its content in the same tab - navigate back in history
            self.page.go_back()
            self.page.wait_for_load_state()
 
        try:
            self._locator(Homedashboardlocators.ASK_QUERY_TEXTAREA).wait_for(
                state="visible", timeout=self.default_timeout
            )
            return True
        except PlaywrightTimeoutError:
            return False

    def ask_invalid_question_and_thumbs_down(self, invalid_question_text: str):
        self._fill(Homedashboardlocators.ASK_QUERY_TEXTAREA, invalid_question_text)
        self._click(Homedashboardlocators.ARROW_BUTTON)
        self._click(Homedashboardlocators.THUMBSDOWN_BUTTON)

    def click_back_arrow(self):
        self._click(Homedashboardlocators.BACK_BUTTON)

    def validate_speaker_details_and_click_arrow(self):
        expect(self._locator(Homedashboardlocators.VALIDATE_SPEAKER_DETAILS)).to_be_visible(
            timeout=self.default_timeout
        )
        self._click(Homedashboardlocators.SPEAKER_DETAILS_ARROW_BUTTON)

    def open_conversation_toggle_and_select_first_question(self):
        self._click(Homedashboardlocators.CONVERSATION_TOGGLE_BUTTON_OPEN)
        self._click(Homedashboardlocators.CHAT_QUESTION_FIRST)

    def close_all_until_conversation_history_deleted(self):
        """Repeatedly clicks the Close (x) button until no more are present,
        i.e. the conversation history has been fully deleted."""
        close_buttons = self._locator(Homedashboardlocators.CLOSE_BUTTON)
        while close_buttons.count() > 0:
            close_buttons.first.click()
            self.page.wait_for_timeout(500)