Feature: Leadingin Analysis
    Scenario: Run leadingin analysis
        Given I have an gz-compressed file in data/queries.log.CMN-CQ-2-375.000000000001.gz
        When I run leadingin analysis on it
        Then I see no exceptions
