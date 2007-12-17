%define modname rpmreader
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A42_%{modname}.ini

Summary:	RPM file meta information reader for PHP
Name:		php-%{modname}
Version:	0.3
Release:	%mkrel 13
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net
Source0:	rpmreader.tar.bz2
BuildRequires:	php-devel >= 3:5.2.0
Epoch:		1

%description
rpmreader is an extension that provides the ability to read RedHat Package
Manager (RPM) files' header information. This extension currently does not
provide the functionality to read the signature or archive sections of the RPM
file.

%prep

%setup -q -n rpmreader

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc examples CREDITS package.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
