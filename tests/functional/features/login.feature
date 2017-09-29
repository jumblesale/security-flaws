Feature: logging in to account

  Background: there is no data in the service
    Given the server is running
      And there are fixtures in the db

  Scenario: a valid user authenticates
    Given I am a client
     When I log in with username "charles" and secret "t dog"
     Then that request is successful (200)


  Scenario: an invalid user authenticates
    Given I am a client
     When I log in with username "charles" and secret "not the correct secret"
     Then that request is unsuccessful (401)
