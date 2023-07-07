import unittest

import keep_ours_paths_merge_driver.xml_merge_driver as xml_merge_driver


class TestXmlMergeDriverGetPreparedTheirsStr(unittest.TestCase):

    def test_version_only(self):
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'pom_01_base.xml') as f_base:
            base_xml_str = f_base.read()
        with open(testfiles_base_path + 'pom_01_ours.xml') as f_ours:
            ours_xml_str = f_ours.read()
        with open(testfiles_base_path + 'pom_01_theirs.xml') as f_theirs:
            theirs_xml_str = f_theirs.read()

        with open(testfiles_base_path + 'pom_01_theirs_expected_replace_only_no_merge.xml') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_version_and_1_property(self):
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'pom_02_base.xml') as f_base:
            base_xml_str = f_base.read()
        with open(testfiles_base_path + 'pom_02_ours.xml') as f_ours:
            ours_xml_str = f_ours.read()
        with open(testfiles_base_path + 'pom_02_theirs.xml') as f_theirs:
            theirs_xml_str = f_theirs.read()

        with open(testfiles_base_path + 'pom_02_theirs_expected_replace_only_no_merge.xml') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        xml_merge_driver.set_paths_and_patterns([
            {'path': './version', 'pattern': None},
            {'path': './properties/', 'pattern': 'some-app.+'}])

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_version_and_2_properties_separate_path_and_patterns(self):
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'pom_03_base.xml') as f_base:
            base_xml_str = f_base.read()
        with open(testfiles_base_path + 'pom_03_ours.xml') as f_ours:
            ours_xml_str = f_ours.read()
        with open(testfiles_base_path + 'pom_03_theirs.xml') as f_theirs:
            theirs_xml_str = f_theirs.read()

        with open(testfiles_base_path + 'pom_03_theirs_expected_replace_only_no_merge.xml') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        xml_merge_driver.set_paths_and_patterns([
            {'path': './version', 'pattern': None},
            # Each 'some-app' has its explicite configuration.
            {'path': './properties/', 'pattern': 'some-app1\\.version'},
            {'path': './properties/', 'pattern': 'some-app2\\.version'}])

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_version_and_2_properties_combined_path_and_patterns(self):
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'pom_03_base.xml') as f_base:
            base_xml_str = f_base.read()
        with open(testfiles_base_path + 'pom_03_ours.xml') as f_ours:
            ours_xml_str = f_ours.read()
        with open(testfiles_base_path + 'pom_03_theirs.xml') as f_theirs:
            theirs_xml_str = f_theirs.read()

        with open(testfiles_base_path + 'pom_03_theirs_expected_replace_only_no_merge.xml') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        xml_merge_driver.set_paths_and_patterns([
            {'path': './version', 'pattern': None},
            # Both 'some-app' are given in one path/pattern config.
            {'path': './properties/', 'pattern': '(some-app1|some-app2)\\.version'}])

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)


if __name__ == '__main__':
    unittest.main()
