%define modname cairo_wrapper
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A99_%{modname}.ini

Summary:	Cairo Wrapper Extension
Name:		php-%{modname}
Version:	0.2.4
Release:	14
Group:		Development/PHP
License:	PHP License
URL:		https://pecl.php.net/package/cairo_wrapper/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Patch0:		cairo_wrapper-0.2.4-php54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	pkgconfig
BuildRequires:	cairo-devel >= 1.2.2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
A cairo API wrapper. For details about cairo see http://cairographics.org/

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
%doc CREDITS package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-13mdv2012.0
+ Revision: 797126
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-12
+ Revision: 761206
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-11
+ Revision: 696399
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-10
+ Revision: 695372
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-9
+ Revision: 646618
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-8mdv2011.0
+ Revision: 629771
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-7mdv2011.0
+ Revision: 628073
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-6mdv2011.0
+ Revision: 600467
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-5mdv2011.0
+ Revision: 588749
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-4mdv2010.1
+ Revision: 514523
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-3mdv2010.1
+ Revision: 485345
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-2mdv2010.1
+ Revision: 468150
- rebuilt against php-5.3.1

* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-1mdv2010.0
+ Revision: 452906
- import php-cairo_wrapper


* Sat Oct 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.4-1mdv2010.0
- initial Mandriva package
