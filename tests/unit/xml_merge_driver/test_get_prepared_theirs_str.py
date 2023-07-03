import os
import unittest

import keep_ours_paths_merge_driver.xml_merge_driver as xml_merge_driver


class TestXmlMergeDriverGetPreparedTheirsStr(unittest.TestCase):

    def test1(self):
        print(f"CWD: {os.getcwd()}")
        pom_base_path = 'tests/unit/resources/'
        with open(pom_base_path + 'pom_01_base.xml') as f_base:
            base_xml_str = f_base.read()
        with open(pom_base_path + 'pom_01_ours.xml') as f_ours:
            ours_xml_str = f_ours.read()
        with open(pom_base_path + 'pom_01_theirs.xml') as f_theirs:
            theirs_xml_str = f_theirs.read()

        with open(pom_base_path + 'pom_01_theirs_expected_replace_only.xml') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)


if __name__ == '__main__':
    unittest.main()
