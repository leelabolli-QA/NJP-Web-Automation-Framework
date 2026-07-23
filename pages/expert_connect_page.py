from playwright.sync_api import Page, expect

from locators.expert_connect_locators import ExpertConnectLocators


class ExpertConnectPage:
    """Page object encapsulating all interactions for the Expert Connect flow."""

    DEFAULT_TIMEOUT = 20000  # milliseconds

    def __init__(self, page: Page):
        self.page = page

    # ---------- generic helpers ----------

    def _xpath(self, locator):
        return f"xpath={locator}"

    def _click(self, locator, index=None):
        loc = self.page.locator(self._xpath(locator))
        if index is not None:
            loc = loc.nth(index)
        loc.scroll_into_view_if_needed(timeout=self.DEFAULT_TIMEOUT)
        loc.click(timeout=self.DEFAULT_TIMEOUT)

    def _fill(self, locator, text):
        loc = self.page.locator(self._xpath(locator))
        loc.scroll_into_view_if_needed(timeout=self.DEFAULT_TIMEOUT)
        loc.fill(text, timeout=self.DEFAULT_TIMEOUT)

    def _scroll_to_bottom(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.page.wait_for_timeout(500)

    def _scroll_page_by(self, pixels=600):
        self.page.evaluate(f"window.scrollBy(0, {pixels})")
        self.page.wait_for_timeout(300)

    # ---------- flow steps ----------

    def click_experts_tab(self):
        self._click(ExpertConnectLocators.EXPERT_CONNECT_TAB)

    def search_expert_by_name(self, expert_name):
        self._click(ExpertConnectLocators.SEARCH_ICON)
        self._fill(ExpertConnectLocators.SEARCH_EXPERTS_BY_NAME_INPUT, expert_name)
        self._click(ExpertConnectLocators.SEARCH_BUTTON)

    def select_industry_filter(self):
        self._click(ExpertConnectLocators.INDUSTRY_DROPDOWN)
        self._click(ExpertConnectLocators.SOFTWARE_AND_IT_SERVICES_OPTION)

    def select_skills_filter(self):
        self._click(ExpertConnectLocators.SKILLS_DROPDOWN)
        self._click(ExpertConnectLocators.RESEARCH_AND_DEVELOPMENT_OPTION)

    def select_location_filter(self):
        # Mapped to Language dropdown/option per available locators.
        self._click(ExpertConnectLocators.LANGUAGE_DROPDOWN)
        self._click(ExpertConnectLocators.ENGLISH_OPTION)

    def validate_profile_summary(self):
        # Scroll required to bring the expert card / profile summary button into view.
        self._scroll_page_by(600)
        self._click(ExpertConnectLocators.PROFILE_SUMMARY_BUTTON)
        summary_element = self.page.locator(
            self._xpath(ExpertConnectLocators.PROFILE_SUMMARY_BUTTON)
        )
        expect(summary_element).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

    def click_request_meeting_button(self):
        # Scroll required before the Request a meeting button is interactable.
        self._scroll_page_by(600)
        self._click(ExpertConnectLocators.REQUEST_A_MEETING_BUTTON)

    def select_date_time_slot_and_proceed(self):
        try:
            self._click(ExpertConnectLocators.AVAILABLE_DATE_ANY)
        except Exception:
            self._click(ExpertConnectLocators.SLOT_DATE)

        try:
            self._click(ExpertConnectLocators.AVAILABLE_SLOT_ANY)
        except Exception:
            self._click(ExpertConnectLocators.SLOT_BUTTON)

        self._click(ExpertConnectLocators.CONFIRM_SLOT_AND_PROCEED_BUTTON)

    def fill_required_details_and_send_request(
        self,
        description="We are a growing SaaS company solving workflow automation "
        "problems for mid-sized enterprises. We need expert guidance to refine "
        "our go-to-market strategy.",
        company_url="www.ithelo.com/home",
        key_decision="I need advice on refining my pricing strategy to improve "
        "conversions.",
    ):
        self._fill(ExpertConnectLocators.BRIEFLY_DESCRIBE_TEXTAREA, description)
        self._fill(ExpertConnectLocators.COMPANY_URL, company_url)

        self._click(ExpertConnectLocators.SELECT_COMPANY_STAGE_DROPDOWN)
        self._click(ExpertConnectLocators.VALIDATION_PRE_REVENUE_OPTION)

        self._fill(ExpertConnectLocators.KEY_DECISION_TEXTAREA, key_decision)

        self._click(ExpertConnectLocators.SEND_REQUEST_TO_EXPERT_BUTTON)

    def click_load_more_experts_button(self):
        # Scroll required to bring the Load more experts button into view.
        self._scroll_to_bottom()
        self._click(ExpertConnectLocators.LOAD_MORE_EXPERTS_BUTTON)

    def is_on_home_page(self):
        element = self.page.locator(self._xpath(ExpertConnectLocators.EXPERT_CONNECT_TAB))
        expect(element).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        return element.is_visible()