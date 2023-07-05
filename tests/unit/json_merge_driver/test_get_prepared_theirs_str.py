import os
import unittest

import keep_ours_paths_merge_driver.json_merge_driver as json_merge_driver


class TestJsonMergeDriverGetPreparedTheirsStr(unittest.TestCase):

    def test_version_only(self):
        print(f"CWD: {os.getcwd()}")
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'package_01_base.json') as f_base:
            base_json_str = f_base.read()
        with open(testfiles_base_path + 'package_01_ours.json') as f_ours:
            ours_json_str = f_ours.read()
        with open(testfiles_base_path + 'package_01_theirs.json') as f_theirs:
            theirs_json_str = f_theirs.read()

        with open(testfiles_base_path + 'package_01_theirs_expected_replace_only_no_merge.json') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        prepared_theirs_str = json_merge_driver.get_prepared_theirs_str(base_json_str, ours_json_str, theirs_json_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_version_and_1_dependency(self):
        print(f"CWD: {os.getcwd()}")
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'package_02_base.json') as f_base:
            base_json_str = f_base.read()
        with open(testfiles_base_path + 'package_02_ours.json') as f_ours:
            ours_json_str = f_ours.read()
        with open(testfiles_base_path + 'package_02_theirs.json') as f_theirs:
            theirs_json_str = f_theirs.read()

        with open(testfiles_base_path + 'package_02_theirs_expected_replace_only_no_merge.json') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        json_merge_driver.set_paths_and_patterns({'$.version': None, '$.dependencies.*': '.mycompany.+'})
        prepared_theirs_str = json_merge_driver.get_prepared_theirs_str(base_json_str, ours_json_str, theirs_json_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)


if __name__ == '__main__':
    unittest.main()
