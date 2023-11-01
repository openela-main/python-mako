%if 0%{?fedora} || 0%{?rhel} >= 8
%bcond_without python3
%else
%bcond_with python3
%endif

%if 0%{?rhel} > 7
%bcond_with beaker_tests
%bcond_with python2
%else
%bcond_without beaker_tests
%bcond_without python2
%endif

%global upname Mako

Name: python-mako
Version: 1.0.6
Release: 14%{?dist}
BuildArch: noarch

# Mostly MIT, but _ast_util.py is Python licensed.
# The documentation contains javascript for search licensed BSD or GPLv2
License: (MIT and Python) and (BSD or GPLv2)
Group: Development/Languages
Summary: Mako template library for Python
URL: http://www.makotemplates.org/
Source0: https://bitbucket.org/zzzeek/mako/get/rel_%(echo %{version} | sed "s/\./_/g").tar.bz2

# https://bugzilla.redhat.com/show_bug.cgi?id=2133606
Patch0:  python-mako-1.0.6-CVE-2022-40023.patch

%if %{with python2}
BuildRequires: python2-devel
BuildRequires: python2-pytest
BuildRequires: python2-setuptools
BuildRequires: python2-markupsafe
BuildRequires: python2-nose
BuildRequires: python2-mock

%if %{with beaker_tests}
BuildRequires: python2-beaker
%endif
%endif #{with python2}

%if %{with python3}
BuildRequires: python3-devel
BuildRequires: python3-pytest
BuildRequires: python3-setuptools
BuildRequires: python3-markupsafe
BuildRequires: python3-mock
BuildRequires: python3-nose

%if %{with beaker_tests}
BuildRequires: python3-beaker
%endif
%endif #{with python3}

%global _description\
Mako is a template library written in Python. It provides a familiar, non-XML\
syntax which compiles into Python modules for maximum performance. Mako's\
syntax and API borrows from the best ideas of many others, including Django\
templates, Cheetah, Myghty, and Genshi. Conceptually, Mako is an embedded\
Python (i.e. Python Server Page) language, which refines the familiar ideas of\
componentized layout and inheritance to produce one of the most straightforward\
and flexible models available, while also maintaining close ties to Python\
calling and scoping semantics.

%description %_description

%if %{with python2}
%package -n python2-mako
Summary: %summary
Requires: python2-markupsafe

# Beaker is the preferred caching backend, but is not strictly necessary
Recommends: python2-beaker

%{?python_provide:%python_provide python2-mako}

%description -n python2-mako %_description
%endif #{with python2}

%package doc
Summary: Documentation for the Mako template library for Python
Group: Documentation
License: (MIT and Python) and (BSD or GPLv2)
%if %{with python3}
Requires:   python3-mako = %{version}-%{release}
%else
Requires:   python2-mako = %{version}-%{release}
%endif #{with python3}

%description doc
Mako is a template library written in Python. It provides a familiar, non-XML
syntax which compiles into Python modules for maximum performance. Mako's
syntax and API borrows from the best ideas of many others, including Django
templates, Cheetah, Myghty, and Genshi. Conceptually, Mako is an embedded
Python (i.e. Python Server Page) language, which refines the familiar ideas of
componentized layout and inheritance to produce one of the most straightforward
and flexible models available, while also maintaining close ties to Python
calling and scoping semantics.

This package contains documentation in text and HTML formats.


%if %{with python3}
%package -n python3-mako
Summary: Mako template library for Python 3
Group: Development/Languages
Requires: python3-markupsafe

# Beaker is the preferred caching backend, but is not strictly necessary
Recommends: python3-beaker

%{?python_provide:%python_provide python3-mako}

%if %{without python2}
Obsoletes: python2-mako < %{version}-%{release}
%endif #{without python2}

%description -n python3-mako
Mako is a template library written in Python. It provides a familiar, non-XML
syntax which compiles into Python modules for maximum performance. Mako's
syntax and API borrows from the best ideas of many others, including Django
templates, Cheetah, Myghty, and Genshi. Conceptually, Mako is an embedded
Python (i.e. Python Server Page) language, which refines the familiar ideas of
componentized layout and inheritance to produce one of the most straightforward
and flexible models available, while also maintaining close ties to Python
calling and scoping semantics.

This package contains the mako module built for use with python3.
%endif #{with python3}

%prep
%autosetup -p1 -n zzzeek-mako-8e83c7561e3c

%build
export RHEL_ALLOW_PYTHON2_FOR_BUILD=1
%{?with_python2:%py2_build}
%{?with_python3:%py3_build}


%install
%{?with_python3:%py3_install}

%if %{with python2}
export RHEL_ALLOW_PYTHON2_FOR_BUILD=1
mv %{buildroot}/%{_bindir}/mako-render %{buildroot}/%{_bindir}/python3-mako-render
%endif

%{?with_python2:%py2_install}

# These are supporting files for building the docs.  No need to ship
rm -rf doc/build

%check
%if %{with python2}
export RHEL_ALLOW_PYTHON2_FOR_BUILD=1
%{__python2} setup.py test
%endif #{with python2}

