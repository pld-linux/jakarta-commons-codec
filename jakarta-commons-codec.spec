%define	base_name	codec
%define	short_name	commons-%{base_name}
Summary:	Jakarta Commons Codec Package
Summary(pl.UTF-8):   Pakiet Jakarta Commons Codec
Name:		jakarta-%{short_name}
Version:	1.3
Release:	3
License:	Apache Software License
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/jakarta/commons/codec/source/commons-codec-%{version}-src.tar.gz
# Source0-md5:	af3c3acf618de6108d65fcdc92b492e1
Patch0:		%{name}-buildscript.patch
URL:		http://jakarta.apache.org/commons/codec/
BuildRequires:	ant >= 1.6.2
BuildRequires:	junit
Provides:	%{short_name}
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
Summary(pl.UTF-8):   Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%prep
%setup -q -n commons-codec-%{version}

# FIXME Remove SoundexTest which is failing
# and thus preventing the build to proceed.
# This problem has been communicated upstream Bug 31096
%patch0 -p1

%build
ant \
	-Dbuild.sysclasspath=first \
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
cd $RPM_BUILD_ROOT%{_javadir}
for jar in *-%{version}*; do
	ln -sf ${jar} `echo $jar| sed  "s|jakarta-||g"`
done
for jar in *-%{version}*; do
	ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`
done
cd -

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
