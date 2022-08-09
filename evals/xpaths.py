import textwrap
import xml.etree.ElementTree as ET

original_xml_str = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <project>
        <parent>
            <groupId>com.mycompany.app</groupId>
            <artifactId>my-app</artifactId>
            <version>ORIGINAL_VALUE</version>
        </parent>
        <modelVersion>4.0.0</modelVersion>
        <groupId>com.dummy</groupId>
        <artifactId>java-web-project</artifactId>
        <packaging>war</packaging>
        <version>ORIGINAL_VALUE</version>
        <name>java-web-project Maven Webapp</name>
        <properties>
            <revision>ORIGINAL_VALUE</revision>
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
                <version>ORIGINAL_VALUE</version>
            </dependency>
        </dependencies>
    </project>
    """)

original_xml_doc = ET.fromstring(original_xml_str)
elem = original_xml_doc.find('./version')
print("elem: {}".format(elem))

xpath = "./dependencies/dependency[groupId='x.groupId.z'][artifactId='x.artifactId.y']/version"
elems = original_xml_doc.findall(xpath)
print("elem: {}".format(elems))
for elem in elems:
    print("version: {}".format(elem.text))

xpath = "./dependencies/dependency[groupId='a.groupId.b'][artifactId='a.artifactId.b']/version"
elems = original_xml_doc.findall(xpath)
print("elem: {}".format(elems))
for elem in elems:
    print("version: {}".format(elem.text))
