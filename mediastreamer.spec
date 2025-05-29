%define major 11
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

# exclude unwanted cmake provides
%global __provides_exclude_from ^%{_datadir}/cmake/.*/Find.*cmake$

# exclude unwanted cmake requires
%global __requires_exclude cmake\\(arts\\)|cmake\\(Arts\\) \
	|cmake\\(bcg729\\)|cmake\\(BCG729\\) \
	|cmake\\(bv16\\)|cmake\\(BV16\\) \
	|cmake\\(camapi\\)|cmake\\(CamApi\\) \
	|cmake\\(gsm\\)|cmake\\(GSM\\) \
	|cmake\\(ffmpeg\\)|cmake\\(FFMpeg\\) \
	|cmake\\(libyuv\\)|cmake\\(LibYUV\\) \
	|cmake\\(opus\\)|cmake\\(Opus\\) \
	|cmake\\(pcap\\)|cmake\\(PCAP\\) \
	|cmake\\(portaudio\\)|cmake\\(PortAudio\\) \
	|cmake\\(qnxaudiomanager\\)|cmake\\(QnxAudioManager\\) \
	|cmake\\(qsa\\)|cmake\\(QSA\\) \
	|cmake\\(screen\\)|cmake\\(Screen\\) \
	|cmake\\(spandsp\\)|cmake\\(SpanDSP\\) \
	|cmake\\(srtp\\)|cmake\\(SRTP\\) \
	|cmake\\(speex\\)|cmake\\(Speex\\) \
	|cmake\\(speexdsp\\)|cmake\\(SpeexDSP\\) \
	|cmake\\(theora\\)|cmake\\(Theora\\) \
	|cmake\\(v4l\\)|cmake\\(V4L\\) \
	|cmake\\(vpx\\)|cmake\\(VPX\\) \
	|cmake\\(turbojpeg\\)|cmake\\(TurboJpeg\\)

%bcond doc			0
%bcond qtgl			1
%bcond strict			0
%bcond unit_tests		1
%bcond unit_tests_install	0
%bcond zrtp			1

Summary:	Audio/video real-time streaming library
Name:		mediastreamer
Version:	5.3.97
Release:	3
License:	GPL-2.0+
Group:		Communications
URL:		https://linphone.org/
Source0:	https://gitlab.linphone.org/BC/public/mediastreamer2/-/archive/%{version}/mediastreamer2-%{version}.tar.bz2
Patch0:		mediastreamer2-5.3.6-soname.patch
Patch1:		mediastreamer-cmake-install-pkgconfig-pc-file.patch
Patch2:		mediastreamer2-5.3.6-cmake-config-location.patch
Patch3:		mediastreamer-cmake-fix-opengl-include.patch
Patch4:		mediastreamer2-5.3.6-cmake-dont-use-bc_git_version.patch
Patch5:		mediastreamer2-5.0.66-ffmpeg-6.0.patch
Patch6:		mediastreamer2-5.3.93-fix_zxing.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	libtool
BuildRequires:	ffmpeg-devel
BuildRequires:	gettext
BuildRequires:	boost-devel
BuildRequires:	cmake(bcmatroska2)
BuildRequires:	cmake(bzrtp)
BuildRequires:	cmake(ortp) >= 0.24.0
BuildRequires:	cmake(pulseaudio)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(zxing)
BuildRequires:	gettext-devel
BuildRequires:	gsm-devel
BuildRequires:	intltool
BuildRequires:	pcap-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(aom)
BuildRequires:	pkgconfig(dav1d)
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
BuildRequires:	pkgconfig(libmatroska)
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
BuildRequires:  qmake-qt6
BuildRequires:	vim-common

%description
mediastreamer is a GPL licensed library to make audio and video
real-time streaming and processing. Written in pure C, it is based
upon the oRTP library.

%files
%{_bindir}/%{name}2-mediastream
%{_bindir}/%{name}2-mkvstream
%dir %{_datadir}/images/
%{_datadir}/images/nowebcamCIF.jpg
%if %{with unit_tests} && %{with unit_tests_install}
%{_bindir}/%{name}2-tester
%{_datadir}/%{name}2-tester/
%endif

#---------------------------------------------------------------------------

%package -n	%{libname}
Summary:	Audio/video real-time streaming library
Group:		System/Libraries

%description -n	%{libname}
mediastreamer is a GPL licensed library to make audio and video
real-time streaming and processing. Written in pure C, it is based
upon the oRTP library.

%files -n %{libname}
%{_libdir}/libmediastreamer2.so.%{major}*
%dir %{_libdir}/%{name}/plugins/
%{_libdir}/%{name}/plugins/*

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
%{_libdir}/libmediastreamer2.so
%{_libdir}/pkgconfig/mediastreamer.pc
%{_datadir}/cmake/Mediastreamer2

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
export CXXFLAGS="%{optflags} -I%{_includedir}/bcmatroska2/"
#	-DENABLE_ZRTP:BOOL=%{?with_zrtp:ON}%{!?with_zrtp:OFF} \

%cmake -Wno-dev \
	-DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/Mediastreamer2 \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_DOC=%{?with_doc:ON}%{?!with_doc:OFF} \
	-DENABLE_NON_FREE_FEATURES:BOOL=NO \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_unit_tests:ON}%{?!with_unit_tests:OFF} \
	-DENABLE_QT_GL:BOOL=%{?with_qtgl:ON}%{!?with_qtgl:OFF} \
	-DENABLE_BV16:BOOL=OFF \
	-DENABLE_G729:BOOL=OFF \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

# FIXME: manually create plugin directory
#install -dm 0755 %{buildroot}%{_libdir}/%{name}/plugins

# don't install unit tester
%if %{with unit_tests} && ! %{with unit_tests_install}
rm -f  %{buildroot}%{_bindir}/%{name}2-tester
rm -fr %{buildroot}%{_datadir}/%{name}2-tester/
%endif

%check
%if %{with unit_tests}
pushd build
ctest
popd
%endif

