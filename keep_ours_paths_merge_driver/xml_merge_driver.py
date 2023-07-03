import logging
import re

from lxml import etree

import utils

logger = logging.getLogger()

# The format is:
#   <the-xpath>:<some-tag-regex>
DEFAULT_PATHS_AND_PATTERNS = {
    './version': None,
    './properties/revision': None,
    './properties/': '.+\\.version'
}

g_path_and_patterns = DEFAULT_PATHS_AND_PATTERNS


def set_path_and_patterns(path_and_patterns):
    g_path_and_patterns = path_and_patterns


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

    base_paths_details = get_paths_details(base_xml_doc)
    ours_paths_details = get_paths_details(ours_xml_doc)
    theirs_paths_details = get_paths_details(theirs_xml_doc)

    logger.debug(f"base_paths_details: {base_paths_details}")
    logger.debug(f"ours_paths_details: {ours_paths_details}")
    logger.debug(f"theirs_paths_details: {theirs_paths_details}")

    # {} makes a set. * dereferences the list-items.
    uniq_paths = {*base_paths_details.keys(), *ours_paths_details.keys(), *theirs_paths_details.keys()}
    logger.debug(f"uniq_paths: {uniq_paths}")
    for uniq_path in uniq_paths:
        base_value = base_paths_details[uniq_path]['value']
        ours_value = ours_paths_details[uniq_path]['value']
        theirs_value = theirs_paths_details[uniq_path]['value']
        # print(f"uniq uniq_path: {uniq_path}; base_value: {base_value}; ours_value: {ours_value}; theirs_value: {theirs_value}")
        # Are the 3 values conflicted? They are conflicted if the number of unique values is 3.
        # To get the number of unique values, put them in a set and get the size.
        num_distinct_values = len({base_value, ours_value, theirs_value})
        is_conflict = num_distinct_values == 3
        logger.debug(f"uniq_path: {uniq_path}; num_distinct_values: {num_distinct_values}; is_conflict: {is_conflict}")

        if is_conflict:
            # Ours tag-name and Theirs tag-name are the same.
            tag_name = ours_paths_details[uniq_path]['tag_name']
            theirs_tag_to_search = f'<{tag_name}>{theirs_value}</{tag_name}>'
            ours_tag_replacement = f'<{tag_name}>{ours_value}</{tag_name}>'

            # Set Ours value to Theirs tag. 'theirs_element_reference' keeps a reference to the element in
            # theirs_xml_doc.
            theirs_element_reference = theirs_paths_details[uniq_path]['element']
            theirs_element_reference.text = ours_value

            #
            # check_if_modified_axl_str_is_equal_to_theirs_xml_control_doc():
            # We have the control-doc as XML-doc, and the XML to be compared against the control-doc as string.
            # What possibilities of comparisons we have?
            # The LXMLOutputChecker().checker.check_output() needs two strings.
            # Comparison is also possible between to XML-docs with etree.tostring(xml_doc).
            # But is there something taking one XML-doc and one XML-string? I don't know.
            #
            neutral_formatted_theirs_xml_str = etree.tostring(theirs_xml_doc)

            def check_if_modified_axl_str_is_equal_to_theirs_xml_control_doc(xml_str: str) -> bool:
                neutral_formatted_prepared_xml_str = \
                    etree.tostring(etree.fromstring(remove_xmlns_from_xml_string(xml_str).encode()))
                return neutral_formatted_theirs_xml_str == neutral_formatted_prepared_xml_str

            theirs_xml_str = utils.replace_token(theirs_xml_str, theirs_tag_to_search, ours_tag_replacement,
                                                 check_if_modified_axl_str_is_equal_to_theirs_xml_control_doc)

    return theirs_xml_str


def get_paths_details(xml_doc):
    xml_doc_tree = etree.ElementTree(xml_doc)
    paths_info = {}
    for xpath, tag_pattern in g_path_and_patterns.items():
        elements = xml_doc.findall(xpath)
        for element in elements:
            if not tag_pattern or tag_pattern and re.match(tag_pattern, element.tag):
                path = xml_doc_tree.getpath(element)
                tag_name = element.tag
                value = element.text
                path_info = {path: {'tag_name': tag_name, 'value': value, 'element': element}}
                paths_info.update(path_info)
    return paths_info
