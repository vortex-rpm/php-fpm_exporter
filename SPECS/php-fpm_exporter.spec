%define debug_package %{nil}

%define _git_url https://github.com/hipages/php-fpm_exporter
%define _git_slug src/github.com/hipages/php-fpm_exporter

Name:    php-fpm_exporter
Version: 1.0.0
Release: 1.vortex%{?dist}
Summary: Prometheus exporter for php-fpm
License: MIT
Vendor:  Vortex RPM
URL:     https://github.com/hipages/php-fpm_exporter

Source1: %{name}.service
Source2: %{name}.default

Requires(preun): chkconfig, initscripts
Requires(pre): shadow-utils
%{?systemd_requires}
BuildRequires: golang, git

%description
Prometheus exporter for php-fpm.

%prep
mkdir _build
export GOPATH=$(pwd)/_build
git clone %{_git_url} $GOPATH/%{_git_slug}
cd $GOPATH/%{_git_slug}
git checkout v%{version}

%build
export GOPATH=$(pwd)/_build
cd $GOPATH/%{_git_slug}
go build main.go
mv main %{name}
strip %{name}

%install
export GOPATH=$(pwd)/_build
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default
install -m 755 $GOPATH/%{_git_slug}/%{name} %{buildroot}/usr/bin/%{name}
install -m 644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service
install -m 644 %{SOURCE2} %{buildroot}/etc/default/%{name}

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d /var/lib/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
/usr/bin/%{name}
/usr/lib/systemd/system/%{name}.service
%config(noreplace) /etc/default/%{name}
%attr(755, prometheus, prometheus)/var/lib/prometheus
%doc _build/%{_git_slug}/LICENSE _build/%{_git_slug}/README.md

%changelog
* Wed Jun 05 2019 Ilya Otyutskiy <ilya.otyutskiy@icloud.com> - 1.0.0-1.vortex
- Initial packaging
