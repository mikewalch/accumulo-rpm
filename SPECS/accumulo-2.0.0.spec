%define __spec_install_post %{nil}
%define debug_package %{nil}
%define __os_install_post %{_dbpath}/brp-compress

Name:    accumulo
Version: 2.0.0
Release: 1
Summary: A software platform for processing vast amounts of data
License: ASL 2.0
Group:   Development/Tools
URL:     https://%{name}.apache.org
Source0: %{name}-%{version}-bin.tar.gz
Source1: %{name}-master.service
Source2: %{name}-tserver.service
Source3: %{name}-gc.service
Source4: %{name}-tracer.service
Source5: %{name}-monitor.service

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
%{summary}

%prep
%setup -q

%build
# Empty section.

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}/usr/bin
mkdir -p  %{buildroot}/etc
mkdir -p  %{buildroot}/opt/accumulo-%{version}
cp -a bin conf lib docs %{buildroot}/opt/accumulo-%{version}/

# create sym links
ln -s /opt/accumulo-%{version}/bin/accumulo %{buildroot}/%{_bindir}/accumulo 
ln -s /opt/accumulo-%{version}/conf %{buildroot}/%{_sysconfdir}/accumulo

# systemd services
install -d -m 755 %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}-master.service
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}-tserver.service
install -p -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}-gc.service
install -p -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}-tracer.service
install -p -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/%{name}-monitor.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,accumulo,accumulo,-)
/opt/accumulo-%{version}/*
%{_bindir}/accumulo
%{_sysconfdir}/*
%{_unitdir}/accumulo-*.service

%preun
%systemd_preun %{name}-master.service
%systemd_preun %{name}-tserver.service
%systemd_preun %{name}-gc.service
%systemd_preun %{name}-tracer.service
%systemd_preun %{name}-monitor.service

%postun
%systemd_postun_with_restart %{name}-master.service
%systemd_postun_with_restart %{name}-tserver.service
%systemd_postun_with_restart %{name}-gc.service
%systemd_postun_with_restart %{name}-tracer.service
%systemd_postun_with_restart %{name}-monitor.service
