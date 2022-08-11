import textwrap
import unittest

from base_ut_test import BaseTest
from xml_paths_merge_driver import replace_values_at_xpaths_in_theirs


#
# TODOs
#
# Vars:
#   - Number of XPaths.
#   - All XPaths present in Ours and Theirs:    test_all_xpath_present_but_unchanged_in_all_and_without_errror
#   - 1 XPath missing in Ours:      test_xpath_missing_in_ours
#   - 1 XPath missing in Theirs:    test_xpath_missing_in_theirs
#   - 1 XPath ambiguous in Ours:    test_xpath_ambuguous_in_ours
#   - 1 XPath ambiguous in Theirs:  test_xpath_ambuguous_in_theirs
#


class ReplaceValuesAtXPaths(BaseTest):
    ancentor_o_xml_str = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <!--    
        This pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
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

    def test_all_xpath_present_but_unchanged_in_all(self):
        xpaths_to_be_replaced = [
            './version',
            '.parent/version',
            './properties/revision'
        ]

        ancenstor_o_xml_str = self.ancentor_o_xml_str
        # Theirs B is unchanged.
        theirs_b_xml_str = ancenstor_o_xml_str
        # In Ours, the XPaths project/parent/version, project/version, and
        # project/properties/revision are changed.
        ours_a_xml_str = textwrap.dedent("""\
        <?xml version="1.0" encoding="UTF-8"?>
        <!--    
            This pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
            The Goal is to control the path to be replaced without changing any other's path version.
        -->
        <project xmlns="http://maven.apache.org/POM/4.0.0"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
            <parent>
                <groupId>com.mycompany.app</groupId>
                <artifactId>my-app</artifactId>
                <version>NEW_VALUE_PARENT_VERSION</version>
            </parent>
            <modelVersion>4.0.0</modelVersion>
            <groupId>com.dummy</groupId>
            <artifactId>java-web-project</artifactId>
            <packaging>war</packaging>
            <version>NEW_VALUE_VERSION</version>
            <name>java-web-project Maven Webapp</name>
            <url>http://maven.apache.org</url>
            <properties>
                <revision>NEW_VALUE_PROPERTIES_REVISION</revision>
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

        modified_theirs_b_xml_str, errors = replace_values_at_xpaths_in_theirs(
            xpaths_to_be_replaced,
            ancenstor_o_xml_str, ours_a_xml_str, theirs_b_xml_str)

        # Because none of the given XPaths are changed in Theirs, there is no need to fake Theirs
        # with values from Ours. This means Theirs keeps unchanged.
        expected_xml_str = theirs_b_xml_str

        # print("expected_xml_str:\n{}".format(expected_xml_str))
        # print("modified_theirs_b_xml_str:\n{}".format(modified_theirs_b_xml_str))

        self.assertEqual(expected_xml_str, modified_theirs_b_xml_str)
        self.assertEqual(0, len(errors), errors)

    def test_no_xpath_present(self):
        xpaths_to_be_replaced = [
            './not/existing/path',
            './another/not/existing/path'
        ]

        ancenstor_o_xml_str = textwrap.dedent("""\
        <?xml version="1.0" encoding="UTF-8"?>
        <project xmlns="http://maven.apache.org/POM/4.0.0"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

        </project>
        """)
        theirs_b_xml_str = ancenstor_o_xml_str
        ours_a_xml_str = ancenstor_o_xml_str

        modified_theirs_b_xml_str, errors = replace_values_at_xpaths_in_theirs(
            xpaths_to_be_replaced,
            ancenstor_o_xml_str, ours_a_xml_str, theirs_b_xml_str)

        expected_xml_str = ours_a_xml_str

        # print("expected_xml_str:\n{}".format(expected_xml_str))
        # print("modified_theirs_b_xml_str:\n{}".format(modified_theirs_b_xml_str))

        self.assertEqual(expected_xml_str, modified_theirs_b_xml_str)
        self.assertEqual(0, len(errors), errors)

    def test_xpath_missing_in_ours(self):
        xpaths_to_be_replaced = [
            './version',
            '.parent/version',  # Missing in ourOurss.
            './properties/revision'
        ]

        ancenstor_o_xml_str = self.ancentor_o_xml_str
        # Theirs B is unchanged.
        theirs_b_xml_str = ancenstor_o_xml_str
        # In Ours, the XPaths project/parent/version, project/version, and
        # project/properties/revision are changed.
        ours_a_xml_str = textwrap.dedent("""\
         <?xml version="1.0" encoding="UTF-8"?>
         <!--    
             This pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
             The Goal is to control the path to be replaced without changing any other's path version.
         -->
         <project xmlns="http://maven.apache.org/POM/4.0.0"
                  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
             <modelVersion>4.0.0</modelVersion>
             <groupId>com.dummy</groupId>
             <artifactId>java-web-project</artifactId>
             <packaging>war</packaging>
             <version>NEW_VALUE_VERSION</version>
             <name>java-web-project Maven Webapp</name>
             <url>http://maven.apache.org</url>
             <properties>
                 <revision>NEW_VALUE_PROPERTIES_REVISION</revision>
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

        modified_theirs_b_xml_str, errors = replace_values_at_xpaths_in_theirs(
            xpaths_to_be_replaced,
            ancenstor_o_xml_str, ours_a_xml_str, theirs_b_xml_str)

        # Because none of the given XPaths are changed in Theirs, there is no need to fake Theirs
        # with values from Ours. This means Theirs keeps unchanged.
        expected_xml_str = theirs_b_xml_str

        self.assertEqual(expected_xml_str, modified_theirs_b_xml_str)
        self.assertEqual(0, len(errors), errors)

    def test_xpath_missing_in_theirs(self):
        xpaths_to_be_replaced = [
            './version',
            '.parent/version',  # Missing in Theirs.
            './properties/revision'
        ]

        ancenstor_o_xml_str = self.ancentor_o_xml_str
        ours_a_xml_str = textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!--    
                This pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
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
                <version>NEW_VALUE_VERSION</version>
                <name>java-web-project Maven Webapp</name>
                <url>http://maven.apache.org</url>
                <properties>
                    <revision>NEW_VALUE_PROPERTIES_REVISION</revision>
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

        theirs_b_xml_str = textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!--    
                This pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
                The Goal is to control the path to be replaced without changing any other's path version.
            -->
            <project xmlns="http://maven.apache.org/POM/4.0.0"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
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

        modified_theirs_b_xml_str, errors = replace_values_at_xpaths_in_theirs(
            xpaths_to_be_replaced,
            ancenstor_o_xml_str, ours_a_xml_str, theirs_b_xml_str)

        # Because none of the given XPaths are changed in Theirs, there is no need to fake Theirs
        # with values from Ours. This means Theirs keeps unchanged.
        expected_xml_str = theirs_b_xml_str

        self.assertEqual(expected_xml_str, modified_theirs_b_xml_str)
        self.assertEqual(0, len(errors), errors)

    def test_xpath_ambuguous_in_ours(self):
        xpaths_to_be_replaced = [
            './dependencies/dependency'  # Ambiguous XPath.
        ]

        ancenstor_o_xml_str = self.ancentor_o_xml_str
        ours_a_xml_str = textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!--    
                This pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
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
            </project>
        """)

        theirs_b_xml_str = textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!--    
                This pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
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
                    <dependency>
                        <groupId>org.springframework</groupId>
                        <artifactId>spring-webmvc</artifactId>
                        <version>${spring.version}</version>
                    </dependency>
                </dependencies>
            </project>
        """)

        modified_theirs_b_xml_str, errors = replace_values_at_xpaths_in_theirs(
            xpaths_to_be_replaced,
            ancenstor_o_xml_str, ours_a_xml_str, theirs_b_xml_str)

        # Because none of the given XPaths are changed in Theirs, there is no need to fake Theirs
        # with values from Ours. This means Theirs keeps unchanged.
        expected_xml_str = theirs_b_xml_str

        self.assertEqual(expected_xml_str, modified_theirs_b_xml_str)
        self.assertEqual(1, len(errors), errors)
        self.assertEqual(
            errors,
            ["The XML-path './dependencies/dependency' in Ours (%A) is ambiguous. It is present 3 times."])

    def test_xpath_ambuguous_in_theirs(self):
        xpaths_to_be_replaced = [
            './dependencies/dependency'  # Ambiguous XPath.
        ]

        ancenstor_o_xml_str = self.ancentor_o_xml_str
        ours_a_xml_str = textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!--    
                This pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
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
                    <dependency>
                        <groupId>org.springframework</groupId>
                        <artifactId>spring-webmvc</artifactId>
                        <version>${spring.version}</version>
                    </dependency>
                </dependencies>
            </project>
        """)
        theirs_b_xml_str = textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!--    
                This pom contains the ORIGINAL_VALUE in multiple XML-path. Imagine it as "1.0.0".
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
            </project>
        """)

        modified_theirs_b_xml_str, errors = replace_values_at_xpaths_in_theirs(
            xpaths_to_be_replaced,
            ancenstor_o_xml_str, ours_a_xml_str, theirs_b_xml_str)

        # Because none of the given XPaths are changed in Theirs, there is no need to fake Theirs
        # with values from Ours. This means Theirs keeps unchanged.
        expected_xml_str = theirs_b_xml_str

        self.assertEqual(expected_xml_str, modified_theirs_b_xml_str)
        self.assertEqual(1, len(errors), errors)
        self.assertEqual(
            errors,
            ["The XML-path './dependencies/dependency' in Theirs (%B) is ambiguous. It is present 3 times."])

    if __name__ == '__main__':
        unittest.main()
