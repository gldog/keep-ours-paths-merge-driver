import unittest

import keep_ours_paths_merge_driver.xml_merge_driver as xml_merge_driver


class TestXmlMergeDriverGetPreparedTheirsStr(unittest.TestCase):

    def test_version_only_with_mergestrategy_onconflict_ours(self):
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'pom_01_base.xml') as f_base:
            base_xml_str = f_base.read()
        with open(testfiles_base_path + 'pom_01_ours.xml') as f_ours:
            ours_xml_str = f_ours.read()
        with open(testfiles_base_path + 'pom_01_theirs.xml') as f_theirs:
            theirs_xml_str = f_theirs.read()

        with open(testfiles_base_path + 'pom_01_theirs_expected_replace_only_no_merge.xml') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        xml_merge_driver.set_paths_and_patterns([
            {'merge_strategy': 'onconflict-ours', 'path': './version', 'pattern': None}])

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_version_and_1_property_with_mergestrategy_onconflict_ours(self):
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
            {'merge_strategy': 'onconflict-ours', 'path': './version', 'pattern': None},
            {'merge_strategy': 'onconflict-ours', 'path': './properties/', 'pattern': 'some-app.+'}])

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_version_and_2_properties_separate_path_and_patterns_with_mergestrategy_onconflict_ours(self):
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
            {'merge_strategy': 'onconflict-ours', 'path': './version', 'pattern': None},
            # Each 'some-app' has its explicite configuration.
            {'merge_strategy': 'onconflict-ours', 'path': './properties/', 'pattern': 'some-app1[.]version'},
            {'merge_strategy': 'onconflict-ours', 'path': './properties/', 'pattern': 'some-app2[.]version'}])

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_version_and_2_properties_combined_path_and_patterns_with_mergestrategy_onconflict_ours(self):
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
            {'merge_strategy': 'onconflict-ours', 'path': './version', 'pattern': None},
            # Both 'some-app' are given in one path/pattern config.
            {'merge_strategy': 'onconflict-ours', 'path': './properties/',
             'pattern': '(some-app1|some-app2)[.]version'}])

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_version_and_2_properties_combined_path_and_patterns_with_mergestrategy_always_ours(self):
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'pom_13_base.xml') as f_base:
            base_xml_str = f_base.read()
        with open(testfiles_base_path + 'pom_13_ours.xml') as f_ours:
            ours_xml_str = f_ours.read()
        with open(testfiles_base_path + 'pom_13_theirs.xml') as f_theirs:
            theirs_xml_str = f_theirs.read()

        with open(testfiles_base_path + 'pom_13_theirs_expected_replace_only_no_merge.xml') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        xml_merge_driver.set_paths_and_patterns([
            {'merge_strategy': 'always-ours', 'path': './version', 'pattern': None},
            # Both 'some-app' are given in one path/pattern config.
            {'merge_strategy': 'always-ours', 'path': './properties/',
             'pattern': '(some-app1|some-app2)[.]version'}])

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_removed_property_in_ours(self):
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'pom_21_base.xml') as f_base:
            base_xml_str = f_base.read()
        with open(testfiles_base_path + 'pom_21_ours.xml') as f_ours:
            ours_xml_str = f_ours.read()
        with open(testfiles_base_path + 'pom_21_theirs.xml') as f_theirs:
            theirs_xml_str = f_theirs.read()

        with open(testfiles_base_path + 'pom_21_theirs_expected_replace_only_no_merge.xml') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        xml_merge_driver.set_paths_and_patterns([
            {'merge_strategy': 'onconflict-ours', 'path': './properties/', 'pattern': '.+[.]version'}])

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_removed_property_in_theirs(self):
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'pom_22_base.xml') as f_base:
            base_xml_str = f_base.read()
        with open(testfiles_base_path + 'pom_22_ours.xml') as f_ours:
            ours_xml_str = f_ours.read()
        with open(testfiles_base_path + 'pom_22_theirs.xml') as f_theirs:
            theirs_xml_str = f_theirs.read()

        with open(testfiles_base_path + 'pom_22_theirs_expected_replace_only_no_merge.xml') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        xml_merge_driver.set_paths_and_patterns([
            {'merge_strategy': 'onconflict-ours', 'path': './properties/', 'pattern': '.+[.]version'}])

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_1(self):
        """
        This tests if lxml still works without encoding set in the pom.xml file. At developing there was an issue about
        that.
        This test is a copy of test_version_only_with_mergestrategy_onconflict_ours(), but with pom.xml files
        without the first line "<?xml version="1.0" encoding="UTF-8"?>" omitting the encoding.
        """
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'pom_31_base.xml') as f_base:
            base_xml_str = f_base.read()
        with open(testfiles_base_path + 'pom_31_ours.xml') as f_ours:
            ours_xml_str = f_ours.read()
        with open(testfiles_base_path + 'pom_31_theirs.xml') as f_theirs:
            theirs_xml_str = f_theirs.read()

        xml_merge_driver.set_paths_and_patterns([
            {'merge_strategy': 'onconflict-ours', 'path': './version', 'pattern': None}])

        with open(testfiles_base_path + 'pom_31_theirs_expected_replace_only_no_merge.xml') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)


if __name__ == '__main__':
    unittest.main()
