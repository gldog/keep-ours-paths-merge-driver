import os

from setuptools import setup

from keep_ours_paths_merge_driver.config import __version__

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
    name='keep_ours_paths_merge_driver',
    version=__version__,
    description='',
    packages=['keep_ours_paths_merge_driver'],
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['keep_ours_paths_merge_driver=keep_ours_paths_merge_driver.__main__:main'],
    },
)
