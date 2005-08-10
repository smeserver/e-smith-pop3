Summary: startup scripts for pop3 package
%define name e-smith-pop3
Name: %{name}
%define version 1.1.0
%define release 01
Version: %{version}
Release: %{release}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
Packager: e-smith developers <bugs@e-smith.com>
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
BuildRequires: e-smith-devtools >= 1.13.0-04
BuildArchitectures: noarch
Requires: runit
Requires: checkpassword
AutoReqProv: no

%changelog
* Wed Aug 10 2001 Shad L. Lords <slords@mail.com>
- [1.1.0-01]
- initial release

%description
Startup scripts for pop3 package.

%prep
%setup

%build
perl createlinks

mkdir -p root/service
ln -s /var/service/pop3 root/service/pop3
touch root/var/service/pop3/down
ln -s /var/service/pop3s root/service/pop3s
touch root/var/service/pop3s/down

mkdir -p root/var/log/popd
mkdir -p root/var/log/pop3s

%install
rm -rf $RPM_BUILD_ROOT
(cd root ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT \
    --dir /var/log/pop3 'attr(0750,smelog,smelog)' \
    --dir /var/service/pop3 'attr(01755,root,root)' \
    --dir /var/service/pop3/control 'attr(01755,root,root)' \
    --file /var/service/pop3/control/1 'attr(0750,root,root)' \
    --file /var/service/pop3s/run 'attr(0750,root,root)' \
    --file /var/service/pop3s/log/run 'attr(0750,root,root)' \
    --dir '/var/log/pop3s' 'attr(2750,smelog,smelog)' \
    --file /var/service/popd/run 'attr(0750,root,root)' \
    --file /var/service/popd/log/run 'attr(0750,root,root)' \
    > %{name}-%{version}-%{release}-filelist
echo "%doc COPYING" >> %{name}-%{version}-%{release}-filelist

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%preun
%post
%postun

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
