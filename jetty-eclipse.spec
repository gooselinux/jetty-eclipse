# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global with_maven 0

%define jettyname   jetty
%define name   	    jetty-eclipse
%define homedir     %{_datadir}/%{name}

Name:           jetty-eclipse
Version:        6.1.21
Release:        1%{?dist}
Summary:        The Jetty Webserver and Servlet Container

Group:          Applications/Internet
License:        ASL 2.0
URL:            http://jetty.mortbay.org/jetty/
Source0:        http://dist.codehaus.org/%{name}/%{jettyname}-%{version}/%{jettyname}-%{version}-src.zip
#Source1:       djetty.script
#Source2:        jetty.init
Source3:        jetty.logrotate
Source4:        jetty-depmap.xml
Source7:        jetty-settings.xml
# Generated with mvn ant:ant
Source8:        jetty-build-files.tar.gz
# Grab the OSGi manifests
Source9:        jetty-manifests.tar.gz
Patch0:     disable-modules.patch
# Fix issues with CookieDump example
Patch1:         jetty-cookiedump.patch
# Fix issues with error logging
Patch2:         jetty-log.patch
# Patch5:       jetty-unix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.6
%if %{with_maven}
# build only
BuildRequires: maven2-plugin-antrun
BuildRequires: maven2-plugin-assembly
BuildRequires: maven2-plugin-compiler
BuildRequires: maven2-plugin-dependency
BuildRequires: maven2-plugin-enforcer
BuildRequires: maven2-plugin-install
BuildRequires: maven2-plugin-jar
BuildRequires: maven2-plugin-plugin
BuildRequires: maven2-plugin-project-info-reports
BuildRequires: maven2-plugin-resources
BuildRequires: maven2-plugin-site
BuildRequires: maven2-plugin-source
BuildRequires: maven2-plugin-remote-resources
BuildRequires: maven2-plugin-war
BuildRequires: maven-plugin-bundle
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-shared-dependency-tree
%else
BuildRequires: ant
%endif
BuildRequires: apache-jasper
BuildRequires: apache-tomcat-apis
BuildRequires: slf4j
BuildRequires: objectweb-asm
BuildRequires: jakarta-commons-el
BuildRequires: jakarta-commons-daemon
BuildRequires: jta

Requires:  jpackage-utils >= 0:1.6
Requires:  ant >= 0:1.6
Requires:  jakarta-commons-el
Requires:  jakarta-commons-logging
Requires:  apache-jasper
Requires:  mx4j >= 0:3.0
Requires:  apache-tomcat-apis
Requires:  slf4j
Requires:  classpathx-mail
Requires:  xerces-j2 >= 0:2.7
Requires:  xml-commons-apis
Requires:  jta
Requires(post): jpackage-utils >= 0:1.6
Requires(postun): jpackage-utils >= 0:1.6

%description
Jetty is a 100% Java HTTP Server and Servlet Container. 
This means that you do not need to configure and run a 
separate web server (like Apache) in order to use java, 
servlets and JSPs to generate dynamic content. Jetty is 
a fully featured web server for static and dynamic content. 
Unlike separate server/container solutions, this means 
that your web server and web application run in the same 
process, without interconnection overheads and complications. 
Furthermore, as a pure java component, Jetty can be simply 
included in your application for demonstration, distribution 
or deployment. Jetty is available on all Java supported 
platforms.  Jetty-eclipse is a subset of fully jetty needed
to run Eclipse. 

%prep
%setup -q -n %{jettyname}-%{version}
for f in $(find . -name "*.?ar"); do rm $f; done
find . -name "*.class" -exec rm {} \;

%patch0 -b .sav
%patch1 -b .sav
%patch2 -b .sav
#%patch5

cp %{SOURCE7} settings.xml

#remove glassfish specific file
rm -fr modules/jsp-2.1/src/main/java/com/sun/org/apache/commons/logging/impl/JettyLog.java

