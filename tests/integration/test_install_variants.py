import filecmp
import os
import pathlib
import unittest

from tests.integration.test_base import TestBase


class TestInstallVariants(TestBase):
    """
    From "gitattributes - Defining attributes per path" https://git-scm.com/docs/gitattributes:

        When deciding what attributes are assigned to a path, Git consults $GIT_DIR/info/attributes file (which has the
        highest precedence), .gitattributes file in the same directory as the path in question, and its parent
        directories up to the toplevel of the work tree (the further the directory that contains .gitattributes is from
        the path in question, the lower its precedence). Finally global and system-wide files are considered (they have
        the lowest precedence).

    This test it not really a test. It demonstrates ways to use attribues.
    """

    def setUp(self) -> None:
        super(TestInstallVariants, self).setUp()
        self.resources_path = pathlib.Path(self.abs_project_root_path, 'tests', 'integration', 'resources', 'test_xml')

    def test_use_dot_gitattributes(self):
        """
        This is a copy of test_xml.test_xpaths_given_on_command_line_using_default_merge_strategy()
        It is copied here to have a direct comparison to the varian in test_use_gitdir_info_attribues().

        self.GITATTRIBUTES_DOTGITATTRIBUTES is the default, but it is given explicitly for better readability.
        """

        self.git_init(attributes_path=self.GITATTRIBUTES_DOTGITATTRIBUTES)

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_03_base.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_03_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_03_ours.xml', 'pom.xml')

        self.install_merge_driver("-p './version' './properties/:(some-app1|some-app2)[.]version'")

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml'), 'pom.xml'))

    def test_use_gitdir_info_attribues(self):
        # Create a test-repo, with a GIT_DIR/info/attributes instead of the default .gitattribues.
        self.git_init(attributes_path=self.GITATTRIBUTES_DOTGIT_INFO_ATTRIBUTES)

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_03_base.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_03_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_03_ours.xml', 'pom.xml')

        self.install_merge_driver("-p './version' './properties/:(some-app1|some-app2)[.]version'")

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml'), 'pom.xml'))


if __name__ == '__main__':
    unittest.main()
