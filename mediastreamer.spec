%define major 10
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}
%ifarch %{ix86}
# Allow undefined references to __udivdi3 and friends
%define _disable_ld_no_undefined 1
%endif

Summary:	Audio/video real-time streaming library
Name:		mediastreamer
Version:	2.16.1
Release:	4
License:	GPL-2.0+
Group:		Communications
URL:		http://linphone.org/eng/documentation/dev/mediastreamer2.html
Source0:	https://linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz
Patch0:		mediastreamer-2.16.1-linkage_fix.patch
Patch1:		0001-allow-MS2_GIT_VERSION-to-be-undefined-as-it-will-be-.patch
Patch2:		mediastreamer-2.16.1-cmake-install-pkgconfig-pc-file.patch
Patch3:		mediastreamer-2.16.1-cmake-config-location.patch
BuildRequires:  cmake
BuildRequires:  libtool
BuildRequires:  ffmpeg-devel
BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  gsm-devel
BuildRequires:  intltool
BuildRequires:  pcap-devel
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xv)
BuildRequires:  vim-common
BuildRequires:  pkgconfig(alsa)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(dri)
BuildRequires:	pkgconfig(libglvnd)
BuildRequires:  pkgconfig(glew) >= 1.5
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(libpulse) >= 0.9.21
BuildRequires:  pkgconfig(libsrtp2)
BuildRequires:  pkgconfig(libupnp) >= 1.6
BuildRequires:  pkgconfig(libupnp) < 1.7
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(opus) >= 0.9.0
BuildRequires:  pkgconfig(ortp) >= 0.24.0
BuildRequires:  pkgconfig(spandsp) >= 0.0.6
BuildRequires:  pkgconfig(speex) >= 1.1.6
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(theora) >= 1.0alpha7
BuildRequires:  pkgconfig(vpx) >= 1.8.0
BuildRequires:	bctoolbox-static-devel
BuildRequires:	cmake(BZRTP)

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
%apply_patches

%build
%cmake \
  -DENABLE_STATIC:BOOL=NO \
  -DENABLE_STRICT:BOOL=NO \
  -DENABLE_DOC=NO \
  -DENABLE_UNIT_TESTS=NO \
  -DOpenGL_GL_PREFERENCE=GLVND \
  -DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/Mediastreamer2

%make

%install
%make_install -C build

#find_lang %{name}

%files
%doc AUTHORS COPYING NEWS README.md
%{_bindir}/mediastream
%{_bindir}/mkvstream
%dir %{_datadir}/images/
%{_datadir}/images/nowebcamCIF.jpg

%files -n %{libname}
%{_libdir}/libmediastreamer_base.so.%{major}*
%{_libdir}/libmediastreamer_voip.so.%{major}*

%files -n %{develname}
%{_includedir}/mediastreamer2/
%{_libdir}/libmediastreamer_*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/Mediastreamer2/