%if %{with python3}
%{__python3} setup.py test
%endif

%if %{with python2}
%files -n python2-mako
%license LICENSE
%doc CHANGES README.rst examples
%{_bindir}/mako-render
%{python2_sitelib}/*
%endif %{with python2}

%if %{with python3}
%files -n python3-mako
%license LICENSE
%doc CHANGES README.rst examples
%if %{with python2}
%{_bindir}/python3-mako-render
%else
%{_bindir}/mako-render
%endif
%{python3_sitelib}/*
%endif

%files doc
%doc doc


%changelog
* Thu Nov 17 2022 David King <amigadave@amigadave.com> - 1.0.6-14
- Fix CVE-2022-40023 (#2128977)

* Wed Jul 11 2018 Petr Viktorin <pviktori@redhat.com> - 1.0.6-13
- Disable the Python 2 subpackage again
  https://bugzilla.redhat.com/show_bug.cgi?id=1590397
- Fix the Python2 workaround

* Mon Jun 25 2018 Petr Viktorin <pviktori@redhat.com> - 1.0.6-12
- Allow Python 2 for build
  see https://hurl.corp.redhat.com/rhel8-py2

* Mon Jun 18 2018 Petr Viktorin <pviktori@redhat.com> - 1.0.6-11
- Add back the Python 2 subpackage (temporarily, for mesa build)
  https://bugzilla.redhat.com/show_bug.cgi?id=1569193

* Mon Apr 16 2018 Petr Viktorin <pviktori@redhat.com> - 1.0.6-10
- Remove python-beaker as a build dependency

* Wed Mar 28 2018 Petr Viktorin <pviktori@redhat.com> - 1.0.6-9
- Make python-beaker an optional dependency
- Add missing python_provide for python3-mako
- Conditionalize the Python 2 subpackage
- Modernize the specfile

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.0.6-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Sep 27 2017 Troy Dawson <tdawson@redhat.com> - 1.0.6-6
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.6-5
- Python 2 binary package renamed to python2-mako
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.6-2
- Rebuild for Python 3.6

* Sat Dec 17 2016 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6 (#1257376).
- Mark LICENSE as the license.
- Drop declaration of BuildRoot.
- Drop use of 2to3 since upstream supports Python 3 now.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 12 2015 Kevin Fenzi <kevin@scrye.com> - 1.0.3-1
- Update to 1.0.3

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 28 2015 Matej Cepl <mcepl@redhat.com> - 1.0.1-1
- Update to 1.0.1 (#1185339)

* Wed Jun 18 2014 Luke Macken <lmacken@redhat.com> - 1.0.0-1
- Update to 1.0.0 (#1106453)
- Add a BR on python-mock

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon May 19 2014 Luke Macken <lmacken@redhat.com> - 0.9.1-2
- Create a subpackage for the documentation (#1006259)

* Mon May 19 2014 Luke Macken <lmacken@redhat.com> - 0.9.1-1
- Update to 0.9.1 (#967837)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr  9 2013 Luke Macken <lmacken@redhat.com> - 0.7.3-1
- Update to 0.7.3 (#784257)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.5.0-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 0.5.0-4
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Luke Macken <lmacken@redhat.com> - 0.5.0-1
- Update to 0.5.0

* Mon Sep 5 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.4.2-2
- Require beaker to run unittests since its required at runtime
- Fix license tag

* Mon Sep 5 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.4.2-1
- Update to 0.4.2
- Run unit tests on python3

* Thu Feb 24 2011 Luke Macken <lmacken@redhat.com> - 0.4.0-1
- Update to 0.4.0 (#654779)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Luke Macken <lmacken@redhat.com> - 0.3.6-1
- Update to 0.3.6
- Remove 2to3 patch

* Wed Oct 27 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.3.5-2
- Use a patch from Debian submitted upstream to convert to python3 syntax

* Thu Oct 21 2010 Luke Macken <lmacken@redhat.com> - 0.3.5-1
- Update to 0.3.5 (#645063)

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.3.4-3
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jun 27 2010 Kyle VanderBeek <kylev@kylev.com> - 0.3.4-1
- Update to 0.3.4 security fix release
- Fix missing python3-beaker dependency

* Sat Jun  5 2010 Kyle VanderBeek <kylev@kylev.com> - 0.3.3-1
- Update to upstream 0.3.3

* Tue May  4 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.2-2
- add python3 subpackage

* Tue May 04 2010 Luke Macken <lmacken@redhat.com> - 0.3.2-1
- Update to 0.3.2
- Run the test suite in %%check

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Luke Macken <lmacken@redhat.com> - 0.2.4-1
- Update to 0.2.4

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.10-3
- Rebuild for Python 2.6

* Sun May 11 2008 Kyle VanderBeek <kylev@kylev.com> - 0.1.10-2
- Fix rpmlint warnings.
- Add docs and examples.

* Wed Apr  9 2008 Kyle VanderBeek <kylev@kylev.com> - 0.1.10-1
- Initial version.
