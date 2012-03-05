import unittest
import dnslog
import datetime
class TestParseLogEntry(unittest.TestCase):
    def test_parse_log_entry(self):
		line = "11-09-01 10:21:25,041 INFO : queries: - |127.0.0.1|www.souxp.com|default|58.68.239.29;|default;|A|success|+|---w--- qr aa rd ra |202|"
		entry = dnslog.parse_log_line(line)
		date = entry[dnslog.DATE]
		self.assertEqual(date, datetime.datetime(2011, 9, 1, 10, 21, 25))
