import json
import logging
import re
from functools import reduce
from operator import getitem

from keep_ours_paths_merge_driver import utils

logger = logging.getLogger()

# The format is:
#   <the-jsonpath>:<some-regex>
DEFAULT_PATHS_AND_PATTERNS = [
    {'path': 'version', 'pattern': None}
]

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

    logger.debug("Getting details for base_json_dict")
    base_paths_details = _get_paths_details(base_json_dict)
    logger.debug("Getting details for ours_json_dict")
    ours_paths_details = _get_paths_details(ours_json_dict)
    logger.debug("Getting details for theirs_json_dict")
    theirs_paths_details = _get_paths_details(theirs_json_dict)

    logger.debug(f"base_paths_details: {base_paths_details}")
    logger.debug(f"ours_paths_details: {ours_paths_details}")
    logger.debug(f"theirs_paths_details: {theirs_paths_details}")

    #
    # Detect conflicts.
    #
    # There are two types of conflicts:
    #   - A value conflict in an JSON-document. This is the case, if a path is given in all three documents, and all
    #       values are different.
    #   - A line/hunk conflict in a file (represented as string). This is the case, if the line/hunk in all three
    #       files are different.
    #
    # Regarding the merge-driver it is assumed the file is not restructured, so an JSON-path represents a line in a
    # file.
    #
    # {} makes a set. * dereferences the list-items.
    #
    common_paths = {*base_paths_details.keys(), *ours_paths_details.keys(), *theirs_paths_details.keys()}
    logger.debug(f"common_paths: {common_paths}")
    for common_path in common_paths:
        base_value = base_paths_details[common_path]['value']
        ours_value = ours_paths_details[common_path]['value']
        theirs_value = theirs_paths_details[common_path]['value']
        # Are the 3 values different? They are conflicted if the number of unique values is 3.
        # To get the number of unique values, put them in a set and get the size.
        num_distinct_values = len({base_value, ours_value, theirs_value})
        is_conflict = num_distinct_values == 3
        logger.debug(
            f"common_path: {common_path}; num_distinct_values: {num_distinct_values}; is_conflict: {is_conflict}")

        if is_conflict:
            attribute_name = ours_paths_details[common_path]['attribute_name']
            # I assume there is always one space between the colon and the value. Otherwise, the theirs-attribute
            # won't be found.
            theirs_attribute_to_search = f'"{attribute_name}": "{theirs_value}"'
            ours_attribute_replacement = f'"{attribute_name}": "{ours_value}"'
            logger.debug(f"theirs_attribute_to_search: {theirs_attribute_to_search}"
                         + f"; ours_attribute_replacement: {ours_attribute_replacement}")

            # Set Ours value to Theirs.
            *parts, last = common_path.split('.')
            dict_temp = theirs_json_dict
            for part in parts:
                dict_temp = dict_temp.setdefault(part, {})
            dict_temp[last] = ours_value

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

            theirs_json_str = utils.replace_token(theirs_json_str, theirs_attribute_to_search,
                                                  ours_attribute_replacement,
                                                  check_if_modified_json_str_is_equal_to_theirs_json_control_dict)

    return theirs_json_str


def _get_paths_details(json_dict):
    paths_info = {}
    # TODO: Assure objects_or_value are unique.
    for path_and_pattern in g_paths_and_patterns:
        jpath = path_and_pattern['path']
        attribute_pattern = path_and_pattern['pattern']
        # Clean-up the jpath. If it starts with a dot, without clean-up the resulting list would have an empty first
        # list-entry. The dollar is JSON-path-specific. To make it compatible with this "small-json-like-parser",
        # remove the dollar-sign.
        jpath = re.sub('^[$.]*', '', jpath)
        # 'objects_or_value' can be a dict, a list, or a str.
        objects_or_value = reduce(getitem, jpath.split('.'), json_dict)
        logger.debug(f"_get_paths_details(); jpath: {jpath}"
                     + f"; objects_or_value: type: {type(objects_or_value)}, len: {len(objects_or_value)}")
        if isinstance(objects_or_value, str):
            # 'objects_or_value' is the str-value of jpath. For easy further processing make it a dict.
            # The attribute_name is the most right part of the dot-separated jpath.
            attribute_name = jpath.split('.')[-1]
            value = objects_or_value
            objects_or_value = {attribute_name: value}
        # TODO: Handle lists
        # Now it is an object (in JSON terminology).
        objects = objects_or_value
        for attribute_name, value in objects.items():
            # TODO: Expect value always as type str.
            logger.debug(f"  attribute_name: {attribute_name}; value: type: {type(value)}, value: {value}")
            # IDEA reports "Unexpected type(s): (None, str)". I assume this is because of the DEFAULT_PATHS_AND_PATTERNS
            # where all values are None. And the values are here the attribute_pattern. But the
            # DEFAULT_PATHS_AND_PATTERNS can be overwritten with set_paths_and_patterns().
            if not attribute_pattern:
                path_info = {jpath: {'attribute_name': attribute_name, 'value': value}}
                paths_info.update(path_info)
            elif re.match(attribute_pattern, str(attribute_name)):
                # jpath += '.' + attribute_name
                path_info = {f'{jpath}.{attribute_name}': {'attribute_name': attribute_name, 'value': value}}
                paths_info.update(path_info)
    return paths_info
