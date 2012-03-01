import os
import unittest
import textfile
from util import ensure_directory

class TestGetFileSize(unittest.TestCase):
    def setUp(self):
        ensure_directory("tmp")
        self.file = "tmp/file.log"
        os.system("touch %s" % self.file)

    def tearDown(self):
        os.system("rm %s" % self.file)

    def test_get_file_size_of_an_empty_file(self):
        self.assertEqual(textfile.get_file_size(self.file), 0)

    def test_get_file_size_of_an_normal_file(self):
        with open(self.file, "w") as f:
            f.write("hello")
        self.assertEqual(textfile.get_file_size(self.file), 5)

class TestSeekNewLine(unittest.TestCase):
    def setUp(self):
        ensure_directory("tmp")
        self.file = "tmp/file.log"
        os.system("touch %s" % self.file)

    def tearDown(self):
        os.system("rm %s" % self.file)

    def test_seek_newline_in_an_empty_file(self):
        with open(self.file) as f:
            self.assertEqual(textfile.seek_newline(f, 0), -1)
            self.assertEqual(textfile.seek_newline(f, 100), -1)

    def test_seek_newline_in_file_does_not_contain_new_line(self):
        with open(self.file, "w") as f:
            f.write("hello world")
        with open(self.file) as f:
            self.assertEqual(textfile.seek_newline(f, 0), -1)

    def test_seek_newline_in_none_empty_file(self):
        with open(self.file, "w") as f:
            f.write("hello\nworld\n")
        with open(self.file) as f:
            self.assertEqual(textfile.seek_newline(f, 0), -1)
            self.assertEqual(textfile.seek_newline(f, 5), 5)
            self.assertEqual(textfile.seek_newline(f, 10), 5)
            self.assertEqual(textfile.seek_newline(f, 11), 11)

class TestDvideChunk(unittest.TestCase):
    def setUp(self):
        ensure_directory("tmp")
        self.file = "tmp/file.log"
        os.system("touch %s" % self.file)

    def tearDown(self):
        os.system("rm %s" % self.file)

    def test_divide_chunk_with_an_empty_file(self):
        self.assertEqual([item for item in textfile.divide_into_chunks(self.file, 1)], [(0, 0)])
        self.assertEqual([item for item in textfile.divide_into_chunks(self.file, 10)], [(0, 0)])

    def test_divide_chunk_with_an_file_not_end_with_newline(self):
        with open(self.file, "w") as f:
            f.write("hello world\nhello python!")
        self.assertEqual([item for item in textfile.divide_into_chunks(self.file, 100)], [(0, 12)])
        self.assertEqual([item for item in textfile.divide_into_chunks(self.file, 4)], [(0, 0)])
    def test_divide_chunk_with_an_normal_file(self):
        with open(self.file, "w") as f:
            f.write("hello world\nhello python!\n")
        self.assertEqual([item for item in textfile.divide_into_chunks(self.file, 20)], [(0, 12),(12, 26)])

class TestDivideIntoNParts(unittest.TestCase):
    def setUp(self):
        ensure_directory("tmp")
        self.file = "tmp/file.log"
        os.system("touch %s" % self.file)

    def tearDown(self):
        os.system("rm %s" % self.file)

    def test_divideIntoNPa(self):
        with open(self.file, "w") as f:
            f.write("hello world\nhello python!\n")
        self.assertEqual([ i for i in textfile.divide_into_parts(self.file, 2)], [(0, 12), (12, 26)])
