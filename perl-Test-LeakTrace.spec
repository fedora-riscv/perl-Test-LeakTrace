Name:           perl-Test-LeakTrace
Summary:        Traces memory leaks
Version:        0.13
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/G/GF/GFUJI/Test-LeakTrace-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Test-LeakTrace
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Test::More) >= 0.62

Requires:       perl(Exporter) >= 5.57

%{?perl_default_filter}
%{?perl_default_subpackage_tests}

%description
'Test::LeakTrace' provides several functions that trace memory leaks.
This module scans arenas, the memory allocation system, so it can detect
any leaked SVs in given blocks.  *Leaked SVs* are SVs which are not
released after the end of the scope they have been created. These SVs
include global variables and internal caches. For example, if you call a
method in a tracing block, perl might prepare a cache for the method.
Thus, to trace true leaks, 'no_leaks_ok()' and 'leaks_cmp_ok()' executes
a block more than once.

%prep
%setup -q -n Test-LeakTrace-%{version}

find . -type f -exec chmod -c -x {} +

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
make test


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto
%{_mandir}/man3/*.3*

%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Paul Howarth <paul@city-fan.org> - 0.13-1
- update to 0.13
  - use ">= 0", instead of "== 0" for no_leaks_ok()
  - add count_sv() to count all the SVs in a perl interpreter
  - fix tests broken for some perls in 0.12

* Wed Nov 17 2010 Paul Howarth <paul@city-fan.org> - 0.11-1
- update to 0.11 (#654301)
  - fix false-positive related to XS code (CPAN RT #58133)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-2
- Mass rebuild with perl-5.12.0

* Sun Apr 04 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- specfile by Fedora::App::MaintainerTools 0.006

