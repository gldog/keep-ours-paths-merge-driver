import filecmp
import os
import pathlib
import unittest

from tests.integration.test_base import TestBase


class TestXmlPathAndPatternsSettings(TestBase):

    def test_xpaths_given_on_command_line(self):
        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_03_base.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_03_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_03_ours.xml', 'pom.xml')

        self.install_merge_driver('-p ./version ./properties/:.+\\\\.version')

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml'), 'pom.xml'))

    def test_xpaths_given_in_env_variable(self):
        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_03_base.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_03_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_03_ours.xml', 'pom.xml')

        # self.install_merge_driver('-p ./version ./properties/:.+\\\\.version')
        self.install_merge_driver(None)

        env = os.environ.copy()
        env['KOP_MERGE_DRVIER_PATHSPATTERNS'] = './version ./properties/:.+\\.version'
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml'), 'pom.xml'))

    def test_xpaths_empty_list_from_env_variable_disables_merge_driver(self):
        """
        Setting KOP_MERGE_DRVIER_PATHSPATTERNS to '' effectively deactivates the merge-driver. Not really a use case.
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

        self.install_merge_driver(None)

        env = os.environ.copy()
        env['KOP_MERGE_DRVIER_PATHSPATTERNS'] = ''
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], expected_exit_code=1, env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_01_expected_conflicted.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_01_expected_conflicted.xml'), 'pom.xml'))


if __name__ == '__main__':
    unittest.main()
