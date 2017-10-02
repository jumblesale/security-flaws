Feature: getting a list of users

  Background: there are existing users
    Given the server is running
      And there are fixtures in the db

  Scenario: I get a list of users
    Given I am a client
     When I request a list of users
     Then that request is successful (200)
     Then I get 2 users
