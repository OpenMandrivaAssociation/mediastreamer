%define major 11
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

%global optflags %{optflags} -fcommon -Wno-implicit-function-declaration
%global build_ldflags %{build_ldflags} -lXext -pthread -lpthread

Summary:	Audio/video real-time streaming library
Name:		mediastreamer
Version:	5.0.44
Release:	1
License:	GPL-2.0+
Group:		Communications
URL:		https://linphone.org/
Source0:	https://gitlab.linphone.org/BC/public/mediastreamer2/-/archive/%{version}/mediastreamer2-%{version}.tar.bz2
Patch0:		mediastreamer-linkage_fix.patch
Patch1:		mediastreamer-cmake-install-pkgconfig-pc-file.patch
Patch2:		mediastreamer-cmake-config-location.patch
Patch3:		mediastreamer-cmake-fix-opengl-include.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	libtool
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	gsm-devel
BuildRequires:	intltool
BuildRequires:	libjpeg-devel
BuildRequires:	pcap-devel
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xv)
BuildRequires:	vim-common
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(dri)
BuildRequires:	pkgconfig(libglvnd)
BuildRequires:	pkgconfig(glew) >= 1.5
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libpulse) >= 0.9.21
BuildRequires:	pkgconfig(libsrtp2)
BuildRequires:	pkgconfig(libupnp) >= 1.6
BuildRequires:	pkgconfig(vpx)
BuildRequires:	pkgconfig(opus) >= 0.9.0
BuildRequires:	pkgconfig(ortp) >= 0.24.0
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(spandsp) >= 0.0.6
BuildRequires:	pkgconfig(speex) >= 1.1.6
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:	pkgconfig(theora) >= 1.0alpha7
BuildRequires:	pkgconfig(vpx) >= 1.8.0
BuildRequires:	bctoolbox-static-devel
BuildRequires:	cmake(bzrtp)
BuildRequires:	cmake(zxing)
BuildRequires:	pkgconfig(sqlite3)

%description
mediastreamer is a GPL licensed library to make audio and video
real-time streaming and processing. Written in pure C, it is based
upon the oRTP library.

%files
%{_bindir}/mediastream
%{_bindir}/mkvstream
%dir %{_datadir}/images/
%{_datadir}/images/nowebcamCIF.jpg

#---------------------------------------------------------------------------

%package -n	%{libname}
Summary:	Audio/video real-time streaming library
Group:		System/Libraries
#Conflicts:	%{mklibname mediastreamer 3}

%description -n	%{libname}
mediastreamer is a GPL licensed library to make audio and video
real-time streaming and processing. Written in pure C, it is based
upon the oRTP library.

%files -n %{libname}
%{_libdir}/libmediastreamer.so.%{major}*
%{_libdir}/mediastreamer/plugins

#---------------------------------------------------------------------------

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

%files -n %{develname}
%{_includedir}/mediastreamer2/
%{_libdir}/libmediastreamer.so
%{_libdir}/pkgconfig/mediastreamer.pc
%dir %{_libdir}/cmake/Mediastreamer2
%{_libdir}/cmake/Mediastreamer2/*.cmake

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n mediastreamer2-%{version}
#use system OpenGL headers
rm -fr include/OpenGL

# fix version
sed -i -e '/mediastreamer2/s/\(VERSION\)\s\+[0-9]\(\.[0-9]\)\+/\1 %{version}/' CMakeLists.txt

# fix xzing include path
sed -i -e "s|zxing/|ZXing/|g" cmake/FindZxing.cmake

%build
%cmake \
	-DENABLE_STATIC:BOOL=NO \
	-DENABLE_STRICT:BOOL=NO \
	-DENABLE_ZRTP:BOOL=YES \
	-DENABLE_DOC=NO \
	-DENABLE_UNIT_TESTS=NO \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-DENABLE_QT_GL:BOOL=YES \
	-DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/Mediastreamer2 \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

#find_lang %{name}
