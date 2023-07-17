#! /usr/bin/env python3

import logging
import os
import shlex
import subprocess
import sys

from keep_ours_paths_merge_driver import config
from keep_ours_paths_merge_driver import json_merge_driver
from keep_ours_paths_merge_driver import xml_merge_driver

#
# Uses xml.etree.ElementTree not to rely on additional libraries.
# The implementations in 2.7 and 3.x versions behave differently.
# Python 2.7: https://docs.python.org/2.7/library/xml.etree.elementtree.html
#
# TODO More description
#

script_name = 'keep_ours_paths_merge_driver'


def main():
    # For parameters see also "Defining a custom merge driver"
    # https://git-scm.com/docs/gitattributes#_defining_a_custom_merge_driver
    cl_parser = config.init_argument_parser()

    cl_args = cl_parser.parse_args()

    config.configure_logger(cl_args.loglevel)
    logger = logging.getLogger()
    logger.info(script_name)
    logger.debug(f"sys.argv: {sys.argv}")
    logger.debug(f"args: {cl_args}")

    #
    # In the following we're using the following terms for the XML-representations:
    #
    #   - filepath: The filename as it is given by the Merge-Driver parameters %O, %A, %B.
    #               These filenames are temp-files and aren't named as the original ones.
    #   - doc:      The file as xml.etree.ElementTree, a "XML-document".
    #   - str:      The file as string.
    #

    base_filepath = cl_args.base  # %O
    ours_filepath = cl_args.ours  # %A'
    theirs_filepath = cl_args.theirs  # %B

    with open(base_filepath) as f_o, open(ours_filepath) as f_a, open(theirs_filepath) as f_b:
        base_file_str = f_o.read()
        ours_file_str = f_a.read()
        theirs_file_str = f_b.read()

    # The merge-driver makes only sense if all three files have content.
    # If the file has been added to ours-branch and theirs-branch, but was not present before in base, the base-file
    # is empty.
    if base_file_str and ours_file_str and theirs_file_str:
        paths_from_cl_args_as_list = getattr(cl_args, 'pathspatterns', None)
        paths_from_environment_as_str = os.getenv('KOP_MERGE_DRVIER_PATHSPATTERNS')
        logger.debug(f"-p: {paths_from_cl_args_as_list}")
        logger.debug(f"KOP_MERGE_DRVIER_PATHSPATTERNS: {paths_from_environment_as_str}")
        # Get path_and_patterns merged from command-line parameter and environment variable.
        paths_and_patterns = config.get_paths_and_patterns(paths_from_environment_as_str, paths_from_cl_args_as_list)
        logger.debug(f"config.get_paths_and_patterns(): {paths_and_patterns}")
        if not paths_and_patterns:
            logger.info("paths_and_patterns-config is empty."
                        + " Nothing has been set in command-line-parameter -p"
                        + " nor in environment-variable KOP_MERGE_DRVIER_PATHSPATTERNS."
                        + " The merge-driver did no merge-preparation.")

        # This is the tiny merge-driver-factory.
        if cl_args.filetype == 'XML':
            merge_driver = xml_merge_driver
        else:
            # The choices are limited to 'XML' and 'JSON'. So there is no need to check any alternative to 'XML'
            # If not 'XML' it is 'JSON'. 'XML' is the default.
            merge_driver = json_merge_driver

        merge_driver.set_paths_and_patterns(paths_and_patterns)
        logger.info(f"paths and patterns: {merge_driver.get_paths_and_patterns()}")
        prepared_theirs_str = merge_driver.get_prepared_theirs_str(base_file_str, ours_file_str, theirs_file_str)

        if cl_args.stdout:
            print(prepared_theirs_str)
            sys.exit(1)
        else:
            with open(theirs_filepath, mode='w') as f:
                f.write(prepared_theirs_str)

    # From the docs https://git-scm.com/docs/git-merge-file:
    #   "git merge-file incorporates all changes that lead from the <base-file> to <other-file> into
    #   <current-file>. The result ordinarily goes into <current-file>.".
    # Despite ours_a_filename is a temp-file, Git notices the merge-result and will write it to
    # the regular file in the workspace.
    cmd = "git merge-file -L ours -L base -L theirs " + ours_filepath + " " + base_filepath + " " + theirs_filepath
    returncode = subprocess.call(shlex.split(cmd))
    sys.exit(returncode)


if __name__ == '__main__':
    main()
