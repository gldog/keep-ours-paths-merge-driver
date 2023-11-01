import os
import pathlib
import shutil
import subprocess
import time
import unittest


class TestBase(unittest.TestCase):
    TESTSUITE_START_TIME = str(time.time())
    PYTHON_BINARY = 'python3'
    # Name of the subdirectory containing the sources to build the zippapp from.
    APP_SOURCE_DIRNAME = 'keep_ours_paths_merge_driver'
    GITATTRIBUTES_DOTGITATTRIBUTES = './.gitattributes'
    GITATTRIBUTES_DOTGIT_INFO_ATTRIBUTES = './.git/info/attributes'
    merge_driver_executable_path = None
    abs_project_root_path = os.getcwd()
    current_test_name = None
    current_test_dir = None
    # Dependent on the git version or config settings the default branch-name is either "master" or something else,
    # e.g. "main".
    main_branch_name = None
    is_zipapp_built = False

    def setUp(self) -> None:
        # self.assertTrue(False, f"CWD:{os.getcwd()}")
        # When called form the project-root, id() is something like:
        #       integration.test_xml.TestXml1XPath.test_1_xpath
        # or
        #       tests.integration.test_xml.TestXml1XPath.test_1_xpath
        # We're interested in the part 'test_xml'. Count from the right side.
        self.current_test_name = self.id()
        self.module_name = self.id().split('.')[-3]
        print(f"self.id(): {self.id()}; module: {self.module_name}")
        # self.abs_project_root_path = os.getcwd()
        # There is the relation of 1 test-module to 1 subdirectory in resources.
        self.resources_path = pathlib.Path(self.abs_project_root_path, 'tests', 'integration', 'resources',
                                           self.module_name)
        self.abs_testsuite_path = pathlib.Path(self.abs_project_root_path, 'target',
                                               f'testsuite-{self.TESTSUITE_START_TIME}')
        self.abs_test_dir_path = pathlib.Path(self.abs_testsuite_path, self.current_test_name)
        self.gitrepo_path = pathlib.Path(self.abs_test_dir_path, 'testrepo')
        os.makedirs(self.gitrepo_path)

        os.chdir(self.gitrepo_path)

        self.merge_driver_executable_path = pathlib.Path(self.abs_testsuite_path, self.APP_SOURCE_DIRNAME + '.pyz')

        # Create a pyz and place it into the 'target' directory. Create it only once per test-suite.
        if not TestBase.is_zipapp_built:
            self.create_zipapp()
            TestBase.is_zipapp_built = True

    def tearDown(self) -> None:
        os.chdir(self.abs_project_root_path)

    def print_commit_graph(self) -> None:
        self.exec_cmd(['git', 'log', '--decorate', '--oneline', '--graph', '--all'])

    def git_init(self, file_type='XML', attributes_path=GITATTRIBUTES_DOTGITATTRIBUTES) -> None:
        """
        Cerate a git-repo. Create also a .gitattributes file in case file_type is XML or JSON.
        :param file_type: XMK (default), JSON, NONE.
        :param attributes_path: Either ./.gitattributes (GITATTRIBUTES_DOTGITATTRIBUTES)
                or ./.git/info/attributes (GITATTRIBUTES_DOTGIT_INFO_ATTRIBUTES).
        """

        self.exec_cmd(['git', '--version'])
        self.exec_cmd(['git', 'init'])

        if attributes_path in [self.GITATTRIBUTES_DOTGITATTRIBUTES, self.GITATTRIBUTES_DOTGIT_INFO_ATTRIBUTES]:
            # The "git init" has created the dirctory .git/info, which is needed for .git/info/attribues.
            with open(attributes_path, 'w') as f:
                if file_type == 'XML':
                    f.write('pom.xml merge=my-merge-driver')
                elif file_type == 'JSON':
                    f.write('package.json merge=my-merge-driver')
                else:
                    self.fail("Expect type 'XML' or 'JSON'")

            # The .gitattributes is checked-in. The .git/info/atttribues not.
            if attributes_path is self.GITATTRIBUTES_DOTGITATTRIBUTES:
                self.exec_cmd(['git', 'add', '.'])
                self.exec_cmd(['git', 'commit', '-m', 'Add .gitattributes'])
            else:
                self.exec_cmd(['git', 'commit', '--allow-empty', '-m', 'Initial'])
        else:
            self.fail(f"Unexpected attributes_path: {attributes_path}")

        self.exec_cmd(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        # The main branch does exist after the first commit.
        self.main_branch_name = self.get_main_branch_name()

    def exec_cmd(self, cmd, env=None, expected_exit_code=0, stderr_to_stdout=False):
        print(f"$ {cmd}")
        if stderr_to_stdout:
            r = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print(f"stdout:\n{r.stdout.decode()}")
        else:
            r = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"stdout:\n{r.stdout.decode()}")
            print(f"stderr:\n{r.stderr.decode()}")
        if r.returncode != expected_exit_code:
            r.check_returncode()
        return r

    def install_merge_driver(self, options) -> None:
        """
        Install custom-merge-driver. Git-configs are not checked in.

        :param options: E.g. '-p ./version'
        """
        merge_driver_params = '-O %O -A %A -B %B -P ./%P'
        if options:
            merge_driver_params += f' {options}'
        merge_driver_path_with_parameters = \
            f'{self.PYTHON_BINARY} {self.merge_driver_executable_path} {merge_driver_params}'
        cmd = ['git', 'config', '--local', 'merge.my-merge-driver.driver', merge_driver_path_with_parameters, '2>&1']
        self.exec_cmd(cmd)

    def get_main_branch_name(self) -> str:
        """
        Dependent on the git version or config settings the default branch-name is either "master" or something else,
        e.g. "main".

        :return: The main-branch-name.
        """
        r = self.exec_cmd(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        # strip(): Remove trailing newline.
        branch_name = r.stdout.strip()
        return branch_name.decode()

    def copy_file_to_existing_branch_and_commit(self, branch_name, src_file_name, dst_file_name) -> None:
        self.exec_cmd(['git', 'status'])
        self.exec_cmd(['git', 'checkout', branch_name])
        src = pathlib.Path(self.resources_path, src_file_name)
        dst = './' + dst_file_name
        # print(f"copy_file_to_existing_branch_and_commit(); src: {src}; dst: {dst}")
        # print(f"copy_file_to_existing_branch_and_commit(); self.testpoms_path: {self.resources_path}")
        shutil.copyfile(src, dst)
        self.exec_cmd(['git', 'add', '.'])
        self.exec_cmd(['git', 'commit', '-m', f'Add file {dst_file_name} to branch {branch_name}'])
        self.exec_cmd(['git', 'status'])

    def create_zipapp(self) -> None:
        # Create the zippapp with the dependencies included.
        self.exec_cmd(['shiv', '-c', self.APP_SOURCE_DIRNAME, '-o', self.merge_driver_executable_path,
                       '-r', self.abs_project_root_path + '/requirements.txt', self.abs_project_root_path])

        # This was the native way for creating the zippapp. But that didn't include the dependencies.
        # zipapp.create_archive(source=f'{self.abs_project_root_path}/{self.APP_SOURCE_DIRNAME}',
        #                      target=self.merge_driver_executable_path)
