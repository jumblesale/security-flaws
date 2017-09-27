Feature: performing sql injection

  Background: there is no data in the service
    Given the server is running
      And there are no existing users

  Scenario: a user deletes all user data
    Given I am a client
      And I register with username "charles" and secret "t dog"
      And the user "charles" exists
     When I register with username "hacker', 'secret'); delete from users; --" and secret "secret"
     Then the user with username "charles" does not exist
      And the user with username "hacker" does not exist
