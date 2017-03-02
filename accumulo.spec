%define __spec_install_post %{nil}
%define debug_package %{nil}
%define __os_install_post %{_dbpath}/brp-compress

Name:    accumulo
Version: 2.0.0
Release: 1
Summary: A sorted, distributed key/value store
License: ASL 2.0
Group:   Development/Tools
URL:     https://%{name}.apache.org
Source0: %{name}-%{version}-bin.tar.gz
Source1: %{name}-master.service
Source2: %{name}-tserver.service
Source3: %{name}-gc.service
Source4: %{name}-tracer.service
Source5: %{name}-monitor.service
Source6: %{name}-multi-tserver-1.service
Source7: %{name}-multi-tserver-2.service

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
%{summary}

%prep
%setup -q

%build
# Empty section.

%install
rm -rf %{buildroot}
install -d -m 755  %{buildroot}/%{_bindir}
install -d -m 755  %{buildroot}/%{_sysconfdir}/
install -d -m 755  %{buildroot}/%{_var}/log/%{name}
install -d -m 755  %{buildroot}/%{_datadir}/%{name}
install -d -m 755  %{buildroot}/%{_datadir}/%{name}/bin
cp -a bin/{%{name},%{name}-util} %{buildroot}/%{_datadir}/%{name}/bin/
sed -i -e 's/conf="\${basedir}\/conf"/conf="\/etc\/accumulo"/' %{buildroot}%{_datadir}/%{name}/bin/%{name}
sed -i -e 's/conf="\${basedir}\/conf"/conf="\/etc\/accumulo"/' %{buildroot}%{_datadir}/%{name}/bin/%{name}-util
cp -a lib docs %{buildroot}/%{_datadir}/%{name}/
cp -a conf %{buildroot}/%{_sysconfdir}/%{name}
sed -i -e 's/export ACCUMULO_LOG_DIR=.*/export ACCUMULO_LOG_DIR=\/var\/log\/accumulo/' %{buildroot}/%{_sysconfdir}/%{name}/%{name}-env.sh

# create sym links
ln -s %{_datadir}/%{name}/bin/%{name} %{buildroot}/%{_bindir}/%{name} 
ln -s %{_datadir}/%{name}/bin/%{name}-util %{buildroot}/%{_bindir}/%{name}-util 

# systemd services
install -d -m 755 %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}-master.service
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}-tserver.service
install -p -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}-gc.service
install -p -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}-tracer.service
install -p -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/%{name}-monitor.service
install -p -m 644 %{SOURCE6} %{buildroot}%{_unitdir}/%{name}-multi-tserver-1.service
install -p -m 644 %{SOURCE7} %{buildroot}%{_unitdir}/%{name}-multi-tserver-2.service

%clean
rm -rf %{buildroot}

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-util
%{_datadir}/%{name}
%{_unitdir}/%{name}-*.service
%attr(-, %{name}, -) %{_sysconfdir}/%{name}
%attr(-, %{name}, -) %{_var}/log/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd --shell /sbin/nologin -g %{name} -M -r %{name}

%preun
%systemd_preun %{name}-master.service
%systemd_preun %{name}-tserver.service
%systemd_preun %{name}-gc.service
%systemd_preun %{name}-tracer.service
%systemd_preun %{name}-monitor.service
%systemd_preun %{name}-multi-tserver-1.service
%systemd_preun %{name}-multi-tserver-2.service

%postun
%systemd_postun_with_restart %{name}-master.service
%systemd_postun_with_restart %{name}-tserver.service
%systemd_postun_with_restart %{name}-gc.service
%systemd_postun_with_restart %{name}-tracer.service
%systemd_postun_with_restart %{name}-monitor.service
%systemd_postun_with_restart %{name}-multi-tserver-1.service
%systemd_postun_with_restart %{name}-multi-tserver-2.service
