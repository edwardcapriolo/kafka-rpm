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

%define kafka_home /opt/kafka
%define kafka_user %{name}
%define kafka_group %{name}
%define zookeeper_user zookeeper
%define zookeeper_group zookeeper


%description
Scalable service for building real time pipelines and streaming applications.


%pre
getent group %{zookeeper_group} >/dev/null || groupadd -r %{zookeeper_group}
getent passwd %{zookeeper_user} >/dev/null || \
    useradd -r -g %{zookeeper_group} -d %{_sharedstatedir}/zookeeper -s /sbin/nologin \
    -c "User for zookeeper services" %{zookeeper_user}
getent group %{kafka_group} >/dev/null || groupadd -r %{kafka_group}
getent passwd %{kafka_user} >/dev/null || \
    useradd -r -g %{kafka_group} -d %{_sharedstatedir}/kafka -s /sbin/nologin \
    -c "User for kafka services" %{kafka_user}
exit 0


%prep
%setup -q -n %{name}-%{version}-src


%build
unzip %{_sourcedir}/gradle-%{gradle_version}-bin.zip
./gradle-%{gradle_version}/bin/gradle
./gradlew jar


%install
mkdir -p %{buildroot}%{kafka_home}
mkdir -p %{buildroot}%{kafka_home}/config
mkdir -p %{buildroot}%{kafka_home}/libs
mkdir -p %{buildroot}%{_localstatedir}/log/kafka
mkdir -p %{buildroot}%{_sharedstatedir}/kafka
mkdir -p %{buildroot}%{_localstatedir}/log/zookeeper
mkdir -p %{buildroot}%{_sharedstatedir}/zookeeper

cp -r bin %{buildroot}%{kafka_home}
cp -r config %{buildroot}%{kafka_home}/config-sample
sed "s,log.dirs=.*,log.dirs=%{_sharedstatedir}/kafka," config/server.properties >%{buildroot}%{kafka_home}/config/server.properties
sed "s,dataDir=.*,dataDir=%{_sharedstatedir}/zookeeper," config/zookeeper.properties >%{buildroot}%{kafka_home}/config/zookeeper.properties
cp config/log4j.properties %{buildroot}%{kafka_home}/config
cp -n */build/libs/* %{buildroot}%{kafka_home}/libs
cp -n */build/dependant-libs*/* %{buildroot}%{kafka_home}/libs
cp -n */*/build/libs/* %{buildroot}%{kafka_home}/libs
cp -n */*/build/dependant-libs*/* %{buildroot}%{kafka_home}/libs
cp LICENSE %{buildroot}%{kafka_home}
cp NOTICE %{buildroot}%{kafka_home}

mkdir -p %{buildroot}/etc/rc.d/init.d
install  -m 755 %{S:1} %{buildroot}%{_initrddir}/kafka
install  -m 755 %{S:2} %{buildroot}%{_initrddir}/kafka-zookeeper
install -d -m0755 %{buildroot}/%{_sharedstatedir}/kafka
install -d -m0755 %{buildroot}/%{_sharedstatedir}/zookeeper


%files
%defattr(-,root,root)

%{kafka_home}
%{_initrddir}/kafka
%{_initrddir}/kafka-zookeeper
%config %attr(-, %{kafka_user}, %{kafka_group}) %{_sharedstatedir}/kafka
%config %attr(-, %{kafka_user}, %{kafka_group}) %{_localstatedir}/log/kafka
%config %attr(-, %{zookeeper_user}, %{zookeeper_group}) %{_sharedstatedir}/zookeeper
%config %attr(-, %{zookeeper_user}, %{zookeeper_group}) %{_localstatedir}/log/zookeeper


%post
chkconfig --add kafka
chkconfig --add kafka-zookeeper


%clean
rm -rf %{buildroot}


%changelog
* Thu Oct 13 2016 "R. David Murray" <rdmurray@bitdance.com>
- Add zookeeper user and log directory
- Move the removal of the builddir to %clean
- More macro use.
- Copy modified configs needed for startup into 'config' to serve as defaults
- Run chkconfig in %post to start kafka automatically
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

