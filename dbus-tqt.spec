%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 3

%define tde_pkg dbus-tqt

%define libdbus %{_lib}dbus

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.63
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Simple inter-process messaging system
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Project
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo" 
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	libtqt4-devel >= %{tde_epoch}:4.2.0

BuildRequires:	trinity-tde-cmake >= %{tde_version}

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

%package -n %{libdbus}-tqt-1-0
Summary:		Simple inter-process messaging system (TQt-based shared library)
Group:			System/Libraries
Provides:		libdbus-tqt-1-0 = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:		trinity-dbus-tqt < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-dbus-tqt = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libdbus}-tqt-1-0
D-BUS is a message bus, used for sending messages between applications.
Conceptually, it fits somewhere in between raw sockets and CORBA in
terms of complexity.

This package provides the TQt-based shared library for applications using the
Qt interface to D-BUS.

See the dbus description for more information about D-BUS in general.

%post -n %{libdbus}-tqt-1-0
/sbin/ldconfig || :

%postun -n %{libdbus}-tqt-1-0
/sbin/ldconfig || :

%files -n %{libdbus}-tqt-1-0
%defattr(-,root,root,-)
%{_libdir}/libdbus-tqt-1.so.0
%{_libdir}/libdbus-tqt-1.so.0.0.0

##########

%package -n %{libdbus}-tqt-1-devel
Summary:		Simple inter-process messaging system (TQt interface)
Group:			Development/Libraries/C and C++
Provides:		libdbus-tqt-1-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		%{libdbus}-tqt-1-0 = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:		trinity-dbus-tqt-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-dbus-tqt-devel = %{?epoch:%{epoch}:}%{version}-%{release}

Requires:	dbus-devel

%description -n %{libdbus}-tqt-1-devel
D-BUS is a message bus, used for sending messages between applications.
Conceptually, it fits somewhere in between raw sockets and CORBA in
terms of complexity.

This package provides the TQt-based shared library for applications using the
Qt interface to D-BUS.

See the dbus description for more information about D-BUS in general.

%post -n %{libdbus}-tqt-1-devel
/sbin/ldconfig || :

%postun -n %{libdbus}-tqt-1-devel
/sbin/ldconfig || :

%files -n %{libdbus}-tqt-1-devel
%defattr(-,root,root,-)
%{_includedir}/dbus-1.0/*
%{_libdir}/libdbus-tqt-1.so
%{_libdir}/libdbus-tqt-1.la
%{_libdir}/pkgconfig/dbus-tqt.pc

