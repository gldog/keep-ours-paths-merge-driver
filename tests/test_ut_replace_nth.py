import unittest

from base_ut_test import BaseTest
from xml_paths_merge_driver import replace_nth


class MyTestCase(BaseTest):

    def test_replace_nth(self):
        original = "aa bb cc aa bb cc aa bb cc"
        expected_unchanges = original

        replaced = replace_nth(original, 'aa', 'xx', 0)
        self.assertEqual(expected_unchanges, replaced)

        original = "aa bb cc aa bb cc aa bb cc"
        replaced = replace_nth(original, 'aa', 'xx', 1)
        expected = "xx bb cc aa bb cc aa bb cc"
        self.assertEqual(expected, replaced)

        replaced = replace_nth(original, 'aa', 'xx', 2)
        expected = "aa bb cc xx bb cc aa bb cc"
        self.assertEqual(expected, replaced)

        replaced = replace_nth(original, 'aa', 'xx', 4)
        self.assertEqual(expected_unchanges, replaced)


if __name__ == '__main__':
    unittest.main()
