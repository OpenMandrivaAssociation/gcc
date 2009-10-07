%define _vendor Manbo
%define _host_vendor manbo
%define _real_vendor manbo

%define name			%{cross_prefix}gcc%{package_suffix}
%define branch			4.4
%define branch_tag		%(perl -e 'printf "%%02d%%02d", split(/\\./,shift)' %{branch})
%define version			4.4.1
%define snapshot		%nil
%define release			%{manbo_mkrel 4}
%define nof_arches		noarch
%define spu_arches		ppc64
%define lsb_arches		i386 x86_64 ia64 ppc ppc64 s390 s390x mips mipsel mips64 mips64el
%define biarches		x86_64 ppc64 mips64 mips64el

# Define libraries major versions
%define libgcc_major		1
%define libstdcxx_major		6
%define libstdcxx_minor		12
%define libgfortran_major	3
%define libgcj_major		10
%define libobjc_major		2
%define libgnat_major		1
%define libffi_major		4
%define libmudflap_major	0
%define libssp_major		0
%define libgomp_major		1
%define libgcj_bc_major		1

# Disable -Werror because there's a format string warning in gcc/cp/parser.c 
# around line 2300 that a comment says is intentional :( 
%define Werror_cflags %nil

# Package holding Java tools (gij, jv-convert, etc.)
%define GCJ_TOOLS		%{cross_prefix}gcj%{package_suffix}-tools

# libgcj-devel should not provide libgcj_bc.so.1
%define _exclude_files_from_autoprov %{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcj_bc.so

#-- JDK version
%define jdk_version	1.5.0
%define jdk_base	java-%{jdk_version}-gcj
%define jdk_home	%{_prefix}/lib/jvm/%{jdk_base}-%{jdk_version}.0/jre

# Define if building a cross compiler
# FIXME: assume user does not define both cross and cross_bootstrap variables
%define build_cross		0
%define build_cross_bootstrap	0
%{expand: %{?cross:		%%global build_cross 1}}
%{expand: %{?cross_bootstrap:	%%global build_cross_bootstrap 1}}

# System compiler in MDV 2009
%if %{mdkversion} >= 200900
%define system_compiler		1
%else
%define system_compiler		0
%endif
%define target_cpu		%{_target_cpu}
%if %{build_cross}
%define system_compiler		0
%define target_cpu		%{cross}
%endif
%if %{build_cross_bootstrap}
%define build_cross		1
%define system_compiler		0
%define target_cpu		%{cross_bootstrap}
%endif
%if %{system_compiler}
%define alternative_priority	30%{branch_tag}
%define cross_prefix		%{nil}
%define cross_program_prefix	%{nil}
%define package_suffix		%{nil}
%define program_prefix		%{nil}
%define program_suffix		%{nil}
%define program_long_suffix     -%{version}
%else
%if %{build_cross}
%define alternative_priority	10%{branch_tag}
%define cross_prefix		cross-%{target_cpu}-
%define cross_program_prefix	%{target_cpu}-linux-
%if "%{target_cpu}" == "spu"
%define cross_program_prefix	%{target_cpu}-unknown-elf-
%endif
%define package_suffix		%{nil}
%define program_prefix		%{cross_program_prefix}
%define program_suffix		%{nil}
%define program_long_suffix	-%{version}
%else
%define alternative_priority	20%{branch_tag}
%define cross_prefix		%{nil}
%define cross_program_prefix	%{nil}
%define package_suffix		%{branch}
%define program_prefix		%{nil}
%define program_suffix		%{branch}
%define program_long_suffix	%{branch}
%endif
%endif
%define _alternativesdir	/etc/alternatives
%if "%{package_suffix}" == "%{nil}"
%define _package_suffix		%{nil}
%else
%define _package_suffix		-%{package_suffix}
%endif
%define gcc42_as_system_compiler 0
%if %{mdkversion} == 200800
%define gcc42_as_system_compiler 1
%endif
%if %{mdkversion} == 200810
%define gcc42_as_system_compiler 1
%endif

%if "%snapshot" != ""
%define source_package		gcc-%{branch}-%{snapshot}
%define source_dir		gcc-%{branch}-%{snapshot}
%else
%define source_package		gcc-%{version}
%define source_dir		gcc-%{version}
%endif

# Define GCC target platform, and arch we built for
%if %{build_cross}
%define biarches		noarch
%define arch			%{target_cpu}
%define gcc_target_platform	%{target_cpu}-linux
%if "%{target_cpu}" == "spu"
%define gcc_target_platform	%{target_cpu}-unknown-elf
%endif
%define target_prefix		%{_prefix}/%{gcc_target_platform}
%define target_libdir		%{target_prefix}/%{target_lib}
%define target_slibdir		%{target_prefix}/%{target_lib}
%define target_slibdir32	%{target_prefix}/lib
%else
%define arch			%(echo %{_target_cpu}|sed -e "s/\\(i.86\\|athlon\\)/i386/" -e "s/amd64/x86_64/" -e "s/\\(sun4.*\\|sparcv[89]\\)/sparc/")
%define gcc_target_platform	%{_target_platform}
%define target_prefix		%{_prefix}
%define target_libdir		%{_libdir}
%define target_slibdir		/%{_lib}
%define target_slibdir32	/lib
%endif
%define isarch()		%(case " %* " in (*" %{arch} "*) echo 1;; (*) echo 0;; esac)
%define gcc_libdir		%{_prefix}/lib/gcc
%define gcj_libdir		%{target_libdir}/gcj-%{version}-%{libgcj_major}

%define target_lib             lib
%if %isarch ppc64 sparc64 x86_64 mips64 mips64el
%define target_lib             lib64
%endif

%if %isarch x86_64
%define multilib_32_arch	i586
%endif
%if %isarch ppc64
%define multilib_32_arch	ppc
%endif
%if %isarch sparc64
%define multilib_32_arch	sparc
%endif
%if %isarch mips64
%define	multilib_32_arch	mips
%endif
%if %isarch mips64el
%define	multilib_32_arch	mipsel
%endif
%if %isarch %{biarches}
%define gcc32_target_platform	%{multilib_32_arch}-%{_real_vendor}-%{_target_os}%{?_gnu}
%endif

# Location of Java headers, don't let them in compiler specific
# directory as they are grabbed first
%define libjava_includedir	%{target_prefix}/include/libgcj-%{version}

# We now have versioned libstdcxx_includedir, that is c++/<VERSION>/
%define libstdcxx_includedir	%{target_prefix}/include/c++/%{version}

%define build_minimal		0
%define build_monolithic	0
%define build_doc		1
%define build_pdf_doc		1
%define build_check		0
%define build_ada		1
%define gpc_snapshot		20040516
%define build_pascal		0
%ifarch noarch
%define build_pascal		1
%endif
%if %isarch %{ix86} x86_64 ia64
%define build_ada		1
%endif
%define build_cxx		1
%define build_libstdcxx		%{build_cxx}
%define build_fortran		1
%define build_objc		1
%define build_objcp		1
%define build_libmudflap	1
%define build_libgomp           1
%define build_libgcj_bc		1
%define build_libffi		1
%define build_java		1
%define build_debug		0
%define build_stdcxxheaders	1
%if %{gcc42_as_system_compiler}
%define build_libstdcxx		0
%define build_libmudflap	0
%endif
%if %{mdkversion} >= 200700
# use SSP support from glibc 2.4
%define use_ssp_glibc		1
%define build_libssp		0
%else
%define build_libssp		1
%define use_ssp_glibc		0
%endif
%if !%{system_compiler}
%define build_objc		0
%define build_objcp		0
%define build_pascal		0
%define build_ada		0
%define build_libffi		0
%define build_libgomp		0
#define build_libgcj_bc		1
%endif
%define use_hash_style_gnu	0
%define build_cloog		1

# Define C library to use
%define libc glibc
%define libc_shared 1
%if "%{libc}" == "glibc"
# Default to --hash-style=gnu on MDK >= 2007.1
%if %{mdkversion} >= 200710
%define use_hash_style_gnu 1
%endif
%endif
%if !%{build_cross_bootstrap}
# Make sure pthread.h doesn't contain __thread keyword
%define libc_version 2.2.5-14mdk
%if %{use_ssp_glibc}
# Make sure glibc supports stack protector
%define libc_version 2.4-1mdk
%endif
%if %isarch ppc ppc64 sparc sparcv9
# Make sure glibc supports 128-bit long doubles
%define libc_version 2.4-4mdk
%endif
%if %{use_hash_style_gnu}
# Make sure glibc supports DT_GNU_HASH
%define libc_version 2.4-6mdk
%endif
%if %isarch spu
# Make sure we build against newlib
%define libc newlib
%define libc_shared 0
%define libc_version 1.15.0
%endif
%endif

%if %isarch spu mips mipsel mips64 mips64el
# spu & mips port doesn't support the following languages yet
%define build_fortran		0
%define build_libssp		0
%define use_ssp_glibc		0
%endif

# Allow --with[out] <feature> at rpm command line build
%{expand: %{?_without_PDF:	%%global build_pdf_doc 0}}
%{expand: %{?_without_DEBUG:	%%global build_debug 0}}
%{expand: %{?_without_check:	%%global build_check 0}}
%{expand: %{?_without_CHECK:	%%global build_check 0}}
%{expand: %{?_without_MINIMAL:	%%global build_minimal 0}}
%{expand: %{?_with_PDF:		%%global build_pdf_doc 1}}
%{expand: %{?_with_DEBUG:	%%global build_debug 1}}
%{expand: %{?_with_CHECK:	%%global build_check 1}}
%{expand: %{?_with_MINIMAL:	%%global build_minimal 1}}

# Allow --without <front-end> at rpm command line build
%{expand: %{?_with_CXX:		%%global build_cxx 1}}
%{expand: %{?_with_ADA:		%%global build_ada 1}}
%{expand: %{?_with_FORTRAN:	%%global build_fortran 1}}
%{expand: %{?_with_JAVA:	%%global build_java 1}}
%{expand: %{?_with_OBJC:	%%global build_objc 1}}
%{expand: %{?_with_OBJCXX:	%%global build_objcp 1}}
%{expand: %{?_with_PASCAL:	%%global build_pascal 1}}

# Allow --with <front-end> at rpm command line build
%{expand: %{?_without_CXX:	%%global build_cxx 0}}
%{expand: %{?_without_ADA:	%%global build_ada 0}}
%{expand: %{?_without_FORTRAN:	%%global build_fortran 0}}
%{expand: %{?_without_JAVA:	%%global build_java 0}}
%{expand: %{?_without_OBJC:	%%global build_objc 0}}
%{expand: %{?_without_OBJCXX:	%%global build_objcp 0}}
%{expand: %{?_without_PASCAL:	%%global build_pascal 0}}

# A minimal build overrides all other options
%if %{build_cross_bootstrap}
%define build_minimal		1
%define libc_shared		0
%endif
%if %{build_minimal}
%define build_doc		0
%define build_pdf_doc		0
%define build_check		0
%define build_ada		0
%define build_cxx		0
%define build_fortran		0
%define build_objc		0
%define build_objcp		0
%define build_java		0
%define build_debug		0
%define build_libffi		0
%define build_libmudflap	0
%endif
%if %{build_cross}
%define build_monolithic	1
%define build_doc		0
%define build_pdf_doc		0
# Unsupported front-ends when cross-compiling for now
%define build_check		0
%define build_java		0
%define build_ada		0
%define build_libffi		0
%define build_libmudflap	0
%endif
%if !%{libc_shared}
%define build_java		0
%endif
%if !%{build_java}
%define build_libffi		0
%endif

# Define library packages names
%define libgcc_name_orig	%{cross_prefix}libgcc
%define libgcc_name		%{libgcc_name_orig}%{libgcc_major}
%define libstdcxx_name_orig	%{cross_prefix}libstdc++
%define libstdcxx_name		%{libstdcxx_name_orig}%{libstdcxx_major}
%define libgfortran_name_orig	%{cross_prefix}libgfortran
%define libgfortran_name	%{libgfortran_name_orig}%{libgfortran_major}
%define libgcj_name_orig	%{cross_prefix}libgcj
%define libgcj_name		%{cross_prefix}%{mklibname gcj %{libgcj_major}}
%define libgcj_devel_name	%{cross_prefix}%{mklibname gcj -d}
%define libgcj_static_devel_name %{cross_prefix}%{mklibname gcj -d -s}
%define libgcj_name_base	%{libgcj_name_orig}%{libgcj_major}
%define libgcj_bc_name		%{cross_prefix}%{mklibname gcj_bc %{libgcj_bc_major}}
%define libobjc_name_orig	%{cross_prefix}libobjc
%define libobjc_name		%{libobjc_name_orig}%{libobjc_major}
%define libgnat_name_orig	%{cross_prefix}libgnat
%define libgnat_name		%{libgnat_name_orig}%{libgnat_major}
%define libffi_name_orig	%{cross_prefix}libffi
%define libffi_name		%{libffi_name_orig}%{libffi_major}
%define libmudflap_name_orig	%{cross_prefix}libmudflap
%define libmudflap_name		%{libmudflap_name_orig}%{libmudflap_major}
%define libssp_name_orig	%{cross_prefix}libssp
%define libssp_name		%{libssp_name_orig}%{libssp_major}
%define libgomp_name_orig	%{cross_prefix}libgomp
%define libgomp_name		%{libgomp_name_orig}%{libgomp_major}

# Extract Mandriva Linux name and version
%define mdk_distro_version_file	/etc/release
%define mdk_distro_version	%(perl -ne '/^([.\\w\\s]+) \\(.+\\).+/ and print $1' < %{mdk_distro_version_file})

Summary:	GNU Compiler Collection
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv3+
Group:		Development/C

# Main source:	(CVS)
URL:		http://gcc.gnu.org/
Source0:	%{source_package}.tar.bz2
Source1:	lsb-headers-3.1.1.tar.bz2
Source5:	gcc35-gpc-%{gpc_snapshot}.tar.bz2
# FIXME: unless we get proper help2man package
Source6:	gcc35-help2man.pl
Source7:	gcc35-gnatmake-bash-completion
Source8:	build_cross_gcc4.sh

# Mandriva patches + backports from trunk
# LSB compliant headers (for cross compiling without (glibc?) headers)
Patch999: lsb-headers-3.1.1-misc.patch
Patch1000: lsb-headers-3.1.1-mips-support.patch
# slibdir is either /lib or /lib64
Patch101: gcc33-pass-slibdir.patch
# pass libdir around
Patch107: gcc33-multi-do-libdir.patch

# testsuite
Patch1: gcc33-pr11536-testcase.patch
Patch2: gcc33-pr9929-testcase.patch
Patch102: gcc32-pr7434-testcase.patch
Patch103: gcc33-pr8213-testcase.patch
Patch113: gcc33-pr11631.patch
# ada
Patch105: gcc35-ada-link.patch
Patch106: gcc40-ada-makefile.patch
# gnu pascal
Patch111: gcc34-gpc-fixes.patch
Patch112: gcc33-gpc-serialize-build.patch

# -Wformat=security fixes
Patch114: gcc-4.3.3-wformat-fixes.patch

# build 32 bits code when running through linux32
Patch115: gcc40-linux32.patch
# ?
Patch116: gcc40-linux32-build-env.patch
# (cjw) disable building of 'nof' libs on ppc
Patch129: gcc-4.1.2-ppc-soft-float-64bit-double-libs.patch

# Load property.files from /usr/lib, not /usr/lib64, so that
# they can be shared with other classpath jvms (asked by dwalluck)
Patch130: gcc43-no-multilib-propertydir.patch
Patch132: gcc43-custom-libgcj_bc-rpath.patch

# Red Hat patches
# allow --disable-libjava-multilib to disable multilib for java
Patch201: gcc4-java-nomulti.patch
# ?
Patch202: gcc4-ppc64-m32-m64-multilib-only.patch
# fix libltdl with multilib?
Patch207: gcc4-libltdl-multilib.patch

# workaround bug with redefined extern inline (mdvbz #41171, upstream #33763)
Patch208: gcc43-pr33763.patch

# use hash style gnu (faster dynamic linking, cf http://lwn.net/Articles/192624/)
Patch211: gcc43-hash-style-gnu.patch

# mips patches from the gdium tree
Patch301: gcc-mips-libjava-interp.patch
Patch302: gcc_mips_gcc_testsuite_fix_loop.patch


BuildRoot:	%{_tmppath}/%{name}-%{version}-root
# Want updated alternatives priorities
%if %{build_cross}
Conflicts:	gcc-cpp < 3.2.2-4mdk
%endif
%define binutils_version 2.16.91.0.2-2mdk
%if %{use_hash_style_gnu}
%define binutils_version 2.16.91.0.7-6mdk
%endif
Requires:	%{cross_prefix}binutils >= %{binutils_version}
BuildRequires:	%{cross_prefix}binutils >= %{binutils_version}
# Make sure gdb will understand DW_FORM_strp
Conflicts:	gdb < 5.1.1
BuildRequires:	zlib-devel
BuildRequires:	chrpath

%if %{gcc42_as_system_compiler}
# We need gcc4.2 + its libstdc++ headers
%define gcc42_version %(gcc4.2-version 2>/dev/null || echo 0)
%if !%{build_stdcxxheaders}
%define libstdcxx_includedir %{target_prefix}/include/c++/%{gcc42_version}
%endif
BuildRequires:	gcc4.2
BuildRequires:	gcc4.2-c++
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires:	%{name}-gnat >= 3.1, %{libgnat_name} >= 3.1
%endif
# cloog is used for Graphite support (optimizations)
# see http://gcc.gnu.org/wiki/Graphite
%if %{build_cloog}
BuildRequires: ppl-devel >= 0.10, cloog-ppl-devel >= 0.15
#Requires: libcloog1 >= 0.15
%endif
Requires:	%{name}-cpp = %{version}-%{release}
# FIXME: We need a libgcc with 3.4 symbols
%if %{libc_shared} && !%{build_monolithic}
Requires:	%{libgcc_name_orig} >= 3.3.2-5mdk
%endif
Requires(post): update-alternatives
Requires(postun): update-alternatives
BuildRequires:	gettext, flex, bison
BuildRequires:	texinfo >= 4.1
# XXX: Needs a GNU awk recent enough to correctly generate options.h
BuildRequires:	gawk >= 3.1.4
%if "%{?libc_version:%{libc_version}}" != ""
Requires:	%{cross_prefix}%{libc}-devel >= %{libc_version}
BuildRequires:	%{cross_prefix}%{libc}-devel >= %{libc_version}
%endif
%if %{build_check}
BuildRequires:	%{cross_prefix}glibc-static-devel
BuildRequires:	autogen
%endif
%if %{system_compiler}
Obsoletes:	gcc%{branch}
Provides:	gcc%{branch} = %{version}-%{release}
%else
Conflicts:	gcc%{branch} < %{version}-%{release}
%endif
%if "%{_real_vendor}" == "manbo"
Requires:	manbo-files-gcc%{program_suffix} = %{version}
%endif
%if %{build_pdf_doc}
BuildRequires:	tetex, tetex-dvips, tetex-latex
%endif
%if %{build_check}
BuildRequires:	dejagnu
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif
BuildRequires:	libgmp-devel
BuildRequires:	libmpfr-devel

%description
A compiler aimed at integrating all the optimizations and features
necessary for a high-performance and stable development environment.
This package is required for all other GCC compilers, namely C++,
Fortran 95, Objective C, Java and Ada 95.

%package -n %{libgcc_name}
Summary:	GNU C library
Group:		System/Libraries
Provides:	%{libgcc_name_orig} = %{version}-%{release}
Obsoletes:	%{libgcc_name_orig}%{branch}
Provides:	%{libgcc_name_orig}%{branch} = %{version}-%{release}
Obsoletes:	%{libgcc_name_orig}3.0
Provides:	%{libgcc_name_orig}3.0 = %{version}-%{release}
Provides:	%{libgcc_name_orig}3.2 = %{version}-%{release}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgcc_name}
The %{libgcc_name} package contains GCC shared libraries for gcc %{branch}

