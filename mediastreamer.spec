%define major 6
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name}

Summary:	Audio/video real-time streaming library
Name:		mediastreamer
Version:	2.13.0
Release:	1
License:	GPL-2.0+
Group:		Communications
URL:		http://linphone.org/eng/documentation/dev/mediastreamer2.html
Source0:	http://download.savannah.gnu.org/releases/linphone/%{name}/%{name}-%{version}.tar.gz
Patch0:		mediastreamer-2.11.1-linkage_fix.diff
BuildRequires:  automake 
BuildRequires:  libtool
BuildRequires:  ffmpeg-devel
BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  gsm-devel
BuildRequires:  intltool
BuildRequires:  pcap-devel
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xv)
BuildRequires:  vim-common
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(glew) >= 1.5
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(libpulse) >= 0.9.21
BuildRequires:  pkgconfig(libsrtp) >= 1.5.2
BuildRequires:  pkgconfig(libupnp) >= 1.6
BuildRequires:  pkgconfig(libupnp) < 1.7
BuildRequires:  pkgconfig(vpx)
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
%apply_patches

%build
sh ./autogen.sh

%configure2_5x \
    --enable-external-ortp \
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
%{_libdir}/libmediastreamer_base.so.%{major}*
%{_libdir}/libmediastreamer_voip.so.%{major}*

%files -n %{develname}
%{_includedir}/mediastreamer2/
%{_libdir}/libmediastreamer_*.so
%{_libdir}/pkgconfig/*.pc

