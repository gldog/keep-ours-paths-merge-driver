import subprocess
import unittest


class MyTestCase(unittest.TestCase):
    """ Test scenarios.

    About the wording "conflicted":

    a) Conflicted means a file has to be merged.
    b) Conflicted doesn't mean there are line "hunk" conflicts.

    We use the terms "file-conflicted" for a) and "line-conflicts" for b).

    The term "merge-driver" means the merge-driver under test.
    This merge-driver always delegates the final merge to the command "git merge-file".


    Test cases:

    TC: No Pom at all.
        In this test case no Pom is involved, but other conflicted files are.
        The merge-driver won't be called.

    TC: Pom modified in Ours %A, but without merge-conflict (Theirs %B isn't changed).
        A Pom ist changed in Ours %A, but not in Theirs %B.
        Git won't call the merge-driver.

    TC: Pom modified in Theirs %B, but without merge-conflict (Ours %A isn't changed).
        A Pom ist changed in Theirs %B, but not in Ours %A.
        Git won't call the merge-driver.

    TC: Pom with file-conflict, no configured XPath is involved.
        A Pom is changed in Ours %A and Theirs %B, but not in common lines nor in
        configured XPaths.
        Git will call the merge-Driver.
        The merge-driver won't find configured XPath and won't fake Theirs %B.
        The merge-driver delegates the final merge to Git.

    TC: Pom with file-conflict, 1 configured XPath is involved.
        A Pom is changed in Ours %A and Theirs %B, but not in common lines, but in
        a configured XPath in Theris %B.
        Git will call the merge-Driver.
        The merge-driver will find the configured XPath and will fake Theirs %B to the value od
        Ours %A.
        The merge-driver delegates the final merge to Git.

    """

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_a(self):
        cmd = 'pwd'
        r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # I'm in directory 'tests'.
        #print(f'PWD: {r.stdout}')

        # rm -rf tmp
        # mkdir tmp
        # cp resources/it01/pom.xml tmp
        # cd tmp
        # echo "pom.xml merge=custom-merge-driver" > .gitattributes
        # git init
        # git config --local merge.custom-merge-strategy.driver "src/xml_paths_merge_driver.py %O %A %B"
        # git add .
        # git commit -m Initial
        # git checkout -b b1
        # git merge --no-edit --no-ff b1


if __name__ == '__main__':
    unittest.main()
