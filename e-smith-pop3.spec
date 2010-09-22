# $Id: e-smith-pop3.spec,v 1.4 2010/09/22 18:16:25 vip-ire Exp $

Summary: startup scripts for pop3 package
%define name e-smith-pop3
Name: %{name}
%define version 2.2.0
%define release 3
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
Patch1: e-smith-pop3-2.2.0-checkpassword_pam.patch
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
BuildRequires: e-smith-devtools >= 1.13.0-04
BuildArchitectures: noarch
Requires: e-smith-email
Requires: runit
Requires: qmail
Requires: checkpassword-pam
Obsoletes: e-smith-ssl-popd
Obsoletes: checkpassword
AutoReqProv: no

%changelog
* Wed Sep 22 2010 Daniel Berteaud <daniel@firewall-services.com> 2.2.0-3.sme
- Add symlink for template-begin of pop3 pam config [SME: 6218]

* Wed Sep 22 2010 Daniel Berteaud <daniel@firewall-services.com> 2.2.0-2.sme
- Shift auth from passwd/shadow files to the pam database [SME: 6218]

* Tue Oct 7 2008 Shad L. Lords <slords@mail.com> 2.2.0-1.sme
- Roll new stream to separate sme7/sme8 trees [SME: 4633]

* Sun Apr 29 2007 Shad L. Lords <slords@mail.com>
- Clean up spec so package can be built by koji/plague

* Thu Dec 07 2006 Shad L. Lords <slords@mail.com>
- Update to new release naming.  No functional changes.
- Make Packager generic

* Fri Mar 24 2006 Charlie Brady <charlie_brady@mitel.com> 1.2.0-02
- Ensure that pop3 and pop3s are started or stopped if required,
  during email-update event. [SME: 1125]

* Wed Mar 15 2006 Charlie Brady <charlie_brady@mitel.com> 1.2.0-01
- Roll stable stream version. [SME: 1016]

* Mon Mar 13 2006 Gordon Rowell <gordonr@gormand.com.au> 1.1.0-04
- Move pop3[s] defaults from e-smith-email [SME: 561]

* Wed Nov 30 2005 Gordon Rowell <gordonr@gormand.com.au> 1.1.0-03
- Bump release number only

* Thu Sep 15 2005 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-02]
- Fix port name pop->pop3 (to match change in /etc/services).
  [SF: 1291836]

* Wed Aug 10 2001 Shad L. Lords <slords@mail.com>
- [1.1.0-01]
- initial release (split from e-smith-email-4.15.2-27).

%description
Startup scripts for pop3 package.

%prep
%setup
%patch1 -p1

%build
perl createlinks

mkdir -p root/service
for i in pop3 pop3s
do
  mkdir -p root/var/service/$i/peers
  mkdir -p root/etc/e-smith/templates/var/service/$i/peers
  mkdir -p root/etc/e-smith/templates/var/service/$i/peers/{0,local}
  touch root/etc/e-smith/templates/var/service/$i/peers/{0,local}/template-begin
  touch root/var/service/$i/down
  ln -s /var/service/$i root/service/$i
done
mkdir -p root/var/log/pop3
mkdir -p root/var/log/pop3s

mkdir -p root/etc/e-smith/templates/etc/pam.d/pop3
ln -s /etc/e-smith/templates-default/template-begin-pam \
     root/etc/e-smith/templates/etc/pam.d/pop3/template-begin


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
    --file /var/service/pop3/run 'attr(0750,root,root)' \
    --file /var/service/pop3/log/run 'attr(0750,root,root)' \
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
