import unittest

import keep_ours_paths_merge_driver.config as config


class TestConfigSplitIntoPathAndPattern(unittest.TestCase):

    def test_split_into_path_and_pattern(self):
        path_and_pattern_str = None
        path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('', path)
        self.assertEqual('', pattern)

        path_and_pattern_str = ''
        path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('', path)
        self.assertEqual('', pattern)

        path_and_pattern_str = 'the-path:the-pattern'
        path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('the-path', path)
        self.assertEqual('the-pattern', pattern)

        path_and_pattern_str = ' the-path : the-pattern '
        path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('the-path', path)
        self.assertEqual('the-pattern', pattern)

        path_and_pattern_str = 'the-path'
        path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('the-path', path)
        self.assertEqual('', pattern)

        path_and_pattern_str = 'the-path:'
        path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)
        self.assertEqual('the-path', path)
        self.assertEqual('', pattern)

        with self.assertRaises(ValueError):
            path_and_pattern_str = ':the-pattern'
            path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)

        with self.assertRaises(ValueError):
            path_and_pattern_str = ':'
            path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)

        with self.assertRaises(ValueError):
            path_and_pattern_str = 'the-path::the-pattern'
            path, pattern = config.split_into_path_and_pattern(path_and_pattern_str)


if __name__ == '__main__':
    unittest.main()