####################################################################
# C++ Compiler

%package c++
Summary:	C++ support for gcc
Group:		Development/C++
%if %{system_compiler}
Obsoletes:	gcc%{branch}-c++
Provides:	gcc%{branch}-c++ = %{version}-%{release}
%else
Conflicts:	gcc%{branch}-c++ < %{version}-%{release}
%endif
Requires:	%{name} = %{version}-%{release}
%if "%{_real_vendor}" == "manbo"
Requires:	manbo-files-gcc-c++%{program_suffix} = %{version}
%endif
%if %{system_compiler}
# some day, rpm will be smart enough: %if (%{system_compiler} || %{build_cross}) && !%{build_monolithic}
%if %{libc_shared}
Requires:	%{libstdcxx_name} = %{version}
%endif
Requires:	%{libstdcxx_name_orig}-devel = %{version}
%else

%if %{gcc42_as_system_compiler}
%if %{libc_shared}
Requires:	%{libstdcxx_name} >= %{gcc42_version}
%endif
%if !%{build_stdcxxheaders}
Requires:	%{libstdcxx_name_orig}-devel >= %{gcc42_version}
%endif
%endif
%endif

%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif
Requires(post): update-alternatives
Requires(postun): update-alternatives

%description c++
This package adds C++ support to the GNU C compiler. It includes support
for most of the current C++ specification, including templates and
exception handling. It does include the static standard C++
library and C++ header files; the library for dynamically linking
programs is available separately.

####################################################################
# C++ Libraries

%package -n %{libstdcxx_name}
Summary:	GNU C++ library
Group:		System/Libraries
Obsoletes:	%{libstdcxx_name_orig}%{branch}
Provides:	%{libstdcxx_name_orig}%{branch} = %{version}-%{release}
Provides:	%{libstdcxx_name_orig} = %{version}-%{release}
%if "%{branch}" == "3.3"
# By default, the libstdc++ from gcc3.3 is ABI compatible with the one
# from gcc3.2. Just tell other packages about it if they relied on that.
Provides:	%{libstdcxx_name_orig}3.2 = %{version}-%{release}
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libstdcxx_name}
This package contains the GCC Standard C++ Library v3, an ongoing
project to implement the ISO/IEC 14882:1998 Standard C++ library.

%package -n %{libstdcxx_name_orig}-devel
Summary:	Header files and libraries for C++ development
Group:		Development/C++
%if "%{_real_vendor}" == "manbo"
Requires:	manbo-files-gcc%{program_suffix} = %{version}
%endif
%if %{libc_shared}
Requires:	%{libstdcxx_name} = %{version}-%{release}
%endif
Obsoletes:	%{libstdcxx_name_orig}%{branch}-devel
Provides:	%{libstdcxx_name_orig}%{branch}-devel = %{version}-%{release}
Provides:	%{libstdcxx_name_orig}6-devel
Obsoletes:	%{libstdcxx_name_orig}6-devel
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libstdcxx_name_orig}-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development.

%package -n %{libstdcxx_name_orig}-static-devel
Summary:	Static libraries for C++ development
Group:		Development/C++
Requires:	%{libstdcxx_name_orig}-devel = %{version}-%{release}
Obsoletes:	%{libstdcxx_name_orig}%{branch}-static-devel
Provides:	%{libstdcxx_name_orig}%{branch}-static-devel = %{version}-%{release}
Provides:	%{libstdcxx_name_orig}6-static-devel
Obsoletes:	%{libstdcxx_name_orig}6-static-devel
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libstdcxx_name_orig}-static-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the static libraries needed for C++ development.

####################################################################
# Objective C Compiler

%package objc
Summary:	Objective C support for gcc
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-objc
Provides:	gcc%{branch}-objc = %{version}-%{release}
%endif
Requires:	%{name} = %{version}-%{release}
%if %{libc_shared} && !%{build_monolithic}
Requires:	%{libobjc_name} = %{version}-%{release}
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description objc
This package adds Objective C support to the GNU C compiler. Objective
C is an object oriented derivative of the C language, mainly used on
systems running NeXTSTEP. This package does not include the standard
Objective C object library.

####################################################################
# Objective C++ Compiler

%package objc++
Summary:	Objective C++ support for gcc
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-objc++
Provides:	gcc%{branch}-objc++ = %{version}-%{release}
%endif
Requires:	%{name}-objc = %{version}-%{release}
Requires:	%{name}-c++ = %{version}-%{release}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description objc++
This package adds Objective C++ support to the GNU C++ compiler.

####################################################################
# Objective C Libraries

%package -n %{libobjc_name}
Summary:	Objective C runtime libraries
Group:		System/Libraries
Obsoletes:	%{libobjc_name_orig}3.0, %{libobjc_name_orig}3.1
Provides:	%{libobjc_name_orig} = %{version}-%{release}
Provides:	%{libobjc_name_orig}3.0 = %{version}-%{release}
Provides:	%{libobjc_name_orig}3.1 = %{version}-%{release}
%if !%{system_compiler}
Conflicts:	%{name}-objc < %{branch}
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libobjc_name}
Runtime libraries for the GNU Objective C Compiler.

####################################################################
# Pascal Compiler

%package gpc
Summary:	Pascal support for gcc
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-gpc
Provides:	gcc%{branch}-gpc = %{version}-%{release}
%endif
Requires:	%{name} = %{version}-%{release}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description gpc
The GNU Pascal Compiler (GPC) is, as the name says, the Pascal
compiler of the GNU family.  The compiler supports the following
language standards and quasi-standards:

  * ISO 7185 Pascal (see Resources),
  * most of ISO 10206 Extended Pascal,
  * Borland Pascal 7.0,
  * parts of Borland Delphi, Mac Pascal and Pascal-SC (PXSC). 

####################################################################
# Fortran 95 Compiler

%package gfortran
Summary:	Fortran 95 support for gcc
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-gfortran
Provides:	gcc%{branch}-gfortran = %{version}-%{release}
%endif
%if "%{_real_vendor}" == "manbo"
Requires:	manbo-files-gcc-gfortran%{program_suffix} = %{version}
%endif
Obsoletes:	gcc%{branch}-g77
Requires:	%{name} = %{version}-%{release}
%if %{libc_shared} && !%{build_monolithic}
Requires:	%{libgfortran_name} = %{version}-%{release}
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description gfortran
This package adds support for compiling Fortran 95 programs with the GNU
compiler.

####################################################################
# Fortran 95 Libraries

%package -n %{libgfortran_name}
Summary:	Fortran 95 runtime libraries
Group:		System/Libraries
Provides:	%{libgfortran_name_orig} = %{version}
Obsoletes:	%{libgfortran_name_orig}%{branch}
Provides:	%{libgfortran_name_orig}%{branch} = %{version}-%{release}
Obsoletes:	libgfortran0
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgfortran_name}
This package contains Fortran 95 shared library which is needed to run
Fortran 95 dynamically linked programs.

####################################################################
# Ada 95 Compiler

%package gnat
Summary:	Ada 95 support for gcc
Group:		Development/Other
Requires:	%{libgnat_name} = %{version}-%{release}
%if %{system_compiler}
Obsoletes:	gcc%{branch}-gnat
Provides:	gcc%{branch}-gnat = %{version}-%{release}
%endif
Obsoletes:	%{cross_prefix}gnat
Provides:	%{cross_prefix}gnat = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description gnat
This package contains an Ada95 compiler and associated development
tools based on the GNU gcc technology. Ada95 is the object oriented
successor of the Ada83 language. To build this package from sources
you must have installed a binary version to bootstrap the compiler.

####################################################################
# Ada 95 Libraries

%package -n %{libgnat_name}
Summary:	Ada 95 runtime libraries
Group:		System/Libraries
Provides:	%{libgnat_name_orig} = %{version}-%{release}
Obsoletes:	%{cross_prefix}gnat-runtime
Provides:	%{cross_prefix}gnat-runtime = %{version}-%{release}

