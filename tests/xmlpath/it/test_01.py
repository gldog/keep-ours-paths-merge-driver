import filecmp
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest


class TestMyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.cwd = os.getcwd()
        print(f"CWD: {self.cwd}")

    def test_1_xpath(self):
        # Create temporary git repo in temp-dir.
        with tempfile.TemporaryDirectory() as tmpdirname:
            os.chdir(tmpdirname)

            cmd = ['git', 'init']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'status']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            # Create top-level pom.xml.
            shutil.copy(pathlib.Path(self.cwd, 'resources', 'it01', 'test_1_xpath', 'pom_o.xml'),
                        pathlib.Path(tmpdirname, 'pom.xml'))
            cmd = ['git', 'add', '.']
            print(f"$ {cmd}")

            r = subprocess.run(cmd)
            cmd = ['git', 'commit', '-m', 'Initial']
            print(f"$ {cmd}")

            r = subprocess.run(cmd)
            cmd = ['git', 'log']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            # Install custom-merge-driver. Git-configs are not checked in.
            merge_driver_params = '%O %A %B ./properties/revision'
            merge_driver_path_with_parameters = \
                f'{pathlib.Path(self.cwd, "..", "src", "keep_ours_xml_paths_merge_driver.py")} ' \
                + merge_driver_params
            cmd = ['git', 'config', '--local', 'merge.custom-merge-driver.driver',
                   merge_driver_path_with_parameters]
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            # Create branch.
            cmd = ['git', 'checkout', '-b', 'f1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            shutil.copy(pathlib.Path(self.cwd, 'resources', 'it01', 'test_1_xpath', 'pom_a.xml'),
                        pathlib.Path(tmpdirname, 'pom.xml'))

            cmd = ['git', 'add', '.']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)
            cmd = ['git', 'commit', '-m', 'Mod. pom.xml on branch f1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            # cmd = ['cat', 'pom.xml']
            # print(f"$ {cmd}")
            # r = subprocess.run(cmd)

            cmd = ['git', 'checkout', 'master']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'checkout', '-b', 'release/r1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            shutil.copy(pathlib.Path(self.cwd, 'resources', 'it01', 'test_1_xpath', 'pom_b.xml'),
                        pathlib.Path(tmpdirname, 'pom.xml'))
            cmd = ['git', 'add', '.']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'commit', '-m', 'Mod. pom.xml on branch release/r1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'checkout', 'f1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            # Check: Does a merge work with a modified .gitattributes?
            with open('.gitattributes', 'w') as f:
                f.write(f'pom.xml merge=custom-merge-driver')

            cmd = ['git', 'merge', '--no-ff', '--no-edit', 'release/r1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'status']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'log', '--all', '--decorate', '--oneline', '--graph']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            self.assertTrue(
                filecmp.cmp(
                    pathlib.Path(self.cwd, 'resources', 'it01', 'test_1_xpath', 'pom_expected.xml'),
                    'pom.xml'))

    def test_4_xpaths(self):
        # Create temporary git repo in temp-dir.
        with tempfile.TemporaryDirectory() as tmpdirname:
            os.chdir(tmpdirname)

            cmd = ['git', 'init']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'status']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            # Create top-level pom.xml.
            shutil.copy(pathlib.Path(self.cwd, 'resources', 'it01', 'test_4_xpaths', 'pom_o.xml'),
                        pathlib.Path(tmpdirname, 'pom.xml'))
            cmd = ['git', 'add', '.']
            print(f"$ {cmd}")

            r = subprocess.run(cmd)
            cmd = ['git', 'commit', '-m', 'Initial']
            print(f"$ {cmd}")

            r = subprocess.run(cmd)
            cmd = ['git', 'log']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            # Install custom-merge-driver. Git-configs are not checked in.
            merge_driver_params = '%O %A %B' + './version,./parent/version' + \
                                  ',./properties/revision,./properties/spring.version'
            merge_driver_path_with_parameters = \
                f'{pathlib.Path(self.cwd, "..", "src", "keep_ours_xml_paths_merge_driver.py")} ' \
                + merge_driver_params
            cmd = ['git', 'config', '--local', 'merge.custom-merge-driver.driver',
                   merge_driver_path_with_parameters]
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            # Create branch.
            cmd = ['git', 'checkout', '-b', 'f1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            shutil.copy(pathlib.Path(self.cwd, 'resources', 'it01', 'test_4_xpaths', 'pom_a.xml'),
                        pathlib.Path(tmpdirname, 'pom.xml'))

            cmd = ['git', 'add', '.']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)
            cmd = ['git', 'commit', '-m', 'Mod. pom.xml on branch f1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            # cmd = ['cat', 'pom.xml']
            # print(f"$ {cmd}")
            # r = subprocess.run(cmd)

            cmd = ['git', 'checkout', 'master']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'checkout', '-b', 'release/r1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            shutil.copy(pathlib.Path(self.cwd, 'resources', 'it01', 'test_4_xpaths', 'pom_b.xml'),
                        pathlib.Path(tmpdirname, 'pom.xml'))
            cmd = ['git', 'add', '.']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'commit', '-m', 'Mod. pom.xml on branch release/r1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'checkout', 'f1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            # Check: Does a merge work with a modified .gitattributes?
            with open('.gitattributes', 'w') as f:
                f.write(f'pom.xml merge=custom-merge-driver')

            cmd = ['git', 'merge', '--no-ff', '--no-edit', 'release/r1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'status']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'log', '--all', '--decorate', '--oneline', '--graph']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            self.assertTrue(
                filecmp.cmp(
                    pathlib.Path(self.cwd, 'resources', 'it01', 'test_4_xpaths',
                                 'pom_expected.xml'),
                    'pom.xml'))


if __name__ == '__main__':
    unittest.main()
