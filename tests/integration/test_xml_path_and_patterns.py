import filecmp
import pathlib
import unittest

from tests.integration.test_base import TestBase


class TestXmlPathAndPatterns(TestBase):

    def test_default_xpaths(self):
        """
        The default for the XML path_and_pattern setting is:

            DEFAULT_PATH_AND_PATTERNS = {
                './version': None,
                './properties/revision': None,
                './properties/': '.+\\.version'
            }

        """

        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_01_base.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_01_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_01_ours.xml', 'pom.xml')

        paths_and_patterns = None
        self.install_merge_driver(paths_and_patterns)

        # Don't know why this is conflicted. kdiff3 can merge this.
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], expected_exit_code=1)
        self.exec_cmd(['git', 'status'])
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_01_expected_conflicted.xml'), 'pom.xml'))

    def test_no_xpaths(self):
        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_01_base.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_01_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_01_ours.xml', 'pom.xml')

        paths_and_patterns = "''"
        self.install_merge_driver(paths_and_patterns)

        # Don't know why this is conflicted. kdiff3 can merge this.
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], expected_exit_code=1)
        self.exec_cmd(['git', 'status'])
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_02_expected_conflicted.xml'), 'pom.xml'))


if __name__ == '__main__':
    unittest.main()
