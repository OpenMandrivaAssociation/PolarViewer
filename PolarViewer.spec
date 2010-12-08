%define name PolarViewer
%define version 1.3.1
%define release %mkrel 6

Summary: A viewer application for exercise files recorded with Polar heartrate monitors
Name: %name
Version: %version
Release: %release
License: GPL
Group: Toys
URL: http://www.saring.de/polarviewer/
Source: http://dl.sourceforge.net/sourceforge/sportstracker/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: glade-sharp2 gtk-sharp2-devel
BuildRequires: ImageMagick
Requires: s710
Requires: mono
BuildArch: noarch

%description
PolarViewer is a viewer application for exercise files 
recorded with Polar heartrate monitors. It displays all 
the recorded exercise data (except power) and creates diagrams.
If you want to organize your exercises and create statistics 
you should use the SportsTracker application together with 
PolarViewer.

%prep
%setup -q

%build
%make 
make test

%install
rm -rf "$RPM_BUILD_ROOT"
%__make PREFIX="$RPM_BUILD_ROOT"/%{_usr} DESTDIR="$RPM_BUILD_ROOT" PREFIX_I18N="$RPM_BUILD_ROOT"/%{_datadir}/locale install
mkdir -p %buildroot%_datadir/%name
mv %buildroot%_bindir/* %buildroot%_datadir/%name
cat << EOF > %buildroot%_bindir/%name
#!/bin/sh
mono %_datadir/%name/%name.exe $*
EOF
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%name
Comment=Heartrate monitor viewer
Exec=%{_bindir}/%{name} %U
Icon=%{name}
Terminal=false
Type=Application
Categories=GNOME;GTK;X-MandrivaLinux-MoreApplications-Education-Sports;
StartupNotify=true
EOF

mkdir -p %buildroot{%_liconsdir,%_miconsdir}
convert -scale 32 resource/pv-logo.png %buildroot%_iconsdir/%name.png
convert -scale 16 resource/pv-logo.png %buildroot%_miconsdir/%name.png
cp resource/pv-logo.png %buildroot%_liconsdir/%name.png

%find_lang polarviewer


%clean
rm -rf "$RPM_BUILD_ROOT"

#SCRIPT PREPOST
%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files -f polarviewer.lang
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}
%_datadir/%name
%_datadir/applications/mandriva*
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png
%doc docs/{CHANGES.txt,I18N.txt,LICENSE.txt,README.txt,TODO.txt} 

