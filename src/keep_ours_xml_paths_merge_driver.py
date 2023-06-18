#! /usr/bin/env python3

import os
import re
import shlex
import subprocess
import sys
import xml.etree.ElementTree as ET

#
# Uses xml.etree.ElementTree not to rely on additional libraries.
# The implementations in 2.7 and 3.x versions behave differently.
# Python 2.7: https://docs.python.org/2.7/library/xml.etree.elementtree.html
#
# TODO More description
#


#
# CONFIG
#

DEFAULT_XPATHS_TO_TAKE_OURS = [
    './version',
    './properties/revision'
]

script_name = os.path.basename(__file__)


def check_parameters():
    # Behave as "git merge-file". From https://git-scm.com/docs/git-merge-file:
    # "The exit value of this program is negative on error, and the number of conflicts otherwise
    # (truncated to 127 if there are more than that many conflicts). If the merge was clean, the
    # exit value is 0."
    if len(sys.argv) < 4:
        print(f"Merge-driver {script_name}:" +
              " Expect at lest 3 parameters for %O (ancestor), %A (ours), %B (theirs)" +
              f", but got {len(sys.argv) - 1}")
        sys.exit(-1)


def remove_xmlns_from_xml_string(xml_str):
    return re.sub(' xmlns="[^"]+"', '', xml_str, count=1)


def is_xpath_present(xpath, xml_doc):
    return True if xml_doc.find(xpath) is not None else False


def count_xpath(xpath, xml_doc):
    path_matches = xml_doc.findall(xpath)
    return len(path_matches)


#   Conflict type       Considered line     Considered line     Action:
#   File 0 / Line 1     changed in          changed in          Fake Theirs %B?
#                       Theirs %B           Ours %A
# ------------------+-------------------+-------------------+---------------------
#       0                   0                   0                   0
#       0                   0                   1                   0
#       0                   1                   0                   1
#       0                   1                   1                   X (not a use case)
#       0                   0                   0                   0
#       0                   0                   1                   0
#       0                   1                   0                   1
#       0                   1                   1                   1
#
# Result: Action if change in Theirs %B
#
def shall_fake_theirs_xpath_to_ours_value(path, ancestor_o_doc, theirs_b_doc):
    try:
        if ancestor_o_doc.find(path).text != theirs_b_doc.find(path).text:
            return True
        return False
    except IndexError:
        return False


def replace_nth(s, old, new, n):
    """
    Credits to vineeshvs, see
    https://stackoverflow.com/questions/35091557/replace-nth-occurrence-of-substring-in-string
    """
    # Replace all originals up to (including) nth occurrence and assign it to the variable.
    replaced_until_n = s.replace(old, new, n)
    first_originals_back = s
    for i in range(n):
        # Restore originals up to nth occurance (not including nth).
        first_originals_back = replaced_until_n.replace(new, old, i)
    return first_originals_back


