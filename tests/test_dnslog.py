import unittest
import dnslog
import datetime

chunk =  \
'''
11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.google.com|default|58.68.239.29;|default;|A|success|+|---w--- qr aa rd ra |202|
11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.baidu.cn|default|58.68.239.14;|default;|A|success|+|---w--- qr aa rd ra |203|
11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.twitter.cn|default|58.68.239.14;|default;|A|success|+|---w--- qr aa rd ra |204|
11-09-01 10:21:25,042 INFO : queries: - |127.0.0.1|www.google.com|default|58.68.239.29;|default;|A|success|+|---w--- qr aa rd ra |205|
'''
class TestParseLogEntry(unittest.TestCase):
    def test_parse_log_line(self):
        line = "11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|\
www.souxp.com|default|58.68.239.29;|default;|A|success|+|\
---w--- qr aa rd ra |202|"
        entry = dnslog.parse_log_line(line)
        date = entry[dnslog.DATE]
        self.assertEqual(date, datetime.datetime(2011, 9, 1, 10, 21, 25))

class TestParseLogChunk(unittest.TestCase):
    def test_chunk(self):
        dnslog.parse_chunk(chunk.splitlines())
class TestInWhilteList(unittest.TestCase):
    def test_in_whitelist(self):
        line = "11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|\
www.souxp.com|default|58.68.239.29;|default;|A|success|+|\
---w--- qr aa rd ra |202|"
        entry = dnslog.parse_log_line(line)
        self.assertTrue(dnslog.in_whitelist(entry[dnslog.RESOLVE_DETAIL]))

class TestIsSilent(unittest.TestCase):
    def test_is_silent(self):
        line = "11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|\
www.souxp.com|default|58.68.239.29;|default;|A|success|+|\
---w--- qr aa rd ra |202|"
        entry = dnslog.parse_log_line(line)
        self.assertFalse(dnslog.is_silent(entry[dnslog.RESOLVE_DETAIL]))

        line = "11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|\
www.souxp.com|default|58.68.239.29;|default;|A|success|+|\
------- qr aa rd ra |202|"
        entry = dnslog.parse_log_line(line)
        self.assertTrue(dnslog.is_silent(entry[dnslog.RESOLVE_DETAIL]))
