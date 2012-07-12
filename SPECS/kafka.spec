%define __jar_repack 0
Summary: Kafka and distributed topic based producer consumer queue
Name: kafka
Version: 0.7.2
Release: 1
License: Apache (v2)
Group: Applications
Source0: ftp://ftp.nowhere.com/kafka-%{version}.tar.gz
Source1: ftp://ftp.nowhere.com/kafka.init
Source2: ftp://ftp.nowhere.com/kafka-zookeeper.init
URL: http://kafka.apache.org
#BuildRoot: tmp/kafka-0.7.1
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Distribution: m6d
Vendor: m6d
Packager: edlinuxguru@gmail.com

Prereq: jdk >= 1.6

%description
Follow this example and you can do no wrong

%prep

%setup

%build

%install
pwd
mkdir -p $RPM_BUILD_ROOT/opt/kafka
mkdir -p $RPM_BUILD_ROOT/opt/kafka/config

cp -r bin $RPM_BUILD_ROOT/opt/kafka
cp -r clients $RPM_BUILD_ROOT/opt/kafka/clients
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

%files
%defattr(-,root,root)

%config %attr(755,root,root) /opt/kafka/config

/opt/kafka
/etc/rc.d/init.d/kafka
/etc/rc.d/init.d/kafka-zookeeper

%clean
#used to cleanup things outside the build area and possibly inside.

%changelog
* Wed Jul 11 2012 Edward Capriolo <edward@m6d.com>
- Rebuild against kafka trunk for mirror mode support
* Mon May  7 2012  Edward Capriolo <edward@m6d.com>
- Fix init scripts, clear conf dir, skip system test dir
* Tue May  3 2012  Edward Capriolo <edward@m6d.com>
- Taking care of business
* Tue May  2 2012  Edward Capriolo <edward@m6d.com>
- Oldest at the bottom 

