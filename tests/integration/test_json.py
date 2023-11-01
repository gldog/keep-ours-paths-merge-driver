import filecmp
import os
import pathlib
import unittest

from tests.integration.test_base import TestBase


class TestJson(TestBase):

    def test_no_merge_base(self):
        """
        - Use the default paths_and_patterns, which is an empty set. The path-configs doesn't matter in this test.
        - The package.json has been added to ours-branch and theirs-branch. It is not present in the base.
        - The merge-driver can't handle that and delegates all three files as is to the git file-merge command.
        - The Git-merge results in a merge-conflict.
        - The line-conflicts doesn't matter to this test (as the merge-driver does nothing than delegating).
        """

        self.git_init(file_type='JSON')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'package_01_theirs.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'package_01_ours.json', 'package.json')

        self.print_commit_graph()

        self.install_merge_driver("-t JSON -p 'version'")

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], expected_exit_code=1, env=env)
        self.exec_cmd(['git', 'status'])
        self.assertTrue(
            filecmp.cmp(pathlib.Path(self.resources_path, 'package_01_expected_conflicted.json'), 'package.json'))

    def test_jpaths_given_on_command_line_using_default_merge_strategy(self):
        """
        Use the default merge-strategy, which is "onconflict-ours".
        """

        self.git_init(file_type='JSON')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'package_03_base.json', 'package.json')

        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'package_03_theirs.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'package_03_ours.json', 'package.json')

        self.install_merge_driver("-t JSON -p 'version' 'dependencies.*:@mycompany/.+' -l DEBUG")

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)
        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'package_03_expected_merged.json')).read(),
        #    open('package.json').read())
        self.assertTrue(
            filecmp.cmp(pathlib.Path(self.resources_path, 'package_03_expected_merged.json'), 'package.json'))

    def test_jpaths_given_on_command_line_using_merge_strategy_onconflict_ours(self):
        """
        Set the merge-strategy "onconflict-ours" explicitly (is default).
        """

        self.git_init(file_type='JSON')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'package_03_base.json', 'package.json')

        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'package_03_theirs.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'package_03_ours.json', 'package.json')

        self.install_merge_driver(
            "-t JSON -p 'onconflict-ours:version' 'onconflict-ours:dependencies.*:@mycompany/.+' -l DEBUG"
        )

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)
        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'package_03_expected_merged.json')).read(),
        #    open('package.json').read())
        self.assertTrue(
            filecmp.cmp(pathlib.Path(self.resources_path, 'package_03_expected_merged.json'), 'package.json'))

    def test_jpaths_given_in_env_variable_using_default_merge_strategy(self):
        """
        Use the default merge-strategy, which is "onconflict-ours".
        """

        self.git_init(file_type='JSON')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'package_03_base.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'package_03_theirs.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'package_03_ours.json', 'package.json')

        self.install_merge_driver('-t JSON -l DEBUG')

        env = os.environ.copy()
        env['KOP_MERGE_DRVIER_PATHSPATTERNS'] = 'version dependencies.*:@mycompany/.+'
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)
        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'package_03_expected_merged.json')).read(),
        #    open('package.json').read())
        self.assertTrue(
            filecmp.cmp(pathlib.Path(self.resources_path, 'package_03_expected_merged.json'), 'package.json'))

    def test_jpaths_given_in_env_variable_using_merge_strategy_onconflict_ours(self):
        """
        Use the default merge-strategy, which is "onconflict-ours".
        """

        self.git_init(file_type='JSON')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'package_03_base.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'package_03_theirs.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'package_03_ours.json', 'package.json')

        self.install_merge_driver('-t JSON -l DEBUG')

        env = os.environ.copy()
        env['KOP_MERGE_DRVIER_PATHSPATTERNS'] = 'onconflict-ours:version onconflict-ours:dependencies.*:@mycompany/.+'
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)
        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'package_03_expected_merged.json')).read(),
        #    open('package.json').read())
        self.assertTrue(
            filecmp.cmp(pathlib.Path(self.resources_path, 'package_03_expected_merged.json'), 'package.json'))

    def test_jpaths_given_on_command_line_using_merge_strategy_always_ours(self):
        """
        Set the merge-strategy "always-ours".
        """

        self.git_init(file_type='JSON')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'package_13_base.json', 'package.json')

        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'package_13_theirs.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'package_13_ours.json', 'package.json')

        self.install_merge_driver(
            "-t JSON -p 'always-ours:version' 'always-ours:dependencies.*:@mycompany/(some-app1|some-app2)' -l DEBUG"
        )

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)
        self.exec_cmd(['git', 'status'])
        self.assertEqual(
            open(pathlib.Path(self.resources_path, 'package_13_expected_merged.json')).read(),
            open('package.json').read())
        self.assertTrue(
            filecmp.cmp(pathlib.Path(self.resources_path, 'package_13_expected_merged.json'), 'package.json'))

    def test_jpaths_empty_list_from_env_variable_disables_merge_driver(self):
        """
        Setting KOP_MERGE_DRVIER_PATHSPATTERNS to '' effectively deactivates the merge-driver.
        """

        self.git_init(file_type='JSON')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'package_01_base.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'package_01_theirs.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'package_01_ours.json', 'package.json')

        self.install_merge_driver('-t JSON')

        env = os.environ.copy()
        # This disables the merge dirver.
        env['KOP_MERGE_DRVIER_PATHSPATTERNS'] = ''
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], expected_exit_code=1, env=env)
        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'package_01_expected_conflicted.json')).read(),
        #    open('package.json').read())
        self.assertTrue(
            filecmp.cmp(pathlib.Path(self.resources_path, 'package_01_expected_conflicted.json'), 'package.json'))


if __name__ == '__main__':
    unittest.main()
