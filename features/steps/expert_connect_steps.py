from behave import when, then

EXPERT_NAME_TO_SEARCH = "Radha"

@when("User clicks on the Experts button")
def step_click_experts_button(context):
    context.expert_connect_page.click_experts_tab()


@then("User clicks on the search icon, enters the expert name, and clicks on the Search button")
def step_search_expert_by_name(context):
    context.expert_connect_page.search_expert_by_name(EXPERT_NAME_TO_SEARCH)


@then("User clicks on the Industry filter and selects an industry")
def step_select_industry_filter(context):
    context.expert_connect_page.select_industry_filter()


@then("User clicks on the Skills filter and selects a skill")
def step_select_skills_filter(context):
    context.expert_connect_page.select_skills_filter()


@then("User clicks on the Location filter and selects a location")
def step_select_location_filter(context):
    context.expert_connect_page.select_location_filter()


@then("User validates the Profile Summary")
def step_validate_profile_summary(context):
    context.expert_connect_page.validate_profile_summary()


@then("User clicks on the Request Meeting button")
def step_click_request_meeting_button(context):
    context.expert_connect_page.click_request_meeting_button()


@then("User selects the date and time slot and clicks on the Proceed button")
def step_select_date_time_slot_and_proceed(context):
    context.expert_connect_page.select_date_time_slot_and_proceed()


@then("User fills in the required details and clicks on the Send Request to Expert button")
def step_fill_details_and_send_request(context):
    context.expert_connect_page.fill_required_details_and_send_request()


@then("User clicks on the Load More Experts button")
def step_click_load_more_experts_button(context):
    context.expert_connect_page.click_load_more_experts_button()

# NOTE: The "Then User is navigated to the Home page" step is also
# intentionally NOT redefined here — it's already defined in
# features/steps/home_dashboard_steps.py and reused as-is (same reasoning
# as the Given step at the top of this file: step text is global across
# all files under features/steps/).