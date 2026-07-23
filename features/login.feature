Feature: Login Functionality

  Scenario: User should be able to login with valid credentials
    Given User is on the login page
    When User enters valid phone number, checks the terms checkbox, and clicks on send OTP button
    And User enters valid OTP and clicks on verify OTP button
    Then User should be logged in successfully
    When User clicks on profile icon and clicks on logout button
    Then User should be logged out successfully