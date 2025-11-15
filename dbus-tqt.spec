#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg dbus-tqt

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libdbus %{_lib}dbus
%else
%define libdbus libdbus
%endif

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)

Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.63
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Simple inter-process messaging system
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Project
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:	https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/dependencies/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:   cmake make

BuildRequires:	libtqt4-devel >= %{tde_epoch}:4.2.0

BuildRequires:	trinity-tde-cmake >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
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

%if 0%{?suse_version}
Requires:	dbus-1-devel
%else
Requires:	dbus-devel
%endif

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

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=ON \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DINCLUDE_INSTALL_DIR=%{_includedir} \
  -DLIB_INSTALL_DIR=%{_libdir} \
  ..

%__make %{?_smp_mflags}


%install
%__make install DESTDIR=%{?buildroot} -C build

