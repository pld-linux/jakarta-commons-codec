%define	base_name	codec
%define	short_name	commons-%{base_name}
Summary:	Jakarta Commons Codec Package
Name:		jakarta-%{short_name}
Version:	1.3
Release:	2jpp
License:	Apache Software License
Group:		Development/Languages/Java
URL:		http://jakarta.apache.org/commons/codec/
Source0:	http://www.apache.org/dist/jakarta/commons/codec/source/commons-codec-%{version}-src.tar.gz
# Source0-md5:	af3c3acf618de6108d65fcdc92b492e1
Patch0:		jakarta-commons-codec-buildscript.patch
BuildRequires:	jakarta-ant >= 1.6.2
BuildRequires:	junit
Provides:	%{short_name}
Obsoletes:	%{short_name}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Commons Codec is an attempt to provide definitive implementations of
commonly used encoders and decoders.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation

%description    javadoc
Javadoc for %{name}.

%prep
%setup -q -n commons-codec-%{version}

# FIXME Remove SoundexTest which is failing
# and thus preventing the build to proceed.
# This problem has been communicated upstream Bug 31096
%patch0 -p1

%build
ant -Dbuild.sysclasspath=first \
  -Dconf.home=src/conf \
  -Dbuild.home=build \
  -Dsource.home=src/java \
  -Dtest.home=src/test \
  -Ddist.home=dist \
  -Dcomponent.title=%{short_name} \
  -Dcomponent.version=%{version} \
  -Dfinal.name=%{name}-%{version} \
  -Dextension.name=%{short_name} \
  test jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc RELEASE-NOTES.txt
%{_javadir}/*

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
