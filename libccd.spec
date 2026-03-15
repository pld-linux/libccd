#
# Conditional build:
%bcond_without	doc	# HTML and man documentation

Summary:	Library for a collision detection between two convex shapes
Summary(pl.UTF-8):	Biblioteka do wykrywania kolizji między dwoma bryłami wypukłymi
Name:		libccd
Version:	2.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/danfis/libccd/tags
# TODO: use
#Source0:	https://github.com/danfis/libccd/archive/%{version}/libccd-%{version}.tar.gz
Source0:	https://github.com/danfis/libccd/archive/refs/tags/v%{version}.tar.gz
# Source0-md5:	fe8ea5024956044a3af6bcbab312950f
Patch0:		%{name}-man.patch
URL:		https://github.com/danfis/libccd
BuildRequires:	cmake >= 2.8.11
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with doc}
BuildRequires:	sphinx-pdg >= 2
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libccd is library for a collision detection between two convex shapes.
libccd implements variation on Gilbert-Johnson-Keerthi algorithm plus
Expand Polytope Algorithm (EPA) and also implements algorithm
Minkowski Portal Refinement (MPR, a.k.a. XenoCollide) as described in
Game Programming Gems 7.

%description -l pl.UTF-8
libccd to biblioteka do wykrywania kolizji między dwiema bryłami
wypukłymi. Implementuje połączenie algorytmu
Gilberta-Johnsona-Keerthiego z algorytmem Expand Polytope Algorithm
(EPA), a także algorytm Minkowski Portal Refinement (MPR, XenoCollide)
zgodnie z opisem w Game Programming Gems 7.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	libccd-static < 2.1

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package apidocs
Summary:	API documentation for libccd library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libccd
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libccd library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libccd.

%prep
%setup -q
%patch -P0 -p1

%build
# autotools build system doesn't install .pc file, use cmake instead
install -d build
cd build
# use relative include,lib dirs for correct .pc file
%cmake .. \
	%{?with_doc:-DBUILD_DOCUMENTATION=ON} \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/ccd

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc BSD-LICENSE README.md
%{_libdir}/libccd.so.*.*
%ghost %{_libdir}/libccd.so.2

%files devel
%defattr(644,root,root,755)
%{_libdir}/libccd.so
%{_includedir}/ccd
%{_pkgconfigdir}/ccd.pc
%dir %{_libdir}/ccd
%{_libdir}/ccd/*.cmake
%if %{with doc}
%{_mandir}/man3/libccd.3*
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/{_static,*.html,*.js}
%endif
