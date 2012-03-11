import unittest
import datetime
import util

class TestRoundBy(unittest.TestCase):
    def test_round_by(self):
        round_num_by_5 = util.round_num_by(5)
        self.assertEqual(round_num_by_5(10), 10)

class TestRoundMinutesBy(unittest.TestCase):
    def test_round_minutes_by(self):
        round_minutes_by_5 = util.round_minutes_by(5)
        self.assertEqual(round_minutes_by_5(datetime.datetime(2011, 11, 1, 12, 56)), datetime.datetime(2011, 11, 1, 12, 55))

class TestSplitEvery(unittest.TestCase):
    def test_split_every(self):
        # a normal case
        result = list(util.split_every(3, range(1, 9)))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], [1, 2, 3])
        self.assertEqual(result[1], [4, 5, 6])
        self.assertEqual(result[2], [7, 8])

        # iterable is empty
        result = list(util.split_every(3, []))
        self.assertEqual(result, [])

        # n is bigger than the length of iterable
        result = list(util.split_every(5, [1, 2, 3, 4]))
        self.assertEqual(result, [[1, 2, 3, 4]])
