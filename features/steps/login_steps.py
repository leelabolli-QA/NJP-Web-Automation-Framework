from behave import given, when, then

from config import env_config
from pages.login_page import LoginPage


@given("User is on the login page")
def step_open_login_page(context):
    context.login_page = LoginPage(context.page)
    context.login_page.goto(env_config.BASE_URL)


@when("User enters valid phone number, checks the terms checkbox, and clicks on send OTP button")
def step_enter_phone_and_send_otp(context):
    context.login_page.enter_phone_number(env_config.PHONE_NUMBER)
    context.login_page.check_terms_checkbox()
    context.login_page.click_send_otp()


@when("User enters valid OTP and clicks on verify OTP button")
def step_enter_otp_and_verify(context):
    context.login_page.enter_otp(env_config.OTP)
    context.login_page.click_verify_otp()


@then("User should be logged in successfully")
def step_verify_login_success(context):
    assert context.login_page.is_login_successful(), "Login was not successful"


@when("User clicks on profile icon and clicks on logout button")
def step_click_profile_and_logout(context):
    context.login_page.click_profile_icon()
    context.login_page.click_logout()


@then("User should be logged out successfully")
def step_verify_logout_success(context):
    assert context.login_page.is_logout_successful(), "Logout was not successful"