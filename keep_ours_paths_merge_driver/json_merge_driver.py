import json
import logging
import re

import jsonpath_ng as jp

import utils

logger = logging.getLogger()

# The format is:
#   <the-jsonpath>:<some-regex>
DEFAULT_PATHS_AND_PATTERNS = {
    '$.version': None
    # , '$.dependencies.*': TO-DO: Pattern
}

g_paths_and_patterns = DEFAULT_PATHS_AND_PATTERNS


def set_paths_and_patterns(path_and_patterns):
    global g_paths_and_patterns
    if path_and_patterns is not None:
        g_paths_and_patterns = path_and_patterns


def get_paths_and_patterns():
    return g_paths_and_patterns


def get_prepared_theirs_str(base_json_str: str, ours_json_str: str, theirs_json_str: str) -> str:
    base_json_dict = json.loads(base_json_str)
    ours_json_dict = json.loads(ours_json_str)
    theirs_json_dict = json.loads(theirs_json_str)

    base_paths_details = _get_paths_details(base_json_dict)
    ours_paths_details = _get_paths_details(ours_json_dict)
    theirs_paths_details = _get_paths_details(theirs_json_dict)

    logger.debug(f"base_paths_details: {base_paths_details}")
    logger.debug(f"ours_paths_details: {ours_paths_details}")
    logger.debug(f"theirs_paths_details: {theirs_paths_details}")

    # Detect conficts.
    # A conflict is possible if the path exist in all three docs. A conflict is given if all three values of a path
    # are different.
    #
    # Get the paths unique to all three docs (the path might not exist in all docs). Merge-conflicts might only occur
    # on lines where all three lines differ. We expect the files as strings not restructures, so the XPaths reflect the
    # position in the files. That means: A XPath in the doc is treated as a line in the file.
    # {} makes a set. * dereferences the list-items.
    uniq_paths = {*base_paths_details.keys(), *ours_paths_details.keys(), *theirs_paths_details.keys()}
    logger.debug(f"uniq_paths: {uniq_paths}")
    for uniq_path in uniq_paths:
        base_value = base_paths_details[uniq_path]['value']
        ours_value = ours_paths_details[uniq_path]['value']
        theirs_value = theirs_paths_details[uniq_path]['value']
        # Are the 3 values different? They are conflicted if the number of unique values is 3.
        # To get the number of unique values, put them in a set and get the size.
        num_distinct_values = len({base_value, ours_value, theirs_value})
        is_conflict = num_distinct_values == 3
        logger.debug(f"uniq_path: {uniq_path}; num_distinct_values: {num_distinct_values}; is_conflict: {is_conflict}")

        if is_conflict:
            tag_name = ours_paths_details[uniq_path]['tag_name']

            # I assume there is always one space between the colon and the value. Otherwise, the theirs-tag won't be
            # found.
            # TODO: Rename "tag" to "element" in both json_merge_driver and xml_merge_driver.
            theirs_tag_to_search = f'"{tag_name}": "{theirs_value}"'
            ours_tag_replacement = f'"{tag_name}": "{ours_value}"'

            # Set Ours value to Theirs.
            jsonpath_expr = jp.parse(uniq_path)
            jsonpath_expr.update(theirs_json_dict, ours_value)

            #
            # check_if_modified_json_str_is_equal_to_theirs_json_control_dict():
            # We have the control-doc as XML-doc, and the XML to be compared against the control-doc as string.
            # What possibilities of comparisons we have?
            # The LXMLOutputChecker().checker.check_output() needs two strings.
            # Comparison is also possible between to XML-docs with etree.tostring(xml_doc).
            # But is there something taking one XML-doc and one XML-string? I don't know.
            #
            neutral_formatted_theirs_xml_str = json.dumps(theirs_json_dict)

            def check_if_modified_json_str_is_equal_to_theirs_json_control_dict(json_str: str) -> bool:
                return neutral_formatted_theirs_xml_str == json.dumps(json.loads(json_str))

            theirs_json_str = utils.replace_token(theirs_json_str, theirs_tag_to_search, ours_tag_replacement,
                                                  check_if_modified_json_str_is_equal_to_theirs_json_control_dict)

    return theirs_json_str


def _get_paths_details(json_dict):
    paths_info = {}
    # TODO: Assure elements are unique.
    for jpath, tag_pattern in g_paths_and_patterns.items():
        jsonpath_expr = jp.parse(jpath)
        elements = jsonpath_expr.find(json_dict)
        logger.debug(f"get_paths_details(); elements: len: {len(elements)}")
        for element in elements:
            # IDEA reports "Unexpected type(s): (None, str)". I assume this is because of the DEFAULT_PATHS_AND_PATTERNS
            # where all values are None. And the values are here the tag_pattern. But the DEFAULT_PATHS_AND_PATTERNS
            # can be overwritten with set_paths_and_patterns().
            if not tag_pattern or re.match(tag_pattern, str(element.path)):
                path = element.full_path
                tag_name = element.path
                value = element.value
                # str(path): Without this there is "TypeError: unhashable type: 'Fields'".
                path_info = {str(path): {'tag_name': tag_name, 'value': value}}
                paths_info.update(path_info)
    return paths_info
