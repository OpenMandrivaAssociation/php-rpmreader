%define modname rpmreader
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A42_%{modname}.ini

Summary:	RPM file meta information reader for PHP
Name:		php-%{modname}
Version:	0.4
Release:	%mkrel 6
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/rpmreader
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Patch0:		rpmreader-0.4-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
rpmreader is an extension that provides the ability to read RedHat Package
Manager (RPM) files' header information. This extension currently does not
provide the functionality to read the signature or archive sections of the RPM
file.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

%patch0 -p0

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

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
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc examples CREDITS package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.4-6mdv2012.0
+ Revision: 797036
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.4-5
+ Revision: 761284
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.4-4
+ Revision: 696461
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.4-3
+ Revision: 695457
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.4-2
+ Revision: 646678
- rebuilt for php-5.3.6

* Wed Feb 16 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.4-1
+ Revision: 638030
- 0.4

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-30mdv2011.0
+ Revision: 629858
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-29mdv2011.0
+ Revision: 628178
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-28mdv2011.0
+ Revision: 600524
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-27mdv2011.0
+ Revision: 588862
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-26mdv2010.1
+ Revision: 514646
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-25mdv2010.1
+ Revision: 485452
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-24mdv2010.1
+ Revision: 468246
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-23mdv2010.0
+ Revision: 451352
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1:0.3-22mdv2010.0
+ Revision: 397590
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-21mdv2010.0
+ Revision: 377022
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-20mdv2009.1
+ Revision: 346601
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-19mdv2009.1
+ Revision: 341792
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-18mdv2009.1
+ Revision: 323046
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-17mdv2009.1
+ Revision: 310301
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-16mdv2009.0
+ Revision: 238425
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-15mdv2009.0
+ Revision: 200262
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-14mdv2008.1
+ Revision: 162239
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-13mdv2008.1
+ Revision: 107712
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-12mdv2008.0
+ Revision: 77570
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-11mdv2008.0
+ Revision: 39518
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-10mdv2008.0
+ Revision: 33871
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-9mdv2008.0
+ Revision: 21351
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.3-8mdv2007.0
+ Revision: 117613
- rebuilt against new upstream version (5.2.1)

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-7mdv2007.0
+ Revision: 79296
- rebuild
- rebuilt for php-5.2.0
- Import php-rpmreader

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-5
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-4mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.3-3mdk
- rebuilt for php-5.1.3

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-2mdk
- rebuilt against php-5.1.2

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.3-1mdk
- 0.3

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-1mdk
- rebuilt against php-5.1.0
- fix versioning

* Sun Oct 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.1-0.RC1.1mdk
- initial Mandriva package