%if %{with_maven}
sed -i "s|<groupId>org.codehaus.mojo</groupId>||g" modules/management/pom.xml
sed -i "s|dependency-maven-plugin|maven-dependency-plugin|g" modules/management/pom.xml
sed -i "s|<groupId>org.codehaus.mojo</groupId>||g" modules/jsp-2.0/pom.xml
sed -i "s|dependency-maven-plugin|maven-dependency-plugin|g" modules/jsp-2.0/pom.xml
sed -i "s|<groupId>org.codehaus.mojo</groupId>||g" modules/naming/pom.xml
sed -i "s|dependency-maven-plugin|maven-dependency-plugin|g" modules/naming/pom.xml
sed -i "s|<groupId>org.codehaus.mojo</groupId>||g" modules/annotations/pom.xml
sed -i "s|dependency-maven-plugin|maven-dependency-plugin|g" modules/annotations/pom.xml

sed -i "s|mvn|mvn-jpp|g" distribution/jetty-assembly/pom.xml
%endif

sed -i "s|zip \$D/\$N|zip \$D/\$N/\$N|g" bin/build_release_bundles.sh

%build

%if %{with_maven}
sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" settings.xml
mkdir external_repo
ln -s %{_javadir} external_repo/JPP

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
    -e \
    -s $(pwd)/settings.xml \
    -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
    -Dmaven2.jpp.depmap.file=%{SOURCE4} \
    -Dmaven.test.skip=true \
    install
    
%else
export M2_REPO=`pwd`/.m2

rm -rf $M2_REPO
mkdir $M2_REPO

export DUMMY_FILE=$M2_REPO/dummy.jar
mkdir META-INF
touch META-INF/MANIFEST.MF
jar cf $DUMMY_FILE META-INF/
rm -rf META-INF

mkdir -p $M2_REPO/antlr/antlr/2.7.7
ln -s $(build-classpath antlr) $M2_REPO/antlr/antlr/2.7.7/antlr-2.7.7.jar
mkdir -p $M2_REPO/commons-collections/commons-collections/2.1
ln -s $(build-classpath commons-collections) $M2_REPO/commons-collections/commons-collections/2.1/commons-collections-2.1.jar
mkdir -p $M2_REPO/commons-lang/commons-lang/2.1
ln -s $(build-classpath commons-lang) $M2_REPO/commons-lang/commons-lang/2.1/commons-lang-2.1.jar
mkdir -p $M2_REPO/geronimo-spec/geronimo-spec-jta/1.0.1B-rc4/
ln -s $(build-classpath geronimo/spec-jta-1.0.1B) $M2_REPO/geronimo-spec/geronimo-spec-jta/1.0.1B-rc4/geronimo-spec-jta-1.0.1B-rc4.jar
mkdir -p $M2_REPO/javax/mail/mail/1.4
ln -s $(build-classpath javamail) $M2_REPO/javax/mail/mail/1.4/mail-1.4.jar
mkdir -p $M2_REPO/junit/junit/4.5
ln -s $(build-classpath junit) $M2_REPO/junit/junit/4.5/junit-4.5.jar
mkdir -p $M2_REPO/org/apache/derby/derby/10.1.1.0
ln -s $DUMMY_FILE $M2_REPO/org/apache/derby/derby/10.1.1.0/derby-10.1.1.0.jar #dummy
mkdir -p $M2_REPO/org/codehaus/plexus/plexus-apacheds/1.0-alpha-1
ln -s $DUMMY_FILE $M2_REPO/org/codehaus/plexus/plexus-apacheds/1.0-alpha-1/plexus-apacheds-1.0-alpha-1.jar #dummy
mkdir -p $M2_REPO/org/codehaus/plexus/plexus-container-default/1.0-alpha-9
ln -s $(build-classpath plexus/container-default) $M2_REPO/org/codehaus/plexus/plexus-container-default/1.0-alpha-9/plexus-container-default-1.0-alpha-9.jar
mkdir -p $M2_REPO/org/codehaus/plexus/plexus-utils/1.4.5
ln -s $(build-classpath plexus/utils) $M2_REPO/org/codehaus/plexus/plexus-utils/1.4.5/plexus-utils-1.4.5.jar
mkdir -p $M2_REPO/org/slf4j/slf4j-api/1.3.1
ln -s $(build-classpath slf4j/api) $M2_REPO/org/slf4j/slf4j-api/1.3.1/slf4j-api-1.3.1.jar
mkdir -p $M2_REPO/org/slf4j/slf4j-simple/1.3.1
ln -s $(build-classpath slf4j/simple) $M2_REPO/org/slf4j/slf4j-simple/1.3.1/slf4j-simple-1.3.1.jar
mkdir -p $M2_REPO/org/mortbay/jetty/servlet-api/2.5-20081211/
ln -s $(build-classpath apache-tomcat-apis/tomcat-servlet2.5-api) $M2_REPO/org/mortbay/jetty/servlet-api/2.5-20081211/servlet-api-2.5-20081211.jar
mkdir -p $M2_REPO/javax/servlet/jsp/jsp-api/2.1/
ln -s $(build-classpath apache-tomcat-apis/tomcat-jsp2.1-api) $M2_REPO/javax/servlet/jsp/jsp-api/2.1/jsp-api-2.1.jar

