import unittest


class TestJsonMergeDriverGetPreparedTheirsStr(unittest.TestCase):

    def test_packagejson_version_only_with_mergestrategy_onconflict_ours_and_jpath_prefix_dollar(self):
        """
        The jpath can be given with the JSON-path prefix "$." and without.
        In this test the prefix is used.
        """
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'package_01_base.json') as f_base:
            base_json_str = f_base.read()
        with open(testfiles_base_path + 'package_01_ours.json') as f_ours:
            ours_json_str = f_ours.read()
        with open(testfiles_base_path + 'package_01_theirs.json') as f_theirs:
            theirs_json_str = f_theirs.read()

        import keep_ours_paths_merge_driver.json_merge_driver as json_merge_driver
        json_merge_driver.set_paths_and_patterns([
            {'merge_strategy': 'onconflict-ours', 'path': '$.version', 'pattern': None}])

        with open(testfiles_base_path + 'package_01_theirs_expected_replace_only_no_merge.json') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        prepared_theirs_str = json_merge_driver.get_prepared_theirs_str(base_json_str, ours_json_str, theirs_json_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_packagejson_version_only_with_mergestrategy_onconflict_ours_and_no_jpath_prefix(self):
        """
        The jpath can be given with the JSON-path prefix "$." and without.
        In this test the prefix is not used.
        """
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'package_01_base.json') as f_base:
            base_json_str = f_base.read()
        with open(testfiles_base_path + 'package_01_ours.json') as f_ours:
            ours_json_str = f_ours.read()
        with open(testfiles_base_path + 'package_01_theirs.json') as f_theirs:
            theirs_json_str = f_theirs.read()

        import keep_ours_paths_merge_driver.json_merge_driver as json_merge_driver
        json_merge_driver.set_paths_and_patterns([
            {'merge_strategy': 'onconflict-ours', 'path': 'version', 'pattern': None}])

        with open(testfiles_base_path + 'package_01_theirs_expected_replace_only_no_merge.json') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        from keep_ours_paths_merge_driver import config
        config.configure_logger('DEBUG')
        prepared_theirs_str = json_merge_driver.get_prepared_theirs_str(base_json_str, ours_json_str, theirs_json_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_packagejson_version_and_1_dependency_with_mergestrategy_onconflict_ours(self):
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'package_02_base.json') as f_base:
            base_json_str = f_base.read()
        with open(testfiles_base_path + 'package_02_ours.json') as f_ours:
            ours_json_str = f_ours.read()
        with open(testfiles_base_path + 'package_02_theirs.json') as f_theirs:
            theirs_json_str = f_theirs.read()

        with open(testfiles_base_path + 'package_02_theirs_expected_replace_only_no_merge.json') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        import keep_ours_paths_merge_driver.json_merge_driver as json_merge_driver
        from keep_ours_paths_merge_driver import config
        config.configure_logger('DEBUG')
        json_merge_driver.set_paths_and_patterns([
            {'merge_strategy': 'onconflict-ours', 'path': '$.version', 'pattern': None},
            {'merge_strategy': 'onconflict-ours', 'path': '$.dependencies.*', 'pattern': '@mycompany/.+'}])
        prepared_theirs_str = json_merge_driver.get_prepared_theirs_str(base_json_str, ours_json_str, theirs_json_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_packagejson_version_and_2_dependencies_with_mergestrategy_onconflict_ours(self):
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + 'package_03_base.json') as f_base:
            base_json_str = f_base.read()
        with open(testfiles_base_path + 'package_03_ours.json') as f_ours:
            ours_json_str = f_ours.read()
        with open(testfiles_base_path + 'package_03_theirs.json') as f_theirs:
            theirs_json_str = f_theirs.read()

        with open(testfiles_base_path + 'package_03_theirs_expected_replace_only_no_merge.json') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        import keep_ours_paths_merge_driver.json_merge_driver as json_merge_driver
        json_merge_driver.set_paths_and_patterns([
            {'merge_strategy': 'onconflict-ours', 'path': '$.version', 'pattern': None},
            {'merge_strategy': 'onconflict-ours', 'path': '$.dependencies.*', 'pattern': '@mycompany/some-app1'},
            {'merge_strategy': 'onconflict-ours', 'path': '$.version', 'pattern': None},
            {'merge_strategy': 'onconflict-ours', 'path': '$.dependencies.*', 'pattern': '@mycompany/some-app2'}
        ])
        prepared_theirs_str = json_merge_driver.get_prepared_theirs_str(base_json_str, ours_json_str, theirs_json_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)

    def test_anyjson(self):
        testfiles_base_path = 'tests/unit/resources/'
        with open(testfiles_base_path + '01_base.json') as f_base:
            base_json_str = f_base.read()
        with open(testfiles_base_path + '01_ours.json') as f_ours:
            ours_json_str = f_ours.read()
        with open(testfiles_base_path + '01_theirs.json') as f_theirs:
            theirs_json_str = f_theirs.read()

        import keep_ours_paths_merge_driver.json_merge_driver as json_merge_driver
        json_merge_driver.set_paths_and_patterns([
            {'merge_strategy': 'onconflict-ours', 'path': 'scalar_12_attr', 'pattern': None},
            {'merge_strategy': 'onconflict-ours', 'path': 'object_21_attr.scalar_12_attr',
             'pattern': None},
            {'merge_strategy': 'onconflict-ours', 'path': 'object_21_attr.object_21_attr.scalar_12_attr',
             'pattern': None},
            {'merge_strategy': 'onconflict-ours', 'path': 'object_21_attr.list_31_attr.[1]',
             'pattern': None},
            {'merge_strategy': 'onconflict-ours', 'path': 'object_21_attr.list_31_attr.[2].scalar_11_attr',
             'pattern': None}
        ])

        with open(testfiles_base_path + '01_theirs_expected_replace_only_no_merge.json') as f_expected:
            prepared_theirs_str_expected = f_expected.read()

        # from keep_ours_paths_merge_driver import config
        # config.configure_logger('DEBUG')
        prepared_theirs_str = json_merge_driver.get_prepared_theirs_str(base_json_str, ours_json_str, theirs_json_str)
        self.assertEqual(prepared_theirs_str_expected, prepared_theirs_str)


if __name__ == '__main__':
    unittest.main()
