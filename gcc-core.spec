# type := core | other | full
%define type core
#define type other
#define type full

%if "%{type}" == "core"
%define _vendor Manbo
%define _host_vendor manbo
%define _real_vendor manbo
%endif

%if "%{type}" == "core"
%define base_name		gcc-core
%define include_core		1
%define include_other		0
%endif
%if "%{type}" == "other"
%define base_name		gcc-other
%define include_core		0
%define include_other		1
%endif
%if "%{type}" == "full"
%define base_name		gcc-full
%define include_core		1
%define include_other		1
%endif

%define name			%{cross_prefix}%{base_name}%{package_suffix}
%define gcc_name		%{cross_prefix}gcc%{package_suffix}
%define branch			4.2
%define branch_tag		%(perl -e 'printf "%%02d%%02d", split(/\\./,shift)' %{branch})
%define version			4.2.3
%define snapshot_version	%{branch}-20071128
%define base_release		4
%if "%{_real_vendor}" == "manbo"
%define release			%{manbo_mkrel %{base_release}}
%else
%define release			%{mkrel %{base_release}}
%endif
%define nof_arches		noarch
%define spu_arches		ppc64
%define lsb_arches		i386 x86_64 ia64 ppc ppc64 s390 s390x
%define biarches		x86_64 ppc64

# Define libraries major versions
%define libgcc_major		1
%define libstdcxx_major		6
%define libstdcxx_minor		9
%define libgfortran_major	2
%define libgcj_major		8
%define libobjc_major		2
%define libgnat_major		1
%define libffi_major		4
%define libmudflap_major	0
%define libssp_major		0
%define libgomp_major		1
%define libgcj_bc_major		1

# Package holding Java tools (gij, jv-convert, etc.)
%define GCJ_TOOLS		%{cross_prefix}gcj%{package_suffix}-tools

