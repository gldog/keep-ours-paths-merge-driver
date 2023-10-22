import unittest

import keep_ours_paths_merge_driver.utils as utils


class MyTestCase(unittest.TestCase):

    def testReplaceTokenWithStringDocReferencePredicate(self):
        expected_str = "AAreplaceTokenBB"

        def compareToReference(s):
            return s == expected_str

        input_str = "AABB"
        expected_str = "AABB"
        replaced_str = utils.replace_token(input_str, "searchToken", "replaceToken", compareToReference)
        self.assertEqual(expected_str, replaced_str)

        input_str = "AAsearchTokenBB"
        expected_str = "AAreplaceTokenBB"
        replaced_str = utils.replace_token(input_str, "searchToken", "replaceToken", compareToReference)
        self.assertEqual(expected_str, replaced_str)

        input_str = "AAsearchTokenBBsearchTokenCC"
        expected_str = "AAsearchTokenBBreplaceTokenCC"
        replaced_str = utils.replace_token(input_str, "searchToken", "replaceToken", compareToReference)
        self.assertEqual(expected_str, replaced_str)

        input_str = "AAsearchTokenBBsearchTokenCCsearchTokenDD"
        expected_str = "AAsearchTokenBBsearchTokenCCreplaceTokenDD"
        replaced_str = utils.replace_token(input_str, "searchToken", "replaceToken", compareToReference)
        self.assertEqual(expected_str, replaced_str)


if __name__ == '__main__':
    unittest.main()
