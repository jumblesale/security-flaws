Feature: managing user notes

  Background: there is no data in the service
    Given the server is running
      And there are fixtures in the db

  Scenario: I send a note
    Given I am user "charles"
      And I send a note "hello!" to user "steve"
      And I send a note "how are you?" to user "steve"
     Then that request is successful (201)
      And user "steve" has 2 notes
      And the first note contains "how are you?"
