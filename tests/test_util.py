import unittest
import datetime
import util

class TestRoundBy(unittest.TestCase):
    def test_round_by(self):
        round_by_5 = util.round_by(5)
        result  = round_by_5(5), round_by_5(10), round_by_5(7)
        self.assertEqual(result, (5, 10, 5))

        round_by_3 = util.round_by(3)
        self.assertEqual(round_by_3(10), 9)
        self.assertEqual(round_by_3(6), 6)

        with self.assertRaises(ValueError):
            util.round_minutes_by(0)

        with self.assertRaises(ValueError):
            util.round_minutes_by(-1)

class TestRoundMinutesBy(unittest.TestCase):
    def test_round_minutes_by(self):
        round_minutes_by_5 = util.round_minutes_by(5)
        self.assertEqual(
            round_minutes_by_5(datetime.datetime(2011, 11, 1, 12, 56)), 
            datetime.datetime(2011, 11, 1, 12, 55))

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

class TestIPConvert(unittest.TestCase):
    def test_ip_to_int(self):
        self.assertEqual(util.ip_to_int("0.0.0.0"), 0)
        self.assertEqual(util.ip_to_int("0.0.0.1"), 1)
        self.assertEqual(util.ip_to_int("74.125.114.92"), 1249735260)

    def test_ip_ranges_to_int(self):
        self.assertTrue(util.ip_to_int("192.168.0.15") in 
                        util.ip_range_to_int("192.168.0.0", "192.168.1.1"))
        self.assertTrue(util.ip_to_int("192.168.0.0") in 
                        util.ip_range_to_int("192.168.0.0", "192.168.1.1"))
        self.assertTrue(util.ip_to_int("192.168.1.1") in 
                        util.ip_range_to_int("192.168.0.0", "192.168.1.1"))
