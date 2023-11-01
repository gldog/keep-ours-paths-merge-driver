import filecmp
import os
import pathlib
import unittest

from tests.integration.test_base import TestBase


class TestXml(TestBase):

    def test_no_baseversion_results_in_mergedriver_not_called(self):
        """
        - Use the default paths_and_patterns, which is an empty set. The path-configs doesn't matter in this test.
        - The pom.xml has been added to ours-branch and theirs-branch. It is not present in the base.
        - The merge-driver can't handle that and delegates all three files as-is to the git file-merge command.
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

    def test_xpaths_given_on_command_line_using_default_merge_strategy(self):
        """
        Use the default merge-strategy, which is "onconflict-ours".
        """

        self.git_init()

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

    def test_xpaths_given_on_command_line_using_merge_strategy_onconflict_ours(self):
        """
        Set the merge-strategy "onconflict-ours" explicitly (is default).
        """

        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_03_base.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_03_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_03_ours.xml', 'pom.xml')

        self.install_merge_driver(
            "-p 'onconflict-ours:./version' 'onconflict-ours:./properties/:(some-app1|some-app2)[.]version'"
        )

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml'), 'pom.xml'))

    def test_xpaths_given_in_env_var_using_default_merge_strategy_onconflict_ours(self):
        """
        Use the default merge-strategy, which is "onconflict-ours".
        """

        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_03_base.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_03_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_03_ours.xml', 'pom.xml')

        self.install_merge_driver(None)

        env = os.environ.copy()
        env['KOP_MERGE_DRVIER_PATHSPATTERNS'] = './version ./properties/:(some-app1|some-app2)[.]version'
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml'), 'pom.xml'))

    def test_xpaths_given_in_env_var_using_merge_strategy_onconflict_ours(self):
        """
        Set the merge-strategy "onconflict-ours" explicitly (is default).
        """

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
        env['KOP_MERGE_DRVIER_PATHSPATTERNS'] = \
            'onconflict-ours:./version onconflict-ours:./properties/:(some-app1|some-app2)[.]version'
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml'), 'pom.xml'))

    def test_xpaths_given_on_command_line_using_merge_strategy_always_ours(self):
        """
        Set the merge-strategy "always-ours".
        No line/hunk conflict.
        """

        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_13_base.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_13_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_13_ours.xml', 'pom.xml')

        self.install_merge_driver(
            "-p 'always-ours:./version' 'always-ours:./properties/:(some-app1|some-app2)[.]version' -l DEBUG -o"
        )

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_13_expected_merged.xml'), 'pom.xml'))

    def test_xpaths_given_on_command_line_using_both_merge_strategies(self):
        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_14_base.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_14_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_14_ours.xml', 'pom.xml')

        self.install_merge_driver(
            "-p 'always-ours:./version' 'onconflict-ours:./properties/:(some-app1|some-app2)[.]version' -l DEBUG -o"
        )

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_14_expected_merged.xml'), 'pom.xml'))

    def test_xpaths_empty_config_from_env_var_disables_merge_driver(self):
        """
        Setting KOP_MERGE_DRVIER_PATHSPATTERNS to '' effectively deactivates the merge-driver.
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

        # This config has no effect, the empty config from env-var takes precedence.
        self.install_merge_driver("-p './version' './properties/:(some-app1|some-app2)[.]version'")

        env = os.environ.copy()
        env['KOP_MERGE_DRVIER_PATHSPATTERNS'] = ''
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], expected_exit_code=1, env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_01_expected_conflicted.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_01_expected_conflicted.xml'), 'pom.xml'))

    def test_separator(self):
        """
        The values of parameter -p are the paths, optionally with the merge-strategy and the pattern.
        The default separtor between them is the colon ':'. Example:
            -p ''./properties/:(some-app1|some-app2)[.]version'
        But the colon is also used in XPath, it is the separator between a namespace and a tag.
        If the colon shall be used in XPath, -s gives an alternative separator.
        """

        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_03_base.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_03_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_03_ours.xml', 'pom.xml')

        self.install_merge_driver("-s '###' -p './version' './properties/###(some-app1|some-app2)[.]version'")

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_03_expected_merged.xml'), 'pom.xml'))

    def test_demonstrate_theirs_win_despite_mergestrategy_alwaysours(self):
        """
        Git calls a merge driver only in case of a 3-way-merge.
        In this test, theirs pom.xml has changed, but ours pom.xml hasn't changed.
        A used expects ours /project/version to be kept, but Git won't call the merge driver. The merge result is theirs.
        """

        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_21_base.xml', 'pom.xml')
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'any_file_base.text', 'any_file.text')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_21_theirs.xml', 'pom.xml')
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'any_file_theirs.text', 'any_file.text')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        # The following line has no effect, as Git notice "nothing to commit, working tree clean".
        # self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_21_ours.xml', 'pom.xml')
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'any_file_ours.text', 'any_file.text')

        self.install_merge_driver("-p 'always-ours:./version'")

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        # The output of the following merge is:
        #       Merge made by the 'ort' strategy.
        #        pom.xml | 2 +-
        #        1 file changed, 1 insertion(+), 1 deletion(-)
        # The pom.xml hasn't been merged!
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        # self.assertEqual(
        #    open(pathlib.Path(self.resources_path, 'pom_21_expected_merged.xml')).read(), open('pom.xml').read())
        self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_21_theirs.xml'), 'pom.xml'))

    def test_prevent_theirs_win_when_no_change_on_ours_by_comment_line(self):
        """
        Git calls a merge driver only in case of a 3-way-merge.
        In this test, theirs pom.xml has changed, but ours pom.xml hasn't changed. Without any further action, Git won't
        call the merge driver.
        But a dummy-change on ours pom.xml just before the merge makes the merge a 3-way-merge, and Gitt triggers
        the merge driver.
        """

        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_21_base.xml', 'pom.xml')
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'any_file_base.text', 'any_file.text')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_21_theirs.xml', 'pom.xml')
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'any_file_theirs.text', 'any_file.text')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'any_file_ours.text', 'any_file.text')

        self.install_merge_driver("-p 'always-ours:./version'")

        # Make a dummy-change on ours pom.xml to let Git trigger the merge driver.
        # The dummy-change initially should be an empty line at the end of the file, but my IDE squeezes trailing empty
        # lines. So the change is an XML comment before the last closing tag (the comment must be inside of the
        # document).
        dummy_text = 'Dummy-change to let Git trigger the merge driver'
        with open('pom.xml', 'r') as f:
            file_content = f.read()
            file_content = file_content.replace('</project>', f'<!-- {dummy_text} -->\n</project>')
        with open('pom.xml', 'w') as f:
            f.write(file_content)
        self.exec_cmd(['git', 'commit', '-am', f'<!-- {dummy_text} -->'])

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        # The output of the following merge is:
        #       Merge made by the 'ort' strategy.
        #        pom.xml | 2 +-
        #        1 file changed, 1 insertion(+), 1 deletion(-)
        # The pom.xml hasn't been merged!
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        self.assertEqual(
            open(pathlib.Path(self.resources_path, 'pom_21_expected_merged.xml')).read(), open('pom.xml').read())
        # self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_21_expected_merged.xml'), 'pom.xml'))

    def test_prevent_theirs_win_when_no_change_on_ours_by_tagline(self):
        """
        Git calls a merge driver only in case of a 3-way-merge.
        In this test, ours pom.xml hasn't changed. Git won't call the merge driver.
        But a  dummy-change on pom.xml triggers Git calling the merge driver.
        """

        self.git_init()

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_22_base.xml', 'pom.xml')
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'any_file_base.text', 'any_file.text')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_22_theirs.xml', 'pom.xml')
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'any_file_theirs.text', 'any_file.text')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'any_file_ours.text', 'any_file.text')

        self.install_merge_driver("-p 'always-ours:./version'")

        # Make a dummy-change on ours pom.xml to let Git trigger the merge driver.
        with open('pom.xml', 'r') as f:
            file_content = f.read()
            file_content = file_content.replace('(12345)', '(abcde)')
        with open('pom.xml', 'w') as f:
            f.write(file_content)
        self.exec_cmd(['git', 'commit', '-am', f'Dummy-change to let Git trigger the merge driver'])

        env = os.environ.copy()
        env['SHIV_ROOT'] = str(pathlib.Path(self.abs_project_root_path, 'target', 'shiv'))
        self.exec_cmd(['git', 'merge', '--no-ff', '--no-edit', 'theirs-branch'], env=env)

        self.exec_cmd(['git', 'status'])
        self.assertEqual(
            open(pathlib.Path(self.resources_path, 'pom_22_expected_merged.xml')).read(), open('pom.xml').read())
        # self.assertTrue(filecmp.cmp(pathlib.Path(self.resources_path, 'pom_21_expected_merged.xml'), 'pom.xml'))


if __name__ == '__main__':
    unittest.main()
