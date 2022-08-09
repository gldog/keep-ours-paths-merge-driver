import re
import xml.etree.ElementTree as ET
from io import BytesIO

xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <properties>
        <revision></revision>
    </properties>
</project>    
"""

# Uses a list comprehension and element tree's iterparse function to create a dictionary containing the namespace prefix
# and it's uri. The underscore is utilized to remove the "start-ns" output from the list.
namespaces = {node[0]: node[1] for _, node in ET.iterparse(BytesIO(xml_template.encode("UTF-8")), events=['start-ns'])}
# Iterates through the newly created namespace list registering each one.
for key, value in namespaces.items():
    ET.register_namespace(key, value)

val = "1.0"

# Modify XML as DOM
root1Elem = ET.fromstring(xml_template)
path = './{*}properties/{*}revision'
root1Elem.find(path).text = val

# Modify XML as string
xml_as_string = \
    re.sub(r'(<properties>.*<revision>)(.*)(</revision>)', r'\g<1>' + val + r'\3', xml_template, flags=re.DOTALL)
root2Elem = ET.fromstring(xml_as_string)

#
# Compare both
#
xml1_as_String = ET.tostring(root1Elem, encoding='unicode')
print("xml1_as_String:\n{}".format(xml1_as_String))
xml2_as_String = ET.tostring(root2Elem, encoding='unicode')
print("xml2_as_String:\n{}".format(xml2_as_String))
assert xml1_as_String == xml2_as_String
