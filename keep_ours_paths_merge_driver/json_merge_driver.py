import json
import logging
import re

# I chose jsonpath-ng because it generates full_path per path-match. This eases generating the control-doc a lot.
import jsonpath_ng as jp

from keep_ours_paths_merge_driver import config
from keep_ours_paths_merge_driver import utils

logger = logging.getLogger()

# The format is:
#   <optional merge-strategy>:<mandatory the-jsonpath>:<optional some-regex>
g_paths_and_patterns = {}


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

    common_paths = set.intersection(
        set(base_paths_details.keys()), set(ours_paths_details.keys()), set(theirs_paths_details.keys()))
    logger.debug(f"common_paths to base/ours/theirs: {common_paths}")
    for common_path in common_paths:
        base_value = base_paths_details[common_path]['value']
        ours_value = ours_paths_details[common_path]['value']
        theirs_value = theirs_paths_details[common_path]['value']
        merge_strategy = ours_paths_details[common_path]['merge_strategy']
        # Are the 3 values different? They are conflicted if the number of unique values is 3.
        # To get the number of unique values, put them in a set and get the size.
        num_distinct_values = len({base_value, ours_value, theirs_value})

        if merge_strategy == config.MERGE_STRATEGY_ALWAYS_OURS:
            prepare_theirs = True
            logger.debug(
                f"common_path: {common_path}; merge_strategy: {merge_strategy}; prepare_theirs: {prepare_theirs}")
        else:
            # Merge-strategy is MERGE_STRATEGY_NAME_ON_CONFLICT_OURS.
            # Are the 3 values different? They are conflicted if the number of unique values is 3.
            prepare_theirs = num_distinct_values == 3
            logger.debug(
                f"common_path: {common_path}; merge_strategy: {merge_strategy}; prepare_theirs: {prepare_theirs}" +
                f"; num_distinct_values: {num_distinct_values}")

        if prepare_theirs:
            theirs_value_to_search = theirs_value
            ours_value_replacement = ours_value
            logger.debug(f"theirs_value_to_search: {theirs_value_to_search}"
                         + f"; ours_value_replacement: {ours_value_replacement}")

            #
            # Using some special chars in jpath like slash '/', the following error occurs:
            #
            #       sonpath_ng.exceptions.JsonPathLexerError: Error on line 1, col 23: Unexpected character: /
            #
            # Example:
            #   jpath = '$.dependencies.@mycompany/app1-version'
            #
            # To work around this, the path-part containing this char have to be quoted:
            #   jpath = '$.dependencies."@mycompany/app1-version"'
            #
            # Quoting the whole path doesn't work. The part in question has to be quoted, or all parts of its own:
            #   jpath = '$."dependencies"."@mycompany/app1-version"'
            #
            # But only the string-values, not the indexes!
            # If a path contains an index, that index must not be quoted:
            #   jpath = '$."dependencies".[1]'
            #
            # See also:
            #   h2non/jsonpath-ng, https://github.com/h2non/jsonpath-ng/issues/127, issue #127:
            #       json-path with slash results in: jsonpath_ng.exceptions.JsonPathLexerError: Error on line 1,
            #       col 10: Unexpected character: / #127
            #
            def quote_jpath(jpath: str):
                path_parts = jpath.split('.')
                quoted_path_parts = []
                for path_part in path_parts:
                    if path_part.startswith('['):
                        quoted_path_parts.append(path_part)
                    else:
                        quoted_path_parts.append('"' + path_part + '"')
                return '.'.join(quoted_path_parts)

            # Set Ours value to Theirs.
            quoted_common_path = quote_jpath(common_path)
            jsonpath_expr = jp.parse(quoted_common_path)
            theirs_json_control_dict = jsonpath_expr.update(theirs_json_dict, ours_value)

            neutral_formatted_theirs_json_str = json.dumps(theirs_json_control_dict)

            def check_if_modified_json_str_is_equal_to_theirs_json_control_dict(json_str: str) -> bool:
                return neutral_formatted_theirs_json_str == json.dumps(json.loads(json_str))

            theirs_json_str = utils.replace_token(theirs_json_str, theirs_value_to_search,
                                                  ours_value_replacement,
                                                  check_if_modified_json_str_is_equal_to_theirs_json_control_dict)

    return theirs_json_str


def _get_paths_details(json_dict):
    paths_info = {}
    for path_and_pattern in g_paths_and_patterns:
        merge_strategy = path_and_pattern['merge_strategy']
        jpath = path_and_pattern['path']
        attribute_pattern = path_and_pattern['pattern']
        jsonpath_expr = jp.parse(jpath)
        jp_matches = jsonpath_expr.find(json_dict)
        logger.debug(f"_get_paths_details(); jpath: {jpath}; matching attributes count: {len(jp_matches)}")

        if len(jp_matches) == 1 and type(jp_matches[0].value) == str and attribute_pattern:
            logger.warning(f"Path '{jpath}' is a non-wildcard path, and a pattern is given."
                           + " Patterns should only used on wildcard-paths"
                           + " like '$.some-object.*' and '$.some-list[*]'.")

        for jp_match in jp_matches:
            # Type of jp_match.path is <class 'jsonpath_ng.jsonpath.Fields'>.
            attribute_name = str(jp_match.path)
            if not attribute_pattern or re.match(attribute_pattern, attribute_name):
                # Type of jp_match.full_path is  <class 'jsonpath_ng.jsonpath.Child'>.
                full_path = str(jp_match.full_path)
                value = jp_match.value
                paths_info.update({full_path: {
                    'merge_strategy': merge_strategy, 'attribute_name': attribute_name,
                    'value': value, 'jsonpath_object': jp_match}})
    return paths_info
