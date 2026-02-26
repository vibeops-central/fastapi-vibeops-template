Feature: User Registration and Login
  As a visitor
  I want to create an account and log in
  So that I can access protected areas of the application

  # ---------------------------------------------------------------------------
  # Registration
  # ---------------------------------------------------------------------------

  Scenario: A new user registers successfully
    Given no account exists for "alice@example.com"
    When a visitor registers with email "alice@example.com" and a valid password
    Then a new account is created
    And the response includes the account email and a unique identifier
    And no password or credential is included in the response

  Scenario: Registration is rejected when the email is already in use
    Given an account already exists for "alice@example.com"
    When a visitor tries to register with email "alice@example.com"
    Then registration is rejected
    And the visitor is told the email address is already taken

  Scenario: Registration is rejected when the email format is invalid
    Given no account exists for "not-an-email"
    When a visitor tries to register with the value "not-an-email" as their email
    Then registration is rejected
    And the visitor is told to provide a valid email address

  Scenario: Registration is rejected when the password is too weak
    Given no account exists for "bob@example.com"
    When a visitor tries to register with email "bob@example.com" and a password that is too short
    Then registration is rejected
    And the visitor is told the password does not meet the requirements

  # ---------------------------------------------------------------------------
  # Login
  # ---------------------------------------------------------------------------

  Scenario: A registered user logs in successfully
    Given an account exists for "alice@example.com" with a known password
    When the user logs in with email "alice@example.com" and the correct password
    Then login succeeds
    And the response contains an access token

  Scenario: Login is rejected when the password is wrong
    Given an account exists for "alice@example.com" with a known password
    When the user tries to log in with email "alice@example.com" and an incorrect password
    Then login is rejected
    And the user receives a generic invalid credentials message

  Scenario: Login is rejected when the email is not registered
    Given no account exists for "ghost@example.com"
    When the user tries to log in with email "ghost@example.com"
    Then login is rejected
    And the user receives a generic invalid credentials message

  Scenario: Login is rejected for an inactive account
    Given an account exists for "suspended@example.com" but the account is inactive
    When the user tries to log in with email "suspended@example.com" and the correct password
    Then login is rejected
    And the user is told the account is not active

  # ---------------------------------------------------------------------------
  # Accessing a protected resource
  # ---------------------------------------------------------------------------

  Scenario: A logged-in user can view their own profile
    Given the user is logged in as "alice@example.com"
    When the user requests their profile
    Then the response contains the account email and identifier
    And no password or credential is included in the response

  Scenario: An unauthenticated request to a protected resource is rejected
    Given the user is not logged in
    When the user attempts to access a protected resource
    Then the request is rejected
    And the user is told authentication is required