# libgcj-devel should not provide libgcj_bc.so.1
%define _exclude_files_from_autoprov %{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcj_bc.so

#-- JDK version
# "gcj" implements the JDK 1.4 language, "libgcj" is largely compatible with JDK 1.4
%define jdk_version	1.4.2
%define jdk_base	java-%{jdk_version}-gcj
%define jdk_package	%{jdk_base}-compat
%define jdk_home	%{_prefix}/lib/jvm/%{jdk_base}-%{jdk_version}.0/jre

#-- Alternatives for Java tools
#       Sun JDK         40
#       Kaffe           30
#       Gcj 3.2         20
%define gcj_alternative_priority 20
%define gcj_alternative_programs grmic grmiregistry

# Define if building a cross compiler
# FIXME: assume user does not define both cross and cross_bootstrap variables
%define build_cross		0
%define build_cross_bootstrap	0
%{expand: %{?cross:		%%global build_cross 1}}
%{expand: %{?cross_bootstrap:	%%global build_cross_bootstrap 1}}

# System compiler in MDV 2007
%if %{mdkversion} >= 200700
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
%else
%define alternative_priority	20%{branch_tag}
%define cross_prefix		%{nil}
%define cross_program_prefix	%{nil}
%define package_suffix		%{branch}
%define program_prefix		%{nil}
%define program_suffix		-%{version}
%endif
%endif
%define _alternativesdir	/etc/alternatives
%if "%{package_suffix}" == "%{nil}"
%define _package_suffix		%{nil}
%else
%define _package_suffix		-%{package_suffix}
%endif
%define gcc34_as_system_compiler 0
%if %{mdkversion} == 10100
%define gcc34_as_system_compiler 1
%endif
%if %{mdkversion} == 10200
%define gcc34_as_system_compiler 1
%endif
%define gcc40_as_system_compiler 0
%if %{mdkversion} == 200600
%define gcc40_as_system_compiler 1
%endif
%if !%{system_compiler}
# XXX even though it's better, we should retain the system behavior
# and let the user decide
%define gcj_alternative_priority 15
%endif

%define source_package		gcc-%{version}
%define source_dir		gcc-%{version}

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
%define gcj_libdir		%{target_libdir}/gcj-%{version}

%define target_lib             lib
%if %isarch ppc64 sparc64 x86_64
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
%define build_check		1
%define build_ada		0
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
%define build_libgomp		1
%define build_libffi		1
%define build_java		1
%define build_debug		0
%if %{gcc34_as_system_compiler}
%define build_libstdcxx		0
%endif
%if %{gcc40_as_system_compiler}
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
%endif
%if %{mdkversion} < 1010
# gcc4 java requires gtk >= 2.4
%define build_java		0
%endif
%define use_hash_style_gnu	0

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

%if %isarch spu
# spu port doesn't support the following languages yet
%define build_fortran		0
%define build_libssp		0
%define use_ssp_glibc		0
%endif

# Allow --with[out] <feature> at rpm command line build
%{expand: %{?_without_DOC:	%%global build_doc 0}}
%{expand: %{?_without_PDF:	%%global build_pdf_doc 0}}
%{expand: %{?_without_DEBUG:	%%global build_debug 0}}
%{expand: %{?_without_CHECK:	%%global build_check 0}}
%{expand: %{?_without_MINIMAL:	%%global build_minimal 0}}
%{expand: %{?_with_DOC:		%%global build_doc 1}}
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
%if "%{type}" == "core"
%define build_minimal		1
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
%define build_libgomp		0
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
%if %{mdkversion} >= 1010
%define mdk_distro_version_file	/etc/release
%else
%define mdk_distro_version_file	/etc/mandriva-release
%endif
%define mdk_distro_version	%(perl -ne '/^([.\\w\\s]+) \\(.+\\).+/ and print $1' < %{mdk_distro_version_file})

Summary:	GNU Compiler Collection
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv3+
Group:		Development/C

# Main source:	(CVS)
URL:		http://gcc.gnu.org/
Source0:	%{source_package}.tar.lzma
Source1:	lsb-headers-3.1.1.tar.bz2
Source5:	gcc35-gpc-%{gpc_snapshot}.tar.bz2
# FIXME: unless we get proper help2man package
Source6:	gcc35-help2man.pl
Source7:	gcc35-gnatmake-bash-completion
Source8:	build_cross_gcc4.sh

# Mandriva patches + backports from trunk
# LSB compliant headers (for cross compiling without (glibc?) headers)
Patch999: lsb-headers-3.1.1-misc.patch
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
# ?
Patch104: gcc40-cross-build-fixes.patch
# ada
Patch105: gcc35-ada-link.patch
Patch106: gcc40-ada-makefile.patch
Patch117: gcc40-ada-64bit-hack.patch
# gnu pascal
Patch111: gcc34-gpc-fixes.patch
Patch112: gcc33-gpc-serialize-build.patch

# build 32 bits code when running through linux32
Patch115: gcc40-linux32.patch
# ?
Patch116: gcc40-linux32-build-env.patch
# ?
Patch118: gcc4-libtool1.4-lib64.patch
# java fix
Patch120: gcc4-gjavah-jint32.patch
# libffi
Patch121: gcc4-libffi_a-with-pic.patch
# cell arch
Patch123: gcc4-cell-ppu-sched.patch
Patch125: gcc4-cell-spu.patch
# SSSE3 support
Patch128: gcc4-ssse3.patch
# (cjw) disable building of 'nof' libs on ppc
Patch129: gcc-4.1.2-ppc-soft-float-64bit-double-libs.patch

# Red Hat patches
# allow --disable-libjava-multilib to disable multilib for java
Patch201: gcc4-java-nomulti.patch
# ?
Patch202: gcc4-ppc64-m32-m64-multilib-only.patch
# fix libltdl with multilib?
Patch207: gcc4-libltdl-multilib.patch

# use hash style gnu (faster dynamic linking, cf http://lwn.net/Articles/192624/)
Patch211: gcc42-hash-style-gnu.patch


BuildRoot:	%{_tmppath}/%{name}-%{version}-root
# Want updated alternatives priorities
%if %{build_cross}
Conflicts:	gcc-cpp < 3.2.2-4mdk
%endif
# We want -pie support
%define binutils_version 2.14.90.0.5-1mdk
%if %{mdkversion} >= 1010
%define binutils_version 2.15.90.0.3-1mdk
%endif
%if %{mdkversion} >= 1020
%define binutils_version 2.15.92.0.2-1mdk
%endif
%if %{mdkversion} >= 200600
%define binutils_version 2.16.91.0.2-2mdk
%endif
%if %{use_hash_style_gnu}
%define binutils_version 2.16.91.0.7-6mdk
%endif
BuildRequires:	%{cross_prefix}binutils >= %{binutils_version}
BuildRequires:	zlib-devel
%if %{gcc34_as_system_compiler}
# We need gcc3.4 + its libstdc++ headers
%define gcc34_version %(gcc3.4-version)
%define libstdcxx_includedir %{target_prefix}/include/c++/%{gcc34_version}
BuildRequires:	gcc3.4 >= %{gcc34_version}, gcc3.4-c++ >= %{gcc34_version}
%endif
%if %{gcc40_as_system_compiler}
# We need gcc4.0 + its libstdc++ headers
%define gcc40_version %(gcc4.0-version)
%define libstdcxx_includedir %{target_prefix}/include/c++/%{gcc40_version}
BuildRequires:	gcc4.0 >= %{gcc40_version}, gcc4.0-c++ >= %{gcc40_version}
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires:	%{gcc_name}-gnat >= 3.1, %{libgnat_name} >= 3.1
%endif
BuildRequires:	gettext, flex, bison
%if %{build_doc}
BuildRequires:	texinfo >= 4.1
%endif
# XXX: Needs a GNU awk recent enough to correctly generate options.h
BuildRequires:	gawk >= 3.1.4
%if "%{?libc_version:%{libc_version}}" != ""
BuildRequires:	%{cross_prefix}%{libc}-devel >= %{libc_version}
%endif
%if %{build_check}
BuildRequires:	%{cross_prefix}glibc-static-devel
BuildRequires:	autogen
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

%description
A compiler aimed at integrating all the optimizations and features
necessary for a high-performance and stable development environment.
This package is required for all other GCC compilers, namely C++,
Fortran 95, Objective C, Java and Ada 95.

If you have multiple versions of GCC installed on your system, it is
preferred to type "gcc-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU C compiler version %{version}.

%if %{include_core}

####################################################################
# GCC libraries

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
# C Compiler

%package -n %{gcc_name}
Summary: 	C compiler
Group:		Development/C
Requires:	%{cross_prefix}binutils >= %{binutils_version}
# Make sure gdb will understand DW_FORM_strp
Conflicts:	gdb < 5.1.1
Requires:	%{gcc_name}-cpp = %{version}-%{release}
%if %{libc_shared} && !%{build_monolithic}
Requires:	%{libgcc_name_orig} >= 3.3.2-5mdk
%endif
# FIXME: We need a libgcc with 3.4 symbols
Requires(post): update-alternatives
Requires(postun): update-alternatives
Requires:	%{cross_prefix}%{libc}-devel >= %{libc_version}
%if "%{gcc_name}" != "%{cross_prefix}gcc%{branch}"
Obsoletes:	%{cross_prefix}gcc%{branch}
Provides:	%{cross_prefix}gcc%{branch} = %{version}-%{release}
%endif
%if "%{_real_vendor}" == "manbo"
Requires:	manbo-files-gcc = %{version}
%endif

%description -n %{gcc_name}
This package contains GNU C compiler.

If you have multiple versions of GCC installed on your system, it is
preferred to type "gcc-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU C compiler version %{version}.

####################################################################
# Preprocessor

%package -n %{gcc_name}-cpp
Summary:	The C Preprocessor
Group:		Development/C
%if %{system_compiler}
Obsoletes:	gcc%{branch}-cpp
Provides:	gcc%{branch}-cpp = %{version}-%{release}
%endif
Requires(post): update-alternatives
Requires(postun): update-alternatives

%description -n %{gcc_name}-cpp
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

If you have multiple versions of GCC installed on your system, you
will have to type "cpp -V%{version}" or "cpp-%{version}" (without double quotes)
in order to use the GNU C Preprocessor version %{version}.

%endif # include_core

%if %{include_other}

####################################################################
# C++ Compiler

%package -n %{gcc_name}-c++
Summary:	C++ support for gcc
Group:		Development/C++
%if %{system_compiler}
Obsoletes:	gcc%{branch}-c++
Provides:	gcc%{branch}-c++ = %{version}-%{release}
%endif
Requires:	%{cross_prefix}gcc%{branch} >= %{version}-%{base_release}
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
# some day, rpm will be smart enough: %if (%{system_compiler} || %{build_cross}) && !%{build_monolithic}
%if %{libc_shared}
Requires:	%{libstdcxx_name} = %{version}
%endif
Requires:	%{libstdcxx_name_orig}-devel = %{version}
%else
%if %{gcc34_as_system_compiler}
%if %{libc_shared}
Requires:	%{libstdcxx_name} = %{gcc34_version}
%endif
Requires:	%{libstdcxx_name_orig}-devel = %{gcc34_version}
%endif
%if %{gcc40_as_system_compiler}
%if %{libc_shared}
Requires:	%{libstdcxx_name} = %{gcc40_version}
%endif
Requires:	%{libstdcxx_name_orig}-devel = %{gcc40_version}
%endif
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif
Requires(post): update-alternatives
Requires(postun): update-alternatives

%description -n %{gcc_name}-c++
This package adds C++ support to the GNU C compiler. It includes support
for most of the current C++ specification, including templates and
exception handling. It does include the static standard C++
library and C++ header files; the library for dynamically linking
programs is available separately.

If you have multiple versions of GCC installed on your system, it is
preferred to type "g++-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU C++ compiler version %{version}.

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
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
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
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
%endif
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

%package -n %{gcc_name}-objc
Summary:	Objective C support for gcc
Group:		Development/Other
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
Obsoletes:	gcc%{branch}-objc
Provides:	gcc%{branch}-objc = %{version}-%{release}
%endif
Requires:	%{cross_prefix}gcc%{branch} >= %{version}-%{base_release}
%if %{libc_shared} && !%{build_monolithic}
Requires:	%{libobjc_name} = %{version}-%{release}
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{gcc_name}-objc
This package adds Objective C support to the GNU C compiler. Objective
C is an object oriented derivative of the C language, mainly used on
systems running NeXTSTEP. This package does not include the standard
Objective C object library.

####################################################################
# Objective C++ Compiler

%package -n %{gcc_name}-objc++
Summary:	Objective C++ support for gcc
Group:		Development/Other
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
Obsoletes:	gcc%{branch}-objc++
Provides:	gcc%{branch}-objc++ = %{version}-%{release}
%endif
Requires:	%{gcc_name}-objc = %{version}-%{release}
Requires:	%{gcc_name}-c++ = %{version}-%{release}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{gcc_name}-objc++
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
Conflicts:	%{gcc_name}-objc < %{branch}
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libobjc_name}
Runtime libraries for the GNU Objective C Compiler.

####################################################################
# Pascal Compiler

%package -n %{gcc_name}-gpc
Summary:	Pascal support for gcc
Group:		Development/Other
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
Obsoletes:	gcc%{branch}-gpc
Provides:	gcc%{branch}-gpc = %{version}-%{release}
%endif
Requires:	%{cross_prefix}gcc%{branch} >= %{version}-%{base_release}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{gcc_name}-gpc
The GNU Pascal Compiler (GPC) is, as the name says, the Pascal
compiler of the GNU family.  The compiler supports the following
language standards and quasi-standards:

  * ISO 7185 Pascal (see Resources),
  * most of ISO 10206 Extended Pascal,
  * Borland Pascal 7.0,
  * parts of Borland Delphi, Mac Pascal and Pascal-SC (PXSC). 

If you have multiple versions of GCC installed on your system, it is
preferred to type "gpc-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU Pascal compiler version %{version}.

####################################################################
# Fortran 95 Compiler

