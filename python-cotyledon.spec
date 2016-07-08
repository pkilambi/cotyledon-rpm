%global pypi_name cotyledon

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{pypi_name}
Version:        1.2.5
Release:        1%{?dist}
Summary:        Cotyledon provides a framework for defining long-running services.

License:        ASL 2.0
URL:            https://cotyledon.readthedocs.io
Source0:        https://pypi.python.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
Requires:  python-setproctitle
# For building documentation
BuildRequires:  python-sphinx
BuildRequires:  python-setproctitle

%description
Cotyledon provides a framework for defining long-running services.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        Cotyledon provides a framework for defining long-running services.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
Requires:  python3-setproctitle
# For building documentation
BuildRequires:  python3-sphinx
BuildRequires:  python3-setproctitle

%description -n python3-%{pypi_name}
Cotyledon provides a framework for defining long-running services.
%endif

%package doc
Summary:    Documentation for %{name}
Group:      Documentation
License:    ASL 2.0

%description doc
Cotyledon provides a framework for defining long-running services.

This package contains documentation in HTML format.


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
# generate html docs
sphinx-build-3 doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%endif # with_python3


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

#delete tests
rm -fr %{buildroot}%{python2_sitelib}/%{pypi_name}/tests/
rm -fr %{buildroot}%{python3_sitelib}/%{pypi_name}/tests/
rm -f %{buildroot}%{_bindir}/%{pypi_name}-example


%files
%doc README.rst LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files doc
%doc html

%changelog
* Wed Jul 6 2016 Mehdi Abaakouk <sileht@redhat.com> - 1.2.3-1
- Initial package.
