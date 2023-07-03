#! /usr/bin/env python3

import logging
import os
import shlex
import subprocess
import sys

import config
import xml_merge_driver

#
# Uses xml.etree.ElementTree not to rely on additional libraries.
# The implementations in 2.7 and 3.x versions behave differently.
# Python 2.7: https://docs.python.org/2.7/library/xml.etree.elementtree.html
#
# TODO More description
#

script_name = 'keep_ours_paths_merge_driver'

if __name__ == '__main__':
    config.configure_logger()
    logger = logging.getLogger()
    logger.info(script_name)

    # For parameters see also "Defining a custom merge driver"
    # https://git-scm.com/docs/gitattributes#_defining_a_custom_merge_driver
    logger.debug(f"sys.argv: {sys.argv}")
    cl_parser = config.parse_command_line_arguments()

    #
    # In the following we're using the following terms for the XML-representations:
    #
    #   - filepath: The filename as it is given by the Merge-Driver parameters %O, %A, %B.
    #               These filenames are temp-files and aren't named as the original ones.
    #   - doc:      The file as xml.etree.ElementTree, a "XML-document".
    #   - str:      The file as string.
    #

    cl_args = cl_parser.parse_args()
    base_filepath = cl_args.base  # %O
    ours_filepath = cl_args.ours  # %A'
    theirs_filepath = cl_args.theirs  # %B

    # logger.info(f'base_filepath {base_filepath}, ours_filepath {ours_filepath}, theirs_filepath {theirs_filepath}')

    with open(base_filepath) \
            as f_o, open(ours_filepath) as f_a, open(theirs_filepath) as f_b:
        base_xml_str = f_o.read()
        ours_xml_str = f_a.read()
        theirs_xml_str = f_b.read()

    # The merge-driver makes only sense it all three files have content.
    # If the file has been added to ours-branch and theirs-branch, but was not present before in base, the base-file
    # is empty.
    if base_xml_str and ours_xml_str and theirs_xml_str:
        from_environment_as_str = os.getenv('KOP_MERGE_DRVIER_PATHS')
        from_cl_args_as_list = cl_args.pathpatterns if hasattr(cl_args, 'pathpatterns') else None
        logger.debug(f"-p: {from_cl_args_as_list}")
        logger.debug(f"KOP_MERGE_DRVIER_PATHS: {from_environment_as_str}")
        paths_and_patterns = config.get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list)
        logger.debug(f"config.get_paths_and_patterns(): {paths_and_patterns}")
        xml_merge_driver.set_paths_and_patterns(paths_and_patterns)

        logger.info(f"paths and patterns: {xml_merge_driver.get_paths_and_patterns()}")

        prepared_theirs_str = xml_merge_driver.get_prepared_theirs_str(base_xml_str, ours_xml_str, theirs_xml_str)
        logger.debug(f"prepared_theirs_str:\n{prepared_theirs_str}")

        with open(theirs_filepath, mode='w') as f:
            f.write(prepared_theirs_str)

    # From the docs https://git-scm.com/docs/git-merge-file:
    #   "git merge-file incorporates all changes that lead from the <base-file> to <other-file> into
    #   <current-file>. The result ordinarily goes into <current-file>.".
    # Despite ours_a_filename is a temp-file, Git notices the merge-result and will write it to
    # the regular file in the workspace.
    cmd = "git merge-file -L ours -L base -L theirs " \
          + ours_filepath + " " + base_filepath + " " + theirs_filepath
    returncode = subprocess.call(shlex.split(cmd))
    sys.exit(returncode)
