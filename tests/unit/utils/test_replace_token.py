import unittest

import keep_ours_paths_merge_driver.utils as utils


class MyTestCase(unittest.TestCase):

    def testReplaceTokenWithStringDocReferencePredicate(self):
        expectedStr = "AAreplaceTokenBB"

        def compareToReference(s):
            return s == expectedStr

        inputStr = "AABB"
        expectedStr = "AABB"
        replacedStr = utils.replace_token(inputStr, "searchToken", "replaceToken", compareToReference)
        self.assertEqual(expectedStr, replacedStr)

        inputStr = "AAsearchTokenBB"
        expectedStr = "AAreplaceTokenBB"
        replacedStr = utils.replace_token(inputStr, "searchToken", "replaceToken", compareToReference)
        self.assertEqual(expectedStr, replacedStr)

        inputStr = "AAsearchTokenBBsearchTokenCC"
        expectedStr = "AAsearchTokenBBreplaceTokenCC"
        replacedStr = utils.replace_token(inputStr, "searchToken", "replaceToken", compareToReference)
        self.assertEqual(expectedStr, replacedStr)

        inputStr = "AAsearchTokenBBsearchTokenCCsearchTokenDD"
        expectedStr = "AAsearchTokenBBsearchTokenCCreplaceTokenDD"
        replacedStr = utils.replace_token(inputStr, "searchToken", "replaceToken", compareToReference)
        self.assertEqual(expectedStr, replacedStr)


if __name__ == '__main__':
    unittest.main()
