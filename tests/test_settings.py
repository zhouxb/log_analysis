import unittest
import settings

class TestLogFilenamePattern(unittest.TestCase):
    def test_log_filename_pattern(self):
        filename = "queries.log.CMN-CQ-2-375.20120217223800.gz"
        pattern = settings.DNS_LOG_FILENAME_PATTERN
        self.assertIsNotNone(pattern.match(filename))
        self.assertEqual(pattern.match(filename).group("PROVINCE"), "CQ")

