import unittest

import keep_ours_paths_merge_driver.config as config


class TestConfigSplitIntoPathAndPattern(unittest.TestCase):

    def test_split_into_path_and_pattern_using_default_merge_strategy(self):
        path_and_pattern_str = None
        merge_strategy, path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('onconflict-ours', merge_strategy)
        self.assertEqual('', path)
        self.assertEqual('', pattern)

        path_and_pattern_str = ''
        merge_strategy, path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('onconflict-ours', merge_strategy)
        self.assertEqual('', path)
        self.assertEqual('', pattern)

        path_and_pattern_str = 'the-path:the-pattern'
        merge_strategy, path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('onconflict-ours', merge_strategy)
        self.assertEqual('the-path', path)
        self.assertEqual('the-pattern', pattern)

        path_and_pattern_str = ' the-path : the-pattern '
        merge_strategy, path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('onconflict-ours', merge_strategy)
        self.assertEqual('the-path', path)
        self.assertEqual('the-pattern', pattern)

        path_and_pattern_str = 'the-path'
        merge_strategy, path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('onconflict-ours', merge_strategy)
        self.assertEqual('the-path', path)
        self.assertEqual('', pattern)

        path_and_pattern_str = 'the-path:'
        merge_strategy, path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('onconflict-ours', merge_strategy)
        self.assertEqual('the-path', path)
        self.assertEqual('', pattern)

        path_and_pattern_str = ':'
        merge_strategy, path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('onconflict-ours', merge_strategy)
        self.assertEqual('', path)
        self.assertEqual('', pattern)

    def test_split_into_path_and_pattern_using_explicite_merge_strategy(self):
        path_and_pattern_str = 'onconflict-ours:the-path:the-pattern'
        merge_strategy, path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('onconflict-ours', merge_strategy)
        self.assertEqual('the-path', path)
        self.assertEqual('the-pattern', pattern)

        path_and_pattern_str = 'always-ours:the-path:the-pattern'
        merge_strategy, path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('always-ours', merge_strategy)
        self.assertEqual('the-path', path)
        self.assertEqual('the-pattern', pattern)

        with self.assertRaises(ValueError):
            path_and_pattern_str = 'invalid-merge-strategy:the-path:the-pattern'
            config.split_into_path_and_pattern(path_and_pattern_str)

    def test_split_into_path_and_pattern_using_explicite_separator(self):
        path_and_pattern_str = 'onconflict-ours###the-path###the-pattern'
        separator = '###'
        merge_strategy, path, pattern = config.split_into_path_and_pattern(
            path_and_pattern_str, separator)
        self.assertEqual('onconflict-ours', merge_strategy)
        self.assertEqual('the-path', path)
        self.assertEqual('the-pattern', pattern)


if __name__ == '__main__':
    unittest.main()
