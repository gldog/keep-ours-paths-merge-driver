import unittest

import keep_ours_paths_merge_driver.config as config


class TestConfigGetPAthWithPatterns(unittest.TestCase):

    def test_get_paths_with_patterns(self):
        expected = [{'merge_strategy': 'onconflict-ours', 'path': 'path-from-env1', 'pattern': 'pattern-from-env1'}]
        from_environment_as_str = 'path-from-env1:pattern-from-env1'
        from_cl_args_as_list = None
        got = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        self.assertEqual(expected, got)

        expected = [
            {'merge_strategy': 'onconflict-ours', 'path': 'path-from-env1', 'pattern': 'pattern-from-env1'},
            {'merge_strategy': 'onconflict-ours', 'path': 'path-from-env2', 'pattern': 'pattern-from-env2'}
        ]
        from_environment_as_str = 'path-from-env1:pattern-from-env1 path-from-env2:pattern-from-env2'
        from_cl_args_as_list = None
        got = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        self.assertEqual(expected, got)
        from_environment_as_str = 'path-from-env1:pattern-from-env1,path-from-env2:pattern-from-env2'
        from_cl_args_as_list = None
        got = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        self.assertEqual(expected, got)
        from_environment_as_str = 'path-from-env1:pattern-from-env1;path-from-env2:pattern-from-env2'
        from_cl_args_as_list = None
        got = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        self.assertEqual(expected, got)

        expected = [
            {'merge_strategy': 'onconflict-ours', 'path': 'path-from-env1', 'pattern': 'pattern-from-env1'},
            {'merge_strategy': 'onconflict-ours', 'path': 'path-from-env2', 'pattern': 'pattern-from-env2'}
        ]
        from_environment_as_str = ',path-from-env1:pattern-from-env1  path-from-env2:pattern-from-env2,'
        from_cl_args_as_list = None
        got = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        self.assertEqual(expected, got)
        from_environment_as_str = ' , path-from-env1:pattern-from-env1 ; path-from-env2:pattern-from-env2 ; , '
        from_cl_args_as_list = None
        got = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        self.assertEqual(expected, got)

        # Switch defaults off by environment variable.
        from_environment_as_str = ''
        from_cl_args_as_list = None
        got = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        expected = []
        self.assertEqual(expected, got)

        # Switch defaults off by environment variable.
        from_environment_as_str = ''
        from_cl_args_as_list = ['path-from-cl1:pattern-from-cl1']
        got = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        expected = []
        self.assertEqual(expected, got)

        from_environment_as_str = None
        from_cl_args_as_list = ['path-from-cl1:pattern-from-cl1']
        got = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        expected = [{'merge_strategy': 'onconflict-ours', 'path': 'path-from-cl1', 'pattern': 'pattern-from-cl1'}]
        self.assertEqual(expected, got)

        from_environment_as_str = None
        from_cl_args_as_list = ['path-from-cl1:pattern-from-cl1', 'path-from-cl2:pattern-from-cl2']
        got = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        expected = [
            {'merge_strategy': 'onconflict-ours', 'path': 'path-from-cl1', 'pattern': 'pattern-from-cl1'},
            {'merge_strategy': 'onconflict-ours', 'path': 'path-from-cl2', 'pattern': 'pattern-from-cl2'}
        ]
        self.assertEqual(expected, got)

        # Switch defaults off by command line.
        from_environment_as_str = None
        from_cl_args_as_list = ['']
        got = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        expected = []
        self.assertEqual(expected, got)

        from_environment_as_str = None
        from_cl_args_as_list = None
        got = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        expected = None
        self.assertEqual(expected, got)


if __name__ == '__main__':
    unittest.main()
