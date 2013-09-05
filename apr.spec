Summary:	Apache Portable Runtime
Name:		apr
Version:	1.4.8
Release:	1
Epoch:		1
License:	Apache v2.0
Group:		Libraries
Source0:	http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
# Source0-md5:	ce2ab01a0c3cdb71cf0a6326b8654f41
URL:		http://apr.apache.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_includedir	/usr/include/apr-1
%define		_datadir	/usr/share/apr-1

%description
The mission of the Apache Portable Runtime (APR) project is to create
and maintain software libraries that provide a predictable and
consistent interface to underlying platform-specific implementations.
The primary goal is to provide an API to which software developers may
code and be assured of predictable if not identical behaviour
regardless of the platform on which their software is built, relieving
them of the need to code special-case conditions to work around or
take advantage of platform-specific deficiencies or features.

%package devel
Summary:	Header files and development documentation for apr
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libtool

%description devel
Header files and development documentation for apr.

%prep
%setup -q

%build
%{__autoconf}
%configure \
	--enable-nonportable-atomics	\
	--enable-static=no		\
	--enable-threads		\
	--with-devrandom=/dev/urandom	\
	--with-installbuilddir=%{_datadir}/build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -snf /usr/bin/libtool $RPM_BUILD_ROOT%{_datadir}/build

%if 0
%{__make} -j check
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES docs/*.html
%attr(755,root,root) %ghost %{_libdir}/libapr-1.so.?
%attr(755,root,root) %{_libdir}/libapr-1.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/apr-1-config
%attr(755,root,root) %{_libdir}/libapr-1.so
%{_libdir}/apr.exp

%dir %{_datadir}
%dir %{_datadir}/build
%attr(755,root,root) %{_datadir}/build/*.sh
%attr(755,root,root) %{_datadir}/build/libtool
%{_datadir}/build/*.awk
%{_datadir}/build/*.mk
%{_includedir}
%{_pkgconfigdir}/apr-1.pc