%description -n %{libgnat_name}
This package contains the shared libraries required to run programs
compiled with the GNU Ada compiler (GNAT) if they are compiled to use
shared libraries.  It also contains the shared libraries for the
Implementation of the Ada Semantic Interface Specification (ASIS), the
implementation of Distributed Systems Programming (GLADE) and the
Posix 1003.5 Binding (Florist).

####################################################################
# Java Compiler

%package java
Summary:	Java support for gcc
Group:		Development/Java
%if %{system_compiler}
Obsoletes:	gcc%{branch}-java
Provides:	gcc%{branch}-java = %{version}-%{release}
%endif
%if "%{_real_vendor}" == "manbo"
Requires:	manbo-files-gcc-java%{program_suffix} = %{version}
%endif
Requires:	%{name} = %{version}-%{release}
Requires:	%{GCJ_TOOLS} = %{version}-%{release}
Requires:	%{libgcj_name} >= %{version}
Requires:	%{libgcj_devel_name} >= %{version}
Requires:	libecj-java

%description java
This package adds experimental support for compiling Java(tm) programs
and bytecode into native code. To use this you will also need the
libgcj package.

####################################################################
# Java Runtime Tools

%package -n %{GCJ_TOOLS}
Summary:	Java related tools from gcc %{version}
Group:		Development/Java
%if %{system_compiler}
Obsoletes:	%{cross_prefix}gcj%{branch}-tools
Provides:	%{cross_prefix}gcj%{branch}-tools = %{version}-%{release}
Requires:	%{libgcj_bc_name} >= %{version}
%endif
%if "%{_real_vendor}" == "manbo"
Requires:	manbo-files-gcc-java%{program_suffix} = %{version}
%endif
Provides:	%{cross_prefix}gcj-tools = %{version}-%{release}
Requires:	%{libgcj_name} >= %{version}
Conflicts:	kaffe < 1.0.7-3mdk
Conflicts:	classpath < 0.97.1-2

%description -n %{GCJ_TOOLS}
This package includes Java related tools built from gcc %{version}:

   * gij: a Java ByteCode Interpreter
   * gcjh: generate header files from class files
   * jcf-dump: print information about class files
   * gcj-dbtool: tool for manipulating class file databases
   * grmic: generate stubs for Remote Method Invocation
   * grmiregistry: the remote object registry
   * aot-compile: ahead-of-time compiler
   * gappletviewer
   * gc-analyze
   * gjar
   * gjarsigner
   * gjavah
   * gkeytool
   * gnative2ascii
   * gorbd
   * grmid
   * gtnameserv
   * gserialver

####################################################################
# Java Libraries

%package -n %{libgcj_name}
Summary:	GNU Java runtime libraries
Group:		System/Libraries
Obsoletes:	%{cross_prefix}gcc-libgcj
Provides:	%{cross_prefix}gcc-libgcj = %{version}-%{release}
Obsoletes:	%{libgcj_name_orig}%{branch}
Provides:	%{libgcj_name_orig}%{branch} = %{version}-%{release}
%if %{build_java}
BuildRequires:	libxt-devel, libxtst-devel
BuildRequires:  jpackage-utils
# needed for cairo support (Graphics2D)
Requires:	gtk+2.0 >= 2.8.0
BuildRequires:	libgtk+2.0-devel >= 2.8.0
# for libgjsmdssi:
BuildRequires:	libjack-devel
BuildRequires:	dssi-devel
# for libgjsmalsa:
BuildRequires:	libalsa-devel
Requires:	libglib2.0 >= 2.4.0
BuildRequires:	libglib2.0-devel >= 2.4.0
BuildRequires:	libart_lgpl-devel >= 2.1.0
BuildRequires:	eclipse-ecj
BuildRequires:	zip
%endif
Obsoletes:	libgcj3, libgcj4
%if %{system_compiler}
Obsoletes:	libgcj5
Obsoletes:	%{mklibname gcj 6}
%endif
Requires:	%{libgcj_name_base}-base = %{version}
%if %isarch %{biarches}
Conflicts:	libgcj6 < 4.0.1-4mdk, lib64gcj6 < 4.0.1-4mdk
%endif

%description -n %{libgcj_name}
Runtime libraries for the GNU Java Compiler. The libgcj includes parts
of the Java Class Libraries, plus glue to connect the libraries to the
compiler and the underlying OS.

%package -n %{libgcj_devel_name}
Summary:	Header files and libraries for Java development
Group:		Development/Java
Requires:	zip >= 2.1
Requires:	zlib-devel
Requires:	%{libgcj_name} = %{version}-%{release}
Provides:	%{libgcj_name_orig}%{branch}-devel = %{version}-%{release}
Provides:	%{libgcj_name_orig}-devel = %{version}-%{release}
%if "%{_real_vendor}" == "manbo"
Requires:	manbo-files-gcc%{program_suffix} = %{version}
%endif
%if %{system_compiler}
Requires:	%{libgcj_bc_name} >= %{version}-%{release}
Obsoletes:	libgcj3-devel
Obsoletes:	libgcj4-devel
Obsoletes:	libgcj5-devel
Obsoletes:	%{mklibname gcj 6}-devel
Obsoletes:	%{mklibname gcj 7}-devel
Obsoletes:	%{mklibname gcj 9}-devel
%endif

%description -n %{libgcj_devel_name}
Development headers and libraries for the GNU Java Compiler. The
libgcj includes parts of the Java Class Libraries, plus glue to
connect the libraries to the compiler and the underlying OS.

%package -n %{libgcj_static_devel_name}
Summary:	Static libraries for Java development
Group:		Development/Java
Requires:	%{libgcj_devel_name} = %{version}-%{release}
Provides:	%{libgcj_name_orig}%{branch}-static-devel = %{version}-%{release}
Provides:	%{libgcj_name_orig}-static-devel = %{version}-%{release}
%if %{system_compiler}
Obsoletes:	libgcj3-static-devel
Obsoletes:	libgcj4-static-devel
Obsoletes:	libgcj5-static-devel
Obsoletes:	%{mklibname gcj 6}-static-devel
Obsoletes:	%{mklibname gcj 7}-static-devel
Obsoletes:	%{mklibname gcj 9}-static-devel
%endif

%description -n %{libgcj_static_devel_name}
Static libraries for the GNU Java Compiler.

%package -n %{libgcj_name_base}-base
Summary: Java library base classes
Group: Development/Java
# For /usr/lib/logging.properties and /usr/lib/security/classpath.security:
Requires: jpackage-utils
Conflicts: %{mklibname gcj 6} < 4.0.1-4mdk
%if %{system_compiler}
Obsoletes: libgcj6-base
%endif

%description -n %{libgcj_name_base}-base
The Java(tm) runtime library classes.

%package -n %{libgcj_name_base}-src
Summary: Java library sources
Group: Development/Java
Requires: %{libgcj_name} = %{version}-%{release}
%if %{system_compiler}
Obsoletes: libgcj6-src
%endif

%description -n %{libgcj_name_base}-src
The Java(tm) runtime library sources.

%package -n %{libgcj_bc_name}
Summary:	GNU Java runtime bytecode wrapper library
Group:		System/Libraries
%if %{system_compiler}
Conflicts:	%{mklibname gcj 8}
Conflicts:	%{mklibname gcj 9} < 4.3.3
%endif
Requires:	%{libgcj_name}

%description -n %{libgcj_bc_name}
Runtime wrapper library for applications using the bytecode interpreter
API of libgcj.

####################################################################
# FFI headers and libraries

%package -n %{libffi_name}
Summary:	GCC support library for FFI
Group:		System/Libraries

%description -n %{libffi_name}
This package contains GCC shared support library which is needed
for FFI support.

%package -n %{libffi_name}-devel
Summary:	Development headers and static library for FFI
Group:		Development/C
%if "%{_real_vendor}" == "manbo"
Requires:	manbo-files-gcc%{program_suffix} = %{version}
%endif
Requires:	%{libffi_name} = %{version}-%{release}
Provides:	%{libffi_name_orig}-devel = %{version}-%{release}
Obsoletes:	%{libffi_name_orig}-devel = 4.3.2
Obsoletes:	%{libffi_name_orig}-devel = 4.3.1
Obsoletes:	%{libffi_name_orig}-devel = 4.2.3
Obsoletes:	%{libffi_name_orig}-devel = 4.2.2
Provides:	ffi-devel = %{version}-%{release}

%description -n %{libffi_name}-devel
This package contains the development headers and the static library
for libffi. The libffi library provides a portable, high level
programming interface to various calling conventions. This allows a
programmer to call any function specified by a call interface
description at run time.

####################################################################
# mudflap headers and libraries

%package -n %{libmudflap_name}
Summary:	GCC mudflap shared support library
Group:		System/Libraries

%description -n %{libmudflap_name}
This package contains GCC shared support library which is needed
for mudflap support.

For front-ends that support it (C and C++), instrument all risky
pointer/array dereferencing operations, some standard library
string/heap functions, and some other associated constructs with
range/validity tests.  Modules so instrumented should be immune to
buffer overflows, invalid heap use, and some other classes of C/C++
programming errors.

Refer to the documentation for -fmudflap and -fmudflapth.

%package -n %{libmudflap_name_orig}-devel
Summary:	GCC mudflap support
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
%if %{libc_shared}
Requires:	%{libmudflap_name} = %{version}-%{release}
%endif
Obsoletes:	libmudflap0-devel

%description -n %{libmudflap_name_orig}-devel
This package contains headers and static libraries for building
mudflap-instrumented programs.

To instrument a non-threaded program, add `-fmudflap' option to GCC
and when linking add `-lmudflap'. For threaded programs also add
`-fmudflapth' and `-lmudflapth'.

####################################################################
# SSP headers and libraries

%package -n %{libssp_name}
Summary:	GCC SSP shared support library
Group:		System/Libraries

%description -n %{libssp_name}
This package contains GCC shared support library which is needed
for SSP support.

%package -n %{libssp_name_orig}-devel
Summary:	GCC SSP support
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
%if %{libc_shared}
Requires:	%{libssp_name} = %{version}-%{release}
%endif

%description -n %{libssp_name_orig}-devel
This package contains headers and static libraries for building
SSP-instrumented programs.

Refer to the documentation for -fstack-protector.

####################################################################
# GCC OpenMP headers and library

%package -n %{libgomp_name}
Summary:	GCC OpenMP support library
Group:		System/Libraries

%description -n %{libgomp_name}
This package contains the GCC shared support library which is needed 
for OpenMP support.

%package -n %{libgomp_name_orig}-devel
Summary:	GCC OpenMP support
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
%if %{libc_shared}
Requires:	%{libgomp_name} = %{version}-%{release}
%endif

%description -n %{libgomp_name_orig}-devel
This package contains headers and static libraries for building 
programs that use OpenMP.

####################################################################
# Preprocessor

%package cpp
Summary:	The C Preprocessor
Group:		Development/C
%if %{system_compiler}
Obsoletes:	gcc%{branch}-cpp
Provides:	gcc%{branch}-cpp = %{version}-%{release}
%endif
Requires(post): update-alternatives
Requires(postun): update-alternatives

%description cpp
The C preprocessor is a 'macro processor' which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define 'macros,' which are abbreviations for longer
constructs.

The C preprocessor provides four separate facilities that you can use as
you see fit:

* Inclusion of header files. These are files of declarations that can be
  substituted into your program.
* Macro expansion. You can define 'macros,' which are abbreviations for 
  arbitrary fragments of C code, and then the C preprocessor will replace
  the macros with their definitions throughout the program.
* Conditional compilation. Using special preprocessing directives,
  you can include or exclude parts of the program according to various
  conditions.
* Line control. If you use a program to combine or rearrange source files
  into an intermediate file which is then compiled, you can use line
  control to inform the compiler about where each source line originated.

You should install this package if you are a programmer who is searching for
such a macro processor.

####################################################################
# SPU compilers

%package -n spu-gcc
Summary:	GNU C Compiler for Cell SPU
Group:		Development/C
Requires:	spu-binutils
Requires:	spu-newlib

%description -n spu-gcc
This package contains the C compiler for Cell SPU.

%package -n spu-gcc-c++
Summary:	GNU C++ Compiler for Cell SPU
Group:		Development/C++
Requires:	spu-gcc
Requires:	%{libstdcxx_name_orig}-devel = %{version}-%{release}

%description -n spu-gcc-c++
This package contains the C++ compiler for Cell SPU.

####################################################################
# Documentation

%package doc
Summary:	GCC documentation
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-doc
Provides:	gcc%{branch}-doc = %{version}-%{release}
%endif
Requires(post): info-install
Requires(preun): info-install

%description doc
GCC is a compiler suite aimed at integrating all the optimizations and
features necessary for a high-performance and stable development
environment. This package contains the compiler documentation in INFO
pages.

%package doc-pdf
Summary:	GCC documentation
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-doc-pdf
Provides:	gcc%{branch}-doc-pdf = %{version}-%{release}
%endif

%description doc-pdf
GCC is a compiler suite aimed at integrating all the optimizations and
features necessary for a high-performance and stable development
environment. This package contains the compiler printable
documentation in PDF.

%prep
%setup -q -n %{source_dir} -a 5
%patch1 -p1 -b .pr11536-testcase
%patch2 -p1 -b .pr9929-testcase

# Mandriva patches
%patch101 -p1 -b .pass-slibdir
%patch102 -p1 -b .pr7434-testcase
%patch103 -p1 -b .pr8213-testcase

%patch105 -p1 -b .ada-link
%patch106 -p1 -b .ada-makefile

%patch107 -p1 -b .multi-do-libdir
%patch113 -p1 -b .pr11631-testcase
%patch114 -p1 -b .wformat
%patch115 -p1 -b .linux32
%patch116 -p1 -b .linux32-build-env
%patch129 -p1 -b .nonof

%patch130 -p1
perl -pi -e 's,\@PROPERTYFILES\@,"%{_prefix}/lib",' libjava/gnu/classpath/natSystemProperties.cc