%package -n %{gcc_name}-gfortran
Summary:	Fortran 95 support for gcc
Group:		Development/Other
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
Obsoletes:	gcc%{branch}-gfortran
Provides:	gcc%{branch}-gfortran = %{version}-%{release}
%endif
Obsoletes:	gcc%{branch}-g77
Requires:	%{cross_prefix}gcc%{branch} >= %{version}-%{base_release}
%if %{libc_shared} && !%{build_monolithic}
Requires:	%{libgfortran_name} = %{version}-%{release}
%endif
%if %{build_fortran}
BuildRequires:	libgmp-devel
BuildRequires:	libmpfr-devel
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{gcc_name}-gfortran
This package adds support for compiling Fortran 95 programs with the GNU
compiler.

If you have multiple versions of GCC installed on your system, it is
preferred to type "gfortran-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU Fortran 95 compiler version %{version}.

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

%package -n %{gcc_name}-gnat
Summary:	Ada 95 support for gcc
Group:		Development/Other
Requires:	%{libgnat_name} = %{version}-%{release}
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
Obsoletes:	gcc%{branch}-gnat
Provides:	gcc%{branch}-gnat = %{version}-%{release}
%endif
Obsoletes:	%{cross_prefix}gnat
Provides:	%{cross_prefix}gnat = %{version}-%{release}
Requires:	%{cross_prefix}gcc%{branch} >= %{version}-%{base_release}

%description -n %{gcc_name}-gnat
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

%package -n %{gcc_name}-java
Summary:	Java support for gcc
Group:		Development/Java
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
Obsoletes:	gcc%{branch}-java
Provides:	gcc%{branch}-java = %{version}-%{release}
%endif
Requires:	%{cross_prefix}gcc%{branch} >= %{version}-%{base_release}
Requires:	%{GCJ_TOOLS} = %{version}-%{release}
Requires:	%{libgcj_name} >= %{version}
Requires:	%{libgcj_devel_name} >= %{version}
Requires(post): update-alternatives
Requires(postun): update-alternatives

%description -n %{gcc_name}-java
This package adds experimental support for compiling Java(tm) programs
and bytecode into native code. To use this you will also need the
libgcj package.

If you have multiple versions of GCC installed on your system, it is
preferred to type "gcj-$(gcc%{branch}-version)" (without double quotes) in
order to use the GNU Java compiler version %{version}.

####################################################################
# Java Runtime Tools

%package -n %{GCJ_TOOLS}
Summary:	Java related tools from gcc %{version}
Group:		Development/Java
%if %{system_compiler}
Obsoletes:	%{cross_prefix}gcj%{branch}-tools
Provides:	%{cross_prefix}gcj%{branch}-tools = %{version}-%{release}
%endif
Provides:	%{cross_prefix}gcj-tools = %{version}-%{release}
Requires:	%{libgcj_name} >= %{version}
Requires:	%{libgcj_devel_name} >= %{version}
Conflicts:	kaffe < 1.0.7-3mdk
Requires(post): update-alternatives
Requires(postun): update-alternatives

%description -n %{GCJ_TOOLS}
This package includes Java related tools built from gcc %{version}:

   * gij: a Java ByteCode Interpreter
   * gcjh: generate header files from class files
   * gjnih: generate JNI header files from class files
   * jv-scan: print information about source files
   * jcf-dump: print information about class files
   * gcj-dbtool: tool for manipulating class file databases
   * grmic: generate stubs for Remote Method Invocation
   * grmiregistry: the remote object registry

If you have multiple versions of GCC installed on your system, the
above-mentioned tools are called as follows: "<gcj_tool>-$(gcc%{branch}-version)"
(without double quotes).

####################################################################
# Java Libraries

%package -n %{libgcj_name}
Summary:	GNU Java runtime libraries
Group:		System/Libraries
Requires:	zip >= 2.1
Obsoletes:	%{cross_prefix}gcc-libgcj
Provides:	%{cross_prefix}gcc-libgcj = %{version}-%{release}
Obsoletes:	%{libgcj_name_orig}%{branch}
Provides:	%{libgcj_name_orig}%{branch} = %{version}-%{release}
%if %{build_java}
%if %{mdkversion} >= 200700
# needed for split X.org
BuildRequires:	libxt-devel, libxtst-devel
%endif
%if %{mdkversion} >= 200600
# needed for cairo support (Graphics2D)
Requires:	gtk+2.0 >= 2.8.0
BuildRequires:	libgtk+2.0-devel >= 2.8.0
%endif
# for libgjsmdssi:
BuildRequires:	libjack-devel
BuildRequires:	dssi-devel
# for libgjsmalsa:
BuildRequires:	libalsa-devel
Requires:	gtk+2.0 >= 2.4.0
BuildRequires:	libgtk+2.0-devel >= 2.4.0
Requires:	libglib2.0 >= 2.4.0
BuildRequires:	libglib2.0-devel >= 2.4.0
BuildRequires:	libart_lgpl-devel >= 2.1.0
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
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
Obsoletes:	libgcj3-devel
Obsoletes:	libgcj4-devel
Obsoletes:	libgcj5-devel
Obsoletes:	%{mklibname gcj 6}-devel
Obsoletes:	%{mklibname gcj 7}-devel
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
Requires(pre):	manbo-files-gcc
Obsoletes:	libgcj3-static-devel
Obsoletes:	libgcj4-static-devel
Obsoletes:	libgcj5-static-devel
Obsoletes:	%{mklibname gcj 6}-static-devel
Obsoletes:	%{mklibname gcj 7}-static-devel
%endif

%description -n %{libgcj_static_devel_name}
Static libraries for the GNU Java Compiler.

%package -n %{libgcj_name_base}-base
Summary: Java library base classes
Group: Development/Java
# For /usr/lib/logging.properties and /usr/lib/security/classpath.security:
Requires: jpackage-utils
Conflicts: %{mklibname gcj 6} < 4.0.1-4mdk
Obsoletes: libgcj6-base

%description -n %{libgcj_name_base}-base
The Java(tm) runtime library classes.

%package -n %{libgcj_name_base}-src
Summary: Java library sources
Group: Development/Java
Requires: %{libgcj_name} = %{version}-%{release}
Obsoletes: libgcj6-src

%description -n %{libgcj_name_base}-src
The Java(tm) runtime library sources.

####################################################################
# FFI headers and libraries

%package -n %{libffi_name}
Summary:	GCC support library for FFI
Group:		System/Libraries

%description -n %{libffi_name}
This package contains GCC shared support library which is needed
for FFI support.

%package -n %{libffi_name_orig}-devel
Summary:	Development headers and static library for FFI
Group:		Development/C
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
%endif
Requires:	%{libffi_name} = %{version}-%{release}
Provides:	%{libffi_name_orig}%{branch}-devel = %{version}-%{release}
Provides:	%{libffi_name_orig}4-devel
Obsoletes:	%{libffi_name_orig}4-devel
Provides:	ffi-devel = %{version}-%{release}

%description -n %{libffi_name_orig}-devel
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
Requires:	%{cross_prefix}gcc%{branch} >= %{version}-%{base_release}
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
%endif
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
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
%endif
Requires:	%{cross_prefix}gcc%{branch} >= %{version}-%{base_release}
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
%if %{system_compiler}
Requires(pre):	manbo-files-gcc
%endif
Requires:	%{gcc_name} >= %{version}-%{base_release}
%if %{libc_shared}
Requires:	%{libgomp_name} = %{version}-%{release}
%endif

%description -n %{libgomp_name_orig}-devel
This package contains headers and static libraries for building 
programs that use OpenMP.

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

%package -n %{gcc_name}-doc
Summary:	GCC documentation
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-doc
Provides:	gcc%{branch}-doc = %{version}-%{release}
%endif
Requires(post): info-install
Requires(preun): info-install

%description -n %{gcc_name}-doc
GCC is a compiler suite aimed at integrating all the optimizations and
features necessary for a high-performance and stable development
environment. This package contains the compiler documentation in INFO
pages.

%package -n %{gcc_name}-doc-pdf
Summary:	GCC documentation
Group:		Development/Other
%if %{system_compiler}
Obsoletes:	gcc%{branch}-doc-pdf
Provides:	gcc%{branch}-doc-pdf = %{version}-%{release}
%endif

