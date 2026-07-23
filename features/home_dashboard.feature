Feature: Home Dashboard
  Scenario: Home menu headers validation
    Given User is on the Home page
    When User clicks on Home button
    When User clicks on Knowledge Library
    When User clicks on Programs
    When User clicks on Experts
    When User clicks on About Us
    When User clicks on My Profile
    Then User is navigated to the Home page

Scenario: Chatbot validation
    Given User is on the Home page
    When User enters the question and clicks on the Send button
    When user clicks on the down arrow button and clicks on the first related question
    When User clicks on the Thumbs Up button
    Then User validates the profile summary and clicks on the Request Meeting button
    When User selects the date, time slot, and clicks on the Proceed button
    When User fills all the required details and clicks on the Send Request to Expert button
    When User clicks on the Resources tab and clicks on the first resource card
    Then user should be navigated to the main browser window
    When User enters an invalid question and clicks on the Thumbs Down button
    When User clicks on the Back Arrow button
    Then User validates the Speaker Details card and clicks on the Speaker Details arrow button
    When User clicks on the Conversation toggle button and selects the first question
    Then User clicks on all the Close buttons until the conversation history is deleted

  # Scenario: Experts validation
  #   Given User is on the Home page
  #   When User clicks on the Experts button
  #   Then User clicks on the search icon, enters the expert name, and clicks on the Search button
  #   Then User clicks on the Industry filter and selects an industry
  #   Then User clicks on the Skills filter and selects a skill
  #   Then User clicks on the Location filter and selects a location
  #   Then User validates the Profile Summary
  #   Then User clicks on the Request Meeting button
  #   Then User selects the date and time slot and clicks on the Proceed button
  #   Then User fills in the required details and clicks on the Send Request to Expert button
  #   Then User clicks on the Load More Experts button
  #   Then User is navigated to the Home page

  Scenario: Our Programs validation
    Given User is on the Home page
    When User clicks on the Our Programs button
    Then User clicks on the search icon, enters the program name, and clicks on the Search button
    Then User clicks on the Industry filter and selects an industry
    Then User clicks on the Skills filter and selects a skill
    Then User clicks on the Location filter and selects a location
    Then User validates the Program Summary
    Then User clicks on the Request Meeting button
    Then User selects the date and time slot and clicks on the Proceed button
    Then User fills in the required details and clicks on the Send Request to Expert button
    Then User clicks on the Load More Programs button
    Then User is navigated to the Home page
