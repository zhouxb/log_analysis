Feature: Seek Newline
    Get the position of newline char in a text file, if the function doesn't find a newline , just return -1
  Scenario: seek newlines in an empty file
    Given I have a filename empty.log
    When I seek newline position in it
    Then I got the positon of -1
