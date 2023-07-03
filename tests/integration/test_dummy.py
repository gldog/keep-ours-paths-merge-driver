import os
import unittest


class TestDummy(unittest.TestCase):

    def test_dummy(self):
        print(f"CWD: {os.getcwd()}")


if __name__ == '__main__':
    unittest.main()
