import os
import pathlib
import unittest

from tests.integration.test_base import TestBase


class TestJsonPathAndPatternsSettings(TestBase):

    def test_jpaths_given_on_command_line(self):
        self.git_init(type='JSON')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'package_03_base.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'package_03_theirs.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'package_03_ours.json', 'package.json')

        self.install_merge_driver('-t JSON -p version dependencies:@mycompany/.+')

        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'])
        self.exec_cmd(['git', 'status'])
        self.assertEqual(
            open(pathlib.Path(self.resources_path, 'package_03_expected_merged.json')).read(),
            open('package.json').read())
        # self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_01_expected_conflicted.xml'), 'pom.xml'))

    def test_fpaths_given_in_env_variable(self):
        self.git_init(type='JSON')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'package_03_base.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'package_03_theirs.json', 'package.json')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'package_03_ours.json', 'package.json')

        self.install_merge_driver(None)

        env = os.environ.copy()
        env['KOP_MERGE_DRVIER_PATHSPATTERNS'] = 'version dependencies:@mycompany/.+'
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)
        self.exec_cmd(['git', 'status'])
        self.assertEqual(
            open(pathlib.Path(self.resources_path, 'package_03_expected_merged.json')).read(),
            open('package.json').read())
        # self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_01_expected_conflicted.xml'), 'pom.xml'))

    def test_jpaths_empty_list_from_env_variable_disables_merge_driver(self):
        """
        Setting KOP_MERGE_DRVIER_PATHSPATTERNS to '' effectively deactivates the merge-driver. Not really a use case.
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

        self.install_merge_driver('-t JSON')

        env = os.environ.copy()
        env['KOP_MERGE_DRVIER_PATHSPATTERNS'] = ''
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], expected_exit_code=1, env=env)
        self.exec_cmd(['git', 'status'])
        self.assertEqual(
            open(pathlib.Path(self.resources_path, 'package_01_expected_conflicted.json')).read(),
            open('package.json').read())
        # self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_01_expected_conflicted.xml'), 'pom.xml'))


if __name__ == '__main__':
    unittest.main()
