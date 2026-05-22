%bcond clang 1

# TDE variables
%define tde_pkg dbus-tqt

%define libname %mklibname %{tde_pkg}-1
%define devname %mklibname %{tde_pkg}-1 -d

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%undefine _debugsource_template

%define tarball_name %{tde_pkg}-trinity

Name:		trinity-%{tde_pkg}
Version:	14.1.6
Release:	1
Summary:	Simple inter-process messaging system
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{version}/main/dependencies/%{tarball_name}-%{version}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo" 
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	pkgconfig(tqt)
BuildRequires:  tqt3-dev-tools
BuildRequires:	trinity-tde-cmake >= %{version}

%{!?with_clang:BuildRequires:	gcc-c++}
BuildRequires:	pkgconfig

# DBUS support
BuildRequires:  pkgconfig(dbus-1)


%description
D-BUS is a message bus, used for sending messages between applications.
Conceptually, it fits somewhere in between raw sockets and CORBA in
terms of complexity.

This package provides the TQt-based shared library for applications using the
Qt interface to D-BUS.

See the dbus description for more information about D-BUS in general.

##########

%package -n %{libname}-0
Summary:		Simple inter-process messaging system (TQt-based shared library)
Group:			System/Libraries

%description -n %{libname}-0
D-BUS is a message bus, used for sending messages between applications.
Conceptually, it fits somewhere in between raw sockets and CORBA in
terms of complexity.

This package provides the TQt-based shared library for applications using the
Qt interface to D-BUS.

See the dbus description for more information about D-BUS in general.

%files -n %{libname}-0
%defattr(-,root,root,-)
%{_libdir}/libdbus-tqt-1.so.0
%{_libdir}/libdbus-tqt-1.so.0.0.0

##########

%package -n %{devname}
Summary:		Simple inter-process messaging system (TQt interface)
Group:			Development/Libraries/C and C++

Requires:		%{libname}-0 = %{EVRD}

Requires:	dbus-devel

%description -n %{devname}
D-BUS is a message bus, used for sending messages between applications.
Conceptually, it fits somewhere in between raw sockets and CORBA in
terms of complexity.

This package provides the TQt-based shared library for applications using the
Qt interface to D-BUS.

See the dbus description for more information about D-BUS in general.

%files -n %{devname}
%defattr(-,root,root,-)
%{_includedir}/dbus-1.0/*
%{_libdir}/libdbus-tqt-1.so
%{_libdir}/libdbus-tqt-1.la
%{_libdir}/pkgconfig/dbus-tqt.pc