mkdir -p $M2_REPO/org/mortbay/jetty/jetty/6.1.21
ln -s ../../../../../../modules/jetty/target/jetty-6.1.21.jar $M2_REPO/org/mortbay/jetty/jetty/6.1.21/jetty-6.1.21.jar
mkdir -p $M2_REPO/org/mortbay/jetty/jetty-client/6.1.21/
ln -s ../../../../../../extras/client/target/jetty-client-6.1.21.jar $M2_REPO/org/mortbay/jetty/jetty-client/6.1.21/jetty-client-6.1.21.jar
mkdir -p $M2_REPO/org/mortbay/jetty/jetty-naming/6.1.21/
ln -s ../../../../../../modules/naming/target/jetty-naming-6.1.21.jar $M2_REPO/org/mortbay/jetty/jetty-naming/6.1.21/jetty-naming-6.1.21.jar
mkdir -p $M2_REPO/org/mortbay/jetty/jetty-plus/6.1.21/
ln -s ../../../../../../modules/plus/target/jetty-plus-6.1.21.jar $M2_REPO/org/mortbay/jetty/jetty-plus/6.1.21/jetty-plus-6.1.21.jar
mkdir -p $M2_REPO/org/mortbay/jetty/jetty-sslengine/6.1.21/
ln -s ../../../../../../extras/sslengine/target/jetty-sslengine-6.1.21.jar $M2_REPO/org/mortbay/jetty/jetty-sslengine/6.1.21/jetty-sslengine-6.1.21.jar
mkdir -p $M2_REPO/org/mortbay/jetty/jetty-util/6.1.21/
ln -s ../../../../../../modules/util/target/jetty-util-6.1.21.jar $M2_REPO/org/mortbay/jetty/jetty-util/6.1.21/jetty-util-6.1.21.jar
mkdir -p $M2_REPO/org/mortbay/jetty/jetty-util5/6.1.21/
ln -s ../../../../../../modules/util5/target/jetty-util5-6.1.21.jar $M2_REPO/org/mortbay/jetty/jetty-util5/6.1.21/jetty-util5-6.1.21.jar

mkdir -p $M2_REPO/jdbm/jdbm/1.0
ln -s $DUMMY_FILE $M2_REPO/jdbm/jdbm/1.0/jdbm-1.0.jar

