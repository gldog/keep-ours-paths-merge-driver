import re
import textwrap


from lxml import etree

xml_str = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <project>
        <parent>
            <groupId>com.mycompany.app</groupId>
            <artifactId>my-app</artifactId>
            <version>ORIGINAL_VALUE_PARENT_VERSION</version>
        </parent>
        <modelVersion>4.0.0</modelVersion>
        <groupId>com.dummy</groupId>
        <artifactId>java-web-project</artifactId>
        <packaging>war</packaging>
        <version>ORIGINAL_VALUE_VERSIOIN</version>
        <name>java-web-project Maven Webapp</name>
        <properties>
            <revision>ORIGINAL_VALUE_PROPERTIES_REVISION</revision>
            <depA.version>ORIGINAL_VALUE_PROPERTIES_DEPA</depA.version>
            <depB.version>ORIGINAL_VALUE_PROPERTIES_DEPB</depB.version>
        </properties>
        <dependencies>
            <dependency>
                <groupId>a.groupId.b</groupId>
                <artifactId>a.artifactId.b</artifactId>
                <version>${spring.version}</version>
            </dependency>
            <dependency>
                <groupId>x.groupId.z</groupId>
                <artifactId>x.artifactId.y</artifactId>
                <version>ORIGINAL_VALUE_DEPENDENCIES_DEPENDENCY_2</version>
            </dependency>
        </dependencies>
    </project>
    """)

# encode() is for lxml.
xml_doc = etree.fromstring(xml_str.encode())
xml_doc_tree = etree.ElementTree(xml_doc)

# find() returns 1 element.
elem = xml_doc.find('./version')
print(f"elem 1.1a: {elem}, {elem.text}")

elem.text = 'New Value!'
elem = xml_doc.find('./version')
print(f"elem 1.1b: {elem}, {elem.text}")

elem = xml_doc.find('./version/')
print(f"elem 1.2: {elem}")

tagRegEx = '.+\\.version'
xpath = "./properties/"
# findall() returns an element-list.
elems = xml_doc.findall(xpath)
print(f"elem 2: {elems}")
for elem in elems:
    print(f"elem: {elem.tag}")
    if re.match(tagRegEx, elem.tag):
        print(f"  match! Path is {xml_doc_tree.getpath(elem)}")

xpath = "./dependencies/dependency[groupId='a.groupId.b'][artifactId='a.artifactId.b']/version"
elems = xml_doc.findall(xpath)
print(f"elem 3: {elems}")
for elem in elems:
    print(f"version: {elem.text}")

xpath = "./dependencies/dependency[groupId='x.groupId.z'][artifactId='x.artifactId.y']/version"
# findall() returns an element-list.
elems = xml_doc.findall(xpath)
print(f"elem 4: {elems}")
for elem in elems:
    print(f"version: {elem.text}")
