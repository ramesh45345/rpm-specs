#### Local build instructions:
#### Ensure RPM Dev tools are installed: dnf install -y rpmdevtools
#### Ensure RPM Dev folder structure is set up in $HOME/rpmbuild : rpmdev-setuptree
#### Download source: spectool -g -R brisk-menu.spec
#### Install dependencies: sudo dnf builddep ./brisk-menu.spec
#### Build both SRPM and RPM: rpmbuild -ba brisk-menu.spec
#### Lint: rpmlint brisk-menu.spec
####
#### Build with mock:
#### Ensure RPM Dev folder structure is set up: rpmdev-setuptree
#### Add user to mock group: sudo usermod -aG mock <user> , then reboot or newgrp.
#### Build only the SRPM: rpmbuild -bs brisk-menu.spec
#### Run mock: mock --verbose <SRPM path>

%define name brisk-menu
%define version 0.6.1
%define build_timestamp %{lua: print(os.date("%Y%m%d"))}

Summary: An efficient menu for the MATE Desktop.
Name: %{name}
Version: %{version}
Release: %{build_timestamp}
Source0: https://github.com/getsolus/brisk-menu/archive/master.tar.gz#/%{name}-master.tar.gz
Source1: https://github.com/getsolus/brisk-menu-translations/archive/master.tar.gz#/%{name}-translations.tar.gz
License: GPL-2.0+ AND CC-BY-SA-4.0
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
ExclusiveArch: %{ix86} %{arm} x86_64
Vendor: solus-project
BuildRequires:  hicolor-icon-theme
BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(gdk-x11-3.0) >= 3.18.0
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.44.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.44.0
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.18.0
BuildRequires:  pkgconfig(libmate-menu) >= 1.18.0
BuildRequires:  pkgconfig(libmatepanelapplet-4.0) >= 1.18.0
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(x11)
Url: https://github.com/getsolus/brisk-menu

%description

brisk-menu is a modern and efficient menu designed to improve the MATE Desktop Environment with modern, first-class options.

%prep
# Extract the translations.
%setup -q -T -b 1 -n %{name}-translations-master
%setup -q -n %{name}-master
# Remove the existing translations folder.
rm -rf $RPM_BUILD_DIR/%{name}-master/subprojects/translations
# Copy translations into the subprojects folder.
cp -ar $RPM_BUILD_DIR/%{name}-translations-master/ $RPM_BUILD_DIR/%{name}-master/subprojects/translations

%build
%meson
%meson_build

%install
%meson_install

%clean
rm -rf %{buildroot}

%files
%doc LICENSE*
%{_libexecdir}/brisk-menu
%dir %{_datadir}/mate-panel/
%dir %{_datadir}/mate-panel/applets/
%{_datadir}/mate-panel/applets/*brisk*.mate-panel-applet
%{_datadir}/icons/hicolor/scalable/actions/brisk*.*
%{_datadir}/glib-2.0/schemas/*%{name}.gschema.xml
%{_datadir}/dbus-1/services/org.mate.panel.applet.BriskMenuFactory.service
/usr/share/locale/*

%post
:;

%preun
:;

%changelog
