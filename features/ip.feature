Feature: IP Analysis
    Scenario: Run ip analysis
        Given I have an gz-compressed file in data/queries.log.CMN-CQ-2-375.000000000001.gz
        When I run ip analysis on it
        Then I see no exceptions
