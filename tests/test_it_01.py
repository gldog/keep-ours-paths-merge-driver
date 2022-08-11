import filecmp
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest


class MyTestCase(unittest.TestCase):

    def test_a(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            cwd = os.getcwd()
            print(f"CWD: {cwd}")
            os.chdir(tmpdirname)
            cmd = ['git', 'init']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)
            cmd = ['git', 'status']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)
            shutil.copy(pathlib.Path(cwd, 'resources', 'it01', 'pom_o.xml'), pathlib.Path(tmpdirname, 'pom.xml'))
            cmd = ['git', 'add', '.']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)
            cmd = ['git', 'commit', '-m', 'Initial']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)
            cmd = ['git', 'log']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            #cmd = ['cat', 'pom.xml']
            #print(f"$ {cmd}")
            #r = subprocess.run(cmd)

            cmd = ['git', 'checkout', '-b', 'f1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)
            shutil.copy(pathlib.Path(cwd, 'resources', 'it01', 'pom_a.xml'), pathlib.Path(tmpdirname, 'pom.xml'))

            with open('.gitattributes', 'w') as f:
                f.write(f'pom.xml merge=custom-merge-driver')

            merge_driver = f'{pathlib.Path(cwd, "..", "src", "xml_paths_merge_driver.py")} %O %A %B'
            cmd = ['git', 'config', '--local', 'merge.custom-merge-driver.driver', merge_driver]
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'add', '.']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)
            cmd = ['git', 'commit', '-m', 'Mod. pom.xml on branch f1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            #cmd = ['cat', 'pom.xml']
            #print(f"$ {cmd}")
            #r = subprocess.run(cmd)

            cmd = ['git', 'checkout', 'master']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)
            cmd = ['git', 'checkout', '-b', 'release/r1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)
            shutil.copy(pathlib.Path(cwd, 'resources', 'it01', 'pom_b.xml'), pathlib.Path(tmpdirname, 'pom.xml'))
            cmd = ['git', 'add', '.']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)
            cmd = ['git', 'commit', '-m', 'Mod. pom.xml on branch release/r1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            #cmd = ['cat', 'pom.xml']
            #print(f"$ {cmd}")
            #r = subprocess.run(cmd)


            cmd = ['git', 'checkout', 'f1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'merge', '--no-ff', '--no-edit', 'release/r1']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'status']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            cmd = ['git', 'log', '--all', '--decorate', '--oneline', '--graph']
            print(f"$ {cmd}")
            r = subprocess.run(cmd)

            #with open('pom.xml') as f:
            #    print("MERGED:")
            #    print(f.read())

            self.assertTrue(filecmp.cmp(pathlib.Path(cwd, 'resources', 'it01', 'pom_expected.xml'), 'pom.xml'))


if __name__ == '__main__':
    unittest.main()