def replace_value_at_xpath(xpath, value, xml_str: str):
    """
    Find the xpath in the given XML-string and replace the current value with the given new one.

    :param value: The new value to be set to the element described in xpath.
    :param xpath: The XPath. The root-node is the dot ".". E.g. the path to the project's version
                    is "./version", and the path to a property is "./property/revision".
    :param xml_str: Original XML as in the file (still including the namespaces).
    :return: The modified XML.
    """

    original_xml_doc = ET.fromstring(remove_xmlns_from_xml_string(xml_str))

    # It is already checked that the xpath is present and is not ambiguous.
    current_value = original_xml_doc.find(xpath).text

    # Extract the tag name from the xpath. E.g. if the xpath is "./version", the tag is "version",
    # and if the xpath is "./properties/revision", the tag is "revision".
    tag = re.sub('.*/', '', xpath)
    current_element = '<' + tag + '>' + current_value + '</' + tag + '>'
    new_element = '<' + tag + '>' + value + '</' + tag + '>'

    # In usual cases like the project/version or the project/properties/revision the number of
    # elements to be replaced is 1. But in more exotic use cases like versions of dependencies the
    # element might occur more than once.
    # Because replacing by Regex is difficult, an algorithm
    #   - generates an expected XML as doc
    #   - replace the occurrences in the XML-string one by one
    #   - and compares each replacement with the expectation
    #   - until the replacement is equal to the expectation.
    current_element_num = len(xml_str.split(current_element)) - 1
    expected_xml_str_without_namespace = remove_xmlns_from_xml_string(xml_str)
    expected_xml_doc = ET.fromstring(expected_xml_str_without_namespace)
    expected_xml_doc.find(xpath).text = value

    # TODO: Anything to be done here regarding ET.toString() ?
    # From the Python 3 docs:
    #   encoding="unicode" to generate a Unicode string (otherwise, a bytestring is generated).
    # But using encoding='unicode' in Python 2.7:
    #   LookupError: unknown encoding: unicode
    expected_xml_formatted_str = ET.tostring(expected_xml_doc)
    # Replace each occurrence of tag one after the other until the XML-document is equal to the
    # expected_xml_doc.
    for i in range(1, current_element_num + 1):
        new_xml_str = replace_nth(xml_str, current_element, new_element, i)
        new_xml_str_without_namespace = remove_xmlns_from_xml_string(new_xml_str)
        new_xml_doc_formatted_string = ET.tostring(ET.fromstring(new_xml_str_without_namespace))
        if expected_xml_formatted_str == new_xml_doc_formatted_string:
            return new_xml_str

    # Return an empty string in case the value couldn't be replaced.
    return xml_str


def replace_values_at_xpaths_in_theirs(xpaths, ancestor_o_xml_str, ours_a_xml_str,
                                       theirs_b_xml_str):
    ancestor_o_xml_doc = ET.fromstring(remove_xmlns_from_xml_string(ancestor_o_xml_str))
    ours_a_xml_doc = ET.fromstring(remove_xmlns_from_xml_string(ours_a_xml_str))
    theirs_b_xml_doc = ET.fromstring(remove_xmlns_from_xml_string(theirs_b_xml_str))
    errors = []
    # Remember:
    # We have to keep/protect the values at the given XPath in Ours by writing those values to
    # Theirs.
    for xpath in xpaths:
        # We have to keep/protect the XPath in Ours only if it is present in Ours document.
        if not is_xpath_present(xpath, ours_a_xml_doc):
            continue

        # We have to keep/protect the XPath in Ours only if it is present in Theirs document.
        if not is_xpath_present(xpath, theirs_b_xml_doc):
            continue

        error_msg = "The XML-path '{}' in {} is ambiguous. It is present {} times."
        xpath_num = count_xpath(xpath, ours_a_xml_doc)
        if xpath_num > 1:
            errors.append(error_msg.format(xpath, 'Ours (%A)', xpath_num))
        xpath_num = count_xpath(xpath, theirs_b_xml_doc)
        if xpath_num > 1:
            errors.append(error_msg.format(xpath, 'Theirs (%B)', xpath_num))
        if errors:
            continue

        if shall_fake_theirs_xpath_to_ours_value(xpath, ancestor_o_xml_doc, theirs_b_xml_doc):
            value = ours_a_xml_doc.find(xpath).text
            theirs_b_xml_doc.find(xpath).text = value
            xml_str = replace_value_at_xpath(xpath, value, theirs_b_xml_str)
            if xml_str:
                theirs_b_xml_str = xml_str
            else:
                # Should never happen.
                errors.append(f"Could not replace value at XML-path '{xpath}' in Theirs (%B)")

    return theirs_b_xml_str, errors


