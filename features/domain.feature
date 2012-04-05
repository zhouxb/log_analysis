Feature: Domain Analysis
    Scenario: Run domain analysis
        Given I have some log records:
            """
            11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.google.com|default|58.68.239.29;|default;|A|success|+|---w--- qr aa rd ra |202|
            11-09-01 10:21:26,041 INFO : queries: - |127.0.0.1|www.google.com|default|58.68.239.29;|default;|A|success|+|---w--- qr aa rd ra |202|
            11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.baidu.com|default|58.68.239.14;|default;|A|success|+|---w--- qr aa rd ra |203|
            11-09-01 10:23:28,041 INFO : queries: - |127.0.0.1|www.baidu.com|default|58.68.239.14;|default;|A|success|+|---w--- qr aa rd ra |203|
            11-09-01 10:26:28,041 INFO : queries: - |127.0.0.1|www.baidu.com|default|58.68.239.14;|default;|A|success|+|---w--- qr aa rd ra |203|
            11-09-01 10:26:26,041 INFO : queries: - |127.0.0.1|www.google.com|default|58.68.239.29;|default;|A|success|+|--w---- qr aa rd ra |202|
            11-09-01 10:27:26,041 INFO : queries: - |127.0.0.1|www.google.com|default|58.68.239.29;|default;|A|success|+|-B----- qr aa rd ra |202|
            """
        Then I create an gzip file named data/queries.log.CMN-CQ-2-375.000000000001.gz with these records
        When I run domain analysis on it
        And I sleep for 1 seconds
        Then I see 4 records in domain.minutely
