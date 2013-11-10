Summary:	Library for a collision detection between two convex shapes
Summary(pl.UTF-8):	Biblioteka do wykrywania kolizji między dwoma bryłami wypukłymi
Name:		libccd
Version:	1.4
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	http://libccd.danfis.cz/files/%{name}-%{version}.tar.gz
# Source0-md5:	684a9f2f44567a12a30af383de992a89
Patch0:		%{name}-pc.patch
URL:		http://libccd.danfis.cz/
BuildRequires:	cmake >= 2.8
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

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q
%patch0 -p1

%build
# autotools build system doesn't install .pc file, use cmake instead
%cmake .
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc BSD-LICENSE README doc/jgt98convex.pdf
%attr(755,root,root) %{_libdir}/libccd.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libccd.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libccd.so
%{_includedir}/ccd
%{_pkgconfigdir}/ccd.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libccd.a
