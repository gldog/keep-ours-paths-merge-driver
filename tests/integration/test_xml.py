import filecmp
import pathlib
import unittest

from tests.integration.test_base import TestBase


class TestXml1XPath(TestBase):

    def test_1_xpath(self):
        """

            $ ['git', 'log', '--decorate', '--oneline', '--graph', '--all']
            stdout:
            * ca694fd (HEAD -> ours-branch) Add file pom.xml to branch ours-branch
            | * 661b161 (theirs-branch) Add file pom.xml to branch theirs-branch
            |/
            * 1acf258 (master) Add file pom.xml to branch b'master'
            * f511e60 Add .gitattributes

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

        self.print_commit_graph()

        self.install_merge_driver('-p ./version')

        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'])
        self.exec_cmd(['git', 'status'])
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_01_expected_merged.xml'), 'pom.xml'))

    def test_no_merge_base(self):
        """
        The pom.xml has been added to ours-branch and theirs-branch. It is not present in the base.

            * 7f17260 (HEAD -> ours-branch) Add file pom.xml to branch ours-branch
            | * 374b389 (theirs-branch) Add file pom.xml to branch theirs-branch
            |/
            * 46172bd (master) Add .gitattributes

        The merge-driver can't handle that. And the Git-merge results in a merge-conflict.
        """

        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_01_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_01_ours.xml', 'pom.xml')

        self.print_commit_graph()

        self.install_merge_driver('-p ./version')

        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], expected_exit_code=1)
        self.exec_cmd(['git', 'status'])
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_01_expected_conflicted.xml'), 'pom.xml'))


if __name__ == '__main__':
    unittest.main()
