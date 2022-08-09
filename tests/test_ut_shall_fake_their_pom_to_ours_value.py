import re
import unittest
import xml.etree.ElementTree as ET

from base_ut_test import BaseTest
from xml_paths_merge_driver import shall_fake_their_pom_to_ours_value


class MyTestCase(BaseTest):

    def test_shall_fake_their_pom_to_ours_value(self):
        #
        # The namespaces are removed to allow simple convenient pathes without
        # namesspaces like './properties/revision'. If the namespace would be part of the XML at the
        # time of parsing, each element would be prefixed with a namespace. And that namespace
        # would have to be given in the path.
        #
        # From https://docs.python.org/3/library/xml.etree.elementtree.html#supported-xpath-syntax:
        #   "Changed in version 3.8: Support for star-wildcards was added."
        # In that case the namespaces could be left as is, and the path contains wildcards
        # for the namespaces: './{*}properties/{*}revision'
        #

        xml_without_namespace = re.sub(' xmlns="[^"]+"', '', self.xml_template, count=1)
        ancestor_o_str = xml_without_namespace
        theirs_b_str = xml_without_namespace
        ancestor_o_doc = ET.fromstring(ancestor_o_str)
        theirs_b_doc = ET.fromstring(theirs_b_str)

        xpath = './properties/revision'

        ancestor_o_doc.find(xpath).text = '1.0'
        theirs_b_doc.find(xpath).text = '1.0'
        shall_fake = shall_fake_their_pom_to_ours_value(xpath, ancestor_o_doc, theirs_b_doc)
        self.assertFalse(shall_fake)

        ancestor_o_doc.find(xpath).text = '1.0'
        theirs_b_doc.find(xpath).text = '2.0'
        shall_fake = shall_fake_their_pom_to_ours_value(xpath, ancestor_o_doc, theirs_b_doc)
        self.assertTrue(shall_fake)


if __name__ == '__main__':
    unittest.main()
