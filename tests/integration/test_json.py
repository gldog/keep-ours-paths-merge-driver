import filecmp
import os
import pathlib
import unittest

from tests.integration.test_base import TestBase


class TestJson1JPath(TestBase):

    def test_default_paths_and_patterns(self):
        """
        - Use the default paths_and_patterns, which is './version'.
        - Only the <version/> tag line is conflicted.
        """

        self.git_init(type='JSON')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'package_01_base.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'package_01_theirs.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'package_01_ours.json', 'package.json')

        self.print_commit_graph()

        # No -p option leads to the default-paths-setting.
        self.install_merge_driver('-t JSON')

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)
        self.exec_cmd(['git', 'status'])
        self.assertTrue(
            filecmp.cmp(pathlib.Path(self.resources_path, 'package_01_expected_merged.json'), 'package.json'))

    def test_no_merge_base(self):
        """
        - Use the default paths_and_patterns, which is 'version'.
        - The package.json has been added to ours-branch and theirs-branch. It is not present in the base.
        - The merge-driver can't handle that and delegates all three files as is to the git file-merge command.
        - The Git-merge results in a merge-conflict.
        - The line-conflicts doesn't matter to this test (as the merge-driver does nothing than delegating).
        """

        self.git_init(type='JSON')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'package_01_theirs.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'package_01_ours.json', 'package.json')

        self.print_commit_graph()

        self.install_merge_driver('-t JSON -p version')

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], expected_exit_code=1, env=env)
        self.exec_cmd(['git', 'status'])
        self.assertTrue(
            filecmp.cmp(pathlib.Path(self.resources_path, 'package_01_expected_conflicted.json'), 'package.json'))


if __name__ == '__main__':
    unittest.main()
