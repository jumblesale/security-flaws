Feature: registering new users

  Background: there is no data in the service
    Given the server is running
      And there are no existing users

  Scenario: a valid user registers
    Given I am a client
     When I register with username "charles" and secret "t dog"
     Then the user "charles" exists

  Scenario: a user with an invalid secret registers
    Given I am a client
     When I register with username "charles" and secret "T dog"
     Then I get a "400" response
      And the user with username "charles" does not exist

  Scenario: a user with a conflicting username registers
    Given I am a client
      And I register with username "charles" and secret "t dog"
      And I get a "201" response
     When I register with username "charles" and secret "t dog"
     Then I get a "400" response
