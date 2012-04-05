
Feature: Non80 Analysis
    Scenario: Run non80 analysis
        Given I have an gz-compressed file in data/queries.log.CMN-CQ-2-375.000000000001.gz
        When I run non80 analysis on it
        Then I see no exceptions
