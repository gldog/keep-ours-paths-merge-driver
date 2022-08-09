import textwrap
import unittest
import xml.etree.ElementTree as ET

from base_ut_test import BaseTest
from xml_paths_merge_driver import is_xpath_ambiguous, replace_value_at_xpath_in_xml_str, \
    remove_xmlns_from_xml_string


class ReplaceOnlySpecificXPath(BaseTest):
    original_xml_str = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <!--    
        Thsi pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
        The Goal is to control the path to be replaced without changing any other's path version.
    -->
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

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
        <url>http://maven.apache.org</url>

        <properties>
            <revision>ORIGINAL_VALUE</revision>
            <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
            <maven.compiler.source>1.8</maven.compiler.source>
            <maven.compiler.target>1.8</maven.compiler.target>
            <spring.version>ORIGINAL_VALUE</spring.version>
            <jetty.maven.plugin-version>ORIGINAL_VALUE</jetty.maven.plugin-version>
        </properties>

        <dependencies>
            <!-- This is a dependency which version is set by a property. -->
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-webmvc</artifactId>
                <version>${spring.version}</version>
            </dependency>
            <!-- This is a dependency with an explicit version. -->
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-test</artifactId>
                <version>ORIGINAL_VALUE</version>
            </dependency>
            <!-- This is another dependency with an explicit version. -->
            <dependency>
                <groupId>ch.qos.logback</groupId>
                <artifactId>logback-classic</artifactId>
                <version>ORIGINAL_VALUE</version>
            </dependency>
        </dependencies>

        <build>
            <finalName>java-web-project</finalName>
            <plugins>
                <!-- This is a plugin which version is set by a property. -->
                <plugin>
                    <groupId>org.eclipse.jetty</groupId>
                    <artifactId>jetty-maven-plugin</artifactId>
                    <version>${jetty.maven.plugin-version}</version>
                </plugin>
                <!-- This is a plugin with an explicit version. -->
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-surefire-plugin</artifactId>
                    <version>ORIGINAL_VALUE</version>
                </plugin>
                <!-- This is another plugin with an explicit version. -->
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-war-plugin</artifactId>
                    <version>ORIGINAL_VALUE</version>
                </plugin>
            </plugins>
        </build>

    </project>
    """)

    def test_replace_value_at_xpath_in_xml_str_for_path_project_version(self):
        xpath = './version'
        original_xml_doc = ET.fromstring(remove_xmlns_from_xml_string(self.original_xml_str))

        # This is just to protect the function unter test.
        is_absent_or_ambiguous = is_xpath_ambiguous(xpath, original_xml_doc)
        self.assertFalse(is_absent_or_ambiguous)

        # Function under test.
        new_value = 'NEW_VALUE'
        modified_xml_str = replace_value_at_xpath_in_xml_str(xpath, new_value, self.original_xml_str)

        expected_xml_str = textwrap.dedent("""\
        <?xml version="1.0" encoding="UTF-8"?>
        <!--    
            Thsi pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
            The Goal is to control the path to be replaced without changing any other's path version.
        -->
        <project xmlns="http://maven.apache.org/POM/4.0.0"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

            <parent>
                <groupId>com.mycompany.app</groupId>
                <artifactId>my-app</artifactId>
                <version>ORIGINAL_VALUE</version>
            </parent>
            
            <modelVersion>4.0.0</modelVersion>
            <groupId>com.dummy</groupId>
            <artifactId>java-web-project</artifactId>
            <packaging>war</packaging>
            <version>NEW_VALUE</version>
            <name>java-web-project Maven Webapp</name>
            <url>http://maven.apache.org</url>

            <properties>
                <revision>ORIGINAL_VALUE</revision>
                <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
                <maven.compiler.source>1.8</maven.compiler.source>
                <maven.compiler.target>1.8</maven.compiler.target>
                <spring.version>ORIGINAL_VALUE</spring.version>
                <jetty.maven.plugin-version>ORIGINAL_VALUE</jetty.maven.plugin-version>
            </properties>

            <dependencies>
                <!-- This is a dependency which version is set by a property. -->
                <dependency>
                    <groupId>org.springframework</groupId>
                    <artifactId>spring-webmvc</artifactId>
                    <version>${spring.version}</version>
                </dependency>
                <!-- This is a dependency with an explicit version. -->
                <dependency>
                    <groupId>org.springframework</groupId>
                    <artifactId>spring-test</artifactId>
                    <version>ORIGINAL_VALUE</version>
                </dependency>
                <!-- This is another dependency with an explicit version. -->
                <dependency>
                    <groupId>ch.qos.logback</groupId>
                    <artifactId>logback-classic</artifactId>
                    <version>ORIGINAL_VALUE</version>
                </dependency>
            </dependencies>

            <build>
                <finalName>java-web-project</finalName>
                <plugins>
                    <!-- This is a plugin which version is set by a property. -->
                    <plugin>
                        <groupId>org.eclipse.jetty</groupId>
                        <artifactId>jetty-maven-plugin</artifactId>
                        <version>${jetty.maven.plugin-version}</version>
                    </plugin>
                    <!-- This is a plugin with an explicit version. -->
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-surefire-plugin</artifactId>
                        <version>ORIGINAL_VALUE</version>
                    </plugin>
                    <!-- This is another plugin with an explicit version. -->
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-war-plugin</artifactId>
                        <version>ORIGINAL_VALUE</version>
                    </plugin>
                </plugins>
            </build>

        </project>
        """)

        self.assertEqual(expected_xml_str, modified_xml_str)
        # d = Differ()
        # self.assertEqual(expected_xml_str, modified_xml_str, d.compare(
        #    expected_xml_str.splitlines(keepends=True),
        #    modified_xml_str.splitlines(keepends=True)))

    def test_replace_value_at_xpath_in_xml_str_for_path_project_parent_version(self):
        xpath = './parent/version'
        original_xml_doc = ET.fromstring(remove_xmlns_from_xml_string(self.original_xml_str))

        # This is just to protect the function unter test.
        is_absent_or_ambiguous = is_xpath_ambiguous(xpath, original_xml_doc)
        self.assertFalse(is_absent_or_ambiguous)

        # Function under test.
        new_value = 'NEW_VALUE'
        modified_xml_str = replace_value_at_xpath_in_xml_str(xpath, new_value, self.original_xml_str)

        expected_xml_str = textwrap.dedent("""\
        <?xml version="1.0" encoding="UTF-8"?>
        <!--    
            Thsi pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
            The Goal is to control the path to be replaced without changing any other's path version.
        -->
        <project xmlns="http://maven.apache.org/POM/4.0.0"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

            <parent>
                <groupId>com.mycompany.app</groupId>
                <artifactId>my-app</artifactId>
                <version>NEW_VALUE</version>
            </parent>

            <modelVersion>4.0.0</modelVersion>
            <groupId>com.dummy</groupId>
            <artifactId>java-web-project</artifactId>
            <packaging>war</packaging>
            <version>ORIGINAL_VALUE</version>
            <name>java-web-project Maven Webapp</name>
            <url>http://maven.apache.org</url>

            <properties>
                <revision>ORIGINAL_VALUE</revision>
                <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
                <maven.compiler.source>1.8</maven.compiler.source>
                <maven.compiler.target>1.8</maven.compiler.target>
                <spring.version>ORIGINAL_VALUE</spring.version>
                <jetty.maven.plugin-version>ORIGINAL_VALUE</jetty.maven.plugin-version>
            </properties>

            <dependencies>
                <!-- This is a dependency which version is set by a property. -->
                <dependency>
                    <groupId>org.springframework</groupId>
                    <artifactId>spring-webmvc</artifactId>
                    <version>${spring.version}</version>
                </dependency>
                <!-- This is a dependency with an explicit version. -->
                <dependency>
                    <groupId>org.springframework</groupId>
                    <artifactId>spring-test</artifactId>
                    <version>ORIGINAL_VALUE</version>
                </dependency>
                <!-- This is another dependency with an explicit version. -->
                <dependency>
                    <groupId>ch.qos.logback</groupId>
                    <artifactId>logback-classic</artifactId>
                    <version>ORIGINAL_VALUE</version>
                </dependency>
            </dependencies>

            <build>
                <finalName>java-web-project</finalName>
                <plugins>
                    <!-- This is a plugin which version is set by a property. -->
                    <plugin>
                        <groupId>org.eclipse.jetty</groupId>
                        <artifactId>jetty-maven-plugin</artifactId>
                        <version>${jetty.maven.plugin-version}</version>
                    </plugin>
                    <!-- This is a plugin with an explicit version. -->
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-surefire-plugin</artifactId>
                        <version>ORIGINAL_VALUE</version>
                    </plugin>
                    <!-- This is another plugin with an explicit version. -->
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-war-plugin</artifactId>
                        <version>ORIGINAL_VALUE</version>
                    </plugin>
                </plugins>
            </build>

        </project>
        """)

        self.assertEqual(expected_xml_str, modified_xml_str)

    def test_replace_value_at_xpath_in_xml_str_for_path_project_properties_revision(self):
        xpath = './properties/revision'
        original_xml_doc = ET.fromstring(remove_xmlns_from_xml_string(self.original_xml_str))

        # This is just to protect the function unter test.
        is_absent_or_ambiguous = is_xpath_ambiguous(xpath, original_xml_doc)
        self.assertFalse(is_absent_or_ambiguous)

        # Function under test.
        new_value = 'NEW_VALUE'
        modified_xml_str = replace_value_at_xpath_in_xml_str(xpath, new_value, self.original_xml_str)

        expected_xml_str = textwrap.dedent("""\
        <?xml version="1.0" encoding="UTF-8"?>
        <!--    
            Thsi pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
            The Goal is to control the path to be replaced without changing any other's path version.
        -->
        <project xmlns="http://maven.apache.org/POM/4.0.0"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

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
            <url>http://maven.apache.org</url>

            <properties>
                <revision>NEW_VALUE</revision>
                <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
                <maven.compiler.source>1.8</maven.compiler.source>
                <maven.compiler.target>1.8</maven.compiler.target>
                <spring.version>ORIGINAL_VALUE</spring.version>
                <jetty.maven.plugin-version>ORIGINAL_VALUE</jetty.maven.plugin-version>
            </properties>

            <dependencies>
                <!-- This is a dependency which version is set by a property. -->
                <dependency>
                    <groupId>org.springframework</groupId>
                    <artifactId>spring-webmvc</artifactId>
                    <version>${spring.version}</version>
                </dependency>
                <!-- This is a dependency with an explicit version. -->
                <dependency>
                    <groupId>org.springframework</groupId>
                    <artifactId>spring-test</artifactId>
                    <version>ORIGINAL_VALUE</version>
                </dependency>
                <!-- This is another dependency with an explicit version. -->
                <dependency>
                    <groupId>ch.qos.logback</groupId>
                    <artifactId>logback-classic</artifactId>
                    <version>ORIGINAL_VALUE</version>
                </dependency>
            </dependencies>

            <build>
                <finalName>java-web-project</finalName>
                <plugins>
                    <!-- This is a plugin which version is set by a property. -->
                    <plugin>
                        <groupId>org.eclipse.jetty</groupId>
                        <artifactId>jetty-maven-plugin</artifactId>
                        <version>${jetty.maven.plugin-version}</version>
                    </plugin>
                    <!-- This is a plugin with an explicit version. -->
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-surefire-plugin</artifactId>
                        <version>ORIGINAL_VALUE</version>
                    </plugin>
                    <!-- This is another plugin with an explicit version. -->
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-war-plugin</artifactId>
                        <version>ORIGINAL_VALUE</version>
                    </plugin>
                </plugins>
            </build>

        </project>
        """)

        self.assertEqual(expected_xml_str, modified_xml_str)

    def test_replace_value_at_xpath_in_xml_str_for_path_dependency(self):
        xpath = "./dependencies/dependency[groupId='ch.qos.logback'][artifactId='logback-classic']/version"
        original_xml_doc = ET.fromstring(remove_xmlns_from_xml_string(self.original_xml_str))

        # This is just to protect the function unter test.
        is_absent_or_ambiguous = is_xpath_ambiguous(xpath, original_xml_doc)
        self.assertFalse(is_absent_or_ambiguous)

        # Function under test.
        new_value = 'NEW_VALUE'
        modified_xml_str = replace_value_at_xpath_in_xml_str(xpath, new_value, self.original_xml_str)

        expected_xml_str = textwrap.dedent("""\
        <?xml version="1.0" encoding="UTF-8"?>
        <!--    
            Thsi pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
            The Goal is to control the path to be replaced without changing any other's path version.
        -->
        <project xmlns="http://maven.apache.org/POM/4.0.0"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

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
            <url>http://maven.apache.org</url>

            <properties>
                <revision>ORIGINAL_VALUE</revision>
                <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
                <maven.compiler.source>1.8</maven.compiler.source>
                <maven.compiler.target>1.8</maven.compiler.target>
                <spring.version>ORIGINAL_VALUE</spring.version>
                <jetty.maven.plugin-version>ORIGINAL_VALUE</jetty.maven.plugin-version>
            </properties>

            <dependencies>
                <!-- This is a dependency which version is set by a property. -->
                <dependency>
                    <groupId>org.springframework</groupId>
                    <artifactId>spring-webmvc</artifactId>
                    <version>${spring.version}</version>
                </dependency>
                <!-- This is a dependency with an explicit version. -->
                <dependency>
                    <groupId>org.springframework</groupId>
                    <artifactId>spring-test</artifactId>
                    <version>ORIGINAL_VALUE</version>
                </dependency>
                <!-- This is another dependency with an explicit version. -->
                <dependency>
                    <groupId>ch.qos.logback</groupId>
                    <artifactId>logback-classic</artifactId>
                    <version>NEW_VALUE</version>
                </dependency>
            </dependencies>

            <build>
                <finalName>java-web-project</finalName>
                <plugins>
                    <!-- This is a plugin which version is set by a property. -->
                    <plugin>
                        <groupId>org.eclipse.jetty</groupId>
                        <artifactId>jetty-maven-plugin</artifactId>
                        <version>${jetty.maven.plugin-version}</version>
                    </plugin>
                    <!-- This is a plugin with an explicit version. -->
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-surefire-plugin</artifactId>
                        <version>ORIGINAL_VALUE</version>
                    </plugin>
                    <!-- This is another plugin with an explicit version. -->
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-war-plugin</artifactId>
                        <version>ORIGINAL_VALUE</version>
                    </plugin>
                </plugins>
            </build>

        </project>
        """)

        self.assertEqual(expected_xml_str, modified_xml_str)

    if __name__ == '__main__':
        unittest.main()
