# TODO
# - enable agent in snmpd
%define		plugin haproxy
%include	/usr/lib/rpm/macros.perl
Summary:	Template for Cacti - HAProxy
Name:		cacti-template-%{plugin}
Version:	0.1
Release:	0.2
License:	GPL v2
Group:		Applications/WWW
# the templates were last modified Oct 25, 2010, there's no point using newer version tarball
Source0:	http://www.haproxy.org/download/1.6/src/haproxy-1.6.3.tar.gz
# Source0-md5:	3362d1e268c78155c2474cb73e7f03f9
Patch0:		bang.patch
URL:		https://github.com/haproxy/haproxy/tree/master/contrib/netsnmp-perl
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.554
Requires:	cacti >= 0.8.7e-8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		snmpdconfdir	/etc/snmp
%define		cactidir		/usr/share/cacti
%define		resourcedir		%{cactidir}/resource
%define		scriptsdir		%{cactidir}/scripts
%define		_libdir			%{_prefix}/lib

%description
Cacti snmp-query definition for backends.

%package -n net-snmp-agent-%{plugin}
Summary:	SNMPd agent to provide HAProxy statistics
Group:		Networking/Daemons
Requires:	net-snmp

%description -n net-snmp-agent-%{plugin}
SNMPd agent to provide HAProxy statistics

%prep
%setup -qc
mv haproxy-*/contrib/netsnmp-perl/* .
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{resourcedir},%{scriptsdir},%{snmpdconfdir},%{_libdir}}
cp -p *.xml $RPM_BUILD_ROOT%{resourcedir}
install -p haproxy.pl $RPM_BUILD_ROOT%{_libdir}/snmpd-agent-haproxy

%clean
rm -rf $RPM_BUILD_ROOT

%post
%cacti_import_template %{resourcedir}/cacti_data_query_haproxy_backends.xml
%cacti_import_template %{resourcedir}/cacti_data_query_haproxy_frontends.xml
%cacti_import_template %{resourcedir}/haproxy_backend.xml
%cacti_import_template %{resourcedir}/haproxy_frontend.xml
%cacti_import_template %{resourcedir}/haproxy_socket.xml

%files
%defattr(644,root,root,755)
%doc README
%{resourcedir}/cacti_data_query_haproxy_backends.xml
%{resourcedir}/cacti_data_query_haproxy_frontends.xml
%{resourcedir}/haproxy_backend.xml
%{resourcedir}/haproxy_frontend.xml
%{resourcedir}/haproxy_socket.xml

%files -n net-snmp-agent-%{plugin}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/snmpd-agent-haproxy
