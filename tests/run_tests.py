#!/usr/bin/python
import os
import sys
import unittest

if __name__ == '__main__':
    sys.path.append("./log_analysis/")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite(loader.discover("tests"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