mkdir -p $M2_REPO//junit/junit/3.8.2
ln -s $DUMMY_FILE $M2_REPO/junit/junit/3.8.2/junit-3.8.2.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-bootstrap-extract/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-bootstrap-extract/1.5.1/apacheds-bootstrap-extract-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-bootstrap-partition/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-bootstrap-partition/1.5.1/apacheds-bootstrap-partition-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-btree-base/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-btree-base/1.5.1/apacheds-btree-base-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-constants/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-constants/1.5.1/apacheds-constants-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-core/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-core/1.5.1/apacheds-core-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-core-shared/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-core-shared/1.5.1/apacheds-core-shared-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-jdbm-store/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-jdbm-store/1.5.1/apacheds-jdbm-store-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-kerberos-shared/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-kerberos-shared/1.5.1/apacheds-kerberos-shared-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-protocol-changepw/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-protocol-changepw/1.5.1/apacheds-protocol-changepw-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-protocol-dns/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-protocol-dns/1.5.1/apacheds-protocol-dns-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-protocol-kerberos/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-protocol-kerberos/1.5.1/apacheds-protocol-kerberos-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-protocol-ldap/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-protocol-ldap/1.5.1/apacheds-protocol-ldap-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-protocol-ntp/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-protocol-ntp/1.5.1/apacheds-protocol-ntp-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-protocol-shared/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-protocol-shared/1.5.1/apacheds-protocol-shared-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-schema-bootstrap/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-schema-bootstrap/1.5.1/apacheds-schema-bootstrap-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-schema-extras/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-schema-extras/1.5.1/apacheds-schema-extras-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-schema-registries/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-schema-registries/1.5.1/apacheds-schema-registries-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-server-jndi/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-server-jndi/1.5.1/apacheds-server-jndi-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/server/apacheds-utils/1.5.1/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/server/apacheds-utils/1.5.1/apacheds-utils-1.5.1.jar

mkdir -p $M2_REPO//org/apache/directory/shared/shared-asn1/0.9.7/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/shared/shared-asn1/0.9.7/shared-asn1-0.9.7.jar

mkdir -p $M2_REPO//org/apache/directory/shared/shared-asn1-codec/0.9.7/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/shared/shared-asn1-codec/0.9.7/shared-asn1-codec-0.9.7.jar

mkdir -p $M2_REPO//org/apache/directory/shared/shared-ldap/0.9.7/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/shared/shared-ldap/0.9.7/shared-ldap-0.9.7.jar

mkdir -p $M2_REPO//org/apache/directory/shared/shared-ldap-constants/0.9.7/
ln -s $DUMMY_FILE $M2_REPO/org/apache/directory/shared/shared-ldap-constants/0.9.7/shared-ldap-constants-0.9.7.jar

mkdir -p $M2_REPO//org/apache/mina/mina-core/1.1.2/
ln -s $DUMMY_FILE $M2_REPO/org/apache/mina/mina-core/1.1.2/mina-core-1.1.2.jar

mkdir -p $M2_REPO//org/apache/mina/mina-filter-ssl/1.1.2/
ln -s $DUMMY_FILE $M2_REPO/org/apache/mina/mina-filter-ssl/1.1.2/mina-filter-ssl-1.1.2.jar

mkdir -p $M2_REPO//org/codehaus/plexus/plexus-classworlds/1.2-alpha-7/
ln -s $DUMMY_FILE $M2_REPO/org/codehaus/plexus/plexus-classworlds/1.2-alpha-7/plexus-classworlds-1.2-alpha-7.jar

mkdir -p $M2_REPO//org/codehaus/plexus/plexus-component-api/1.0-alpha-20/
ln -s $DUMMY_FILE $M2_REPO/org/codehaus/plexus/plexus-component-api/1.0-alpha-20/plexus-component-api-1.0-alpha-20.jar

tar xzf %{SOURCE8} # build files
tar xzf %{SOURCE9} # osgi manifests
ant -Dmaven.mode.offline=true -Dmaven.repo.local=$M2_REPO -Djunit.skipped=true -Dmaven.test.skip=true javadoc package

mkdir -p lib
cp modules/jetty/target/jetty-6.1.21.jar modules/util/target/jetty-util-6.1.21.jar lib/

%endif

sh bin/build_release_bundles.sh .

