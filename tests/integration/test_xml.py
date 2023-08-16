import filecmp
import os
import pathlib
import unittest

from tests.integration.test_base import TestBase


class TestXml1XPath(TestBase):

    def test_no_merge_base(self):
        """
        - Use the default paths_and_patterns, which is './version'.
        - The pom.xml has been added to ours-branch and theirs-branch. It is not present in the base.
        - The merge-driver can't handle that and delegates all three files as is to the git file-merge command.
        - The Git-merge results in a merge-conflict.
        - The line-conflicts doesn't matter to this test (as the merge-driver does nothing than delegating).
        """

        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_01_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_01_ours.xml', 'pom.xml')

        self.print_commit_graph()

        # None leads to omit the -p option, which leads to the default-paths-setting.
        self.install_merge_driver(None)

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], expected_exit_code=1, env=env)
        self.exec_cmd(['git', 'status'])

        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_01_expected_conflicted.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_01_expected_conflicted.xml'), 'pom.xml'))


if __name__ == '__main__':
    unittest.main()
