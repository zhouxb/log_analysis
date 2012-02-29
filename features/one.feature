Feature: Compute The Size of A File
    Get the size of a file

  Scenario: get the size of an empty file
    Given I have a filename empty.log
    #When I Compute its size
    Then I see the number 0

  Scenario: get the size of non-empty file
    Given I have a filename tmp.log
    When I write 100 bytes chars into the file, and compute its size
    Then I see the number 100