%patch132 -p1
%if %build_libgcj_bc && !%system_compiler
perl -pi -e 's,\@ADDITIONAL_RPATH\@,-rpath %{target_libdir}/gcj_bc-%{libgcj_major},' libjava/Makefile.{am,in}
%else
perl -pi -e 's,\@ADDITIONAL_RPATH\@,,' libjava/Makefile.{am,in}
%endif

# Red Hat patches
%patch201 -p1 -b .java-nomulti
%patch202 -p1 -b .ppc64-m32-m64-multilib-only
%patch207 -p1 -b .libltdl-multilib
%patch208 -p1 -b .pr33763
%if %{use_hash_style_gnu}
%patch211 -p1 -b .hash-style-gnu
%endif

# Integrate GNU Pascal compiler
%if %{build_pascal}
mv gpc-%{gpc_snapshot}/p gcc/p
rmdir gpc-%{gpc_snapshot}
patch -p1 < gcc/p/diffs/gcc-3.5.0.diff
%patch111 -p1 -b .gpc-fixes
%patch112 -p1 -b .gpc-serialize-build
%endif
%patch301 -p1 -b .mips_java
%patch302 -p1 -b .mips-testsuite-addr

# Setup files for cross-compilation
# XXX embed uClibc / dietlibc sources? [ia64 checks for __GLIBC__]
%ifarch %{spu_arches}
sysroot=%{_prefix}/spu
%endif
%if %{build_cross}
sysroot=%{_prefix}/%{gcc_target_platform}
%endif
if [[ -n "$sysroot" ]]; then
mkdir sysroot
cd sysroot
[[ -d $sysroot/bin ]] &&
ln -s $sysroot/bin bin
[[ -f $sysroot/usr/include/stdio.h ]] &&
ln -s $sysroot/usr/include include
[[ -f $sysroot/lib/crti.o ]] &&
ln -s $sysroot/lib lib
[[ -f $sysroot/lib64/crti.o ]] &&
ln -s $sysroot/lib64 lib64
[[ -L usr/include ]] || {
mkdir -p usr/include
tar jxf %{SOURCE1} -C usr/include
cd usr
%patch999 -p0
%patch1000 -p0 -b .mips~
}
cd ../..
fi

# We can actually link binaries at this stage
# XXX integrate into Patch104 (cross-build-fixes)?
%if %{build_cross}
perl -pi -e '/^DRIVER_DEFINES/ .. /^gcc/ and s/(\@TARGET_SYSTEM_ROOT_DEFINE\@)/-DSYSROOT_SPEC="\\"\\"" \1/' gcc/Makefile.in
perl -ni -e '/^m4_define.+AC_LINK/ .. /^m4_defn.+AC_LINK/ or print' config/no-executables.m4
perl -pi -e 's/^(.+GLIBCXX_IS_NATIVE)=false/\1=true/' libstdc++-v3/configure.ac
for d in libiberty libgfortran libstdc++-v3; do
cd $d
autoconf
cd ..
done
%endif

%if !%build_libgcj_bc
perl -pi -e 's,use_libgcj_bc=yes,use_libgcj_bc=no,' libjava/configure.host
%endif

# Patch version for Mandriva and bug reports
echo "%{version}" > gcc/BASE-VER
perl -pi -e '/^\#define VERSUFFIX/ and s/""/" (%{version}-%{release})"/' gcc/version.c

# Fix java-ext path
sed -i -e 's,\$(jardir)/ext,$(jardir)-ext,g' libjava/Makefile.{am,in}

%build
# FIXME: extra tools needed
mkdir -p bin
install -m755 %{SOURCE6} bin/help2man
export PATH=$PATH:$PWD/bin

# Prepare OPT_FLAGS
OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g' -e 's/-fno-exceptions//g' -e 's/-mcpu=pentiumpro//g'`
%if %{build_debug}
OPT_FLAGS=`echo "$OPT_FLAGS -g" | sed -e "s/-fomit-frame-pointer//g"`
%endif
%if %{build_cross}
OPT_FLAGS="-O2 -g -pipe"
%endif
%if %isarch %{biarches}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/\(-m64\|-m32\)//g'`
%endif
%ifarch ppc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Wp,-D_FORTIFY_SOURCE=2 -fstack-protector --param=ssp-buffer-size=4//'`
%endif
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-fomit-frame-pointer//g'`

# don't build crt files with -fasynchronous-unwind-tables
case " $OPT_FLAGS " in
*" -fasynchronous-unwind-tables "*)
  perl -pi -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables /' gcc/Makefile.in
  ;;
esac

# Force a seperate object dir
rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

# Make bootstrap-lean
LANGUAGES="c"
%if %{build_cxx}
LANGUAGES="$LANGUAGES,c++"
%endif
%if %{build_ada}
LANGUAGES="$LANGUAGES,ada"
%endif
%if %{build_fortran}
LANGUAGES="$LANGUAGES,fortran"
%endif
%if %{build_objc}
LANGUAGES="$LANGUAGES,objc"
LIBOBJC_FLAGS="--enable-objc-gc"
%endif
%if %{build_objcp}
LANGUAGES="$LANGUAGES,obj-c++"
%endif
%if %{build_java}
LANGUAGES="$LANGUAGES,java"
%endif
%if %{build_pascal}
LANGUAGES="$LANGUAGES,pascal"
%endif
PROGRAM_SUFFIX=""
%if "%{program_suffix}" != ""
PROGRAM_SUFFIX="--program-suffix=%{program_suffix}"
%endif
PROGRAM_PREFIX=""
%if "%{program_prefix}" != ""
PROGRAM_PREFIX="--program-prefix=%{program_prefix}"
%endif
%if %{build_cxx}
LIBSTDCXX_FLAGS="--enable-long-long --enable-__cxa_atexit --disable-libunwind-exceptions"
case %{libc} in
glibc)		LIBSTDCXX_FLAGS="$LIBSTDCXX_FLAGS --enable-clocale=gnu";;
esac
%endif
%if %{build_java}
LIBJAVA_FLAGS="--enable-java-awt=gtk --with-java-home=%{jdk_home} --with-ecj-jar=%{_datadir}/java/eclipse-ecj.jar"
LIBJAVA_FLAGS="$LIBJAVA_FLAGS --enable-gtk-cairo"
LIBJAVA_FLAGS="$LIBJAVA_FLAGS --disable-libjava-multilib"
%else
LIBJAVA_FLAGS="--disable-libgcj"
%endif
SSP_FLAGS="--disable-ssp --disable-libssp"
%if %{build_libssp}
SSP_FLAGS="--enable-ssp --enable-libssp"
%endif
%if %{use_ssp_glibc}
SSP_FLAGS="--enable-ssp --disable-libssp"
%endif
%if !%{build_libmudflap}
MUDFLAP_FLAGS="--disable-libmudflap"
%endif
%if !%{build_libgomp}
LIBGOMP_FLAGS="--disable-libgomp"
%endif
%if %{build_cloog}
CLOOG_FLAGS="--with-ppl --with-cloog"
%endif
%if !%{build_libffi} && !%{build_java}
LIBFFI_FLAGS="--disable-libffi"
%endif
%if %{build_cross}
CROSS_FLAGS="--with-build-sysroot=$PWD/../sysroot --with-headers --disable-multilib --disable-nls"
%endif
%if %{build_cross_bootstrap}
CROSS_FLAGS="--disable-multilib --disable-threads"
%if %isarch %{lsb_arches}
# we have embedded the LSB 3.1 headers, so we can build the unwinding stuff too (ia64)
CROSS_FLAGS="$CROSS_FLAGS --with-build-sysroot=$PWD/../sysroot --with-headers"
%endif
%endif
%if !%{system_compiler} && !%{build_stdcxxheaders}
LIBSTDCXX_FLAGS="$LIBSTDCXX_FLAGS --with-gxx-include-dir=%{libstdcxx_includedir}"
%endif
[[ -n "$CROSS_FLAGS" ]] && CROSS_FLAGS="$CROSS_FLAGS --target=%{gcc_target_platform}"
case %{libc} in
%if %{build_cross_bootstrap}
glibc)		LIBC_FLAGS="";;
%else
glibc)		LIBC_FLAGS="--enable-threads=posix";;
%endif
newlib)		LIBC_FLAGS="--with-newlib --with-headers --disable-threads";;
*)		echo "ERROR: unsupported %{libc} C library"; exit 1;;
esac
%if %{libc_shared}
LIBC_FLAGS="$LIBC_FLAGS --enable-shared"
%else
LIBC_FLAGS="$LIBC_FLAGS --disable-shared"
%endif
# target specific flags (don't %ifarch for cross compilers)
case %{target_cpu} in
x86_64)		TARGET_FLAGS="--with-cpu=generic";;
i?86|athlon)	TARGET_FLAGS="--with-cpu=generic";;
ppc)		TARGET_FLAGS="--with-cpu=750 --with-long-double-128";;
ppc32|ppc64)	TARGET_FLAGS="--with-cpu=power4 --with-long-double-128";;
sparc|sparcv9)	TARGET_FLAGS="--with-long-double-128";;
mips64|mips64el) TARGET_FLAGS="--enable-long-long --with-abi=64";;
esac

# (anssi) building with external jar fails
%define python_dir %(echo "%{py_puresitedir}" | sed 's!^%{_prefix}!!g')
export JAR="no"
export FASTJAR="no"
CC="%{__cc}" CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --libexecdir=%{_prefix}/lib --with-slibdir=%{target_slibdir} \
	--with-bugurl=https://qa.mandriva.com/ \
	--mandir=%{_mandir} --infodir=%{_infodir} --enable-checking=release \
	--enable-languages="$LANGUAGES" $PROGRAM_PREFIX $PROGRAM_SUFFIX \
	--build=%{_target_platform} --host=%{_target_platform} $CROSS_FLAGS $TARGET_FLAGS \
	--with-system-zlib $LIBC_FLAGS $LIBOBJC_FLAGS $LIBSTDCXX_FLAGS $LIBJAVA_FLAGS $SSP_FLAGS \
	$MUDFLAP_FLAGS $LIBFFI_FLAGS --disable-werror $LIBGOMP_FLAGS \
	$CLOOG_FLAGS --with-python-dir=%{python_dir}
touch ../gcc/c-gperf.h
%if %{build_cross}
# (peryvind): xgcc seems to ignore --sysroot, so let's just workaround it for
# by adding a symlink to the headers since xgcc already passes -isystem ./include
mkdir -p %{target_cpu}-linux/libgcc
ln -sf $PWD/../sysroot/usr/include %{target_cpu}-linux/libgcc/include
%make
%else
# bootstrap-lean is similar to bootstrap except "object files from the stage1
# and stage2 of the 3-stage bootstrap of the compiler are deleted as soon as
# they are no longer needed."
%make bootstrap-lean BOOT_CFLAGS="$OPT_FLAGS"

%endif

%if !%{build_cross}
# Make protoize
make -C gcc CC="./xgcc -B ./ -O2" proto
%endif
cd ..

# Build the SPU compiler
%ifarch %{spu_arches}
rm -rf objs-spu
mkdir objs-spu
cd objs-spu

%define spu_prefix %{_prefix}/spu
%define spu_program_prefix spu-
SPU_OPT_FLAGS="-O2 -g -pipe -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
CC="%{__cc} $OPT_FLAGS" CFLAGS="$SPU_OPT_FLAGS" CXXFLAGS="$SPU_OPT_FLAGS" XCFLAGS="$SPU_OPT_FLAGS" TCFLAGS="$SPU_OPT_FLAGS" \
../configure \
	--prefix=%{_prefix} --libexecdir=%{_prefix}/lib --with-slibdir=%{spu_prefix}/lib \
	--mandir=%{_mandir} --infodir=%{_infodir} \
	--with-build-sysroot=$PWD/../sysroot --with-newlib --with-headers --disable-shared \
	--disable-threads --disable-multilib --disable-nls \
	--enable-checking=release --enable-languages="c,c++" --disable-libssp --disable-libmudflap \
	--host=%{_target_platform} --build=%{_target_platform} --target=spu \
	--program-prefix=%{spu_program_prefix}
%make
cd ..
%endif

# Copy various doc files here and there
mkdir -p rpm.doc/gfortran
mkdir -p rpm.doc/objc
mkdir -p rpm.doc/objcp
mkdir -p rpm.doc/libjava
mkdir -p rpm.doc/libobjc
mkdir -p rpm.doc/boehm-gc
mkdir -p rpm.doc/gpc
mkdir -p rpm.doc/c++
mkdir -p rpm.doc/libstdc++

%if %{build_libstdcxx}
(cd libstdc++-v3; for i in ChangeLog*; do
	ln -f $i ../rpm.doc/libstdc++/$i
done)
%endif
%if %{build_cxx}
(cd gcc/cp; for i in ChangeLog*; do
	ln -f $i ../../rpm.doc/c++/$i
done)
%endif
%if %{build_pascal}
(cd gcc/p; for i in ChangeLog* README NEWS FAQ; do
	ln -f $i ../../rpm.doc/gpc/$i
done)
%endif
%if %{build_fortran}
(cd gcc/fortran; for i in ChangeLog*; do
	ln -f $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	ln -f $i ../rpm.doc/gfortran/$i.libgfortran
done)
%endif
%if %{build_objc}
(cd gcc/objc; for i in README*; do
	ln -f $i ../../rpm.doc/objc/$i.objc
done)
(cd libobjc; for i in README*; do
	ln -f $i ../rpm.doc/libobjc/$i.libobjc
done)
%endif
%if %{build_objcp}
(cd gcc/objcp;
  # XXX placeholder, there may be docs in the future
  echo "Objective-C++ support for GCC" > ../../rpm.doc/objcp/README)
%endif
%if %{build_java}
(cd boehm-gc; for i in ChangeLog*; do
        ln -f $i ../rpm.doc/boehm-gc/$i.gc
done)
(cd libjava; for i in README THANKS COPYING ChangeLog; do
	ln -f $i ../rpm.doc/libjava/$i.libjava
done)
(cd libjava; ln -f LIBGCJ_LICENSE ../rpm.doc/libjava/LICENSE.libjava)
%endif

