%define __jar_repack 0
Summary: Kafka and distributed topic based producer consumer queue
Name: kafka
Version: 0.7.2
Release: 1
License: Apache (v2)
Group: Applications
# You can get the sources by selecting one of the mirrors from the https://www.apache.org/dyn/closer.cgi/incubator/kafka/kafka-0.7.2-incubating/kafka-0.7.2-incubating-src.tgz site
Source0: %{name}-%{version}-incubating-src.tgz
Source1: ftp://ftp.nowhere.com/kafka.init
Source2: ftp://ftp.nowhere.com/kafka-zookeeper.init
URL: http://kafka.apache.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Distribution: m6d
Vendor: m6d
Packager: edlinuxguru@gmail.com

Requires(pre): jdk >= 1.6

%description
Follow this example and you can do no wrong

%pre
getent group kafka >/dev/null || groupadd -r kafka
getent passwd kafka >/dev/null || \
    useradd -r -g kafka -d %{_sharedstatedir}/kafka -s /sbin/nologin \
    -c "User for kafka services" kafka
exit 0
%prep

%setup -q -n kafka-0.7.2-incubating-src
%build
./sbt update
./sbt package

%install
pwd
rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/opt/kafka
mkdir -p $RPM_BUILD_ROOT/opt/kafka/config

cp -r bin $RPM_BUILD_ROOT/opt/kafka
cp -r config $RPM_BUILD_ROOT/opt/kafka/config-sample

cp -r contrib $RPM_BUILD_ROOT/opt/kafka/contrib
cp -r core $RPM_BUILD_ROOT/opt/kafka/core
cp -r examples $RPM_BUILD_ROOT/opt/kafka/examples
cp -r lib $RPM_BUILD_ROOT/opt/kafka/lib
cp -r lib_managed $RPM_BUILD_ROOT/opt/kafka/lib_managed
cp -r perf $RPM_BUILD_ROOT/opt/kafka/perf
cp -r project $RPM_BUILD_ROOT/opt/kafka/project
cp sbt $RPM_BUILD_ROOT/opt/kafka/
#cp -r system_test $RPM_BUILD_ROOT/opt/kafka/system_test #Do not need this 

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

%clean
#used to cleanup things outside the build area and possibly inside.

%changelog
* Wed Oct 12 2016 "R. David Murray" <rdmurray@bitdance.com>
- Bring changelog up to date.
- Remove copy of 'clients' directory, that doesn't exist after the build.
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

