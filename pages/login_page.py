from locators.login_locators import Loginlocators


class LoginPage:
    """Page Object Model for the Login (Phone Number + OTP) page."""

    def __init__(self, page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded", timeout=60000)

    def enter_phone_number(self, phone_number: str):
        field = self.page.locator(Loginlocators.PHONE_NUMBER_FIELD)
        field.wait_for(state="visible")
        field.fill(phone_number)

    def check_terms_checkbox(self):
        checkbox = self.page.locator(Loginlocators.CHECKBOX)
        checkbox.wait_for(state="attached")
        if not checkbox.is_checked():
            checkbox.check(force=True)

    def click_send_otp(self):
        self.page.locator(Loginlocators.SEND_OTP_BUTTON).click()

    def enter_otp(self, otp: str):
        inputs = self.page.locator(Loginlocators.OTP_FIELD)
        inputs.first.wait_for(state="visible")
        for index, digit in enumerate(otp):
            inputs.nth(index).fill(digit)

    def click_verify_otp(self):
        self.page.locator(Loginlocators.VERIFY_OTP_BUTTON).click()

    def is_login_successful(self) -> bool:
        """
        Confirms login succeeded by checking that the profile icon
        (shown in the header once logged in) becomes visible.
        """
        profile_icon = self.page.locator(Loginlocators.PROFILE_ICON)
        profile_icon.wait_for(state="visible", timeout=15000)
        return profile_icon.is_visible()

    def click_profile_icon(self):
        self.page.locator(Loginlocators.PROFILE_ICON).click()

    def click_logout(self):
        self.page.locator(Loginlocators.LOGOUT_BUTTON).click()

    def is_logout_successful(self) -> bool:
        """
        Confirms logout succeeded by checking that the phone number
        field (from the login page) becomes visible again.
        """
        phone_field = self.page.locator(Loginlocators.PHONE_NUMBER_FIELD)
        phone_field.wait_for(state="visible", timeout=15000)
        return phone_field.is_visible()