# [ghibo] - build printable documentation
%if %{build_pdf_doc}
%if %{mdkversion} >= 200710
export PDFTEX=pdftex
%endif
unset TEXINPUTS
(cd gcc/doc; for file in gcc.texi cpp.texi cppinternals.texi; do
  texi2dvi -p -t @afourpaper -t @finalout -I ./include -I ../../obj-%{gcc_target_platform}/gcc $file
done)
(cd gcc/fortran;
  texi2dvi -p -t @afourpaper -t @finalout -I ../doc/include -I ../../obj-%{gcc_target_platform}/gcc gfortran.texi)
%if %{build_ada}
(cd gcc/ada;
  texi2dvi -p -t @afourpaper -t @finalout -I ../doc/include -I ../../obj-%{gcc_target_platform}/gcc gnat_rm.texi)
(cd obj-%{gcc_target_platform}/gcc/doc;
  texi2dvi -p -t @afourpaper -t @finalout -I ../../../gcc/doc/include -I .. gnat_ugn.texi
  mv gnat_ugn.pdf ../../../gcc/ada/gnat_ugn.pdf)
%endif
%endif

%check
echo ====================TESTING=========================
%if %{build_check}
cd obj-%{gcc_target_platform}
time %make -k check || true
echo "XXX check time above XXX"
../contrib/test_summary > ../test_summary.log
cd ..
%endif
echo ====================TESTING END=====================
 
%install
rm -rf %{buildroot}

# Fix HTML docs for libstdc++-v3
perl -pi -e \
  's~href="l(ibstdc|atest)~href="http://gcc.gnu.org/onlinedocs/libstdc++/l\1~' \
  libstdc++-v3/doc/html/api.html

# Create some directories, just to make sure (e.g. ColorGCC)
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}
mkdir -p %{buildroot}%{_infodir}
mkdir -p %{buildroot}%{_sysconfdir}

%ifarch %{spu_arches}
%makeinstall_std -C objs-spu
%endif

pushd obj-%{gcc_target_platform};
  %makeinstall_std
  %if %{build_java}
  %makeinstall_std -C %{gcc_target_platform}/libjava install-src.zip
  %endif
popd

FULLVER=`%{buildroot}%{_bindir}/%{gcc_target_platform}-gcc%{program_suffix} --version | head -n 1 | cut -d' ' -f3`
FULLPATH=$(dirname %{buildroot}%{gcc_libdir}/%{gcc_target_platform}/%{version}/cc1)

# Create /usr/bin/%{program_prefix}gcc%{branch}-version that contains the full version of gcc
cat >%{buildroot}%{_bindir}/%{program_prefix}gcc%{branch}-version <<EOF
#!/bin/sh
echo "$FULLVER"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{program_prefix}gcc%{branch}-version

%if "%{program_suffix}" == ""
mv %{buildroot}%{_bindir}/%{program_prefix}cpp %{buildroot}%{_bindir}/%{program_prefix}cpp-%{version}
mv %{buildroot}%{_bindir}/%{program_prefix}gcc %{buildroot}%{_bindir}/%{program_prefix}gcc-%{version}
%if %{build_cxx}
mv %{buildroot}%{_bindir}/%{program_prefix}g++ %{buildroot}%{_bindir}/%{program_prefix}g++-%{version}
%endif
%endif

# replacing hardlinks with symlinks
ln -sf %{program_prefix}gcc%{program_long_suffix} %{buildroot}%{_bindir}/%{gcc_target_platform}-gcc%{program_suffix}
# TODO: cleanups?
%if "%{program_prefix}" != "%{gcc_target_platform}-"
ln -sf %{program_prefix}gcc%{program_long_suffix} %{buildroot}%{_bindir}/%{gcc_target_platform}-gcc-%{version}
%endif
%if %{build_cxx}
ln -sf %{program_prefix}g++%{program_long_suffix} %{buildroot}%{_bindir}/c++%{program_long_suffix}
ln -sf %{program_prefix}g++%{program_long_suffix} %{buildroot}%{_bindir}/%{gcc_target_platform}-c++%{program_suffix}
ln -sf %{program_prefix}g++%{program_long_suffix} %{buildroot}%{_bindir}/%{gcc_target_platform}-g++%{program_suffix}
%endif
%if %{build_fortran}
ln -sf %{program_prefix}gfortran%{program_suffix} %{buildroot}%{_bindir}/%{gcc_target_platform}-gfortran%{program_suffix}
%endif
%if %{build_java}
ln -sf %{program_prefix}gcj%{program_suffix} %{buildroot}%{_bindir}/%{gcc_target_platform}-gcj%{program_suffix}
ln -sf %{program_prefix}gcjh%{program_suffix} %{buildroot}%{_bindir}/%{gcc_target_platform}-gcjh%{program_suffix}
%endif

%if %{system_compiler}
ln -s gcc %{buildroot}%{_bindir}/cc
%endif

rm -f %{buildroot}%{_infodir}/dir

%if %{build_ada} && %{libc_shared}
%if %isarch ppc64 sparc64 x86_64 mips64 mips64el
rm -rf $FULLPATH/32/ada{include,lib}
%endif
# Dispatch Ada 95 libraries (special case)
pushd $FULLPATH/adalib
  rm -f libgnarl.so* libgnat.so*
  mv -f libgnarl-*.so.* %{buildroot}%{_libdir}/
  ln -s ../../../../../%{_lib}/libgnarl-*.so.* libgnarl-%{branch}.so
  ln -s libgnarl-%{branch}.so libgnarl.so
  mv -f libgnat-*.so.* %{buildroot}%{_libdir}/
  ln -s ../../../../../%{_lib}/libgnat-*.so.* libgnat-%{branch}.so
  ln -s libgnat-%{branch}.so libgnat.so
popd
%endif

# Strip debug info from libraries
STRIP_DEBUG=/bin/true
%if !%{build_debug}
if [[ "%{_enable_debug_packages}" != "1" ]]; then
  STRIP_DEBUG="strip -g"
  if [[ "%{_target_cpu}" != "%{target_cpu}" ]]; then
    STRIP_DEBUG="%{target_cpu}-linux-$STRIP_DEBUG"
  fi
fi
%endif

# Dispatch libraries to the right directories
DispatchLibs() {
	libname=$1 libversion=$2
	[[ -f ../../../../..%{target_libdir}/$libname.so.$libversion ]] && {
	$STRIP_DEBUG ../../../../..%{target_libdir}/$libname.so.$libversion
	rm -f $libname.so
	ln -s ../../../../..%{target_libdir}/$libname.so.$libversion $libname.so
	rm -f ../../../../..%{target_libdir}/$libname.so
	} || :
	[[ -f ../../../../..%{target_libdir}/$libname.a ]] && {
	$STRIP_DEBUG ../../../../..%{target_libdir}/$libname.a
	rm -f $libname.a
	cp -f ../../../../..%{target_libdir}/$libname.a $libname.a
	rm -f ../../../../..%{target_libdir}/$libname.a
	} || :
	%if %isarch %{biarches}
	[ -d 32 ] || mkdir 32
	pushd 32
	mkdir -p %{buildroot}%{_prefix}/lib
	skip32=
	[[ -z "$skip32" ]] && [[ -f ../../../../$libname.so.$libversion ]] && {
	$STRIP_DEBUG ../../../../$libname.so.$libversion
	ln -s ../../../../$libname.so.$libversion $libname.so
	rm -f ../../../../$libname.so
	[[ -f ../../../../$libname.a ]] && {
	$STRIP_DEBUG ../../../../$libname.a
	cp -f ../../../../$libname.a $libname.a
	rm -f ../../../../$libname.a
	} || :
	} || :
	popd
	%endif
	%if %isarch %{nof_arches}
	[ -d nof ] || mkdir nof
	pushd nof
	$STRIP_DEBUG ../../../../nof/$libname.so.$libversion
	ln -s ../../../../nof/$libname.so.$libversion $libname.so
	rm -f ../../../../nof/$libname.so
	[[ -f ../../../../nof/$libname.a ]] && {
	$STRIP_DEBUG ../../../../nof/$libname.a
	cp -f ../../../../nof/$libname.a $libname.a
	rm -f ../../../../nof/$libname.a
	} || :
	popd
	%endif
}
pushd $FULLPATH
	%if %{build_libssp}
	DispatchLibs libssp		%{libssp_major}.0.0
	mv ../../../../..%{target_libdir}/libssp_nonshared.a libssp_nonshared.a
	%if %isarch %{biarches}
	mv ../../../libssp_nonshared.a 32/libssp_nonshared.a
	%endif
	%endif
        %if %{build_libgomp}
	DispatchLibs libgomp		%{libgomp_major}.0.0
        %endif
	%if %{build_libmudflap}
	DispatchLibs libmudflap		%{libmudflap_major}.0.0
	DispatchLibs libmudflapth	%{libmudflap_major}.0.0
	%endif
	%if %{build_cxx}
	DispatchLibs libstdc++	%{libstdcxx_major}.0.%{libstdcxx_minor}
	mv ../../../../..%{target_libdir}/libsupc++.a libsupc++.a
	%if %isarch %{biarches}
	mv -f ../../../libsupc++.a 32/libsupc++.a
	%endif
	%if %isarch %{nof_arches}
	mv -f ../../../nof/libsupc++.a nof/libsupc++.a
	%endif
	%endif
	# Make it less hard dependent on libstdc++ 3.4 minor changes
	%if !%{system_compiler}
	[[ -f  ../../../../..%{target_libdir}/libstdc++.so.%{libstdcxx_major} ]] &&
	ln -sf ../../../../..%{target_libdir}/libstdc++.so.%{libstdcxx_major} libstdc++.so || :
	%if %isarch %{biarches}
	[[ -f  ../../../libstdc++.so.%{libstdcxx_major} ]] &&
	ln -sf ../../../../libstdc++.so.%{libstdcxx_major} 32/libstdc++.so || :
	%endif
	%endif
	%if %{build_java}
	DispatchLibs libgcj			%{libgcj_major}.0.0
	DispatchLibs libgij			%{libgcj_major}.0.0
	DispatchLibs libgcj-tools		%{libgcj_major}.0.0
	%if %build_libgcj_bc
	# Do not dispatch libgcj_bc, libgcj_bc.so and libgcj_bc.so.1.0.0
	# are different libraries intentionally. We move it manually:
	mv ../../../../..%{target_libdir}/libgcj_bc.{so,a} .
	%endif
	%endif
	%if %{build_objc}
	DispatchLibs libobjc	%{libobjc_major}.0.0
	DispatchLibs libobjc_gc	%{libobjc_major}.0.0
	%endif
	%if %{build_fortran}
	DispatchLibs libgfortran	%{libgfortran_major}.0.0
	[[ -f ../../../libgfortranbegin.a ]] &&
	mv -f ../../../libgfortranbegin.a 32/libgfortranbegin.a || :
	%if %isarch %{nof_arches}
	[[ -f ../../../nof/libgfortranbegin.a ]] &&
	mv -f ../../../nof/libgfortranbegin.a nof/libgfortranbegin.a || :
	%endif
	%endif
popd

