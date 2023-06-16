import unittest

from base_test import BaseTest
from keep_ours_xml_paths_merge_driver import replace_nth


class MyTestCase(BaseTest):

    def test_replace_nth(self):
        original = "aa bb cc aa bb cc aa bb cc"
        expected_unchanged = original

        replaced = replace_nth(original, 'aa', 'xx', 0)
        self.assertEqual(expected_unchanged, replaced)

        original = "aa bb cc aa bb cc aa bb cc"
        replaced = replace_nth(original, 'aa', 'xx', 1)
        expected = "xx bb cc aa bb cc aa bb cc"
        self.assertEqual(expected, replaced)

        replaced = replace_nth(original, 'aa', 'xx', 2)
        expected = "aa bb cc xx bb cc aa bb cc"
        self.assertEqual(expected, replaced)

        replaced = replace_nth(original, 'aa', 'xx', 4)
        self.assertEqual(expected_unchanged, replaced)


if __name__ == '__main__':
    unittest.main()
