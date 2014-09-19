# Pick up the right dictionary for the spell check
%if %(perl -e 'print $] >= 5.010000 ? 1 : 0;')
%global speller hunspell
%else
%global speller aspell
%endif

# some arches don't have valgrind so we need to disable its support on them
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le s390x %{arm} aarch64
%global with_valgrind 1
%endif

Name:		perl-Test-LeakTrace
Summary:	Trace memory leaks
Version:	0.14
Release:	13%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-LeakTrace/
Source0:	http://search.cpan.org/CPAN/authors/id/G/GF/GFUJI/Test-LeakTrace-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
# Module Build
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(inc::Module::Install)
BuildRequires:	perl(Module::Install::AuthorTests)
BuildRequires:	perl(Module::Install::Repository)
# Module Runtime
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder::Module)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader)
# Test Suite
BuildRequires:	perl(autouse)
BuildRequires:	perl(Class::Struct)
BuildRequires:	perl(constant)
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(Test::More) >= 0.62
BuildRequires:	perl(threads)
# Extra Tests
BuildRequires:	perl(Test::Pod) >= 1.14
BuildRequires:	perl(Test::Pod::Coverage) >= 1.04
%if !%{defined perl_bootstrap}
# Cycle: perl-Test-LeakTrace → perl-Test-Spelling → perl-Pod-Spell
# → perl-File-SharedDir-ProjectDistDir → perl-Path-Tiny → perl-Unicode-UTF8
# → perl-Test-LeakTrace
BuildRequires:	perl(Test::Spelling), %{speller}-en
%endif
BuildRequires:	perl(Test::Synopsis)
%if 0%{?with_valgrind}
BuildRequires:	perl(Test::Valgrind)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't provide private perl libs
%{?perl_default_filter}

%description
Test::LeakTrace provides several functions that trace memory leaks. This module
scans arenas, the memory allocation system, so it can detect any leaked SVs in
given blocks.

Leaked SVs are SVs that are not released after the end of the scope they have
been created. These SVs include global variables and internal caches. For
example, if you call a method in a tracing block, perl might prepare a cache
for the method. Thus, to trace true leaks, no_leaks_ok() and leaks_cmp_ok()
executes a block more than once.

%prep
%setup -q -n Test-LeakTrace-%{version}

# Remove redundant exec bits
chmod -c -x lib/Test/LeakTrace/Script.pm t/lib/foo.pl

# Fix up shellbangs in doc scripts
sed -i -e 's|^#!perl|#!/usr/bin/perl|' benchmark/*.pl example/*.{pl,t} {t,xt}/*.t

# Avoid bundled Module::Install and use the system version instead
rm -rf inc/
sed -i -e '/^inc\//d' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

# Run the release tests
# Don't spell-check JA.pod as it can generate false positives
mv lib/Test/LeakTrace/JA.pod ./
touch lib/Test/LeakTrace/JA.pod
%if 0%{?with_valgrind}
DICTIONARY=en_US make test TEST_FILES="xt/*.t"
%else
DICTIONARY=en_US make test TEST_FILES="$(echo xt/*.t | sed 's|xt/05_valgrind.t||')"
%endif
rm lib/Test/LeakTrace/JA.pod
mv ./JA.pod lib/Test/LeakTrace/

%clean
rm -rf %{buildroot}

%files
%doc Changes README benchmark/ example/ %{?perl_default_filter:t/ xt/}
%{perl_vendorarch}/auto/Test/
%{perl_vendorarch}/Test/
%{_mandir}/man3/Test::LeakTrace.3pm*
%{_mandir}/man3/Test::LeakTrace::JA.3pm*
%{_mandir}/man3/Test::LeakTrace::Script.3pm*

%changelog
* Fri Sep 19 2014 Paul Howarth <paul@city-fan.org> - 0.14-13
- ppc64le and aarch64 have valgrind
- Drop obsoletes/provides for old -tests sub-package
- Avoid bundled Module::Install and use system version instead
- Classify buildreqs by usage

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-12
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-11
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Petr Pisar <ppisar@redhat.com> - 0.14-8
- Break build-cycle: perl-Test-LeakTrace → perl-Test-Spelling → perl-Pod-Spell
  → perl-File-SharedDir-ProjectDistDir → perl-Path-Tiny → perl-Unicode-UTF8
  → perl-Test-LeakTrace

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 0.14-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Dan Horák <dan[at]danny.cz> - 0.14-4
- valgrind is available only on selected arches and perl(Test::Valgrind) is noarch

* Mon Jun 18 2012 Petr Pisar <ppisar@redhat.com> - 0.14-3
- Perl 5.16 rebuild

* Thu May  3 2012 Paul Howarth <paul@city-fan.org> - 0.14-2
- BR: perl(Test::Valgrind) for additional test coverage

* Mon Mar 12 2012 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Fix Test::Valgrind failures
- Drop tests subpackage; move tests to main package documentation as long as
  we have %%{perl_default_filter} to avoid the resulting doc-file dependencies
- Run the release tests too, except for xt/05_valgrind.t since we don't have
  Test::Valgrind yet
- BR: perl(Test::Pod), perl(Test::Pod::Coverage), perl(Test::Spelling),
  aspell-en/hunspell-en and perl(Test::Synopsis) for the release tests
- Drop version requirement of perl(ExtUtils::MakeMaker) to 6.30, which works
  fine in EPEL-5
- Tidy %%description
- Make %%files list more explicit
- Package benchmark/ and example/ as documentation
- Drop explicit versioned requires of perl(Exporter) ≥ 5.57, satisfied by all
  supported distributions
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Drop %%defattr, redundant since rpm 4.4
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Use ">= 0", instead of "== 0" for no_leaks_ok()
  - Add count_sv() to count all the SVs in a perl interpreter
  - Fix tests broken for some perls in 0.12

* Wed Nov 17 2010 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11 (#654301)
  - Fix false-positive related to XS code (CPAN RT #58133)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10-2
- Mass rebuild with perl-5.12.0

* Sun Apr 04 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.10-1
- Specfile by Fedora::App::MaintainerTools 0.006

