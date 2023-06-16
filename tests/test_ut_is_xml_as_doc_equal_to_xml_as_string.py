import re
import unittest
import xml.etree.ElementTree as ET

from base_test import BaseTest
from keep_ours_xml_paths_merge_driver import is_xml_as_doc_equal_to_xml_as_string, remove_xmlns_from_xml_string


class TestIsXmlAsDocEqualToXmlAsString(BaseTest):

    def test_o1(self):
        xml_str_without_namespace = remove_xmlns_from_xml_string(self.xml_template)
        new_value = '1.0'
        xml_doc = ET.fromstring(xml_str_without_namespace)
        xml_path = './properties/revision'
        xml_doc.find(xml_path).text = new_value
        path_pattern = r'(<properties>.*<revision>)(.*)(</revision>)'
        xml_str = re.sub(path_pattern, r'\g<1>' + new_value + r'\3', xml_str_without_namespace, 1, flags=re.DOTALL)
        self.assertTrue(is_xml_as_doc_equal_to_xml_as_string(xml_doc, xml_str))


if __name__ == '__main__':
    unittest.main()
