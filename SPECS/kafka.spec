%define __jar_repack 0
Summary: Kafka distributed topic based producer consumer queue
Name: kafka
Version: 0.10.0.1
Release: 1
License: Apache (v2)
Group: Applications
URL: http://kafka.apache.org
Source0: http://archive.apache.org/dist/%{name}/%{version}/%{name}-%{version}-src.tgz
Source1: kafka.init
Source2: kafka-zookeeper.init
# Note: does not work with newer version of gradle.
%define gradle_version 2.8
Source3: https://services.gradle.org/distributions/gradle-%{gradle_version}-bin.zip

BuildRoot: %{_tmppath}/%{name}-%{version}-root

# IMO this should be 'BuildRequires: java-devel', but while 'yum provides' says
# the openjdk package provides that, once installed 'rpm -q --provides' says it
# doesn't, and rpmbuild also says it doesn't.
BuildRequires: java-1.8.0-openjdk-devel >= 1.8
Requires: jre >= 1.8
Provides: kafka

%description
Scalable service for building real time pipelines and streaming applications.

%pre
getent group kafka >/dev/null || groupadd -r kafka
getent passwd kafka >/dev/null || \
    useradd -r -g kafka -d %{_sharedstatedir}/kafka -s /sbin/nologin \
    -c "User for kafka services" kafka
exit 0
%prep

%setup -q -n %{name}-%{version}-src
%build
unzip %{_sourcedir}/gradle-%{gradle_version}-bin.zip
./gradle-%{gradle_version}/bin/gradle
./gradlew jar

%install
rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/opt/kafka
mkdir -p $RPM_BUILD_ROOT/opt/kafka/config
mkdir -p $RPM_BUILD_ROOT/opt/kafka/libs
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/kafka

cp -r bin $RPM_BUILD_ROOT/opt/kafka
cp -r config $RPM_BUILD_ROOT/opt/kafka/config-sample
cp -n */build/libs/* $RPM_BUILD_ROOT/opt/kafka/libs
cp -n */build/dependant-libs*/* $RPM_BUILD_ROOT/opt/kafka/libs
cp -n */*/build/libs/* $RPM_BUILD_ROOT/opt/kafka/libs
cp -n */*/build/dependant-libs*/* $RPM_BUILD_ROOT/opt/kafka/libs
cp LICENSE $RPM_BUILD_ROOT/opt/kafka
cp NOTICE $RPM_BUILD_ROOT/opt/kafka

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install  -m 755 %{S:1} $RPM_BUILD_ROOT/etc/rc.d/init.d/kafka
install  -m 755 %{S:2} $RPM_BUILD_ROOT/etc/rc.d/init.d/kafka-zookeeper
install -d -m0755 $RPM_BUILD_ROOT/%{_sharedstatedir}/kafka

%files
%defattr(-,root,root)

%config %attr(755,root,root) /opt/kafka/config

/opt/kafka
%{_sysconfdir}/rc.d/init.d/kafka
%{_sysconfdir}/rc.d/init.d/kafka-zookeeper
%config %attr(-, kafka, kafka) %{_sharedstatedir}/kafka
%config %attr(-, kafka, kafka) %{_localstatedir}/log/kafka

%clean
#used to cleanup things outside the build area and possibly inside.

%changelog
* Wed Oct 12 2016 "R. David Murray" <rdmurray@bitdance.com>
- Bring changelog up to date.
- Specify build (java-devel) and run (jre) requirements.
- Require java 1.8 since the kafka group says earlier versions are insecure.
- Claim to provide 'kafka'
- Improve the package summary and description strings.
- Update version to and rewrite build rules for kafka 0.10.0.1
- Add kafka log directory
* Tue Jan 15 2013 Balazs Kossovics <bko@witbe.net>
- Compile from source
* Fri Jan 11 2013 Balazs Kossovics <bko@witbe.net>
- Use RPM macros instead of hard coded paths
- Specify attributes for kafka /var/lib directory
- Remove the old buildroot before building
* Thu Jan 10 2013 Balazs Kossovics <bko@witbe.net>
- Add creation of kafka dir in /var/lib
- Specify /bin/sh in runuser so it works even if kafka user has no shell
* Fri Dec 21 2012 kosii <kossovics@gmail.com>
- Fixed program name in init script usage output.
* Wed Jul 11 2012 Edward Capriolo <edward@m6d.com>
- Rebuild against kafka trunk for mirror mode support
* Mon May  7 2012  Edward Capriolo <edward@m6d.com>
- Fix init scripts, clear conf dir, skip system test dir
* Tue May  3 2012  Edward Capriolo <edward@m6d.com>
- Taking care of business
* Tue May  2 2012  Edward Capriolo <edward@m6d.com>
- Oldest at the bottom

