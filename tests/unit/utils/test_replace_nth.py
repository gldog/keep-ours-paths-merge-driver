import unittest

import keep_ours_paths_merge_driver.utils as utils


class MyTestCase(unittest.TestCase):

    def test_replace_nth(self):
        original = "aa bb cc aa bb cc aa bb cc"
        expected = ""
        replaced = utils.replace_nth(original, 'aa', 'xx', 0)
        self.assertEqual(expected, replaced)

        original = "aa bb cc aa bb cc aa bb cc"
        replaced = utils.replace_nth(original, 'aa', 'xx', 1)
        expected = "xx bb cc aa bb cc aa bb cc"
        self.assertEqual(expected, replaced)

        replaced = utils.replace_nth(original, 'aa', 'xx', 2)
        expected = "aa bb cc xx bb cc aa bb cc"
        self.assertEqual(expected, replaced)

        replaced = utils.replace_nth(original, 'aa', 'xx', 4)
        expected = ""
        self.assertEqual(expected, replaced)

    def test_replace_nth_on_empty_string(self):
        input_str = ''
        expected_str = ''
        replaced_str = utils.replace_nth(input_str, 'searchToken', 'replaceToken', 1)
        self.assertEqual(expected_str, replaced_str)

    def test_replace_nth_on_0_occurences_results_in_empty_string(self):
        input_str = ''
        expected_str = ''

        replaced_str = utils.replace_nth(input_str, 'searchToken', 'replaceToken', 1)
        self.assertEqual(expected_str, replaced_str)

        replaced_str = utils.replace_nth(input_str, 'searchToken', 'replaceToken', 0)
        self.assertEqual(expected_str, replaced_str)

        replaced_str = utils.replace_nth(input_str, 'searchToken', 'replaceToken', 2)
        self.assertEqual(expected_str, replaced_str)

    def test_replace_nth_on_search_token_at_begin_of_string(self):
        input_str = "searchToken"

        expected_str = "replaceToken"
        replaced_str = utils.replace_nth(input_str, 'searchToken', 'replaceToken', 1)
        self.assertEqual(expected_str, replaced_str)

        expected_str = ""
        replaced_str = utils.replace_nth(input_str, 'searchToken', 'replaceToken', 0)
        self.assertEqual(expected_str, replaced_str)

        replaced_str = utils.replace_nth(input_str, 'searchToken', 'replaceToken', 2)
        expected_str = ""
        self.assertEqual(expected_str, replaced_str)

        input_str = "searchTokenAA\nBB"

        expected_str = "replaceTokenAA\nBB"
        replaced_str = utils.replace_nth(input_str, 'searchToken', 'replaceToken', 1)
        self.assertEqual(expected_str, replaced_str)

        replaced_str = utils.replace_nth(input_str, 'searchToken', 'replaceToken', 0)
        expected_str = ""
        self.assertEqual(expected_str, replaced_str)

        replaced_str = utils.replace_nth(input_str, 'searchToken', 'replaceToken', 2)
        expected_str = ""
        self.assertEqual(expected_str, replaced_str)

    def testReplaceNthOnSearchTokenAtEndOfString(self):
        input_str = "AA\nBBsearchToken"
        replaced_str = utils.replace_nth(input_str, "searchToken", "replaceToken", 1)
        expected_str = "AA\nBBreplaceToken"
        self.assertEqual(expected_str, replaced_str)

        replaced_str = utils.replace_nth(input_str, "searchToken", "replaceToken", 0)
        expected_str = ""
        self.assertEqual(expected_str, replaced_str)

        replaced_str = utils.replace_nth(input_str, "searchToken", "replaceToken", 2)
        expected_str = ""
        self.assertEqual(expected_str, replaced_str)

    def testReplaceNthOnMultipleOccurencesWith1Replacement(self):
        input_str = "searchTokenAAsearchToken\nsearchTokenBBsearchToken"

        replaced_str = utils.replace_nth(input_str, "searchToken", "replaceToken", 1)
        expected_str = "replaceTokenAAsearchToken\nsearchTokenBBsearchToken"
        self.assertEqual(expected_str, replaced_str)

        replaced_str = utils.replace_nth(input_str, "searchToken", "replaceToken", 2)
        expected_str = "searchTokenAAreplaceToken\nsearchTokenBBsearchToken"
        self.assertEqual(expected_str, replaced_str)

        replaced_str = utils.replace_nth(input_str, "searchToken", "replaceToken", 3)
        expected_str = "searchTokenAAsearchToken\nreplaceTokenBBsearchToken"
        self.assertEqual(expected_str, replaced_str)

        replaced_str = utils.replace_nth(input_str, "searchToken", "replaceToken", 4)
        expected_str = "searchTokenAAsearchToken\nsearchTokenBBreplaceToken"
        self.assertEqual(expected_str, replaced_str)

        replaced_str = utils.replace_nth(input_str, "searchToken", "replaceToken", 5)
        expected_str = ""
        self.assertEqual(expected_str, replaced_str)


if __name__ == '__main__':
    unittest.main()