%description -n %{gcc_name}-doc-pdf
GCC is a compiler suite aimed at integrating all the optimizations and
features necessary for a high-performance and stable development
environment. This package contains the compiler printable
documentation in PDF.

%endif # include_other

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
%patch115 -p1 -b .linux32
%patch116 -p1 -b .linux32-build-env
%patch117 -p1 -b .ada-64bit-hack
%patch118 -p1 -b .libtool1.4-lib64
%patch120 -p1 -b .gjavah-jint32
%patch121 -p1 -b .libffi_a-with-pic
%patch123 -p1 -b .cell-ppu-sched
%patch125 -p1 -b .cell-spu
%patch128 -p1 -b .ssse3
%patch129 -p1 -b .nonof

# Red Hat patches
%patch201 -p1 -b .java-nomulti
%patch202 -p0 -b .ppc64-m32-m64-multilib-only
%patch207 -p0 -b .libltdl-multilib
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

# Setup files for cross-compilation
# XXX embed uClibc / dietlibc sources? [ia64 checks for __GLIBC__]
%patch104 -p1 -b .cross-build-fixes
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
[[ -f $sysroot/include/stdio.h ]] &&
ln -s $sysroot/include include
[[ -f $sysroot/lib/crti.o ]] &&
ln -s $sysroot/lib lib
[[ -f $sysroot/lib64/crti.o ]] &&
ln -s $sysroot/lib64 lib64
[[ -L include ]] || {
mkdir include
tar jxf %{SOURCE1} -C include
%patch999 -p0
}
cd ..
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

# Patch version for Mandriva and bug reports
echo "%{version}" > gcc/BASE-VER
perl -pi -e '/^\#define VERSUFFIX/ and s/""/" (%{version}-%{release})"/' gcc/version.c
perl -pi -e "/bug_report_url/ and s/\"[^\"]+\"/\"<URL:https:\/\/qa.mandriva.com\/>\"/;" gcc/version.c

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
  perl -pi -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables/' gcc/Makefile.in
  ;;
esac

# update config.{sub,guess} scripts
%{?__cputoolize: %{__cputoolize} -c .}
%{?__cputoolize: %{__cputoolize} -c ./boehm-gc}

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
LIBJAVA_FLAGS="--enable-java-awt=gtk --with-java-home=%{jdk_home}"
%if %{mdkversion} >= 200600
LIBJAVA_FLAGS="$LIBJAVA_FLAGS --enable-gtk-cairo"
%endif
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
%if ! %{build_libmudflap}
MUDFLAP_FLAGS="--disable-libmudflap"
%endif
%if ! %{build_libgomp}
LIBGOMP_FLAGS="--disable-libgomp"
%endif
%if !%{build_libffi}
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
%if !%{system_compiler}
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
esac
CC="%{__cc}" CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --libexecdir=%{_prefix}/lib --with-slibdir=%{target_slibdir} \
	--mandir=%{_mandir} --infodir=%{_infodir} --enable-checking=release \
	--enable-languages="$LANGUAGES" $PROGRAM_PREFIX $PROGRAM_SUFFIX \
	--host=%{_target_platform} $CROSS_FLAGS $TARGET_FLAGS \
	--with-system-zlib $LIBC_FLAGS $LIBSTDCXX_FLAGS $LIBJAVA_FLAGS $SSP_FLAGS $MUDFLAP_FLAGS $LIBFFI_FLAGS $LIBGOMP_FLAGS
touch ../gcc/c-gperf.h
%if %{build_cross}
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

%if %{build_pascal}
(cd gcc/p; for i in ChangeLog* README NEWS FAQ; do
	cp -p $i ../../rpm.doc/gpc/$i
done)
%endif
%if %{build_fortran}
(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
%endif
%if %{build_objc}
(cd gcc/objc; for i in README*; do
	cp -p $i ../../rpm.doc/objc/$i.objc
done)
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/libobjc/$i.libobjc
done)
%endif
%if %{build_objcp}
(cd gcc/objcp;
  # XXX placeholder, there may be docs in the future
  echo "Objective-C++ support for GCC" > ../../rpm.doc/objcp/README)
%endif
%if %{build_java}
(cd boehm-gc; for i in ChangeLog*; do
        cp -p $i ../rpm.doc/boehm-gc/$i.gc
done)
(cd libjava; for i in README THANKS COPYING ChangeLog; do
	cp -p $i ../rpm.doc/libjava/$i.libjava
done)
(cd libjava; cp -p LIBGCJ_LICENSE ../rpm.doc/libjava/LICENSE.libjava)
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
(cd gcc/ada;
  texi2dvi -p -t @afourpaper -t @finalout -I ../doc/include -I ../../obj-%{gcc_target_platform}/gcc gnat_rm.texi)
(cd obj-%{gcc_target_platform}/gcc/doc;
  texi2dvi -p -t @afourpaper -t @finalout -I ../../../gcc/doc/include -I .. gnat_ugn_unw.texi
  mv gnat_ugn_unw.pdf ../../../gcc/ada/gnat_ug.pdf)
%endif

# Run tests
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
rm -rf $RPM_BUILD_ROOT

# Fix HTML docs for libstdc++-v3
perl -pi -e \
  's~href="l(ibstdc|atest)~href="http://gcc.gnu.org/onlinedocs/libstdc++/l\1~' \
  libstdc++-v3/docs/html/documentation.html
ln -sf documentation.html libstdc++-v3/docs/html/index.html
find libstdc++-v3/docs/html -name CVS | xargs rm -rf

# Create some directories, just to make sure (e.g. ColorGCC)
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}
mkdir -p $RPM_BUILD_ROOT%{_infodir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}

%ifarch %{spu_arches}
%makeinstall_std -C objs-spu
%endif

pushd obj-%{gcc_target_platform};
  %makeinstall_std
  %if %{build_java}
  %makeinstall_std -C %{gcc_target_platform}/libjava install-src.zip
  %endif
  %if %{build_ada}
  for f in $RPM_BUILD_ROOT%{_infodir}/gnat_ugn_unw.info*; do
    sed -e "s/gnat_ugn_unw/gnat_ug/g" $f > ${f/gnat_ugn_unw/gnat_ug}
  done
  chmod 644 $RPM_BUILD_ROOT%{_infodir}/gnat*
  %endif
popd

FULLVER=`$RPM_BUILD_ROOT%{_bindir}/%{gcc_target_platform}-gcc%{program_suffix} --version | head -n 1 | cut -d' ' -f3`
FULLPATH=$(dirname $RPM_BUILD_ROOT%{gcc_libdir}/%{gcc_target_platform}/%{version}/cc1)

# Create /usr/bin/%{program_prefix}gcc%{branch}-version that contains the full version of gcc
cat >$RPM_BUILD_ROOT%{_bindir}/%{program_prefix}gcc%{branch}-version <<EOF
#!/bin/sh
echo "$FULLVER"
EOF
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/%{program_prefix}gcc%{branch}-version

mv $RPM_BUILD_ROOT%{_bindir}/cpp $RPM_BUILD_ROOT%{_bindir}/cpp-%{version}
mv $RPM_BUILD_ROOT%{_bindir}/gcc $RPM_BUILD_ROOT%{_bindir}/gcc-%{version}
%if %{build_cxx}
mv $RPM_BUILD_ROOT%{_bindir}/g++ $RPM_BUILD_ROOT%{_bindir}/g++-%{version}
%endif
%if %{build_fortran}
mv $RPM_BUILD_ROOT%{_bindir}/gfortran $RPM_BUILD_ROOT%{_bindir}/gfortran-%{version}
%endif
%if %{build_java}
mv $RPM_BUILD_ROOT%{_bindir}/gcj $RPM_BUILD_ROOT%{_bindir}/gcj-%{version}
mv $RPM_BUILD_ROOT%{_bindir}/gij $RPM_BUILD_ROOT%{_bindir}/gij-%{version}
%endif

