%global pypi_name cotyledon

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{pypi_name}
Version:        1.2.5
Release:        3%{?dist}
Summary:        Cotyledon provides a framework for defining long-running services

License:        ASL 2.0
URL:            https://cotyledon.readthedocs.io
Source0:        https://pypi.io/packages/source/c/cotyledon/cotyledon-1.2.5.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
# For building documentation
BuildRequires:  python-sphinx
BuildRequires:  python-setproctitle

Requires:  python-setproctitle

%description
Cotyledon provides a framework for defining long-running services.


%package -n python2-%{pypi_name}-tests
Summary:          Cotyledon provides a framework for defining long-running services
Requires:         python-%{pypi_name} = %{version}-%{release}
Requires:         python-oslotest
Requires:         python-testrepository
Requires:         python-testscenarios
Requires:         python-testtools

%description -n python2-%{pypi_name}-tests
Cotyledon provides a framework for defining long-running services.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Cotyledon provides a framework for defining long-running services
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
# For building documentation
BuildRequires:  python3-sphinx
BuildRequires:  python3-setproctitle

Requires:  python3-setproctitle

%description -n python3-%{pypi_name}
Cotyledon provides a framework for defining long-running services.

%package -n python3-%{pypi_name}-tests
Summary:    Tests for %{name}
Requires:         python3-%{pypi_name} = %{version}-%{release}
Requires:         python3-oslotest
Requires:         python3-testrepository
Requires:         python3-testscenarios
Requires:         python3-testtools

%description -n python3-%{pypi_name}-tests
Cotyledon provides a framework for defining long-running services.

This package contains test files
%endif

%package doc
Summary:    Documentation for %{name}
Group:      Documentation

%description doc
Cotyledon provides a framework for defining long-running services.

This package contains documentation in HTML format.


%prep
%setup -q -n %{pypi_name}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -rf html/.doctrees html/.buildinfo


%check
%{__python2} setup.py test ||:

%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/%{pypi_name}/tests

%endif

%files doc
%doc html

%files -n python2-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/%{pypi_name}/tests/
%{_bindir}/%{pypi_name}-example


%changelog
* Fri Jul 15 2016 Pradeep Kilambi <pkilambi@redhat.com> - 1.2.3-3
- Add check section
- added new test dependencies
- fixed tests sub packages

* Thu Jul 14 2016 Pradeep Kilambi <pkilambi@redhat.com> - 1.2.3-2
- Fix source url

* Wed Jul 6 2016 Mehdi Abaakouk <sileht@redhat.com> - 1.2.3-1
- Initial package.
