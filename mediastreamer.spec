%define major 6
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Audio/video real-time streaming library
Name:		mediastreamer
Version:	2.12.0
Release:	%mkrel 1
License:	GPL-2.0+
Group:		Communications/Telephony
URL:		http://linphone.org/eng/documentation/dev/mediastreamer2.html
Source0:	http://download.savannah.gnu.org/releases/linphone/%{name}/%{name}-%{version}.tar.gz
Patch0:		mediastreamer-2.11.1-linkage_fix.diff
BuildRequires:  alsa-lib-devel
BuildRequires:  automake 
BuildRequires:  libtool
BuildRequires:  ffmpeg-devel
BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  gsm-devel
BuildRequires:  intltool
BuildRequires:  libpcap-devel
BuildRequires:  libv4l-devel
BuildRequires:  libxext-devel
BuildRequires:  libxv-devel
BuildRequires:  vim-common
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(glew) >= 1.5
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(libbzrtp) >= 1.0.1
BuildRequires:  pkgconfig(libpulse) >= 0.9.21
BuildRequires:  pkgconfig(libsrtp) >= 1.5.2
BuildRequires:  pkgconfig(libupnp) >= 1.6
BuildRequires:  pkgconfig(libupnp) < 1.7
BuildRequires:  pkgconfig(libvpx)
BuildRequires:  pkgconfig(opus) >= 0.9.0
BuildRequires:  pkgconfig(ortp) >= 0.24.0
BuildRequires:  pkgconfig(spandsp) >= 0.0.6
BuildRequires:  pkgconfig(speex) >= 1.1.6
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(theora) >= 1.0alpha7
BuildRequires:  pkgconfig(vpx)
# mediastreamer was broken out from linphone which provided lib[64]mediastreamer4-3.8.1-1.mga5
Epoch: 1

%description
mediastreamer is a GPL licensed library to make audio and video
real-time streaming and processing. Written in pure C, it is based
upon the oRTP library.

%package -n	%{libname}
Summary:	Audio/video real-time streaming library
Group:		System/Libraries
#Conflicts:	%{mklibname mediastreamer 3}

%description -n	%{libname}
mediastreamer is a GPL licensed library to make audio and video
real-time streaming and processing. Written in pure C, it is based
upon the oRTP library.

%package -n	%{develname}
Summary:	Headers, libraries and docs for the mediastreamer2 library
Group:		Development/C
Requires:	%{libname} => %{version}
# mediastreamer was broken out from linphone
Conflicts:	linphone-devel < 3.8.5-1

%description -n	%{develname}
mediastreamer is a GPL licensed library to make audio and video
real-time streaming and processing. Written in pure C, it is based
upon the ortp library.

This package contains header files and development libraries needed to
develop programs using the mediastreamer library.

%prep

%setup -q
%autopatch -p1

%build
sh ./autogen.sh

%configure2_5x \
    --enable-external-ortp \
    --enable-zrtp \
    --disable-strict \
    --disable-static

%make

%install
%make_install
%find_lang %{name}

find %{buildroot} -type f -name "*.la" -delete -print

# remove unwanted docs, generated if doxygen is installed
rm -rf %{buildroot}%{_docdir}/mediastreamer*

%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/mediastream
%{_bindir}/msaudiocmp
%dir %{_datadir}/images/
%{_datadir}/images/nowebcamCIF.jpg

%files -n %{libname}
%{_libdir}/libmediastreamer_base.so.%{major}{,.*}
%{_libdir}/libmediastreamer_voip.so.%{major}{,.*}

%files -n %{develname}
%{_includedir}/mediastreamer2/
%{_libdir}/libmediastreamer_*.so
%{_libdir}/pkgconfig/*.pc




%changelog
* Mon Nov 16 2015 oden <oden> 1:2.12.0-1.mga6
+ Revision: 903588
- soname bump to 6
- 2.12.0

* Mon Aug 24 2015 sander85 <sander85> 1:2.11.2-2.mga6
+ Revision: 869124
- Rebuild for glew 1.13.0

* Sun Aug 02 2015 oden <oden> 1:2.11.2-1.mga6
+ Revision: 860701
- fix br: vim-common
- imported package mediastreamer

