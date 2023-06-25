import subprocess
import unittest


class TestMyTestCaseTodo(unittest.TestCase):
    """ Test scenarios.

    About the wording "conflicted":

    a) Conflicted means a file has to be merged.
    b) Conflicted doesn't mean there are line "hunk" conflicts.

    We use the terms "file-conflict" for a) and "line-conflict" for b).

    The term "merge-driver" means the merge-driver under test.
    This merge-driver always delegates the final file-merge to the command "git merge-file".


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
        r = subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    unittest.main()