%install
rm -rf $RPM_BUILD_ROOT
install -dm 755 $RPM_BUILD_ROOT%{_javadir}/%{name}

%if %{with_maven}
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_datadir}/maven2/poms/JPP.jetty-jetty.pom
install -pm 644 modules/util/pom.xml $RPM_BUILD_ROOT/%{_datadir}/maven2/poms/JPP.jetty-jetty-util.pom

%add_to_maven_depmap org.mortbay.jetty jetty %{version} JPP/jetty jetty
%add_to_maven_depmap org.mortbay.jetty jetty-util %{version} JPP/jetty jetty-util
%add_to_maven_depmap org.mortbay.jetty servlet-api %{version} JPP tomcat6-servlet-2.5-api
%endif

# main pkg
unzip -q %{jettyname}-%{version}.zip -d $RPM_BUILD_ROOT%{homedir}
mv $RPM_BUILD_ROOT%{homedir}/%{jettyname}-%{version}/* $RPM_BUILD_ROOT%{homedir}/
rm -fr $RPM_BUILD_ROOT%{homedir}/%{jettyname}-%{version}

ln -s %{homedir}/lib/%{jettyname}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/%{jettyname}-%{version}.jar
ln -s %{homedir}/lib/%{jettyname}-util-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/%{jettyname}-util-%{version}.jar
pushd $RPM_BUILD_ROOT%{_javadir}/%{name}
ln -s %{jettyname}-%{version}.jar %{jettyname}.jar
ln -s %{jettyname}-util-%{version}.jar %{jettyname}-util.jar
popd

rm -fr $RPM_BUILD_ROOT%{homedir}/logs
rm -fr $RPM_BUILD_ROOT%{homedir}/etc
rm -fr $RPM_BUILD_ROOT%{homedir}/resources
rm -fr $RPM_BUILD_ROOT%{homedir}/webapps
rm -fr $RPM_BUILD_ROOT%{homedir}/contrib
rm -fr $RPM_BUILD_ROOT%{homedir}/distribution
rm -fr $RPM_BUILD_ROOT%{homedir}/examples
rm -fr $RPM_BUILD_ROOT%{homedir}/extras
rm -fr $RPM_BUILD_ROOT%{homedir}/modules
rm -fr $RPM_BUILD_ROOT%{homedir}/patches
rm -fr $RPM_BUILD_ROOT%{homedir}/jxr
rm -fr $RPM_BUILD_ROOT%{homedir}/project-website
rm -fr $RPM_BUILD_ROOT%{homedir}/LICENSES
rm -fr $RPM_BUILD_ROOT%{homedir}/bin
rm -rf $RPM_BUILD_ROOT%{homedir}/contexts
rm -fr $RPM_BUILD_ROOT%{homedir}/*.txt
rm -fr $RPM_BUILD_ROOT%{homedir}/*.xml
rm -fr $RPM_BUILD_ROOT%{homedir}/start.jar
rm -fr $RPM_BUILD_ROOT%{homedir}/pom.*
rm -fr $RPM_BUILD_ROOT%{homedir}/*.zip
rm -fr $RPM_BUILD_ROOT%{homedir}/README.txt

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with_maven}
%post
%update_maven_depmap

%postun
%update_maven_depmap
%endif

%files
%defattr(-,root,root,-)
# %{_bindir}/*
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/%{jettyname}.jar
%{_javadir}/%{name}/%{jettyname}-%{version}.jar
%{_javadir}/%{name}/%{jettyname}-util.jar
%{_javadir}/%{name}/%{jettyname}-util-%{version}.jar
%if %{with_maven}
%{_datadir}/maven2
%{_mavendepmapfragdir}
%endif
%{homedir}
%doc NOTICE.txt
%doc VERSION.txt

%changelog
* Wed Feb 17 2010 Jeff Johnston <jjohnstn@redhat.com> - 6.1.21-1
- Initial release based on jetty-6.1.21-7.
