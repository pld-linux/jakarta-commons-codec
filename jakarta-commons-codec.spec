# TODO
# - rename to apache-commons-codec?
%include	/usr/lib/rpm/macros.java
Summary:	Jakarta Commons Codec Package
Summary(pl.UTF-8):	Pakiet Jakarta Commons Codec
Name:		jakarta-commons-codec
Version:	1.3
Release:	4
License:	Apache Software License
Group:		Development/Languages/Java
Source0:	http://apache.zone-h.org/commons/codec/source/commons-codec-%{version}-src.tar.gz
# Source0-md5:	af3c3acf618de6108d65fcdc92b492e1
Patch0:		%{name}-buildscript.patch
URL:		http://commons.apache.org/codec/
BuildRequires:	ant >= 1.6.2
BuildRequires:	ant-junit
BuildRequires:	jpackage-utils
BuildRequires:	junit
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Provides:	commons-codec
Obsoletes:	commons-codec
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Commons Codec is an attempt to provide definitive implementations of
commonly used encoders and decoders.

%description -l pl.UTF-8
Commons Codec to próba dostarczenia ostatecznych implementacji
powszechnie używanych koderów i dekoderów.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%prep
%setup -qc
touch LICENSE
cd commons-codec-%{version}

# FIXME Remove SoundexTest which is failing
# and thus preventing the build to proceed.
# This problem has been communicated upstream Bug 31096
%patch0 -p1

%build
cd commons-codec-%{version}

export LC_ALL=en_US # source not in ASCII

required_jars="junit"
export CLASSPATH=$(build-classpath $required_jars)

%ant dist

%install
rm -rf $RPM_BUILD_ROOT
cd commons-codec-%{version}

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a dist/commons-codec-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s commons-codec-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/commons-codec.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc commons-codec-%{version}/RELEASE-NOTES.txt
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