# Move Java headers to /usr/include/libgcj-<version>
%if %{build_java}
if [ "%{libjava_includedir}" != "%{_includedir}" ]; then
  mkdir -p %{buildroot}%{libjava_includedir}
  for dir in gcj gnu java javax org; do
    mkdir -p %{buildroot}%{libjava_includedir}/$dir
    mv %{buildroot}%{libstdcxx_includedir}/$dir/* %{buildroot}%{libjava_includedir}/$dir/
    rmdir %{buildroot}%{libstdcxx_includedir}/$dir
  done

  # include <libgcj/XXX.h> should lead to <libgcj-VERSION/XXX.h>
  ln -s %{libjava_includedir} %{buildroot}%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/libgcj

  # fix pkgconfig files
  perl -pi -e 's,^(includedir=).+,\1%{libjava_includedir},' %{buildroot}%{_prefix}/lib/pkgconfig/libgcj-%{branch}.pc
%if %isarch %{biarches}
  mkdir -p %{buildroot}%{_libdir}/pkgconfig
  perl -pe '/^libdir=/ and s,/lib,/%{target_lib},' %{buildroot}%{_prefix}/lib/pkgconfig/libgcj-%{branch}.pc > %{buildroot}%{_libdir}/pkgconfig/libgcj-%{branch}.pc
  rm %{buildroot}%{_prefix}/lib/pkgconfig/libgcj-%{branch}.pc
%endif
fi
# In java-1.5.0-gcj(-devel):
rm -rf %{buildroot}%{_bindir}/rebuild-gcj-db%{program_suffix}
rm -rf %{buildroot}%{_bindir}/aot-compile%{program_suffix}
rm -rf %{buildroot}%{_mandir}/man1/aot-compile*.1*
rm -rf %{buildroot}%{_mandir}/man1/rebuild-gcj-db*.1*
rm -f %{buildroot}%{py_puresitedir}/{aotcompile,classfile}.py
%endif

# Move libgcj.spec to compiler-specific directories
%if %{build_java}
mv %{buildroot}%{_prefix}/lib/libgcj.spec $FULLPATH/libgcj.spec
%endif

# Move <cxxabi.h> to compiler-specific directories
%if %{build_cxx}
mkdir -p $FULLPATH/include/bits/
mv %{buildroot}%{libstdcxx_includedir}/cxxabi.h $FULLPATH/include/
mv %{buildroot}%{libstdcxx_includedir}/%{gcc_target_platform}/bits/cxxabi_tweaks.h $FULLPATH/include/bits/
%endif

# Ship with biarch c++config.h headers
%if %{build_cxx}
pushd obj-%{gcc_target_platform}
cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    file_32=x file_64=x
    case $i in
      %{gcc_target_platform}/32/*) file_32=$i; file_64=$cxxconfig ;;
      %{gcc_target_platform}/64/*) file_32=$cxxconfig; file_64=$i ;;
    esac
    { [[ -f "$file_32" ]] && [[ -f "$file_64" ]]; } ||
      { echo "c++config.h dispatch error"; exit 1; }

    cat > %{buildroot}%{libstdcxx_includedir}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
`cat $file_32`
#else
`cat $file_64`
#endif
#endif
EOF
    break
  fi
done
popd
%endif

# Link gnatgcc to gcc
%if %{build_ada}
ln -sf gcc %{buildroot}%{_bindir}/gnatgcc
%endif

# Create an empty file with perms 0755
FakeAlternatives() {
  for file in ${1+"$@"}; do
    rm -f %{cross_program_prefix}$file
    touch %{cross_program_prefix}$file
    chmod 0755 %{cross_program_prefix}$file
  done
}

# Alternatives provide /lib/cpp and %{_bindir}/cpp
(cd %{buildroot}%{_bindir}; FakeAlternatives cpp)
%if !%{build_cross} && %{system_compiler}
(mkdir -p %{buildroot}/lib; cd %{buildroot}/lib; ln -sf %{_bindir}/cpp cpp)
%endif

# Alternatives provide /usr/bin/c++
%if %{build_cxx}
(cd %{buildroot}%{_bindir}; FakeAlternatives c++)
%endif

if [[ -z "%{?cross_bootstrap:1}" ]] && [[ "%{libc_shared}" = "1" ]]; then
# Move libgcc_s.so* to /%{_lib}
pushd %{buildroot}%{_prefix}/%{target_lib}
  chmod 0755 libgcc_s.so.%{libgcc_major}
  mkdir -p %{buildroot}%{target_slibdir}
  mv -f  libgcc_s.so.%{libgcc_major} %{buildroot}%{target_slibdir}/libgcc_s-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s-%{version}.so.%{libgcc_major} %{buildroot}%{target_slibdir}/libgcc_s.so.%{libgcc_major}
  ln -sf %{target_slibdir}/libgcc_s.so.%{libgcc_major} %{buildroot}%{target_libdir}/libgcc_s.so
%if %isarch %{nof_arches}
  chmod 0755 nof/libgcc_s.so.%{libgcc_major}
  mkdir -p %{buildroot}%{target_slibdir}/nof
  mv -f  nof/libgcc_s.so.%{libgcc_major} %{buildroot}%{target_slibdir}/nof/libgcc_s-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s-%{version}.so.%{libgcc_major} %{buildroot}%{target_slibdir}/nof/libgcc_s.so.%{libgcc_major}
  ln -sf %{target_slibdir}/nof/libgcc_s.so.%{libgcc_major} %{buildroot}%{target_libdir}/nof/libgcc_s.so
%endif
popd
%if %isarch %{biarches}
pushd %{buildroot}%{_prefix}/lib
  chmod 0755 libgcc_s.so.%{libgcc_major}
  mkdir -p %{buildroot}/lib
  mv -f  libgcc_s.so.%{libgcc_major} %{buildroot}/lib/libgcc_s-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s-%{version}.so.%{libgcc_major} %{buildroot}/lib/libgcc_s.so.%{libgcc_major}
  ln -sf ../../lib/libgcc_s.so.%{libgcc_major} %{buildroot}%{_prefix}/lib/libgcc_s.so
  ln -sf ../../lib/libgcc_s.so.%{libgcc_major} %{buildroot}%{_prefix}/lib/libgcc_s_32.so
popd
%if %build_java
libs="libgcj libgij libgcj-tools"
%if %build_libgcj_bc
libs="$libs libgcj_bc"
%endif
for lib in $libs; do
  ln -sf ../../../%{gcc32_target_platform}/%{version}/$lib.a  $FULLPATH/32/$lib.a
  ln -sf ../../../%{gcc32_target_platform}/%{version}/$lib.so $FULLPATH/32/$lib.so
done
%endif
%endif
fi

# Create c89 and c99 wrappers
%if %{system_compiler}
cat > %{buildroot}%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec %{_bindir}/gcc-%{version} $fl ${1+"$@"}
EOF
cat > %{buildroot}%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec %{_bindir}/gcc-%{version} $fl ${1+"$@"}
EOF
chmod 755 %{buildroot}%{_prefix}/bin/c?9
%endif

# FIXME: cpp, gcov manpages names
pushd %{buildroot}%{_mandir}/man1;
  if [[ -n "%{program_prefix}%{program_suffix}" ]]; then
    for f in gcov cpp gcc g++ gfortran gpc; do
      [[ -f "$f.1" ]] && mv $f.1 %{program_prefix}$f%{program_suffix}.1 || :
    done
  fi
popd

# Fix info pages
if [[ "%{name}" = "gcc%{branch}" ]]; then
  pushd %{buildroot}%{_infodir}/
  for f in cpp cppinternals gcc gpc gpcs gfortran gnat-style gnat_rm gnat_ugn gcj; do
    if [[ -f "$f.info" ]]; then
      perl -pe "/^START-INFO-DIR-ENTRY/ .. /^END-INFO-DIR-ENTRY/ and s/($f)/\${1}-%{branch}/ig" $f.info > ${f}-%{branch}.info
      rm -f $f.info
    fi
  done
  popd
fi

# Sanitize rpath
for bin in %{buildroot}%{_bindir}/* $FULLPATH/*.so $FULLPATH/ecj1; do
  if [[ ! -f $bin ]]; then
    continue
  fi
  oldrpath=$(chrpath -l $bin | awk -F= '{ print $2 }')
  newrpath=
  for rpathdir in ${oldrpath//:/ }; do
    rpathdir=${rpathdir/lib\/..\/lib64/lib64}
    [[ "$rpathdir" != "%{_libdir}" ]] || continue
    newrpath=$newrpath:$rpathdir
  done
  newrpath=${newrpath#:}
  [[ "$newrpath" != "$oldrpath" ]] || continue
  if [[ "$newrpath" == "" ]]; then
    chrpath -d $bin
  else
    chrpath -r $newrpath $bin
  fi
done

%if %{system_compiler}
%define find_lang /usr/lib/rpm/find-lang.sh %buildroot
%find_lang %{name}
%find_lang cpplib
%if %{build_cxx}
%find_lang libstdc++
%endif
%else
touch %{name}.lang cpplib.lang libstdc++.lang
%endif

# Remove unpackaged files
rm  -f %{buildroot}%{_bindir}/jar
rm  -f %{buildroot}%{_bindir}/addr2name.awk
rm -rf %{buildroot}%{_prefix}/doc
rm -rf %{buildroot}%{_mandir}/man7
rm  -f %{buildroot}%{_libdir}/*.la
rm  -f %{buildroot}%{gcj_libdir}/*.la
rm  -f %{buildroot}%{_prefix}/lib*/libiberty.a
rm  -f %{buildroot}%{target_libdir}/libiberty.a
%if %isarch %{biarches}
rm  -f %{buildroot}%{_prefix}/lib/*.la
rm  -f %{buildroot}%{_prefix}/lib/32/libiberty.a
%endif
rm -rf %{buildroot}%{gcc_libdir}/%{gcc_target_platform}/%{version}/install-tools
%ifarch %{spu_arches}
rm -rf %{buildroot}%{_prefix}/lib/gcc/spu/%{version}/install-tools
rm  -f %{buildroot}%{spu_prefix}/lib/*.la
%endif
%if !%{build_doc}
rm -fr %{buildroot}/%{_datadir}/info/
%endif

%if %{build_cross}
rm %{buildroot}%{_mandir}/man1/%{program_prefix}gcov%{program_suffix}.1*
rm %{buildroot}%{_bindir}/%{program_prefix}gcov%{program_suffix}
%endif


%if !%system_compiler && !%build_cross && %libc_shared
rm %{buildroot}%{target_slibdir}/libgcc_s-%{version}.so.%{libgcc_major}
rm %{buildroot}%{target_slibdir}/libgcc_s.so.%{libgcc_major}
rm %{buildroot}%{target_libdir}/libgcc_s.so
%if %isarch %{biarches}
rm %{buildroot}%{target_slibdir32}/libgcc_s-%{version}.so.%{libgcc_major}
rm %{buildroot}%{target_slibdir32}/libgcc_s.so.%{libgcc_major}
rm %{buildroot}%{target_libdir}/../lib/libgcc_s.so
rm %{buildroot}%{target_libdir}/../lib/libgcc_s_32.so
%endif
%endif

# limits.h and syslimits.h are needed in includedir
mv %{buildroot}%{gcc_libdir}/%{gcc_target_platform}/%{version}/include-fixed/{sys,}limits.h \
	%{buildroot}%{gcc_libdir}/%{gcc_target_platform}/%{version}/include
rm -r %{buildroot}%{gcc_libdir}/%{gcc_target_platform}/%{version}/include-fixed

%if %build_libgcj_bc && !%system_compiler
# moved away, otherwise conflicts with system compiler libgcj
mkdir -p %{buildroot}%{target_libdir}/gcj_bc-%{libgcj_major}
mv %{buildroot}%{target_libdir}/libgcj_bc.so.%{libgcj_bc_major}.0.0 %{buildroot}%{target_libdir}/gcj_bc-%{libgcj_major}
mv %{buildroot}%{target_libdir}/libgcj_bc.so.%{libgcj_bc_major} %{buildroot}%{target_libdir}/gcj_bc-%{libgcj_major}
%endif

%if %build_java
# Handled by jpackage-utils, see #23693
rm  -f %{buildroot}%{target_libdir}/security/classpath.security
rm  -f %{buildroot}%{target_libdir}/logging.properties
%endif

%if %build_java && !%build_libffi
rm %{buildroot}%{target_libdir}/libffi.*
%if %isarch %biarches
rm %{buildroot}%{target_libdir}/../lib/libffi.*
%endif
%endif

%if !%{system_compiler}
rm -f %{buildroot}%{_infodir}/gccinstall.info*
rm -f %{buildroot}%{_infodir}/gccint.info*
rm -rf %{buildroot}%{_datadir}/locale
%endif
rm -f %{buildroot}%{_infodir}/cp-tools.info

# In case we are cross-compiling, don't bother to remake symlinks and
# don't let spec-helper when stripping files either
%if %build_cross
export DONT_SYMLINK_LIBS=1
export DONT_STRIP=1
%endif

%if %{build_debug}
# Don't strip in debug mode
export DONT_STRIP=1
%endif

%if %{build_ada}
# gnatmake bash completion
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/bash_completion.d/gnatmake
%endif

%if %{build_java}
mkdir -p %{buildroot}%{_datadir}/java/gcj-endorsed \
         %{buildroot}%{gcj_libdir}/classmap.db.d
chmod 755 %{buildroot}%{_datadir}/java/gcj-endorsed \
          %{buildroot}%{gcj_libdir} \
          %{buildroot}%{gcj_libdir}/classmap.db.d
touch %{buildroot}%{gcj_libdir}/classmap.db

# check if gcj-dbtool hasn't been incorrectly relinked.  rh#165781
classmap_db=`LD_LIBRARY_PATH=%{buildroot}%{_libdir}:%{buildroot}/%{_lib} \
             %{buildroot}%{_bindir}/gcj-dbtool%{program_suffix} -p`
case "$classmap_db" in
  # XXX: grmpf, make sure it's at a unique location!?
  %{gcj_libdir}/classmap.db) ;;
  %{_prefix}/lib/../%{_lib}/gcj-%{version}-%{libgcj_major}/classmap.db) ;;
  *) echo Unexpected gcj-dbtool%{program_suffix} -p output; exit 1 ;;
esac
%endif

%clean
rm -rf %{buildroot}

%post
/usr/sbin/update-alternatives --install %{_bindir}/%{cross_program_prefix}gcc %{cross_program_prefix}gcc %{_bindir}/%{program_prefix}gcc-%{version} %{alternative_priority}
[ -e %{_bindir}/%{cross_program_prefix}gcc ] || /usr/sbin/update-alternatives --auto %{cross_program_prefix}gcc

%postun
if [ ! -f %{_bindir}/%{cross_program_prefix}gcc-%{version} ]; then
  /usr/sbin/update-alternatives --remove %{cross_program_prefix}gcc %{_bindir}/%{program_prefix}gcc-%{version}
fi

%if %{build_cxx}
%post c++
/usr/sbin/update-alternatives --install %{_bindir}/%{cross_program_prefix}g++ %{cross_program_prefix}g++ %{_bindir}/%{program_prefix}g++-%{version} %{alternative_priority} --slave %{_bindir}/%{cross_program_prefix}c++ %{cross_program_prefix}c++ %{_bindir}/%{program_prefix}g++-%{version}
[ -e %{_bindir}/%{cross_program_prefix}g++ ] || /usr/sbin/update-alternatives --auto %{cross_program_prefix}g++

%postun c++
if [ ! -f %{_bindir}/%{cross_program_prefix}g++-%{version} ]; then
  /usr/sbin/update-alternatives --remove %{cross_program_prefix}g++ %{_bindir}/%{program_prefix}g++-%{version}
fi
%endif

%if %{build_libstdcxx}
%if %mdkversion < 200900
%post -n %{libstdcxx_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libstdcxx_name} -p /sbin/ldconfig
%endif
%endif

%if %mdkversion < 200900
%post -n %{libgcc_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libgcc_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libmudflap_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libmudflap_name} -p /sbin/ldconfig
%endif

%if %{build_libssp}
%if %mdkversion < 200900
%post -n %{libssp_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libssp_name} -p /sbin/ldconfig
%endif
%endif

%if %mdkversion < 200900
%post -n %{libgomp_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libgomp_name} -p /sbin/ldconfig
%endif

%post cpp
/usr/sbin/update-alternatives --install %{_bindir}/%{cross_program_prefix}cpp %{cross_program_prefix}cpp %{_bindir}/%{program_prefix}cpp-%{version} %{alternative_priority} --slave /lib/%{cross_program_prefix}cpp %{cross_program_prefix}lib_cpp %{_bindir}/%{program_prefix}cpp-%{version}
[ -e %{_bindir}/%{cross_program_prefix}cpp ] || /usr/sbin/update-alternatives --auto %{cross_program_prefix}cpp

%postun cpp
if [ ! -f %{_bindir}/%{cross_program_prefix}cpp-%{version} ]; then
  /usr/sbin/update-alternatives --remove %{cross_program_prefix}cpp %{_bindir}/%{program_prefix}cpp-%{version}
fi

%if %{build_java}
%if %mdkversion < 200900
%post -n %{libgcj_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libgcj_name} -p /sbin/ldconfig
%endif
%endif

%if %{build_objc}
%if %mdkversion < 200900
%post -n %{libobjc_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libobjc_name} -p /sbin/ldconfig
%endif
%endif

%if %{build_fortran}
%if %mdkversion < 200900
%post -n %{libgfortran_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libgfortran_name} -p /sbin/ldconfig
%endif
%endif

%if %{build_ada}
%if %mdkversion < 200900
%post -n %{libgnat_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libgnat_name} -p /sbin/ldconfig
%endif
%endif

%post doc
%_install_info gcc%{_package_suffix}.info
%_install_info cpp%{_package_suffix}.info
%if %{build_pascal}
%_install_info gpc%{_package_suffix}.info
%_install_info gpcs%{_package_suffix}.info
%endif
%if %{build_fortran}
%_install_info gfortran%{_package_suffix}.info
%endif
%if %{build_ada}
%_install_info gnat-style%{_package_suffix}.info
%_install_info gnat_rm%{_package_suffix}.info
%_install_info gnat_ugn%{_package_suffix}.info
%endif
%if %{build_java}
%_install_info gcj%{_package_suffix}_ug.info
%endif

%preun doc
if [ "$1" = "0" ];then /sbin/install-info %{_infodir}/gcc%{_package_suffix}.info.bz2 --dir=%{_infodir}/dir --remove;fi;
%_remove_install_info cpp%{_package_suffix}.info
%if %{build_pascal}
%_remove_install_info gpc%{_package_suffix}.info
%_remove_install_info gpcs%{_package_suffix}.info
%endif
%if %{build_fortran}
%_remove_install_info gfortran%{_package_suffix}.info
%endif
%if %{build_ada}
%_remove_install_info gnat-style%{_package_suffix}.info
%_remove_install_info gnat_rm%{_package_suffix}.info
%_remove_install_info gnat_ugn%{_package_suffix}.info
%endif
%if %{build_java}
%_remove_install_info gcj%{_package_suffix}.info
%endif

%files -f %{name}.lang
%defattr(-,root,root)
#
%doc gcc/README*
%{_mandir}/man1/%{program_prefix}gcc%{program_suffix}.1*
%if "%{name}" == "gcc%{package_suffix}"
%{_mandir}/man1/gcov%{program_suffix}.1*
%endif
#
%{_bindir}/%{program_prefix}gcc%{branch}-version
%{_bindir}/%{program_prefix}gcc%{program_long_suffix}
%{_bindir}/%{gcc_target_platform}-gcc%{program_suffix}
%{_bindir}/%{gcc_target_platform}-gcc-%{version}
%{_bindir}/%{program_prefix}gccbug%{program_suffix}
%if "%{name}" == "gcc%{package_suffix}"
%{_bindir}/protoize%{program_suffix}
%{_bindir}/unprotoize%{program_suffix}
%{_bindir}/gcov%{program_suffix}
%endif
%if %{system_compiler}
%{_bindir}/cc
%{_bindir}/c89
%{_bindir}/c99
%endif
#
%if %{libc_shared} && %{build_cross} || %{system_compiler}
%if !%{build_cross_bootstrap}
%{target_libdir}/libgcc_s.so
%endif
%if "%{name}" == "gcc%{package_suffix}"
%if %isarch %{nof_arches}
%{_libdir}/nof/libgcc_s.so
%endif
%if %isarch %{biarches}
%{_prefix}/lib/libgcc_s.so
%{_prefix}/lib/libgcc_s_32.so
%endif
%endif
%endif
#
%dir %{gcc_libdir}/%{gcc_target_platform}
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}
#
%{gcc_libdir}/%{gcc_target_platform}/%{version}/collect2
%{gcc_libdir}/%{gcc_target_platform}/%{version}/crt*.o
%if %isarch ppc ppc64
%{gcc_libdir}/%{gcc_target_platform}/%{version}/ecrt*.o
%{gcc_libdir}/%{gcc_target_platform}/%{version}/ncrt*.o
%endif
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcc.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcov.a
%if !%{build_cross_bootstrap}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcc_eh.a
%endif
%if "%{name}" == "gcc%{package_suffix}"
%{gcc_libdir}/%{gcc_target_platform}/%{version}/SYSCALLS.c.X
%if %isarch %{biarches}
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}/32
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/crt*.o
%if %isarch ppc64
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/ecrt*.o
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/ncrt*.o
%endif
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcc.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcc_eh.a
%endif
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcov.a
%endif
%if %isarch %{nof_arches}
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}/nof
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/crt*.o
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/ecrt*.o
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libgcc.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libgcc_eh.a
%endif
%endif
%endif
#
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}/include
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/float.h
%if %isarch %{ix86} x86_64
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/ammintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/nmmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/smmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/mm3dnow.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/mm_malloc.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/mmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/xmmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/pmmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/emmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/tmmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/avxintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/immintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/wmmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/x86intrin.h
%endif
%if %isarch ppc ppc64
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/spe.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/altivec.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/ppc-asm.h
%endif
%if %isarch spu
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/vmx2spu.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/spu_intrinsics.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/spu_internals.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/spu_mfcio.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/vec_types.h
%endif
%if %isarch ia64
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/ia64intrin.h
%endif
%if %isarch m68k
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/math-68881.h
%endif
%if %isarch armel armeb
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/mmintrin.h
%endif
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/iso646.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/limits.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/stdarg.h
%if %isarch %{ix86} x86_64
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/cross-stdarg.h
%endif
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/stdbool.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/stddef.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/syslimits.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/unwind.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/varargs.h
%if %isarch i386 x86_64
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/bmmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/cpuid.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/mmintrin-common.h
%endif
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/stdfix.h

%if !%build_libffi && %build_java
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/ffi*.h
%endif

%if "%{name}" == "%{cross_prefix}gcc" && %{libc_shared}
%if !%{build_monolithic}
%files -n %{libgcc_name}
%endif
%defattr(-,root,root)
%{target_slibdir}/libgcc_s-%{version}.so.%{libgcc_major}
%{target_slibdir}/libgcc_s.so.%{libgcc_major}
%if %isarch %{biarches}
%{target_slibdir32}/libgcc_s-%{version}.so.%{libgcc_major}
%{target_slibdir32}/libgcc_s.so.%{libgcc_major}
%{_prefix}/lib/libgcc_s.so.%{libgcc_major}
%endif
%if %isarch %{nof_arches}
%{target_slibdir}/nof/libgcc_s-%{version}.so.%{libgcc_major}
%{target_slibdir}/nof/libgcc_s.so.%{libgcc_major}
%endif
%endif

%if %{build_libssp} && %{libc_shared}
%if !%{build_monolithic}
%files -n %{libssp_name}
%endif
%defattr(-,root,root)
%{target_libdir}/libssp.so.%{libssp_major}
%{target_libdir}/libssp.so.%{libssp_major}.0.0
%if %isarch %{biarches}
%{_prefix}/lib/libssp.so.%{libssp_major}
%{_prefix}/lib/libssp.so.%{libssp_major}.0.0
%endif
%endif

%if %{build_libssp}
%if !%{build_monolithic}
%files -n %{libssp_name_orig}-devel
%endif
%defattr(-,root,root)
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}/include/ssp
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/ssp/*.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libssp.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libssp_nonshared.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libssp.so
%endif
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libssp.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libssp_nonshared.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libssp.so
%endif
%endif
%endif

%if %{build_libmudflap} && %{libc_shared}
%if !%{build_monolithic}
%files -n %{libmudflap_name}
%endif
%defattr(-,root,root)
#
%{target_libdir}/libmudflap.so.%{libmudflap_major}
%{target_libdir}/libmudflap.so.%{libmudflap_major}.0.0
%{target_libdir}/libmudflapth.so.%{libmudflap_major}
%{target_libdir}/libmudflapth.so.%{libmudflap_major}.0.0
%if %isarch %{biarches}
%{_prefix}/lib/libmudflap.so.%{libmudflap_major}
%{_prefix}/lib/libmudflap.so.%{libmudflap_major}.0.0
%{_prefix}/lib/libmudflapth.so.%{libmudflap_major}
%{_prefix}/lib/libmudflapth.so.%{libmudflap_major}.0.0
%endif
%endif

%if %{build_libmudflap}
%if !%{build_monolithic}
%files -n %{libmudflap_name_orig}-devel
%endif
%defattr(-,root,root)
#
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/mf-runtime.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libmudflap.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libmudflapth.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libmudflap.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libmudflapth.so
%endif
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libmudflap.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libmudflapth.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libmudflap.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libmudflapth.so
%endif
%endif
%endif

%if %{build_libgomp}
%files -n %{libgomp_name}
%{target_libdir}/libgomp.so.%{libgomp_major}
%{target_libdir}/libgomp.so.%{libgomp_major}.0.0
%if %isarch %{biarches}
%{_prefix}/lib/libgomp.so.%{libgomp_major}
%{_prefix}/lib/libgomp.so.%{libgomp_major}.0.0
%endif

%files -n %{libgomp_name_orig}-devel
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgomp.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgomp.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/omp.h
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgomp.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgomp.so
%endif
%{target_libdir}/libgomp.spec
%if %isarch %{biarches}
%{_prefix}/lib/libgomp.spec
%endif
%endif

%files cpp -f cpplib.lang
%defattr(-,root,root)
#
%{_mandir}/man1/%{program_prefix}cpp%{program_suffix}.1*
#
%if %{build_cross} && !%{build_cross_bootstrap}|| %{system_compiler}
/lib/%{cross_program_prefix}cpp
%endif
%ghost %{_bindir}/%{cross_program_prefix}cpp
%{_bindir}/%{program_prefix}cpp%{program_long_suffix}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/cc1

%if %{build_cxx}
%files c++ -f libstdc++.lang
%defattr(-,root,root)
#
%{_mandir}/man1/%{program_prefix}g++%{program_suffix}.1*
#
%ghost %{_bindir}/%{cross_program_prefix}c++
%{_bindir}/%{program_prefix}g++%{program_long_suffix}
%{_bindir}/%{program_prefix}c++%{program_long_suffix}
%{_bindir}/%{gcc_target_platform}-g++%{program_suffix}
%{_bindir}/%{gcc_target_platform}-c++%{program_suffix}
#
%{gcc_libdir}/%{gcc_target_platform}/%{version}/cc1plus
# symlinks to gcc3.4 stuff
%if !%{system_compiler}
#
%if %{build_stdcxxheaders}
%dir %{target_prefix}/include/c++
%{libstdcxx_includedir}
%endif
#
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/cxxabi.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/bits
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libstdc++.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libsupc++.a
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libstdc++.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libsupc++.a
%endif
%endif
%endif

%if %{build_libstdcxx} && %{libc_shared}
%if !%{build_monolithic}
%files -n %{libstdcxx_name}
%endif
%defattr(-,root,root)
%{target_libdir}/libstdc++.so.%{libstdcxx_major}
%{target_libdir}/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%if %isarch %{biarches}
%{_prefix}/lib/libstdc++.so.%{libstdcxx_major}
%{_prefix}/lib/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%endif
%if %isarch %{nof_arches}
%dir %{_libdir}/nof
%{_libdir}/nof/libstdc++.so.%{libstdcxx_major}
%{_libdir}/nof/libstdc++.so.%{libstdcxx_major}.0.%{libstdcxx_minor}
%endif
%endif

%if %{build_libstdcxx}
%if !%{build_monolithic}
%files -n %{libstdcxx_name_orig}-devel
%endif
%defattr(-,root,root)
#
%doc libstdc++-v3/README*
#
%dir %{libstdcxx_includedir}
%{libstdcxx_includedir}/*
%ifarch %{spu_arches}
%exclude %dir %{libstdcxx_includedir}/spu
%exclude %dir %{libstdcxx_includedir}/spu/bits
%exclude %{libstdcxx_includedir}/spu/bits/*
%endif
%if %{system_compiler}
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}/include
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/cxxabi.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/bits
%endif
#
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libsupc++.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libstdc++.so
%endif
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libsupc++.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libstdc++.so
%endif
%endif
%if %isarch %{nof_arches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libsupc++.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libstdc++.so
%endif
%endif
%endif

%if %{build_libstdcxx}
%if !%{build_monolithic}
%files -n %{libstdcxx_name_orig}-static-devel
%endif
%defattr(-,root,root)
%doc libstdc++-v3/README
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libstdc++.a
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libstdc++.a
%endif
%if %isarch %{nof_arches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libstdc++.a
%endif
%endif

%if %{build_objc}
%files objc
%defattr(-,root,root)
#
%doc rpm.doc/objc/*
#
%{gcc_libdir}/%{gcc_target_platform}/%{version}/cc1obj
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libobjc.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libobjc_gc.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libobjc.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libobjc_gc.so
%endif
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libobjc.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libobjc_gc.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libobjc.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libobjc_gc.so
%endif
%endif
%if %isarch %{nof_arches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libobjc.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libobjc_gc.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libobjc.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libobjc_gc.so
%endif
%endif
#
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}/include/objc
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/objc/*.h
%endif

%if %{build_objc} && %{libc_shared}
%if !%{build_monolithic}
%files -n %{libobjc_name}
%endif
%defattr(-,root,root)
#
%doc rpm.doc/libobjc/*
%doc libobjc/THREADS* libobjc/ChangeLog
#
%{target_libdir}/libobjc.so.%{libobjc_major}
%{target_libdir}/libobjc.so.%{libobjc_major}.0.0
%{target_libdir}/libobjc_gc.so.%{libobjc_major}
%{target_libdir}/libobjc_gc.so.%{libobjc_major}.0.0
%if %isarch %{biarches}
%{_prefix}/lib/libobjc.so.%{libobjc_major}
%{_prefix}/lib/libobjc.so.%{libobjc_major}.0.0
%{_prefix}/lib/libobjc_gc.so.%{libobjc_major}
%{_prefix}/lib/libobjc_gc.so.%{libobjc_major}.0.0
%endif
%endif

%if %{build_objcp}
%files objc++
%defattr(-,root,root)
%doc rpm.doc/objcp/*
%{gcc_libdir}/%{gcc_target_platform}/%{version}/cc1objplus
%endif

%if %{build_pascal}
%files gpc
%defattr(-,root,root)
#
%doc rpm.doc/gpc/*
%{_mandir}/man1/%{program_prefix}gpc%{program_suffix}.1*
%{_mandir}/man1/%{program_prefix}/gpc-run%{program_suffix}.1*
#
%{_bindir}/gpc-run
%{_bindir}/binobj
%{_bindir}/%{program_prefix}gpc%{program_suffix}
%{_bindir}/%{program_prefix}gpidump%{program_suffix}
#
%{gcc_libdir}/%{gcc_target_platform}/%{version}/gpc1
%{gcc_libdir}/%{gcc_target_platform}/%{version}/gpcpp
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgpc.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/gpc-in-c.h
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}/units
%{gcc_libdir}/%{gcc_target_platform}/%{version}/units/*.c
%{gcc_libdir}/%{gcc_target_platform}/%{version}/units/*.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/units/*.s
%{gcc_libdir}/%{gcc_target_platform}/%{version}/units/*.inc
%{gcc_libdir}/%{gcc_target_platform}/%{version}/units/*.pas
%endif

%if %{build_fortran}
%files gfortran
%defattr(-,root,root)
#
%doc rpm.doc/gfortran/*
%{_mandir}/man1/%{program_prefix}gfortran%{program_suffix}.1*
#
%{_bindir}/%{program_prefix}gfortran%{program_suffix}
%{_bindir}/%{gcc_target_platform}-gfortran%{program_suffix}
#
%{gcc_libdir}/%{gcc_target_platform}/%{version}/f951
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgfortranbegin.la
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgfortranbegin.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgfortran.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgfortran.so
%endif
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgfortranbegin.la
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgfortranbegin.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgfortran.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgfortran.so
%endif
%endif
%if %isarch %{nof_arches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libgfortran.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libgfortran.so
%endif
%endif
%{gcc_libdir}/%{gcc_target_platform}/%{version}/finclude/omp*
%endif

%if %{build_fortran} && %{libc_shared}
%if !%{build_monolithic}
%files -n %{libgfortran_name}
%endif
%defattr(-,root,root)
#
%{target_libdir}/libgfortran.so.%{libgfortran_major}
%{target_libdir}/libgfortran.so.%{libgfortran_major}.0.0
%if %isarch %{biarches}
%{_prefix}/lib/libgfortran.so.%{libgfortran_major}
%{_prefix}/lib/libgfortran.so.%{libgfortran_major}.0.0
%endif
%endif

%if %{build_java}
%files java
%defattr(-,root,root)
%doc gcc/java/ChangeLog*
%{_bindir}/gcj%{program_suffix}
%{_bindir}/%{gcc_target_platform}-gcj
%{gcc_libdir}/%{gcc_target_platform}/%{version}/ecj1
%{gcc_libdir}/%{gcc_target_platform}/%{version}/jc1
%{gcc_libdir}/%{gcc_target_platform}/%{version}/jvgenmain
%{_mandir}/man1/%{program_prefix}gcj%{program_suffix}.1*
%endif

%if %{build_java}
%files -n %{GCJ_TOOLS}
%defattr(-,root,root)
%{_bindir}/gij%{program_suffix}
%{_bindir}/grmic%{program_suffix}
%{_bindir}/grmiregistry%{program_suffix}
%{_bindir}/gappletviewer%{program_suffix}
%{_bindir}/gc-analyze%{program_suffix}
%{_bindir}/gjar%{program_suffix}
%{_bindir}/gjarsigner%{program_suffix}
%{_bindir}/gjavah%{program_suffix}
%{_bindir}/gkeytool%{program_suffix}
%{_bindir}/gnative2ascii%{program_suffix}
%{_bindir}/gorbd%{program_suffix}
%{_bindir}/grmid%{program_suffix}
%{_bindir}/gserialver%{program_suffix}
%{_bindir}/gtnameserv%{program_suffix}
%{_bindir}/gcj-dbtool%{program_suffix}
%{_bindir}/gcjh%{program_suffix}
%{_bindir}/%{gcc_target_platform}-gcjh
%{_bindir}/jcf-dump%{program_suffix}

#
%{_mandir}/man1/gij*.1*
%{_mandir}/man1/gcjh*.1*
%{_mandir}/man1/grmic*.1*
%{_mandir}/man1/grmiregistry*.1*
%{_mandir}/man1/gcj-dbtool*.1*
%{_mandir}/man1/jcf-dump*.1*
%{_mandir}/man1/gappletviewer*.1*
%{_mandir}/man1/gc-analyze*.1*
%{_mandir}/man1/gjar*.1*
%{_mandir}/man1/gjavah*.1*
%{_mandir}/man1/gjdoc*.1*
%{_mandir}/man1/gkeytool*.1*
%{_mandir}/man1/gnative2ascii*.1*
%{_mandir}/man1/gorbd*.1*
%{_mandir}/man1/grmid*.1*
%{_mandir}/man1/gserialver*.1*
%{_mandir}/man1/gtnameserv*.1*
%{_mandir}/man1/jv-convert*.1*
%endif

%if %{build_java}
%files -n %{libgcj_name}
%defattr(-,root,root)
%{target_libdir}/libgcj.so.%{libgcj_major}
%{target_libdir}/libgcj.so.%{libgcj_major}.0.0
%{target_libdir}/libgij.so.%{libgcj_major}
%{target_libdir}/libgij.so.%{libgcj_major}.0.0
%{target_libdir}/libgcj-tools.so.%{libgcj_major}
%{target_libdir}/libgcj-tools.so.%{libgcj_major}.0.0
%dir %{gcj_libdir}
%{gcj_libdir}/libgjsmalsa.so
%{gcj_libdir}/libgjsmdssi.so
%{gcj_libdir}/libgtkpeer.so
%{gcj_libdir}/libjavamath.so
%{gcj_libdir}/libjawt.so
%{gcj_libdir}/libjvm.so
#
%if %build_libgcj_bc && !%system_compiler
%{target_libdir}/gcj_bc-%{libgcj_major}
%endif
#
%dir %{gcj_libdir}/classmap.db.d
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{gcj_libdir}/classmap.db
%endif

%if %{build_java}
%files -n %{libgcj_name_base}-base
%defattr(-,root,root)
%dir %{_datadir}/java
%dir %{_datadir}/java/gcj-endorsed
%{_datadir}/java/libgcj-%{version}.jar
%{_datadir}/java/libgcj-tools-%{version}.jar
%endif

%if %{build_java}
%files -n %{libgcj_devel_name}
%defattr(-,root,root)
#
%doc rpm.doc/boehm-gc/*
%doc rpm.doc/libjava/*
#
%{_bindir}/jv-convert%{program_suffix}
%{_mandir}/man1/jv-convert%{program_suffix}.1*
#
%{_libdir}/pkgconfig/libgcj*.pc
#
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}/include
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/gcj
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/libgcj
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/jni.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/jni_md.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/jvmpi.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/jawt.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/jawt_md.h
#
%dir %{libjava_includedir}
%dir %{libjava_includedir}/gcj
%{libjava_includedir}/gcj/*.h
%dir %{libjava_includedir}/gnu
%{libjava_includedir}/gnu/*
%dir %{libjava_includedir}/java
%{libjava_includedir}/java/*
%dir %{libjava_includedir}/javax
%{libjava_includedir}/javax/*
%dir %{libjava_includedir}/org
%{libjava_includedir}/org/*
#
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcj.spec
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcj.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgij.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcj-tools.so
%if %build_libgcj_bc
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcj_bc.so
%endif
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcj.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgij.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcj-tools.so
%if %build_libgcj_bc
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcj_bc.so
%endif
%endif
%if %isarch %{nof_arches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libgcj.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libgij.so
%endif
%endif

%if %{build_java}
%files -n %{libgcj_static_devel_name}
%defattr(-,root,root)
%doc libjava/README libjava/LIBGCJ_LICENSE
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcj.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgij.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcj-tools.a
%if %build_libgcj_bc
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcj_bc.a
%endif
%{gcj_libdir}/libjvm.a
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcj.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgij.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcj-tools.a
%if %build_libgcj_bc
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcj_bc.a
%endif
%endif
%if %isarch %{nof_arches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libgcj.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libgij.a
%endif
%endif

%if %{build_java}
%files -n %{libgcj_name_base}-src
%defattr(-,root,root)
%dir %{_datadir}/java
%{_datadir}/java/src*.zip
%endif

%if %{build_java} && %{system_compiler}
%files -n %{libgcj_bc_name}
%defattr(-,root,root)
%{target_libdir}/libgcj_bc.so.%{libgcj_bc_major}
%{target_libdir}/libgcj_bc.so.%{libgcj_bc_major}.0.0
%endif

%if %{build_ada}
%files gnat
%defattr(-,root,root)
#
%{_bindir}/gnat*
%config(noreplace) %{_sysconfdir}/bash_completion.d/gnatmake
#
%{gcc_libdir}/%{gcc_target_platform}/%{version}/gnat1
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}/adainclude
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adainclude/*.adb
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adainclude/*.ads
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}/adalib
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adalib/*.ali
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adalib/g-trasym.o
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adalib/libgccprefix.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adalib/libgmem.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adalib/libgnala.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adalib/libgnat.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adalib/libgnarl.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adalib/libgnat.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adalib/libgnat-%{branch}.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adalib/libgnarl.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/adalib/libgnarl-%{branch}.so
%endif
%endif

%if %{build_libffi}
%files -n %{libffi_name}
%defattr(-,root,root)
%{target_libdir}/libffi.so.%{libffi_major}
%{target_libdir}/libffi.so.%{libffi_major}.0.1
%if %isarch %{biarches}
%{_prefix}/lib/libffi.so.%{libffi_major}
%{_prefix}/lib/libffi.so.%{libffi_major}.0.1
%endif

%files -n %{libffi_name}-devel
%defattr(-,root,root)
%doc libffi/README libffi/LICENSE libffi/ChangeLog*
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}
%dir %{gcc_libdir}/%{gcc_target_platform}/%{version}/include
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/ffi*.h
%{_libdir}/libffi.a
%{_libdir}/libffi.so
%if %isarch %{biarches}
%{_prefix}/lib/libffi.a
%{_prefix}/lib/libffi.so
%endif
%endif

%if %{build_ada} && %{libc_shared}
%files -n %{libgnat_name}
%defattr(-,root,root)
#
%{target_libdir}/libgnat-*.so.*
%{target_libdir}/libgnarl-*.so.*
%endif

%ifarch %{spu_arches}
%files -n spu-gcc
%defattr(-,root,root)
%{_bindir}/%{spu_program_prefix}cpp
%{_bindir}/%{spu_program_prefix}gcc
%dir %{gcc_libdir}/spu/%{version}
%{gcc_libdir}/spu/%{version}/cc1
%{gcc_libdir}/spu/%{version}/collect2
%{gcc_libdir}/spu/%{version}/*.o
%{gcc_libdir}/spu/%{version}/*.a
%dir %{gcc_libdir}/spu/%{version}/include
%{gcc_libdir}/spu/%{version}/include/*.h
%{_mandir}/man1/%{spu_program_prefix}cpp.1*
%{_mandir}/man1/%{spu_program_prefix}gcc.1*

%files -n spu-gcc-c++
%defattr(-,root,root)
%{_bindir}/%{spu_program_prefix}c++
%{_bindir}/%{spu_program_prefix}g++
%{spu_prefix}/lib/libsupc++.a
%{spu_prefix}/lib/libstdc++.a
%{gcc_libdir}/spu/%{version}/cc1plus
%dir %{libstdcxx_includedir}/spu
%dir %{libstdcxx_includedir}/spu/bits
%{libstdcxx_includedir}/spu/bits/*
%{_mandir}/man1/%{spu_program_prefix}g++.1*
%endif

%if %{build_doc}
%files doc
%doc gcc/*ChangeLog*
%doc libstdc++-v3/doc/html/
%defattr(-,root,root)
%if %{build_check}
%doc test_summary.log
%endif
%{_infodir}/cppinternals%{_package_suffix}.info*
%{_infodir}/cpp%{_package_suffix}.info*
%{_infodir}/gcc%{_package_suffix}.info*
%{_infodir}/gccinstall%{_package_suffix}.info*
%{_infodir}/gccint%{_package_suffix}.info*
%if %{build_libstdcxx}
%doc rpm.doc/libstdc++/
%endif
%if %{build_cxx}
%doc rpm.doc/c++
%endif
%if %{build_libgomp}
%{_infodir}/libgomp%{_package_suffix}.info*
%endif
%if %{build_ada}
%{_infodir}/gnat-style%{_package_suffix}.info*
%{_infodir}/gnat_rm%{_package_suffix}.info*
%{_infodir}/gnat_ugn%{_package_suffix}.info*
%endif
%if %{build_java}
%{_infodir}/gcj%{_package_suffix}.info*
%endif
%if %{build_pascal}
%{_infodir}/gpc%{_package_suffix}.info*
%{_infodir}/gpcs%{_package_suffix}.info*
%endif
%if %{build_fortran}
%{_infodir}/gfortran%{_package_suffix}.info*
%endif
%endif

%if %{build_pdf_doc}
%files doc-pdf
%defattr(-,root,root)
%doc gcc/doc/cppinternals.pdf
%doc gcc/doc/gcc.pdf
%doc gcc/doc/cpp.pdf
%if %{build_ada}
%doc gcc/ada/gnat_rm.pdf
%doc gcc/ada/gnat_ugn.pdf
%endif
%if %{build_fortran}
%doc gcc/fortran/gfortran.pdf
%endif
%endif


