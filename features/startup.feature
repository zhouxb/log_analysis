Feature: Startup 
    Scenario: Run with non-exist file
        Given I have an non-exist file in /data/queries.log.CMN-CQ-2-375.000000000000.gz
        When I run all the analysis on it
        Then I see no exceptions

    #Scenario: Run log_analysis with an empty gz-compressed file
        #Given I have an empty gz-compressed file in data/queries.log.CMN-CQ-2-375.000000000000.gz
        #When I run all the analysis on it
        #Then I see no exceptions

    #Scenario: Run log_analysis with an gz-compressed file
        #Given I have an gz-compressed file in data/queries.log.CMN-CQ-2-375.201202172238.gz
        #When I run all the analysis on it
        #Then I see no exceptions
