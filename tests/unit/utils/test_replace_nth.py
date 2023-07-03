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
        inputStr = "searchToken"

        expectedStr = "replaceToken"
        replacedStr = utils.replace_nth(inputStr, 'searchToken', 'replaceToken', 1)
        self.assertEqual(expectedStr, replacedStr)

        expectedStr = ""
        replacedStr = utils.replace_nth(inputStr, 'searchToken', 'replaceToken', 0)
        self.assertEqual(expectedStr, replacedStr)

        replacedStr = utils.replace_nth(inputStr, 'searchToken', 'replaceToken', 2)
        expectedStr = ""
        self.assertEqual(expectedStr, replacedStr)

        inputStr = "searchTokenAA\nBB"

        expectedStr = "replaceTokenAA\nBB"
        replacedStr = utils.replace_nth(inputStr, 'searchToken', 'replaceToken', 1)
        self.assertEqual(expectedStr, replacedStr)

        replacedStr = utils.replace_nth(inputStr, 'searchToken', 'replaceToken', 0)
        expectedStr = ""
        self.assertEqual(expectedStr, replacedStr)

        replacedStr = utils.replace_nth(inputStr, 'searchToken', 'replaceToken', 2)
        expectedStr = ""
        self.assertEqual(expectedStr, replacedStr)

    def testReplaceNthOnSearchTokenAtEndOfString(self):
        inputStr = "AA\nBBsearchToken"
        replacedStr = utils.replace_nth(inputStr, "searchToken", "replaceToken", 1)
        expectedStr = "AA\nBBreplaceToken"
        self.assertEqual(expectedStr, replacedStr)

        replacedStr = utils.replace_nth(inputStr, "searchToken", "replaceToken", 0)
        expectedStr = ""
        self.assertEqual(expectedStr, replacedStr)

        replacedStr = utils.replace_nth(inputStr, "searchToken", "replaceToken", 2)
        expectedStr = ""
        self.assertEqual(expectedStr, replacedStr)

    def testReplaceNthOnMultipleOccurencesWith1Replacement(self):
        inputStr = "searchTokenAAsearchToken\nsearchTokenBBsearchToken"

        replacedStr = utils.replace_nth(inputStr, "searchToken", "replaceToken", 1)
        expectedStr = "replaceTokenAAsearchToken\nsearchTokenBBsearchToken"
        self.assertEqual(expectedStr, replacedStr)

        replacedStr = utils.replace_nth(inputStr, "searchToken", "replaceToken", 2)
        expectedStr = "searchTokenAAreplaceToken\nsearchTokenBBsearchToken"
        self.assertEqual(expectedStr, replacedStr)

        replacedStr = utils.replace_nth(inputStr, "searchToken", "replaceToken", 3)
        expectedStr = "searchTokenAAsearchToken\nreplaceTokenBBsearchToken"
        self.assertEqual(expectedStr, replacedStr)

        replacedStr = utils.replace_nth(inputStr, "searchToken", "replaceToken", 4)
        expectedStr = "searchTokenAAsearchToken\nsearchTokenBBreplaceToken"
        self.assertEqual(expectedStr, replacedStr)

        replacedStr = utils.replace_nth(inputStr, "searchToken", "replaceToken", 5)
        expectedStr = ""
        self.assertEqual(expectedStr, replacedStr)


if __name__ == '__main__':
    unittest.main()
