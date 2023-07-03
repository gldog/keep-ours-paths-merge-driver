import os
import pathlib
import shutil
import subprocess
import time
import unittest
import zipapp


class TestBase(unittest.TestCase):
    PYTHON_BINARY = 'python3'
    # Name of the subdirectory containing the product-sources.
    APP_SOURCE_DIRNAME = 'keep_ours_paths_merge_driver'
    merge_driver_executable_path = None
    abs_project_root_path = None
    current_test_name = None
    current_test_dir = None
    # Dependent on the git version or config settings the default branch-name is either "master" or something else,
    # e.g. "main".
    main_branch_name = None

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
        self.abs_project_root_path = os.getcwd()
        # There is the relation of 1 test-module to 1 subdirectory in resources.
        self.resources_path = pathlib.Path(self.abs_project_root_path, 'tests', 'integration', 'resources',
                                           self.module_name)
        self.temp_test_dir_path = pathlib.Path(self.abs_project_root_path, 'target',
                                               f'{time.time()}-{self.current_test_name}')
        self.gitrepo_path = pathlib.Path(self.temp_test_dir_path, 'testrepo')
        os.makedirs(self.gitrepo_path)

        os.chdir(self.gitrepo_path)

        self.merge_driver_executable_path = pathlib.Path(self.abs_project_root_path, self.temp_test_dir_path,
                                                         self.APP_SOURCE_DIRNAME + '.pyz')

        # Create a pyz and place it into the 'target' directory.
        self.create_pyz()

    def tearDown(self) -> None:
        os.chdir(self.abs_project_root_path)

    def print_commit_graph(self) -> None:
        self.exec_cmd(['git', 'log', '--decorate', '--oneline', '--graph', '--all'])

    def git_init(self) -> None:
        self.exec_cmd(['git', '--version'])
        self.exec_cmd(['git', 'init'])

        with open('./.gitattributes', 'w') as f:
            f.write('pom.xml merge=jos-merge-driver')

        self.exec_cmd(['git', 'add', '.'])
        self.exec_cmd(['git', 'commit', '-m', 'Add .gitattributes'])
        self.exec_cmd(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        # The main branch does exist after the first commit.
        self.main_branch_name = self.get_main_branch_name()

    def prepare_3_branches__OLD(self):
        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.copy_file_to_existing_branch_and_commit(self.main_branch_name, 'pom_01_base.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'theirs-branch'])
        self.copy_file_to_existing_branch_and_commit('theirs-branch', 'pom_01_theirs.xml', 'pom.xml')

        self.exec_cmd(['git', 'checkout', self.main_branch_name])
        self.exec_cmd(['git', 'checkout', '-b', 'ours-branch'])
        self.copy_file_to_existing_branch_and_commit('ours-branch', 'pom_01_ours.xml', 'pom.xml')

        self.print_commit_graph()

    def exec_cmd(self, cmd, expected_exit_code=0):
        print(f"$ {cmd}")
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"stdout:\n{r.stdout.decode()}")
        print(f"stderr:\n{r.stderr.decode()}")
        if r.returncode != expected_exit_code:
            r.check_returncode()
        return r

    def install_merge_driver(self, paths_and_patterns_cl_option) -> None:
        """
        Install custom-merge-driver. Git-configs are not checked in.

        :param paths_and_patterns_cl_option: E.g. '-p ./version'
        """
        merge_driver_params = f'-O %O -A %A -B %B'
        if paths_and_patterns_cl_option:
            merge_driver_params += f' {paths_and_patterns_cl_option}'
        merge_driver_path_with_parameters = \
            f'{self.PYTHON_BINARY} {self.merge_driver_executable_path} {merge_driver_params}'
        cmd = ['git', 'config', '--local', 'merge.jos-merge-driver.driver', merge_driver_path_with_parameters]
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

    def create_pyz(self) -> None:
        """
        Make the PYZ-file.
        All files in the project-dir are included.

        Prepare:

            # Collect dependency-information.
            $ pip3 freeze > requirements.txt
            # Add dependencies to the project-dir.
            $ python -m pip install -r requirements.txt --target  keep_ours_paths_merge_driver
        """
        # self.assertTrue(False, f"{os.getcwd()}")
        # self.assertTrue(False, f"{os.listdir(self.APP_SOURCE_DIRNAME)}")
        zipapp.create_archive(source=f'{self.abs_project_root_path}/{self.APP_SOURCE_DIRNAME}',
                              target=self.merge_driver_executable_path)
