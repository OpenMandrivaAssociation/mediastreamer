%define major 11
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

%global optflags %{optflags} -fcommon -Wno-implicit-function-declaration
%global build_ldflags %{build_ldflags} -lXext -pthread -lpthread

%bcond_with	doc
%bcond_without	qtgl
%bcond_with	static
%bcond_with	strict
%bcond_with	tests
%bcond_without	zrtp

Summary:	Audio/video real-time streaming library
Name:		mediastreamer
Version:	5.2.59
Release:	1
License:	GPL-2.0+
Group:		Communications
URL:		https://linphone.org/
Source0:	https://gitlab.linphone.org/BC/public/mediastreamer2/-/archive/%{version}/mediastreamer2-%{version}.tar.bz2
Patch0:		mediastreamer-linkage_fix.patch
Patch1:		mediastreamer-cmake-install-pkgconfig-pc-file.patch
Patch2:		mediastreamer-cmake-config-location.patch
Patch3:		mediastreamer-cmake-fix-opengl-include.patch
Patch4:		mediastreamer2-5.2.0-cmake-dont-use-bc_git_version.patch
Patch5:		mediastreamer2-5.0.66-ffmpeg-5.0.patch
Patch6:		mediastreamer2-5.2.0-fix_zxing.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	libtool
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext
BuildRequires:	bctoolbox-static-devel
BuildRequires:	boost-devel
BuildRequires:	cmake(bcmatroska2)
BuildRequires:	cmake(bzrtp)
BuildRequires:	cmake(ortp) >= 0.24.0
BuildRequires:	cmake(pulseaudio)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Quick)
BuildRequires:	cmake(zxing)
BuildRequires:	gettext-devel
BuildRequires:	gsm-devel
BuildRequires:	intltool
BuildRequires:	pcap-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dri)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libglvnd)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libsrtp2)
BuildRequires:	pkgconfig(libupnp)
BuildRequires:	pkgconfig(libyuv)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(spandsp)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(vpx)
BuildRequires:  qmake5
BuildRequires:	vim-common

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

%description -n	%{libname}
mediastreamer is a GPL licensed library to make audio and video
real-time streaming and processing. Written in pure C, it is based
upon the oRTP library.

%files -n %{libname}
%{_libdir}/libmediastreamer.so.%{major}*
%{_libdir}/mediastreamer/plugins

#---------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Headers, libraries and docs for the mediastreamer2 library
Group:		Development/C
Requires:	%{libname} => %{version}
# mediastreamer was broken out from linphone
Conflicts:	linphone-devel < 3.8.5-1

%description -n	%{devname}
mediastreamer is a GPL licensed library to make audio and video
real-time streaming and processing. Written in pure C, it is based
upon the ortp library.

This package contains header files and development libraries needed to
develop programs using the mediastreamer library.

%files -n %{devname}
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
sed -i -e "s|zxing/|ZXing/|g" cmake/FindZXing.cmake

%build
%cmake \
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_ZRTP:BOOL=%{?with_zrtp:ON}%{!?with_zrtp:OFF} \
	-DENABLE_DOC=%{?with_doc:ON}%{?!with_doc:OFF} \
	-DENABLE_UNIT_TESTS=%{?with_tests:ON}%{?!with_tests:OFF} \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-DENABLE_QT_GL:BOOL=%{?with_qtgl:ON}%{!?with_qtgl:OFF} \
	-DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/Mediastreamer2 \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

#find_lang %{name}
