import logging
import re

from lxml import etree

import utils

logger = logging.getLogger()

# The format is:
#   <the-xpath>:<some-tag-regex>
DEFAULT_PATHS_AND_PATTERNS = [
    {'path': './version', 'pattern': None}
]

g_paths_and_patterns = DEFAULT_PATHS_AND_PATTERNS


def set_paths_and_patterns(path_and_patterns):
    global g_paths_and_patterns
    if path_and_patterns is not None:
        g_paths_and_patterns = path_and_patterns


def get_paths_and_patterns():
    return g_paths_and_patterns


def remove_xmlns_from_xml_string(xml_str):
    return re.sub(' xmlns="[^"]+"', '', xml_str, count=1)


def get_prepared_theirs_str(base_xml_str: str, ours_xml_str: str, theirs_xml_str: str) -> str:
    #
    # TODO Explain why remove_xmlns_from_xml_string() is used.
    #
    # About encode():
    #
    # Without encode(), lxml blames:
    #       ValueError: Unicode strings with encoding declaration are not supported. Please use bytes input or XML
    #       fragments without declaration.
    #
    base_xml_doc = etree.fromstring(remove_xmlns_from_xml_string(base_xml_str).encode())
    ours_xml_doc = etree.fromstring(remove_xmlns_from_xml_string(ours_xml_str).encode())
    theirs_xml_doc = etree.fromstring(remove_xmlns_from_xml_string(theirs_xml_str).encode())

    base_paths_details = _get_paths_details(base_xml_doc)
    ours_paths_details = _get_paths_details(ours_xml_doc)
    theirs_paths_details = _get_paths_details(theirs_xml_doc)

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
            theirs_tag_to_search = f'<{tag_name}>{theirs_value}</{tag_name}>'
            ours_tag_replacement = f'<{tag_name}>{ours_value}</{tag_name}>'

            # Set Ours value to Theirs. 'theirs_element_reference' keeps a reference to the element in theirs_xml_doc.
            theirs_element_reference = theirs_paths_details[uniq_path]['tag_object']
            theirs_element_reference.text = ours_value

            #
            # check_if_modified_xml_str_is_equal_to_theirs_xml_control_doc():
            # We have the control-doc as XML-doc, and the XML to be compared against the control-doc as string.
            # What possibilities of comparisons we have?
            # The LXMLOutputChecker().checker.check_output() needs two strings.
            # Comparison is also possible between to XML-docs with etree.tostring(xml_doc).
            # But is there something taking one XML-doc and one XML-string? I don't know.
            #
            neutral_formatted_theirs_xml_str = etree.tostring(theirs_xml_doc)

            def check_if_modified_xml_str_is_equal_to_theirs_xml_control_doc(xml_str: str) -> bool:
                neutral_formatted_prepared_xml_str = \
                    etree.tostring(etree.fromstring(remove_xmlns_from_xml_string(xml_str).encode()))
                return neutral_formatted_theirs_xml_str == neutral_formatted_prepared_xml_str

            theirs_xml_str = utils.replace_token(theirs_xml_str, theirs_tag_to_search, ours_tag_replacement,
                                                 check_if_modified_xml_str_is_equal_to_theirs_xml_control_doc)

    return theirs_xml_str


def _get_paths_details(xml_doc):
    xml_doc_tree = etree.ElementTree(xml_doc)
    paths_info = {}
    # TODO: Assure tags are unique.
    for path_and_pattern in g_paths_and_patterns:
        xpath = path_and_pattern['path']
        tag_pattern = path_and_pattern['pattern']
        tags = xml_doc.findall(xpath)
        logger.debug(f"get_paths_details(); xpath: {xpath}; tags len: {len(tags)}")
        for tag in tags:
            if not tag_pattern or re.match(tag_pattern, tag.tag):
                path = xml_doc_tree.getpath(tag)
                tag_name = tag.tag
                value = tag.text
                path_info = {path: {'tag_name': tag_name, 'value': value, 'tag_object': tag}}
                paths_info.update(path_info)
    return paths_info
