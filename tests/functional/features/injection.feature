Feature: performing sql injection

  Background: there is no data in the service
    Given the server is running
      And there are no existing users

  Scenario: a user deletes all user data
    Given I am a client
      And I register with username "charles" and secret "t dog"
     When I do an injection
     Then user with username "charles" does not exist
