Summary: Tancredi provisioning engine packaging and configuration
Name: nethserver-tancredi
Version: 1.1.0
Release: 1%{?dist}
License: GPLv3
Source: %{name}-%{version}.tar.gz
Source1: https://github.com/nethesis/tancredi/archive/c5d612533c0921e2c3b7f6111cbda229d2ae2e6b/tancredi.tar.gz
BuildArch: noarch

BuildRequires: nethserver-devtools
BuildRequires: rh-php56-php-cli, rh-php56-php-mbstring, rh-php56-php-xml, composer
Requires: nethserver-rh-php56-php-fpm
Requires: nethserver-httpd
Requires: nethserver-freepbx

%description
Tancredi provisioning engine packaging and configuration

%prep
%setup -q
%setup -q -D -T -a 1

%build
perl createlinks
(
    cd tancredi-*
    if [[ -n "%{?github_token}" ]]; then
        scl enable rh-php56 -- /usr/bin/composer config github-oauth.github.com "%{github_token}"
    fi
    if [[ -n "%{?composer_cachedir}" ]]; then
        scl enable rh-php56 -- /usr/bin/composer config cache-dir "%{composer_cachedir}"
    fi
    scl enable rh-php56 -- /usr/bin/composer diagnose || :
    scl enable rh-php56 -- /usr/bin/composer install --no-dev
)

%install
(cd root; find . -depth -print | cpio -dump %{buildroot})
(
    cd tancredi-*
    rm -v src/Entity/SampleFilter.php
    mkdir -p %{buildroot}/usr/share/tancredi/data/
    cp -a {public,src,vendor}/ %{buildroot}/usr/share/tancredi/
    cp -a data/{templates,patterns.d,scopes} %{buildroot}/usr/share/tancredi/data/
)
install NethVoiceAuth.php %{buildroot}/usr/share/tancredi/src/Entity/
install AsteriskRuntimeFilter.php %{buildroot}/usr/share/tancredi/src/Entity/
mkdir -p %{buildroot}/var/lib/tancredi/data/{first_access_tokens,scopes,templates-custom,tokens}

%{genfilelist} %{buildroot} \
    --file /etc/tancredi.conf 'attr(0644,root,root) %config(noreplace)' \
    --dir /var/lib/tancredi/data/first_access_tokens 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/scopes 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/templates-custom 'attr(0770,root,apache)' \
    --dir /var/lib/tancredi/data/tokens 'attr(0770,root,apache)' \
    --dir /var/log/tancredi 'attr(0750,apache,apache)' \
    > filelist

%files -f filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc tancredi-*/docs
%doc test
%doc README.rst
%license LICENSE


%changelog
* Wed Apr 15 2020 Davide Principi <davide.principi@nethesis.it> - 1.1.0-1
- Tancredi v1.0-alpha.1
-   Fix Snom softkeys (#107,#100)
-   Fix Gigaset array to string notice (#108)
-   Adjust log verbosity and information (#106)
-   Selectable log handler and verbosity (#105)
-   Fix Snom http password (#102)
-   Fix log timezone (#103)
-   Disable Yealink https web UI (#104)
-   Fix Yealink TLS error 218910881 (#98)
-   Fix Yealink "var" user password (#99)
-   Rename jobs and remove extra spaces
-   Implement build syntax checks (#97)
-   Fix Yealink macros and DTMF mode translation (#95,#96)
-   Fix Fanvil TLS 1.2 support (#94)
- Tancredi beta1 log file issues - Bug nethesis/dev#5773

* Wed Apr 01 2020 Stefano Fancello <stefano.fancello@nethesis.it> - 1.0.0-1
- Beta1 release

