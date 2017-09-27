Feature: registering new users

  Background: there is no data in the service
    Given the server is running
      And there are no existing users

  Scenario: a valid user registers
    Given I am a client
     When I register with username "charles" and secret "t dog"
     Then the user "charles" exists