if __name__ == '__main__':
    print(f"Merge-driver {script_name}: It's me, the merge-driver.")

    # For parameters see also "Defining a custom merge driver"
    # https://git-scm.com/docs/gitattributes#_defining_a_custom_merge_driver
    check_parameters()

    #
    # In the following we're using the following terms for the XML-representations:
    #   - filename: The filename as it is given by the Merge-Driver parameters %O, %A, %B.
    #               These filenames are temp-files and aren't named as the original ones.
    #   - doc:      The file as xml.etree.ElementTree, a "XML-document".
    #   - str:      The file as string.
    #

    ancestor_o_filename = sys.argv[1]  # %O
    ours_a_filename = sys.argv[2]  # %A'
    theirs_b_filename = sys.argv[3]  # %B

    # Order of precedence reading XPaths:
    #   1. Environment variable KOX_MERGE_DRVIER_XPATHS
    #   2. Script parameter #4
    #   3. Default
    #
    # Setting KOX_MERGE_DRVIER_XPATHS to an empty value effectively disables the merge-driver.
    xpaths_to_keep_ours_from_environment = os.getenv('KOX_MERGE_DRVIER_XPATHS')
    split_regex = "\\s*,+\\s*"
    if xpaths_to_keep_ours_from_environment:
        xpaths_to_keep_ours = re.split(split_regex, xpaths_to_keep_ours_from_environment.strip())
        # Delete empty list-entries.
        xpaths_to_keep_ours = [x for x in xpaths_to_keep_ours if x]
    elif len(sys.argv) > 4:
        xpaths_to_keep_ours = re.split(split_regex, sys.argv[4].strip())
        # Delete empty list-entries.
        xpaths_to_keep_ours = [x for x in xpaths_to_keep_ours if x]
    else:
        xpaths_to_keep_ours = DEFAULT_XPATHS_TO_TAKE_OURS

    print(f"Merge-driver {script_name}: XPaths: {xpaths_to_keep_ours}")

    with open(ancestor_o_filename) \
            as f_o, open(ours_a_filename) as f_a, open(theirs_b_filename) as f_b:
        ancestor_o_xml_str = f_o.read()
        ours_a_xml_str = f_a.read()
        theirs_b_xml_str = f_b.read()

    # print(f"FILE %O original:\n{ancestor_o_xml_str}")
    # print(f"FILE %A original:\n{ours_a_xml_str}")
    # print(f"FILE %B original:\n{theirs_b_xml_str}")

    theirs_b_prepared_xml_str, errors = replace_values_at_xpaths_in_theirs(
        xpaths_to_keep_ours,
        ancestor_o_xml_str,
        ours_a_xml_str, theirs_b_xml_str)

    # In case of an error, this merge-driver exits with -1. Git doesn't take any more action
    # on this and keeps Ours file-version in the workspace. Now it is difficult for the user to
    # proceed on this merge, because the temporary files for Ancestor (%O) and Theirs (%B) are gone.
    # It is expected the case of ambiguous XPaths should be a rare case or an configuration error.
    # So for now, no more implementation effort is taken on this.
    if errors:
        print(f"Merge-driver {script_name}: {errors}")
        # The exit code is like of 'git merge-file'.
        # From the doc https://git-scm.com/docs/git-merge-file:
        #   "The exit value of this program is negative on error, and the number of conflicts
        #   otherwise (truncated to 127 if there are more than that many conflicts). If the merge
        #   was clean, the exit value is 0."
        sys.exit(-1)

    with open(theirs_b_filename, mode='w') as f:
        f.write(theirs_b_prepared_xml_str)

    # TODO --marker-size=<n>

    # From the docs https://git-scm.com/docs/git-merge-file:
    #   "git merge-file incorporates all changes that lead from the <base-file> to <other-file> into
    #   <current-file>. The result ordinarily goes into <current-file>.".
    # Despite ours_a_filename is a temp-file, Git notices the merge-result and will write it to
    # the regular file in the workspace.
    cmd = "git merge-file -L ours -L base -L theirs " \
          + ours_a_filename + " " + ancestor_o_filename + " " + theirs_b_filename
    returncode = subprocess.call(shlex.split(cmd))

    sys.exit(returncode)