# replacing hardlinks with symlinks
ln -sf gcc-%{version} $RPM_BUILD_ROOT%{_bindir}/%{gcc_target_platform}-gcc
ln -sf gcc-%{version} $RPM_BUILD_ROOT%{_bindir}/%{gcc_target_platform}-gcc-%{version}
%if %{build_cxx}
ln -sf g++-%{version} $RPM_BUILD_ROOT%{_bindir}/c++-%{version}
ln -sf g++-%{version} $RPM_BUILD_ROOT%{_bindir}/%{gcc_target_platform}-c++
ln -sf g++-%{version} $RPM_BUILD_ROOT%{_bindir}/%{gcc_target_platform}-g++
%endif
%if %{build_fortran}
ln -sf gfortran-%{version} $RPM_BUILD_ROOT%{_bindir}/%{gcc_target_platform}-gfortran
%endif
%if %{build_java}
ln -sf gcj-%{version} $RPM_BUILD_ROOT%{_bindir}/%{gcc_target_platform}-gcj
ln -sf gcjh $RPM_BUILD_ROOT%{_bindir}/%{gcc_target_platform}-gcjh
%endif

ln -s gcc $RPM_BUILD_ROOT%{_bindir}/cc

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# Dispatch Ada 95 libraries (special case)
%if %{build_ada} && %{libc_shared}
pushd $FULLPATH/adalib
  rm -f libgnarl.so* libgnat.so*
  mv -f libgnarl-*.so.* $RPM_BUILD_ROOT%{_libdir}/
  ln -s ../../../../../%{_lib}/libgnarl-*.so.* libgnarl-%{branch}.so
  ln -s libgnarl-%{branch}.so libgnarl.so
  mv -f libgnat-*.so.* $RPM_BUILD_ROOT%{_libdir}/
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
	rm -f $libname.so $libname.a
	[[ -f ../../../../..%{target_libdir}/$libname.so.$libversion ]] && {
	$STRIP_DEBUG ../../../../..%{target_libdir}/$libname.so.$libversion
	ln -s ../../../../..%{target_libdir}/$libname.so.$libversion $libname.so
	rm -f ../../../../..%{target_libdir}/$libname.so
	} || :
	[[ -f ../../../../..%{target_libdir}/$libname.a ]] && {
	$STRIP_DEBUG ../../../../..%{target_libdir}/$libname.a
	cp -f ../../../../..%{target_libdir}/$libname.a $libname.a
	rm -f ../../../../..%{target_libdir}/$libname.a
	} || :
	%if %isarch %{biarches}
	[ -d 32 ] || mkdir 32
	pushd 32
	mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib
	skip32=
	[[ -z "$skip32" ]] && {
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
	%if ! %{system_compiler}
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
	# Do not dispatch libgcj_bc, libgcj_bc.so and libgcj_bc.so.1.0.0
	# are different libraries intentionally. We move it manually:
	mv ../../../../..%{target_libdir}/libgcj_bc.{so,a} .
	%endif
	%if %{build_objc}
	DispatchLibs libobjc	%{libobjc_major}.0.0
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
  mkdir -p $RPM_BUILD_ROOT%{libjava_includedir}
  for dir in gcj gnu java javax org; do
    mkdir -p $RPM_BUILD_ROOT%{libjava_includedir}/$dir
    mv $RPM_BUILD_ROOT%{libstdcxx_includedir}/$dir/* $RPM_BUILD_ROOT%{libjava_includedir}/$dir/
    rmdir $RPM_BUILD_ROOT%{libstdcxx_includedir}/$dir
  done

  # include <libgcj/XXX.h> should lead to <libgcj-VERSION/XXX.h>
  ln -s %{libjava_includedir} $RPM_BUILD_ROOT%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/libgcj

  # fix pkgconfig files
  perl -pi -e 's,^(includedir=).+,\1%{libjava_includedir},' $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig/libgcj-%{branch}.pc
%if %isarch %{biarches}
  mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
  perl -pe '/^libdir=/ and s,/lib,/%{target_lib},' $RPM_BUILD_ROOT%{_prefix}/lib/pkgconfig/libgcj-%{branch}.pc > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libgcj-%{branch}.pc
  rm %{buildroot}%{_prefix}/lib/pkgconfig/libgcj-%{branch}.pc
%endif
fi
%endif

# Move libgcj.spec to compiler-specific directories
%if %{build_java}
mv $RPM_BUILD_ROOT%{_prefix}/lib/libgcj.spec $FULLPATH/libgcj.spec
%endif

# Rename jar because it could clash with Kaffe/classpath's if this gcc
# is primary compiler (aka don't have the -<version> extension)
%if %{build_java}
pushd $RPM_BUILD_ROOT%{_bindir}
  for app in %{gcj_alternative_programs} gappletviewer gjarsigner gkeytool; do
    [[ -f $app ]] && mv -f $app $app-%{version} || :
    [[ -f $app-%{version} ]] || { echo "Missing $app"; exit 1; }
  done
popd
%endif

# Move <cxxabi.h> to compiler-specific directories
%if %{build_cxx}
mkdir -p $FULLPATH/include/bits/
mv $RPM_BUILD_ROOT%{libstdcxx_includedir}/cxxabi.h $FULLPATH/include/
mv $RPM_BUILD_ROOT%{libstdcxx_includedir}/%{gcc_target_platform}/bits/cxxabi_tweaks.h $FULLPATH/include/bits/
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

    cat > $RPM_BUILD_ROOT%{libstdcxx_includedir}/%{gcc_target_platform}/bits/c++config.h <<EOF
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
ln -sf gcc $RPM_BUILD_ROOT%{_bindir}/gnatgcc
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
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives cpp)
%if !%{build_cross}
(mkdir -p $RPM_BUILD_ROOT/lib; cd $RPM_BUILD_ROOT/lib; ln -sf %{_bindir}/cpp cpp)
%endif

# Alternatives provide /usr/bin/{gfortran,f95}
%if %{build_fortran}
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives gfortran f95)
%endif

# Alternatives provide /usr/bin/c++
%if %{build_cxx}
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives c++)
%endif

# Alternatives provide java programs
%if %{build_java}
(cd $RPM_BUILD_ROOT%{_bindir}; FakeAlternatives gij %{gcj_alternative_programs})
%endif

if [[ -z "%{?cross_bootstrap:1}" ]] && [[ "%{libc_shared}" = "1" ]]; then
# Move libgcc_s.so* to /%{_lib}
pushd $RPM_BUILD_ROOT%{_prefix}/%{target_lib}
  chmod 0755 libgcc_s.so.%{libgcc_major}
  mkdir -p $RPM_BUILD_ROOT%{target_slibdir}
  mv -f  libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{target_slibdir}/libgcc_s-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s-%{version}.so.%{libgcc_major} $RPM_BUILD_ROOT%{target_slibdir}/libgcc_s.so.%{libgcc_major}
  ln -sf %{target_slibdir}/libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{target_libdir}/libgcc_s.so
%if %isarch %{nof_arches}
  chmod 0755 nof/libgcc_s.so.%{libgcc_major}
  mkdir -p $RPM_BUILD_ROOT%{target_slibdir}/nof
  mv -f  nof/libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{target_slibdir}/nof/libgcc_s-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s-%{version}.so.%{libgcc_major} $RPM_BUILD_ROOT%{target_slibdir}/nof/libgcc_s.so.%{libgcc_major}
  ln -sf %{target_slibdir}/nof/libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{target_libdir}/nof/libgcc_s.so
%endif
popd
%if %isarch %{biarches}
pushd $RPM_BUILD_ROOT%{_prefix}/lib
  chmod 0755 libgcc_s.so.%{libgcc_major}
  mkdir -p $RPM_BUILD_ROOT/lib
  mv -f  libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT/lib/libgcc_s-%{version}.so.%{libgcc_major}
  ln -sf libgcc_s-%{version}.so.%{libgcc_major} $RPM_BUILD_ROOT/lib/libgcc_s.so.%{libgcc_major}
  ln -sf ../../lib/libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{_prefix}/lib/libgcc_s.so
  ln -sf ../../lib/libgcc_s.so.%{libgcc_major} $RPM_BUILD_ROOT%{_prefix}/lib/libgcc_s_32.so
popd
%if %build_java
  for lib in libgcj libgij libgcj-tools libgcj_bc; do
    ln -sf ../../../%{gcc32_target_platform}/%{version}/$lib.a  $FULLPATH/32/$lib.a
    ln -sf ../../../%{gcc32_target_platform}/%{version}/$lib.so $FULLPATH/32/$lib.so
  done
%endif
%endif
fi

# Create c89 and c99 wrappers
%if %{system_compiler}
cat > $RPM_BUILD_ROOT%{_prefix}/bin/c89 <<"EOF"
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
cat > $RPM_BUILD_ROOT%{_prefix}/bin/c99 <<"EOF"
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
chmod 755 $RPM_BUILD_ROOT%{_prefix}/bin/c?9
%endif

# FIXME: cpp, gcov manpages names
pushd $RPM_BUILD_ROOT%{_mandir}/man1;
  if [[ -n "%{program_prefix}%{program_suffix}" ]]; then
    for f in gcov cpp gcc g++ gfortran gpc; do
      [[ -f "$f.1" ]] && mv $f.1 %{program_prefix}$f%{program_suffix}.1 || :
    done
  fi
popd

# Fix info pages
if [[ "%{gcc_name}" = "gcc%{branch}" ]]; then
  cd $RPM_BUILD_ROOT%{_infodir}/
  for f in cpp cppinternals gcc gpc gpcs gfortran gnat-style gnat_rm gnat_ug gcj; do
    if [[ -f "$f.info" ]]; then
      perl -pe "/^START-INFO-DIR-ENTRY/ .. /^END-INFO-DIR-ENTRY/ and s/($f)/\${1}-%{branch}/ig" $f.info > ${f}-%{branch}.info
      rm -f $f.info
    fi
  done
  cd ..
fi

files_files=""

%define find_lang /usr/lib/rpm/find-lang.sh %buildroot
%find_lang %{gcc_name}
%find_lang cpplib
%if %{include_other}
%find_lang libstdc++
%endif

# Remove unpackaged files
rm  -f $RPM_BUILD_ROOT%{_bindir}/jar
rm  -f $RPM_BUILD_ROOT%{_bindir}/addr2name.awk
rm -rf $RPM_BUILD_ROOT%{_prefix}/doc
rm -rf $RPM_BUILD_ROOT%{_mandir}/man7
rm  -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm  -f $RPM_BUILD_ROOT%{gcj_libdir}/*.la
rm  -f $RPM_BUILD_ROOT%{_prefix}/lib/libiberty.a
rm  -f $RPM_BUILD_ROOT%{target_libdir}/libiberty.a
%if %isarch %{biarches}
rm  -f $RPM_BUILD_ROOT%{_prefix}/lib/*.la
rm  -f $RPM_BUILD_ROOT%{_prefix}/lib/32/libiberty.a
%endif
rm -rf $RPM_BUILD_ROOT%{gcc_libdir}/%{gcc_target_platform}/%{version}/install-tools
%ifarch %{spu_arches}
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib/gcc/spu/%{version}/install-tools
rm  -f $RPM_BUILD_ROOT%{spu_prefix}/lib/*.la
%endif
%if ! %{build_doc}
rm -fr $RPM_BUILD_ROOT/%{_datadir}/info/
%endif

# the list of files below depend on the files installed on the system.
# only keeping a fixed list:
pushd $RPM_BUILD_ROOT%{gcc_libdir}/%{gcc_target_platform}/%{version}
  mv include include-other
  mkdir include 
  for i in README altivec.h cxxabi.h emmintrin.h ffi.h ffitarget.h float.h gpc-in-c.h \
    ia64intrin.h iso646.h jawt.h jawt_md.h jni.h jni_md.h jvmpi.h limits.h       \
    math-68881.h mf-runtime.h mm3dnow.h mm_malloc.h mmintrin.h omp.h pmmintrin.h \
    ppc-asm.h spe.h spu_internals.h spu_intrinsics.h spu_mfcio.h stdarg.h        \
    stdbool.h stddef.h syslimits.h tmmintrin.h unwind.h varargs.h vec_types.h    \
    vmx2spu.h xmmintrin.h bits gcj libgcj objc ssp                               \
  ; do mv include-other/$i include 2>/dev/null ||: ; done
  rm -rf include-other
popd

%if %build_java
# Handled by jpackage-utils, see #23693
rm  -f $RPM_BUILD_ROOT%{target_libdir}/security/classpath.security
rm  -f $RPM_BUILD_ROOT%{target_libdir}/logging.properties
%endif

# In case we are cross-compiling, don't bother to remake symlinks and
# don't let spec-helper when stripping files either
%if "%{gcc_name}" != "gcc"
export DONT_SYMLINK_LIBS=1
export DONT_STRIP=1
%endif

%if %{build_debug}
# Don't strip in debug mode
export DONT_STRIP=1
%endif

%if %{build_ada}
# gnatmake bash completion
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/gnatmake
%endif

%if %{build_java}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/java/gcj-endorsed \
         $RPM_BUILD_ROOT%{gcj_libdir}/classmap.db.d
chmod 755 $RPM_BUILD_ROOT%{_datadir}/java/gcj-endorsed \
          $RPM_BUILD_ROOT%{gcj_libdir} \
          $RPM_BUILD_ROOT%{gcj_libdir}/classmap.db.d
touch $RPM_BUILD_ROOT%{gcj_libdir}/classmap.db

# check if gcj-dbtool hasn't been incorrectly relinked.  rh#165781
classmap_db=`LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}:$RPM_BUILD_ROOT/%{_lib} \
             $RPM_BUILD_ROOT%{_bindir}/gcj-dbtool%{program_suffix} -p`
case "$classmap_db" in
  # XXX: grmpf, make sure it's at a unique location!?
  %{gcj_libdir}/classmap.db) ;;
  %{_prefix}/lib/../%{_lib}/gcj-%{version}/classmap.db) ;;
  *) echo Unexpected gcj-dbtool%{program_suffix} -p output; exit 1 ;;
esac
%endif

files_files="$files_files files.%{gcc_name}-cpp"
cat <<EOF > files.%{gcc_name}-cpp
%defattr(-,root,root)
#
%{_mandir}/man1/%{program_prefix}cpp%{program_suffix}.1*
#
%if !%{build_cross}
/lib/cpp
%endif
%ghost %{_bindir}/%{cross_program_prefix}cpp
%{_bindir}/%{program_prefix}cpp-%{version}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/cc1
EOF
cat cpplib.lang >> files.%{gcc_name}-cpp

files_files="$files_files files.%{gcc_name}"
cat <<EOF > files.%{gcc_name}
%defattr(-,root,root)
#
%doc gcc/README*
%{_mandir}/man1/%{program_prefix}gcc%{program_suffix}.1*
%if "%{gcc_name}" == "gcc%{package_suffix}"
%{_mandir}/man1/gcov%{program_suffix}.1*
%endif
#
%{_bindir}/%{program_prefix}gcc%{branch}-version
%{_bindir}/%{program_prefix}gcc-%{version}
%{_bindir}/%{gcc_target_platform}-gcc%{program_suffix}
%{_bindir}/%{gcc_target_platform}-gcc-%{version}
%{_bindir}/gccbug
%if "%{gcc_name}" == "gcc%{package_suffix}"
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
%if %{libc_shared}
%if !%{build_cross_bootstrap}
%{target_libdir}/libgcc_s.so
%endif
%if "%{gcc_name}" == "gcc%{package_suffix}"
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
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcc_eh.a
%if "%{gcc_name}" == "gcc%{package_suffix}"
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
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/mm3dnow.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/mm_malloc.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/mmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/xmmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/pmmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/emmintrin.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/tmmintrin.h
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
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/stdbool.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/stddef.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/syslimits.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/unwind.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/varargs.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/README

%if !%build_libffi && %build_java
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/ffi*.h
%endif
EOF
cat %{gcc_name}.lang >> files.%{gcc_name}

%if "%{gcc_name}" == "%{cross_prefix}gcc" && %{libc_shared}
%if !%{build_monolithic}
files_files="$files_files files.%{libgcc_name}"
rm -f files.%{libgcc_name}
%define output files.%{libgcc_name}
%else
%define output files.%{gcc_name}
%endif
cat <<EOF >> %{output}
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
EOF
%endif

%if ! %{include_core} && %{include_other}
for file in $files_files
do
  cat $file | grep -v "^%dir" | sed -e 's/.* //' | while read i
  do
    if test -n "$i"
    then
      rm -fr $RPM_BUILD_ROOT/$i
    fi
  done
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{include_core}
%post -n %{gcc_name}
/usr/sbin/update-alternatives --install %{_bindir}/%{cross_program_prefix}gcc %{cross_program_prefix}gcc %{_bindir}/%{program_prefix}gcc-%{version} %{alternative_priority}
[ -e %{_bindir}/%{cross_program_prefix}gcc ] || /usr/sbin/update-alternatives --auto %{cross_program_prefix}gcc

%postun -n %{gcc_name}
if [ ! -f %{_bindir}/%{cross_program_prefix}gcc-%{version} ]; then
  /usr/sbin/update-alternatives --remove %{cross_program_prefix}gcc %{_bindir}/%{program_prefix}gcc-%{version}
fi

%post -n %{libgcc_name} -p /sbin/ldconfig
%postun -n %{libgcc_name} -p /sbin/ldconfig

%post -n %{gcc_name}-cpp
/usr/sbin/update-alternatives --install %{_bindir}/%{cross_program_prefix}cpp %{cross_program_prefix}cpp %{_bindir}/%{program_prefix}cpp-%{version} %{alternative_priority} --slave /lib/%{cross_program_prefix}cpp %{cross_program_prefix}lib_cpp %{_bindir}/%{program_prefix}cpp-%{version}
[ -e %{_bindir}/%{cross_program_prefix}cpp ] || /usr/sbin/update-alternatives --auto %{cross_program_prefix}cpp

%postun -n %{gcc_name}-cpp
if [ ! -f %{_bindir}/%{cross_program_prefix}cpp-%{version} ]; then
  /usr/sbin/update-alternatives --remove %{cross_program_prefix}cpp %{_bindir}/%{program_prefix}cpp-%{version}
fi
%endif # include_core

%if %{include_other}
%if %{build_cxx}
%post -n %{gcc_name}-c++
/usr/sbin/update-alternatives --install %{_bindir}/%{cross_program_prefix}g++ %{cross_program_prefix}g++ %{_bindir}/%{program_prefix}g++-%{version} %{alternative_priority} --slave %{_bindir}/%{cross_program_prefix}c++ %{cross_program_prefix}c++ %{_bindir}/%{program_prefix}g++-%{version}
[ -e %{_bindir}/%{cross_program_prefix}g++ ] || /usr/sbin/update-alternatives --auto %{cross_program_prefix}g++

%postun -n %{gcc_name}-c++
if [ ! -f %{_bindir}/%{cross_program_prefix}g++-%{version} ]; then
  /usr/sbin/update-alternatives --remove %{cross_program_prefix}g++ %{_bindir}/%{program_prefix}g++-%{version}
fi
%endif

%if %{build_libstdcxx}
%post -n %{libstdcxx_name} -p /sbin/ldconfig
%postun -n %{libstdcxx_name} -p /sbin/ldconfig
%endif

%post -n %{libmudflap_name} -p /sbin/ldconfig
%postun -n %{libmudflap_name} -p /sbin/ldconfig

%if %{build_libssp}
%post -n %{libssp_name} -p /sbin/ldconfig
%postun -n %{libssp_name} -p /sbin/ldconfig
%endif

%post -n %{libgomp_name} -p /sbin/ldconfig
%postun -n %{libgomp_name} -p /sbin/ldconfig

%if %{build_pascal}
%post -n %{gcc_name}-gpc
/usr/sbin/update-alternatives --install %{_bindir}/gpc gpc %{_bindir}/%{program_prefix}gpc-%{version} %{alternative_priority} --slave %{_bindir}/gpidump gpidump %{_bindir}/%{program_prefix}gpidump-%{version}
[ -e %{_bindir}/gpc ] || /usr/sbin/update-alternatives --auto gpc

%postun -n %{gcc_name}-gpc
if [ ! -f %{_bindir}/gpc-%{version} ]; then
  /usr/sbin/update-alternatives --remove gpc %{_bindir}/%{program_prefix}gpc-%{version}
fi
%endif

%if %{build_fortran}
%post -n %{gcc_name}-gfortran
/usr/sbin/update-alternatives --install %{_bindir}/%{cross_program_prefix}gfortran %{cross_program_prefix}gfortran %{_bindir}/%{program_prefix}gfortran-%{version} %{alternative_priority} --slave %{_bindir}/f95 f95 %{_bindir}/%{program_prefix}gfortran-%{version}
[ -e %{_bindir}/%{cross_program_prefix}gfortran ] || /usr/sbin/update-alternatives --auto %{cross_program_prefix}gfortran

%postun -n %{gcc_name}-gfortran
if [ ! -f %{_bindir}/%{cross_program_prefix}gfortran-%{version} ]; then
  /usr/sbin/update-alternatives --remove %{cross_program_prefix}gfortran %{_bindir}/%{program_prefix}gfortran-%{version}
fi
%endif

%if %{build_java}
%post -n %{gcc_name}-java
/usr/sbin/update-alternatives --install %{_bindir}/gcj gcj %{_bindir}/gcj-%{version} %{alternative_priority}
[ -e %{_bindir}/gcj ] || /usr/sbin/update-alternatives --auto gcj

%postun -n %{gcc_name}-java
if [ ! -f %{_bindir}/gcj-%{version} ]; then
  /usr/sbin/update-alternatives --remove gcj %{_bindir}/gcj-%{version}
fi
%endif

%if %{build_java}
%post -n %{GCJ_TOOLS}
for app in %{gcj_alternative_programs}; do
  # Remove binaries if not alternativeszificated yet
  [ ! -L %{_bindir}/$app ] && /bin/rm -f %{_bindir}/$app
  # Build slaves list
  slaves="$slaves --slave %{_bindir}/$app $app %{_bindir}/$app-%{version}"
done
/usr/sbin/update-alternatives --install %{_bindir}/gij gij %{_bindir}/gij-%{version} %{gcj_alternative_priority} $slaves
%endif

%if %{build_java}
%postun -n %{GCJ_TOOLS}
if [ ! -f "%{_bindir}/gij-%{version}" ]; then
  /usr/sbin/update-alternatives --remove gij %{_bindir}/gij-%{version}
fi
%endif

%if %{build_java}
%post -n %{libgcj_devel_name}
/usr/sbin/update-alternatives --install %{_includedir}/libgcj libgcj %{_includedir}/libgcj-%{version} %{gcj_alternative_priority}
%endif

%if %{build_java}
%postun -n %{libgcj_devel_name}
if [ ! -d %{_includedir}/libgcj-%{version} ]; then
  /usr/sbin/update-alternatives --remove libgcj %{_includedir}/libgcj-%{version}
fi
%endif

%if %{build_java}
%post -n %{libgcj_name} -p /sbin/ldconfig
%postun -n %{libgcj_name} -p /sbin/ldconfig
%endif

%if %{build_objc}
%post -n %{libobjc_name} -p /sbin/ldconfig
%postun -n %{libobjc_name} -p /sbin/ldconfig
%endif

%if %{build_fortran}
%post -n %{libgfortran_name} -p /sbin/ldconfig
%postun -n %{libgfortran_name} -p /sbin/ldconfig
%endif

%if %{build_ada}
%post -n %{libgnat_name} -p /sbin/ldconfig
%postun -n %{libgnat_name} -p /sbin/ldconfig
%endif

%post -n %{gcc_name}-doc
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
%_install_info gnat_ug%{_package_suffix}.info
%endif
%if %{build_java}
%_install_info gcj%{_package_suffix}_ug.info
%endif

%preun -n %{gcc_name}-doc
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
%_remove_install_info gnat_ug%{_package_suffix}.info
%endif
%if %{build_java}
%_remove_install_info gcj%{_package_suffix}.info
%endif
%endif # include_other

%if %{include_core}

%files -n %{gcc_name}-cpp -f files.%{gcc_name}-cpp

%files -n %{gcc_name} -f files.%{gcc_name}

%if "%{gcc_name}" == "%{cross_prefix}gcc" && %{libc_shared}
%if !%{build_monolithic}
%files -n %{libgcc_name} -f files.%{libgcc_name}
%endif
%endif

%endif # include_core

%if %{include_other}
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

%if %{build_cxx}
%files -n %{gcc_name}-c++ -f libstdc++.lang
%defattr(-,root,root)
#
%doc gcc/cp/ChangeLog*
%{_mandir}/man1/%{program_prefix}g++%{program_suffix}.1*
#
%ghost %{_bindir}/%{cross_program_prefix}c++
%{_bindir}/%{program_prefix}g++-%{version}
%{_bindir}/%{program_prefix}c++-%{version}
%{_bindir}/%{gcc_target_platform}-g++%{program_suffix}
%{_bindir}/%{gcc_target_platform}-c++%{program_suffix}
#
%{gcc_libdir}/%{gcc_target_platform}/%{version}/cc1plus
# symlinks to gcc3.4 stuff
%if !%{system_compiler}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/cxxabi.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/bits/cxxabi_tweaks.h
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
%doc libstdc++-v3/ChangeLog* libstdc++-v3/README* libstdc++-v3/docs/html/
#
%dir %{libstdcxx_includedir}
%{libstdcxx_includedir}/*
%ifarch %{spu_arches}
%exclude %dir %{libstdcxx_includedir}/spu
%exclude %dir %{libstdcxx_includedir}/spu/bits
%exclude %{libstdcxx_includedir}/spu/bits/*
%endif
%if %{system_compiler}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/cxxabi.h
%{gcc_libdir}/%{gcc_target_platform}/%{version}/include/bits/cxxabi_tweaks.h
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
%files -n %{gcc_name}-objc
%defattr(-,root,root)
#
%doc rpm.doc/objc/*
#
%{gcc_libdir}/%{gcc_target_platform}/%{version}/cc1obj
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libobjc.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libobjc.so
%endif
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libobjc.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libobjc.so
%endif
%endif
%if %isarch %{nof_arches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libobjc.a
%if %{libc_shared}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/nof/libobjc.so
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
%if %isarch %{biarches}
%{_prefix}/lib/libobjc.so.%{libobjc_major}
%{_prefix}/lib/libobjc.so.%{libobjc_major}.0.0
%endif
%endif

%if %{build_objcp}
%files -n %{gcc_name}-objc++
%defattr(-,root,root)
%doc rpm.doc/objcp/*
%{gcc_libdir}/%{gcc_target_platform}/%{version}/cc1objplus
%endif

%if %{build_pascal}
%files -n %{gcc_name}-gpc
%defattr(-,root,root)
#
%doc rpm.doc/gpc/*
%{_mandir}/man1/%{program_prefix}gpc%{program_suffix}.1*
%{_mandir}/man1/%{program_prefix}/gpc-run%{program_suffix}.1*
#
%{_bindir}/gpc-run
%{_bindir}/binobj
%ghost %{_bindir}/gpc
%ghost %{_bindir}/gpidump
%{_bindir}/%{program_prefix}gpc-%{version}
%{_bindir}/%{program_prefix}gpidump-%{version}
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
%files -n %{gcc_name}-gfortran
%defattr(-,root,root)
#
%doc rpm.doc/gfortran/*
%{_mandir}/man1/%{program_prefix}gfortran%{program_suffix}.1*
#
%ghost %{_bindir}/%{cross_program_prefix}gfortran
%ghost %{_bindir}/%{cross_program_prefix}f95
%{_bindir}/%{program_prefix}gfortran-%{version}
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
%files -n %{gcc_name}-java
%defattr(-,root,root)
%doc gcc/java/ChangeLog*
%{_bindir}/gcj-%{version}
%{_bindir}/%{gcc_target_platform}-gcj
%{gcc_libdir}/%{gcc_target_platform}/%{version}/jc1
%{gcc_libdir}/%{gcc_target_platform}/%{version}/jvgenmain
%{_mandir}/man1/%{program_prefix}gcj%{program_suffix}.1*
%endif

%if %{build_java}
%files -n %{GCJ_TOOLS}
%defattr(-,root,root)
%{_bindir}/gij-%{version}
%{_bindir}/grmic-%{version}
%{_bindir}/grmiregistry-%{version}
%ghost %{_bindir}/gij
%ghost %{_bindir}/grmic
%ghost %{_bindir}/grmiregistry
%{_bindir}/gappletviewer-%{version}
%{_bindir}/gjarsigner-%{version}
%{_bindir}/gkeytool-%{version}
%{_bindir}/gcj-dbtool%{program_suffix}
%{_bindir}/gcjh%{program_suffix}
%{_bindir}/%{gcc_target_platform}-gcjh
%{_bindir}/gjnih%{program_suffix}
%{_bindir}/jcf-dump%{program_suffix}
%{_bindir}/jv-scan%{program_suffix}
#
%{_mandir}/man1/gij*.1*
%{_mandir}/man1/gcjh*.1*
%{_mandir}/man1/gjnih*.1*
%{_mandir}/man1/grmic*.1*
%{_mandir}/man1/grmiregistry*.1*
%{_mandir}/man1/gcj-dbtool*.1*
%{_mandir}/man1/jv-scan*.1*
%{_mandir}/man1/jcf-dump*.1*
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
%{target_libdir}/libgcj_bc.so.%{libgcj_bc_major}
%{target_libdir}/libgcj_bc.so.%{libgcj_bc_major}.0.0
%dir %{gcj_libdir}
%{gcj_libdir}/libgjsmalsa.so
%{gcj_libdir}/libgjsmdssi.so
%{gcj_libdir}/libgtkpeer.so
%{gcj_libdir}/libjawt.so
%{gcj_libdir}/libjvm.so
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
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcj_bc.so
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcj.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgij.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcj-tools.so
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcj_bc.so
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
%{gcc_libdir}/%{gcc_target_platform}/%{version}/libgcj_bc.a
%{gcj_libdir}/libjvm.a
%if %isarch %{biarches}
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcj.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgij.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcj-tools.a
%{gcc_libdir}/%{gcc_target_platform}/%{version}/32/libgcj_bc.a
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

%if %{build_ada}
%files -n %{gcc_name}-gnat
%defattr(-,root,root)
#
%{_bindir}/gprmake
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

%files -n %{libffi_name_orig}-devel
%defattr(-,root,root)
%doc libffi/README libffi/LICENSE libffi/ChangeLog*
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
%files -n %{gcc_name}-doc
%doc gcc/*ChangeLog*
%defattr(-,root,root)
%if %{build_check}
%doc test_summary.log
%endif
%{_infodir}/cppinternals%{_package_suffix}.info*
%{_infodir}/cpp%{_package_suffix}.info*
%{_infodir}/gcc%{_package_suffix}.info*
%{_infodir}/gccinstall%{_package_suffix}.info*
%{_infodir}/gccint%{_package_suffix}.info*
%{_infodir}/libgomp%{_package_suffix}.info*
%if %{build_ada}
%{_infodir}/gnat-style%{_package_suffix}.info*
%{_infodir}/gnat_rm%{_package_suffix}.info*
%{_infodir}/gnat_ug%{_package_suffix}.info*
%{_infodir}/gnat_ugn_unw%{_package_suffix}.info*
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
%files -n %{gcc_name}-doc-pdf
%defattr(-,root,root)
%doc gcc/doc/cppinternals.pdf
%doc gcc/doc/gcc.pdf
%doc gcc/doc/cpp.pdf
%if %{build_ada}
%doc gcc/ada/gnat_rm.pdf
%doc gcc/ada/gnat_ug.pdf
%endif
%if %{build_fortran}
%doc gcc/fortran/gfortran.pdf
%endif
%endif
%endif # include_other
