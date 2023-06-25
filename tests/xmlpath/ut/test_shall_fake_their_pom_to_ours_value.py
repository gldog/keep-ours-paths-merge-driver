import re
import unittest
import xml.etree.ElementTree as ET

from test_base_xml import BaseXmlTest
from keep_ours_xml_paths_merge_driver import shall_fake_theirs_xpath_to_ours_value


class TestShallFakeTheirsPomToOursValue(BaseXmlTest):

    def test_shall_fake_theirs_pom_to_ours_value(self):
        #
        # The namespaces are removed to allow simple convenient paths without
        # namespaces like './properties/revision'. If the namespace was part of the XML at the
        # time of parsing, each element would be prefixed with a namespace. And that namespace
        # would have to be given in the path.
        #
        # From https://docs.python.org/3/library/xml.etree.elementtree.html#supported-xpath-syntax:
        #   "Changed in version 3.8: Support for star-wildcards was added."
        # In that case the namespaces could be left as is, and the path contains wildcards
        # for the namespaces: './{*}properties/{*}revision'
        #

        #
        # For all tests:
        # It must have been checked the xpath is not ambiguous.
        #

        xml_without_namespace = re.sub(' xmlns="[^"]+"', '', self.xml_template, count=1)
        ancestor_o_str = xml_without_namespace
        theirs_b_str = xml_without_namespace
        ancestor_o_doc = ET.fromstring(ancestor_o_str)
        theirs_b_doc = ET.fromstring(theirs_b_str)

        xpath = './properties/revision'

        # The path above has the same value in both docs.
        shall_fake = shall_fake_theirs_xpath_to_ours_value(xpath, ancestor_o_doc, theirs_b_doc)
        self.assertFalse(shall_fake)

        # Make the values different.
        ancestor_o_doc.find(xpath).text = '1.0'
        theirs_b_doc.find(xpath).text = '2.0'
        shall_fake = shall_fake_theirs_xpath_to_ours_value(xpath, ancestor_o_doc, theirs_b_doc)
        self.assertTrue(shall_fake)


if __name__ == '__main__':
    unittest.main()
