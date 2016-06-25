# TODO: PLDify init script
Summary:	iWarp Port Mapper userspace daemon
Summary(pl.UTF-8):	Demon przestrzeni użytkownika usługi iWarp Port Mapper
Name:		libiwpm
Version:	1.0.5
Release:	1
License:	BSD or GPL v2
Group:		Libraries
Source0:	https://www.openfabrics.org/downloads/libiwpm/%{name}-%{version}.tar.gz
# Source0-md5:	946a177c5cc912981ff08d7bca15977a
URL:		https://www.openfabrics.org/
BuildRequires:	libnl-devel >= 3.2
BuildRequires:	rpmbuild(macros) >= 1.647
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	systemd-units >= 0.38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

%description
libiwpm provides a userspace service for iWarp drivers to claim TCP
ports through the standard socket interface.

%description -l pl.UTF-8
libiwpm dostarcza usługę przestrzeni użytkownika dla sterowników
iWarp, pozwalającą im zajmować porty TCP poprzez standardowy interfejs
gniazdowy.

%package devel
Summary:	Header files for iWarp Port Mapper
Summary(pl.UTF-8):	Pliki nagłówkowe usługi iWarp Port Mapper
Group:		Development/Libraries
Requires:	libnl-devel >= 3.2

%description devel
Header files for iWarp Port Mapper.

%description devel -l pl.UTF-8
Pliki nagłówkowe usługi iWarp Port Mapper.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -Dp iwpmd_init $RPM_BUILD_ROOT/etc/rc.d/init.d/iwpmd
install -Dp iwpmd.service $RPM_BUILD_ROOT%{systemdunitdir}/iwpmd.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add iwpmd
%systemd_post iwpmd.service
%service iwpmd restart

%preun
%systemd_preun iwpmd.service
if [ "$1" = "0" ]; then
	%service -q iwpmd stop
	/sbin/chkconfig --del iwpmd
fi

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/iwpmd
%attr(754,root,root) /etc/rc.d/init.d/iwpmd
%{systemdunitdir}/iwpmd.service

%files devel
%defattr(644,root,root,755)
%{_includedir}/rdma/iwarp_pm.h
%{_includedir}/rdma/iwpm_netlink.h
