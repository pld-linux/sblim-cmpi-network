Summary:	SBLIM CMPI Network instrumentation
Summary(pl.UTF-8):	Przyrządy pomiarowe sieci dla SBLIM CMPI
Name:		sblim-cmpi-network
Version:	1.4.0
Release:	1
License:	Eclipse Public License v1.0
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
# Source0-md5:	2e48152a4b3c9a74736b0d47cae5bea7
URL:		http://sblim.sourceforge.net/
BuildRequires:	sblim-cmpi-base-devel
BuildRequires:	sblim-cmpi-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	sblim-cmpi-base
Requires:	sblim-sfcb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SBLIM CMPI Network providers.

%description -l pl.UTF-8
Dostawcy informacji na temat sieci dla SBLIM CMPI.

%package libs
Summary:	SBLIM Network instrumentation library
Summary(pl.UTF-8):	Biblioteka pomiarowa SBLIM Network
Group:		Libraries

%description libs
SBLIM Network instrumentation library.

%description libs -l pl.UTF-8
Biblioteka pomiarowa SBLIM Network.

%package devel
Summary:	Header files for SBLIM Network instrumentation library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki pomiarowej SBLIM Network
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for SBLIM Network instrumentation library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki pomiarowej SBLIM Network.

%package static
Summary:	Static SBLIM Network instrumentation library
Summary(pl.UTF-8):	Statyczna biblioteka pomiarowa SBLIM Network
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static SBLIM Network instrumentation library.

%description static -l pl.UTF-8
Statyczna biblioteka pomiarowa SBLIM Network.

%prep
%setup -q

%build
%configure \
	CIMSERVER=sfcb \
	PROVIDERDIR=%{_libdir}/cmpi

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cmpi/lib*.{la,a}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_datadir}/%{name}/provider-register.sh \
	-r %{_datadir}/%{name}/Linux_Network.registration \
	-m %{_datadir}/%{name}/Linux_Network.mof >/dev/null

%preun
if [ "$1" = "0" ]; then
	%{_datadir}/%{name}/provider-register.sh -d \
		-r %{_datadir}/%{name}/Linux_Network.registration \
		-m %{_datadir}/%{name}/Linux_Network.mof >/dev/null
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog DEBUG NEWS README README.TEST
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_CSNetworkPortProvider.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_EthernetPortProvider.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_IPProtocolEndpointProvider.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_LocalLoopbackPortProvider.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_NetworkPortImplementsIPEndpointProvider.so
%attr(755,root,root) %{_libdir}/cmpi/libcmpiOSBase_TokenRingPortProvider.so
%dir %{_datadir}/sblim-cmpi-network
%{_datadir}/sblim-cmpi-network/Linux_Network.mof
%{_datadir}/sblim-cmpi-network/Linux_Network.registration
%attr(755,root,root) %{_datadir}/sblim-cmpi-network/provider-register.sh

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSBase_CommonNetwork.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOSBase_CommonNetwork.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOSBase_CommonNetwork.so
%{_libdir}/libOSBase_CommonNetwork.la
# XXX: shared dir
%dir %{_includedir}/sblim
%{_includedir}/sblim/OSBase_CommonNetwork.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libOSBase_CommonNetwork.a
