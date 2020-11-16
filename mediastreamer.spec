%define major 11
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

%global optflags %{optflags} -fcommon -Wno-implicit-function-declaration
%global build_ldflags %{build_ldflags} -lXext -pthread -lpthread

Summary:	Audio/video real-time streaming library
Name:		mediastreamer
Version:	4.4.8
Release:	1
License:	GPL-2.0+
Group:		Communications
URL:		https://www.linphone.org/technical-corner/mediastreamer2
# https://gitlab.linphone.org/BC/public/mediastreamer2
Source0:	https://gitlab.linphone.org/BC/public/mediastreamer2/-/archive/%{version}/mediastreamer2-%{version}.tar.bz2
BuildRequires:  cmake
BuildRequires:  ninja
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
#BuildRequires:  pkgconfig(libupnp) < 1.7
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(opus) >= 0.9.0
BuildRequires:  pkgconfig(ortp) >= 0.24.0
BuildRequires:  pkgconfig(spandsp) >= 0.0.6
BuildRequires:  pkgconfig(speex) >= 1.1.6
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(theora) >= 1.0alpha7
BuildRequires:  pkgconfig(vpx) >= 1.8.0
BuildRequires:	bctoolbox-static-devel
BuildRequires:	cmake(bzrtp)
BuildRequires:	pkgconfig(sqlite3)

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
%autosetup -p1 -n mediastreamer2-%{version}
%cmake \
	-DENABLE_STATIC:BOOL=NO \
	-DENABLE_STRICT:BOOL=NO \
	-DENABLE_DOC=NO \
	-DENABLE_UNIT_TESTS=NO \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/Mediastreamer2 \
	-G Ninja

%build

%ninja_build -C build

%install
%ninja_install -C build

#find_lang %{name}

%files
%{_bindir}/mediastream
%{_bindir}/mkvstream
%dir %{_datadir}/images/
%{_datadir}/images/nowebcamCIF.jpg

%files -n %{libname}
%{_libdir}/libmediastreamer.so.%{major}*

%files -n %{develname}
%{_includedir}/mediastreamer2/
%{_libdir}/libmediastreamer.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/cmake/Mediastreamer2/
