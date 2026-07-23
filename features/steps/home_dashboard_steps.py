from behave import given, when, then
from pages.homedashboard_page import HomeDashboardPage


# ---------------- Scenario: Home menu headers validation ----------------

@given('User is on the Home page')
def step_given_user_on_home_page(context):
    context.home_page = HomeDashboardPage(context.page)
    assert context.home_page.is_on_home_page(), "User is not on the Home page"


@when('User clicks on Home button')
def step_when_click_home_button(context):
    context.home_page.click_home_tab()


@when('User clicks on Knowledge Library')
def step_when_click_knowledge_library(context):
    context.home_page.click_knowledge_library_tab()


@when('User clicks on Programs')
def step_when_click_programs(context):
    context.home_page.click_programs_tab()


@when('User clicks on Experts')
def step_when_click_experts(context):
    context.home_page.click_experts_tab()


@when('User clicks on About Us')
def step_when_click_about_us(context):
    # Handles popup tab internally: closes it and returns focus to the main page.
    context.home_page.click_about_us_tab()


@when('User clicks on My Profile')
def step_when_click_my_profile(context):
    context.home_page.click_my_profile()


@then('User is navigated to the Home page')
def step_then_user_on_home_page(context):
    assert context.home_page.is_on_home_page(), "User was not navigated back to the Home page"


# ---------------- Scenario: Chatbot validation ----------------

@when('User enters the question and clicks on the Send button')
def step_when_ask_question(context):
    context.home_page = getattr(context, "home_page", HomeDashboardPage(context.page))
    context.home_page.ask_question("How to start a business")


@when('user clicks on the down arrow button and clicks on the first related question')
def step_when_click_down_arrow_and_first_related_question(context):
    context.home_page.click_down_arrow_and_first_related_question()


@when('User clicks on the Thumbs Up button')
def step_when_click_thumbs_up(context):
    context.home_page.click_thumbs_up()


@then('User validates the profile summary and clicks on the Request Meeting button')
def step_then_validate_profile_summary_request_meeting(context):
    context.home_page.validate_profile_summary_and_request_meeting()


@when('User selects the date, time slot, and clicks on the Proceed button')
def step_when_select_date_time_proceed(context):
    # Handles fallback internally: if today's date/first slot is unavailable,
    # the next available day/slot is selected automatically.
    context.home_page.select_date_time_and_proceed()


@when('User fills all the required details and clicks on the Send Request to Expert button')
def step_when_fill_details_and_send_request(context):
    context.home_page.fill_required_details_and_send_request(
        description=(
            "We are building an AI-powered analytics platform for small businesses, "
            "targeting retail owners with real-time sales insights and inventory forecasting."
        ),
        company_url="www.ithelo.com/home",
        key_decision="I need advice on refining my pricing strategy to improve conversions.",
    )


@when('User clicks on the Resources tab and clicks on the first resource card')
def step_when_open_resources_first_card(context):
    context.home_page.open_resources_tab_and_first_card()


@then('user should be navigated to the main browser window')
def step_then_navigated_to_main_browser_window(context):
    assert context.home_page.navigate_back_to_main_browser_window(), (
        "User was not navigated back to the main browser window"
    )

@when('User enters an invalid question and clicks on the Thumbs Down button')
def step_when_invalid_question_thumbs_down(context):
    context.home_page.ask_invalid_question_and_thumbs_down("asdkjaskjd 12312 !!! random gibberish text")

@when('User clicks on the Back Arrow button')
def step_when_click_back_arrow(context):
    context.home_page.click_back_arrow()


@then('User validates the Speaker Details card and clicks on the Speaker Details arrow button')
def step_then_validate_speaker_details(context):
    context.home_page.validate_speaker_details_and_click_arrow()


@when('User clicks on the Conversation toggle button and selects the first question')
def step_when_conversation_toggle_select_question(context):
    context.home_page.open_conversation_toggle_and_select_first_question()


@then('User clicks on all the Close buttons until the conversation history is deleted')
def step_then_close_all_until_deleted(context):
    context.home_page.close_all_until_conversation_history_deleted()