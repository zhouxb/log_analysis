import util
import unittest
import datetime

class TestRoundBy(unittest.TestCase):
    def test_round_by(self):
        round_num_by_5 = util.round_num_by(5)
        self.assertEqual(round_num_by_5(10), 10)

class TestRoundMinutesBy(unittest.TestCase):
    def test_round_minutes_by(self):
        round_minutes_by_5 = util.round_minutes_by(5)
        self.assertEqual(round_minutes_by_5(datetime.datetime(2011, 11, 1, 12, 56)), datetime.datetime(2011, 11, 1, 12, 55))
