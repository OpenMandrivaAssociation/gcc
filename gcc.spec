# functions with printf format attribute but with special parser and also
# receiving non constant format strings
%define		Werror_cflags			%{nil}

# avoid failures when testing if compiler used to build gcc can generate
# shared objects (regardless of unresolved symbols)
%define		_disable_ld_no_undefined	1

# avoid build failure due to configure built with different autoconf version
%define		_disable_libtoolize		1

#-----------------------------------------------------------------------
%define		official		1
%if %{official}
  %define	snapshot		%{nil}
%else
  %define	snapshot		-20120413
%endif
%define		system_compiler		1
%define		branch			4.9
%define		ver			%{branch}.1
%define		linaro			2014.05
%define		linaro_spin		%nil
%define		alternatives		/usr/sbin/update-alternatives
%define		gcclibexecdir		%{_libexecdir}/gcc/%{_target_platform}/%{ver}
%define		gccdir			%{_libdir}/gcc/%{_target_platform}/%{ver}
%define		multigccdir		%{_libdir}/gcc/%{_target_platform}/%{ver}/32
%define		multilibdir		%{_prefix}/lib
%define		multirootlibdir		/lib

#-----------------------------------------------------------------------
%define		gcc_major		1
%define		libgcc			%mklibname gcc %{gcc_major}
%define		multilibgcc		libgcc%{gcc_major}
%define		stdcxx_major		6
%define		libstdcxx		%mklibname stdc++ %{stdcxx_major}
%define		libstdcxx_devel		%mklibname stdc++ -d
%define		libstdcxx_static_devel	%mklibname stdc++ -d -s
%define		multilibstdcxx		libstdc++%{stdcxx_major}
%define		gcj_major		15
%define		libgcj			%mklibname gcj %{gcj_major}
%define		libgcj_devel		%mklibname gcj -d
%define		libgcj_static_devel	%mklibname gcj -d -s
%define		gcj_bc_major		1
%define		libgcj_bc		%mklibname gcj_bc %{gcj_bc_major}
# gcj multilib explicitly disabled
%define		gfortran_major		3
%define		libgfortran		%mklibname gfortran %{gfortran_major}
%define		libgfortran_devel	%mklibname gfortran -d
%define		libgfortran_static_devel %mklibname gfortran -d -s
%define		multilibgfortran	libgfortran%{gfortran_major}
%define		ffi_major		4
%define		libffi			%mklibname ffi %{ffi_major}
%define		libffi_devel		%mklibname ffi -d
%define		libffi_static_devel	%mklibname ffi -d -s
%define		multilibffi		libffi%{ffi_major}
%define		gnat_major		1
%define		libgnat			%mklibname gnat %{gnat_major}
%define		libgnat_devel		%mklibname gnat -d
%define		libgnat_static_devel	%mklibname gnat -d -s
%define		multilibgnat		libgnat%{gnat_major}
%define		go_major		5
%define		libgo			%mklibname go %{go_major}
%define		libgo_devel		%mklibname go -d
%define		libgo_static_devel	%mklibname go -d -s
%define		multilibgo		libgo%{go_major}
%define		gomp_major		1
%define		libgomp			%mklibname gomp %{gomp_major}
%define		libgomp_devel		%mklibname gomp -d
%define		libgomp_static_devel	%mklibname gomp -d -s
%define		multilibgomp		libgomp%{gomp_major}
%define		objc_major		4
%define		libobjc			%mklibname objc %{objc_major}
%define		libobjc_devel		%mklibname objc -d
%define		libobjc_static_devel	%mklibname objc -d -s
%define		multilibobjc		libobjc%{objc_major}
%define		quadmath_major		0
%define		libquadmath		%mklibname quadmath %{quadmath_major}
%define		libquadmath_devel	%mklibname quadmath -d
%define		libquadmath_static_devel %mklibname quadmath -d -s
%define		multilibquadmath	libquadmath%{quadmath_major}
%define		ssp_major		0
%define		libssp			%mklibname ssp %{ssp_major}
%define		libssp_devel		%mklibname ssp -d
%define		libssp_static_devel	%mklibname ssp -d -s
%define		multilibssp		libssp%{ssp_major}
%define		itm_major		1
%define		libitm			%mklibname itm %{itm_major}
%define		libitm_devel		%mklibname itm -d
%define		libitm_static_devel	%mklibname itm -d -s
%define		multilibitm		libitm%{itm_major}
%define		asan_major		1
%define		libasan			%mklibname asan %{asan_major}
%define		libasan_devel		%mklibname asan -d
%define		libasan_static_devel	%mklibname asan -d -s
%define		multilibasan		libasan%{asan_major}
%define		tsan_major		0
%define		libtsan			%mklibname tsan %{tsan_major}
%define		libtsan_devel		%mklibname tsan -d
%define		libtsan_static_devel	%mklibname tsan -d -s
%define		atomic_major		1
%define		libatomic		%mklibname atomic %{atomic_major}
%define		libatomic_devel		%mklibname atomic -d
%define		libatomic_static_devel	%mklibname atomic -d -s
%define		multilibatomic		libatomic%{atomic_major}
%define		cilk_major		5
%define		libcilkrts		%mklibname cilkrts %{cilk_major}
%define		libcilkrts_devel	%mklibname cilkrts -d
%define		libcilkrts_static_devel	%mklibname cilkrts -d -s
%define		multilibcilkrts		libcilkrts%{cilk_major}
%define		ubsan_major		0
%define		libubsan		%mklibname ubsan %{ubsan_major}
%define		libubsan_devel		%mklibname ubsan -d
%define		libubsan_static_devel	%mklibname ubsan -d -s
%define		multilibubsan		libubsan%{ubsan_major}
%define		vtv_major		0
%define		libvtv			%mklibname vtv %{vtv_major}
%define		libvtv_devel		%mklibname vtv -d
%define		libvtv_static_devel	%mklibname vtv -d -s
%define		multilibvtv		libvtv%{vtv_major}
%define		lsan_major		0
%define		liblsan			%mklibname lsan %{lsan_major}
%define		liblsan_devel		%mklibname lsan -d
%define		liblsan_static_devel	%mklibname lsan -d -s

#-----------------------------------------------------------------------
%define		build_ada		0
%define		build_asan		0
%define		build_check		0
%define		build_multilib		0
%define		build_go		0
%define		build_lto		1
%define		build_objc		0
%define		build_objcxx		0
%define		build_quadmath		0
%define		build_ssp		0
%ifarch	%{ix86} x86_64 %{arm}
%define		build_itm		1
%else
# aarch64 libitm support not implemented yet
%define		build_itm		0
%endif
%define		build_cloog		%{system_compiler}
%define		build_cxx		%{system_compiler}
%define		build_doc		0
%define		build_ffi		%{system_compiler}
%define		build_fortran		%{system_compiler}
%define		build_gomp		%{system_compiler}
# system_compiler && build_ffi
%ifarch %{ix86} x86_64 %{arm}
  %define	build_java		%{system_compiler}
%else
  %define	build_java		0
%endif
# need to build if major does not conflict with current system_compiler
%define		build_libgcc		%{system_compiler}
%define		build_pdf		%{build_doc}
%define		build_plugin		%{system_compiler}
%ifarch x86_64
  %define	build_multilib		%{system_compiler}
%endif
%ifarch %{ix86} x86_64
  %define	build_ada		%{system_compiler}
  %define	build_quadmath		%{system_compiler}
  %define	build_doc		1
# system_compiler && build_cxx
  %define	build_go		%{system_compiler}
%endif
%ifarch %{ix86} x86_64 %{arm} aarch64
  %define	build_objc		%{system_compiler}
  %define	build_objcxx		%{system_compiler}
  %define	build_asan		%{system_compiler}
%endif

%define		build_doc		0
%define		build_pdf		0

%define		package_ffi		0

# Some versions of gcc build shared libgnat/libgnarl, some don't...
%define		shared_libgnat		1

# Adapted from fedora procedure:
#   If there is no usable gcc-java neither libgcj for the arch,
# on an arch that has it, run:
#	rpmbuild -bc --define "_topdir `pwd`" --with java_build_tar SPECS/gcc.spec
# which creates libjava-classes-@{version}-@{release}.tar.bz2
#   With the tarball on the new arch, run:
#	rpmbuild -ba --define "_topdir `pwd`" -v --with java_bootstrap SPECS/gcc.spec
%bcond_with	java_build_tar
%bcond_with	java_bootstrap

%bcond_with	x32_bootstrap

#-----------------------------------------------------------------------

Summary:	GNU Compiler Collection
%if %{system_compiler}
Name:		gcc
%else
Name:		gcc%{branch}
%endif
Release:	5
License:	GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group:		Development/C
Url:		http://gcc.gnu.org/
%if "%{linaro}" != ""
Version:	%{ver}_%{linaro}
%if "%{linaro_spin}" != ""
Source0:	http://cbuild.validation.linaro.org/snapshots/gcc-linaro-%{branch}-%{linaro}-%{linaro_spin}.tar.xz
%else
Source0:	http://cbuild.validation.linaro.org/snapshots/gcc-linaro-%{branch}-%{linaro}.tar.xz
%endif
%else
Version:	%{ver}
%if %{official}
  #http://www.gnu.org/prep/ftp.html ...
Source0:	gcc-%{version}.tar.bz2
Source1:	gcc-%{version}.tar.bz2.sig
%else
  # http://gcc.gnu.org/mirrors.html
  # <<mirror>>/snapshots/@{branch}@{snapshot}/
Source0:	gcc-%{branch}%{snapshot}.tar.bz2
Source1:	md5.sum
%endif
%endif
Source4:	c89
Source5:	c99
%if %{with java_bootstrap}
Source6:	libjava-classes-%{version}-%{release}.tar.bz2
%endif
Source7:	gcc-x32-seed.tar.xz

Source100:	%{name}.rpmlintrc

Patch0:		gcc-4.7.1-uclibc-ldso-path.patch
Patch1:		gcc-4.6.0-java-nomulti.patch
Patch2:		gcc-4.8-aarch64-ld-path.patch
Patch3:		gcc-4.7.1-linux32.patch
Patch4:		gnatmake-execstack.patch
# http://gcc.gnu.org/bugzilla/show_bug.cgi?id=55930
Patch5:		gcc-4.8-disable-dependency-tracking.patch
Patch6:		gcc-4.7.1-autoconf-2.69.patch
Patch7:		gcc-4.7.1-linker-plugin-detect.patch
Patch8:		gcc-4.7.1-extern-inline-not-inlined.patch
# Patch for Android compatibility (creating Linux->Android crosscompilers etc)
Patch9:		gcc-4.7-androidcompat.patch
Patch10:	gcc-4.7.3-texinfo-5.0.patch
# Fix build failure
Patch11:	gcc-4.8-istream-ignore.patch
Patch12:	gcc-4.8-non-fatal-compare-failure.patch
# https://bugs.launchpad.net/gcc-linaro/+bug/1225317
Patch13:	Gcc-4.8.2-arm-thumb2-CASE_VECTOR_SHORTEN_MODE.patch

BuildRequires:	binutils >= 2.20.51.0.2
BuildRequires:	dejagnu
BuildRequires:	elfutils-devel >= 0.147
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gdb
BuildRequires:	gettext
BuildRequires:	sharutils
BuildRequires:	texinfo
%if %{build_doc}
BuildRequires:	texi2html
%endif
%if %{build_pdf}
BuildRequires:	texlive
%endif
BuildRequires:	gmp-devel
BuildRequires:	mpfr-devel
BuildRequires:	libmpc-devel
BuildRequires:	pkgconfig(zlib)
%if %{build_cloog}
BuildRequires:	ppl-devel >= 0.11
BuildRequires:	ppl_c-devel >= 0.11
BuildRequires:	pkgconfig(cloog-isl)
BuildRequires:	pkgconfig(isl)
%endif

%if %{system_compiler}
Requires:	gcc-cpp >= %{EVRD}
Requires:	libgcc >= %{EVRD}
Requires:	libgomp >= %{EVRD}
%endif
Requires:	binutils >= 2.20.51.0.2
# Ensure https://qa.mandriva.com/show_bug.cgi?id=62943
# have been addressed if using an older version
Requires:	glibc-devel >= 2.13

%ifarch armv7l armv7hl
# find-provides fail to provide devel(libgcc_s) because it is a linker script
Provides:	devel(libgcc_s) = %{EVRD}
%endif

Obsoletes:	%{_lib}mudflap0 < 4.9.1_2014.05
Obsoletes:	%{_lib}mudflap-devel < 4.9.1_2014.05
Obsoletes:	%{_lib}mudflap-static-devel < 4.9.1_2014.05

%description
The gcc package contains the GNU Compiler Collection version %{branch}.

%files
%if %{system_compiler}
%{_bindir}/cc
%{_bindir}/c89
%{_bindir}/c99
%{_bindir}/gcc
%{_bindir}/gcc-ar
%{_bindir}/gcc-nm
%{_bindir}/gcc-ranlib
%{_bindir}/gcov
%{_bindir}/%{_target_platform}-gcc
%{_bindir}/%{_target_platform}-gcc-ar
%{_bindir}/%{_target_platform}-gcc-nm
%{_bindir}/%{_target_platform}-gcc-ranlib
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man7/*
%{_localedir}/*/LC_MESSAGES/gcc.mo
%{_infodir}/gcc.info*
%{_infodir}/gccint.info*
%{_infodir}/gccinstall.info*
%{_libdir}/libgcc_s.so
%if %{build_multilib}
%{multilibdir}/libgcc_s.so
%endif
%endif
%{_bindir}/gcc-%{ver}
%{_bindir}/%{_target_platform}-gcc-%{ver}
%dir %{gccdir}
%{gcclibexecdir}/cc1
%{gcclibexecdir}/collect2
%{gccdir}/*.o
%{gccdir}/libgcc*.a
%{gccdir}/libgcov.a
%if %{build_lto}
%{gcclibexecdir}/lto*
%{gcclibexecdir}/liblto*
%endif
%dir %{gccdir}/include
%{gccdir}/include/*.h
%if %{build_java}
%exclude %{gccdir}/include/jawt*.h
%exclude %{gccdir}/include/jni*.h
%exclude %{gccdir}/include/jvm*.h
%endif
%{gcclibexecdir}/install-tools
%if "%{gcclibexecdir}" != "%{gccdir}"
%{gccdir}/install-tools
%endif
%if %{build_quadmath}
%exclude %{gccdir}/include/quadmath*.h
%endif
%if %{build_gomp}
%exclude %{gccdir}/include/omp*.h
%endif
%if %{build_multilib}
%dir %{multigccdir}
%{multigccdir}/*.o
%{multigccdir}/libgcc*.a
%{multigccdir}/libgcov.a
%endif
%if %{build_doc}
%doc %{_docdir}/gcc
%endif
%if %{build_check}
%doc %{_docdir}/gcc/test_summary.log
%endif

########################################################################
%if %{build_libgcc}
#-----------------------------------------------------------------------

%package -n %{libgcc}
Summary:	GNU C library
Group:		System/Libraries
%if "%{libgcc}" != "libgcc"
Provides:	libgcc = %{EVRD}
%endif

%description -n %{libgcc}
The %{libgcc} package contains GCC shared libraries for gcc %{branch}

%files -n %{libgcc}
/%{_lib}/libgcc_s.so.%{gcc_major}

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibgcc}
Summary:	GNU C library
Group:		System/Libraries
Conflicts:	%{libgcc} < 4.6.2-11

%description -n %{multilibgcc}
The %{multilibgcc} package contains GCC shared libraries for gcc %{branch}

%files -n %{multilibgcc}
%{multirootlibdir}/libgcc_s.so.%{gcc_major}
%endif

#-----------------------------------------------------------------------
# build libgcc
%endif

########################################################################
%if %{build_plugin}
#-----------------------------------------------------------------------

%package plugin-devel
Summary:	Headers to build gcc plugins
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	gmp-devel
Requires:	mpfr-devel
Requires:	libmpc-devel
Requires:	ppl-devel
Requires:	ppl_c-devel

%description plugin-devel
This package contains header files and other support files
for compiling GCC plugins. The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%files plugin-devel
%{gccdir}/plugin
%if "%{gccdir}" != "%{gcclibexecdir}"
%{gcclibexecdir}/plugin
%endif

#-----------------------------------------------------------------------
# build_plugin
%endif

########################################################################
%if %{system_compiler}
#-----------------------------------------------------------------------

%package cpp
Summary:	The C Preprocessor
Group:		Development/C
Provides:	cpp = %{EVRD}
Requires:	%{name} = %{EVRD}

%description cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities:

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

%files cpp
/lib/cpp
%{_bindir}/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%if %{build_doc}
%doc %{_docdir}/gcc-cpp
%endif
%{_localedir}/*/LC_MESSAGES/cpplib.mo

#-----------------------------------------------------------------------
# system_compiler
%endif

########################################################################
%if %{build_cxx}
#-----------------------------------------------------------------------

%package c++
Summary:	C++ support for gcc
Group:		Development/C++
Requires:	%{name} = %{EVRD}
%if %{system_compiler}
Requires:	%{libstdcxx_devel} = %{version}
%endif

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%files c++
%if %{system_compiler}
%{_bindir}/c++
%{_bindir}/g++
%{_bindir}/%{_target_platform}-c++
%{_bindir}/%{_target_platform}-g++
%{_mandir}/man1/g++.1*
%endif
%{_bindir}/c++-%{ver}
%{_bindir}/g++-%{ver}
%{_bindir}/%{_target_platform}-g++-%{ver}
%{gcclibexecdir}/cc1plus

#-----------------------------------------------------------------------

%package -n %{libstdcxx}
Summary:	GNU Standard C++ library
Group:		System/Libraries
%if "%{libstdcxx}" != "libstdc++"
Provides:	libstdc++ = %{EVRD}
%endif
%if %{build_doc}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif

%description -n %{libstdcxx}
The libstdc++ package contains a rewritten standard compliant
GCC Standard C++ Library.

%files -n %{libstdcxx}
/%{_lib}/libstdc++.so.%{stdcxx_major}*
%if %{system_compiler}
%{_localedir}/*/LC_MESSAGES/libstdc++.mo
%endif

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibstdcxx}
Summary:	GNU Standard C++ library
Group:		System/Libraries
Conflicts:	%{libstdcxx} < 4.6.2-11

%description -n %{multilibstdcxx}
The libstdc++ package contains a rewritten standard compliant
GCC Standard C++ Library.

%files -n %{multilibstdcxx}
%{multirootlibdir}/libstdc++.so.%{stdcxx_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libstdcxx_devel}
Summary:	Header files and libraries for C++ development
Group:		Development/C++
Requires:	%{libstdcxx} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibstdcxx} = %{EVRD}
%endif
%if "%{libstdcxx_devel}" != "libstdc++-devel"
Provides:	libstdc++-devel = %{EVRD}
%endif
Provides:	stdc++-devel = %{EVRD}
%if "%{ver}" != "%{version}"
# 4.7.2_2010.10 should provide 4.7.2 so clang can pick up the dep
%if "%{libstdcxx_devel}" != "libstdc++-devel"
Provides:	%{libstdcxx_devel} = %{ver}-%{release}
%endif
Provides:	libstdc++-devel = %{ver}-%{release}
Provides:	stdc++-devel = %{ver}-%{release}
%endif
# We don't want to pull in an entire Python environment just because of
# libstdc++'s python based gdb plugin...
%define __noautoreq '.*python.*'

%description -n %{libstdcxx_devel}
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%files -n %{libstdcxx_devel}
%{_includedir}/c++/%{ver}
%{_libdir}/libstdc++.so
%{_datadir}/gdb/auto-load%{_libdir}/libstdc++.*.py
%if %{build_multilib}
%{multilibdir}/libstdc++.so
%{_datadir}/gdb/auto-load%{multilibdir}/libstdc++.*.py
%endif
%{py_puresitedir}/libstdcxx
%if %{build_doc}
%doc %{_docdir}/libstdc++
%endif

#-----------------------------------------------------------------------

%package -n %{libstdcxx_static_devel}
Summary:	Static libraries for the GNU standard C++ library
Group:		Development/C++
Requires:	%{libstdcxx_devel} = %{EVRD}
%if "%{libstdcxx_static_devel}" != "libstdc++-static-devel"
Provides:	libstdc++-static-devel = %{EVRD}
%endif
Provides:	stdc++-static-devel = %{EVRD}

%description -n %{libstdcxx_static_devel}
Static libraries for the GNU standard C++ library.

%files -n %{libstdcxx_static_devel}
%{_libdir}/libstdc++.*a
%{_libdir}/libsupc++.*a
%if %{build_multilib}
%{multilibdir}/libstdc++.*a
%{multilibdir}/libsupc++.*a
%endif

#-----------------------------------------------------------------------
# build_cxx
%endif

########################################################################
%if %{build_ada}
#-----------------------------------------------------------------------

%package gnat
Summary:	Ada 95 support for gcc
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Requires:	%{libgnat_devel} = %{EVRD}
# no bootstrap support
BuildRequires:	gcc-gnat >= 3.1, libgnat >= 3.1

%description gnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes development
tools, the documents and Ada 95 compiler.

%files gnat
%{_bindir}/gnat*
%if %{build_java}
%exclude %{_bindir}/gnative2ascii
%endif
%{gcclibexecdir}/gnat1
%{_infodir}/gnat*
%if %{build_doc}
%doc %{_docdir}/gcc-gnat
%endif

# libgnat and libgnarl are static-only these days
%if %{shared_libgnat}
#-----------------------------------------------------------------------

%package -n %{libgnat}
Summary:	GNU Ada 95 runtime libraries
Group:		System/Libraries
Provides:	libgnat = %{EVRD}
Obsoletes:	gnat-runtime < %{EVRD}

%description -n %{libgnat}
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared
libraries, which are required to run programs compiled with the GNAT.

%files -n %{libgnat}
%{_libdir}/libgnat-%{branch}.so.%{gnat_major}
%{_libdir}/libgnarl-%{branch}.so.%{gnat_major}

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibgnat}
Summary:	GNU Ada 95 runtime libraries
Group:		System/Libraries
Conflicts:	%{libgnat} < 4.6.2-11

%description -n %{multilibgnat}
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared
libraries, which are required to run programs compiled with the GNAT.

%files -n %{multilibgnat}
%{multilibdir}/libgnat-%{branch}.so.%{gnat_major}
%{multilibdir}/libgnarl-%{branch}.so.%{gnat_major}
%endif
%endif

#-----------------------------------------------------------------------

%package -n %{libgnat_devel}
Summary:	GNU Ada 95 libraries
Group:		Development/Other
%if %{shared_libgnat}
Requires:	%{libgnat} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibgnat} = %{EVRD}
%endif
%else
Obsoletes:	%{libgnat} < %{EVRD}
Obsoletes:	%{multilibgnat} < %{EVRD}
Requires:	%{libgnat_static_devel} = %{EVRD}
%endif
Provides:	libgnat-devel = %{EVRD}
Provides:	gnat-devel = %{EVRD}

%description -n %{libgnat_devel}
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared
libraries, which are required to compile with the GNAT.

%files -n %{libgnat_devel}
%if %{shared_libgnat}
%{_libdir}/libgnat*.so
%{_libdir}/libgnarl*.so
%endif
%{gccdir}/adalib
%{gccdir}/adainclude
%exclude %{gccdir}/adalib/lib*.a
%if %{build_multilib}
%if %{shared_libgnat}
%{multilibdir}/libgnat*.so
%{multilibdir}/libgnarl*.so
%endif
%{multigccdir}/adalib
%{multigccdir}/adainclude
%exclude %{multigccdir}/adalib/lib*.a
%endif

#-----------------------------------------------------------------------

%package -n %{libgnat_static_devel}
Summary:	GNU Ada 95 static libraries
Group:		Development/Other
Requires:	%{libgnat_devel} = %{EVRD}
Provides:	libgnat-static-devel = %{EVRD}
Provides:	gnat-static-devel = %{EVRD}

%description -n %{libgnat_static_devel}
GNAT is a GNU Ada 95 front-end to GCC. This package includes static
libraries.

%files -n %{libgnat_static_devel}
%{gccdir}/adalib/lib*.a
%if %{build_multilib}
%{multigccdir}/adalib/lib*.a
%endif
#-----------------------------------------------------------------------
# build ada
%endif

########################################################################
%if %{build_fortran}
#-----------------------------------------------------------------------

%package gfortran
Summary:	Fortran 95 support for gcc
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Requires:	%{libgfortran_devel} = %{EVRD}

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%files gfortran
%{_bindir}/gfortran
%{_bindir}/gfortran-%{ver}
%{_bindir}/%{_target_platform}-gfortran
%{_bindir}/%{_target_platform}-gfortran-%{ver}
%{_infodir}/gfortran.info*
%{_mandir}/man1/gfortran.1*
%{gcclibexecdir}/f951
%{gccdir}/finclude
%{gccdir}/libgfortranbegin.*a
%{gccdir}/libcaf_single.a
%if %{build_multilib}
%{multigccdir}/libgfortranbegin.a
%{multigccdir}/libcaf_single.a
%endif
%if %{build_doc}
%doc %{_docdir}/gcc-gfortran
%endif

#-----------------------------------------------------------------------

%package -n %{libgfortran}
Summary:	Fortran 95 runtime libraries
Group:		System/Libraries
%if %{build_quadmath}
Requires:	%{libquadmath} = %{EVRD}
%endif
Provides:	libgfortran = %{EVRD}
%if %{build_multilib}
Provides:	%{multilibgfortran} = %{EVRD}
%endif

%description -n %{libgfortran}
This package contains Fortran 95 shared library which is needed to run
Fortran 95 dynamically linked programs.

%files -n %{libgfortran}
%{_libdir}/libgfortran.so.%{gfortran_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibgfortran}
Summary:	Fortran 95 runtime libraries
Group:		System/Libraries
%if %{build_quadmath}
Requires:	%{multilibquadmath} = %{EVRD}
%endif
Conflicts:	%{libgfortran} < 4.6.2-11

%description -n %{multilibgfortran}
This package contains Fortran 95 shared library which is needed to run
Fortran 95 dynamically linked programs.

%files -n %{multilibgfortran}
%{multilibdir}/libgfortran.so.%{gfortran_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libgfortran_devel}
Summary:	Fortran 95 libraries
Group:		System/Libraries
Requires:	%{libgfortran} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibgfortran} = %{EVRD}
%endif
%if %{build_quadmath}
Requires:	%{libquadmath_devel} = %{EVRD}
%endif
Provides:	libgfortran-devel = %{EVRD}
Provides:	gfortran-devel = %{EVRD}

%description -n %{libgfortran_devel}
This package contains Fortran 95 shared library which is needed to
compile Fortran 95 programs.

%files -n %{libgfortran_devel}
%{_libdir}/libgfortran.so
%{_libdir}/libgfortran.spec
%if %{build_multilib}
%{multilibdir}/libgfortran.so
%{multilibdir}/libgfortran.spec
%endif

#-----------------------------------------------------------------------

%package -n %{libgfortran_static_devel}
Summary:	Fortran 95 static libraries
Group:		System/Libraries
Requires:	%{libgfortran_devel} = %{EVRD}
Provides:	libgfortran-static-devel = %{EVRD}
Provides:	gfortran-static-devel = %{EVRD}

%description -n %{libgfortran_static_devel}
This package contains Fortran 95 static library which is needed to
compile Fortran 95 programs.

%files -n %{libgfortran_static_devel}
%{_libdir}/libgfortran.*a
%if %{build_multilib}
%{multilibdir}/libgfortran.*a
%endif
#-----------------------------------------------------------------------
# build fortran
%endif

########################################################################
%if %{build_go}
#-----------------------------------------------------------------------

%package go
Summary:	Go support for gcc
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Requires:	%{libgo_devel} = %{EVRD}
BuildRequires:	gcc-go

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%files go
%{_bindir}/gccgo
%{_bindir}/%{_target_platform}-gccgo
%dir %{_libdir}/go
%if %{build_multilib}
%dir %{multilibdir}/go
%endif
%{_infodir}/gccgo.info*
%{_mandir}/man1/gccgo.1*
%{_bindir}/gccgo-%{ver}
%{_bindir}/%{_target_platform}-gccgo-%{ver}
%{gcclibexecdir}/go1
%{_libdir}/go/%{ver}
%{_libdir}/libgobegin.a
%if %{build_multilib}
%{multilibdir}/go/%{ver}
%{multilibdir}/libgobegin.a
%endif
%if %{build_doc}
%doc %{_docdir}/gcc-go
%endif

#-----------------------------------------------------------------------

%package -n %{libgo}
Summary:	Go runtime libraries
Group:		System/Libraries
Provides:	libgo = %{EVRD}

%description -n %{libgo}
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%files -n %{libgo}
%{_libdir}/libgo.so.%{go_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibgo}
Summary:	Go runtime libraries
Group:		System/Libraries
Conflicts:	%{libgo} < 4.6.2-11

%description -n %{multilibgo}
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%files -n %{multilibgo}
%{multilibdir}/libgo.so.%{go_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libgo_devel}
Summary:	Go development libraries
Group:		Development/Other
Requires:	%{libgo} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibgo} = %{EVRD}
%endif
Provides:	libgo-devel = %{EVRD}
Provides:	go-devel = %{EVRD}

%description -n %{libgo_devel}
This package includes libraries and support files for compiling
Go programs.

%files -n %{libgo_devel}
%{_libdir}/libgo.so
%if %{build_multilib}
%{multilibdir}/libgo.so
%endif

#-----------------------------------------------------------------------

%package -n %{libgo_static_devel}
Summary:	Static Go libraries
Group:		Development/Other
Requires:	%{libgo_devel} = %{EVRD}
Provides:	libgo-static-devel = %{EVRD}
Provides:	go-static-devel = %{EVRD}

%description -n %{libgo_static_devel}
This package contains static Go libraries.

%files -n %{libgo_static_devel}
%{_libdir}/libgo.*a
%if %{build_multilib}
%{multilibdir}/libgo.*a
%endif

#-----------------------------------------------------------------------
# build go
%endif

########################################################################
%if %{build_java}
#-----------------------------------------------------------------------

%package java
Summary:	Java support for GCC
Group:		Development/Java
Requires:	%{name} = %{EVRD}
Requires:	%{libgcj_devel} = %{EVRD}
Requires:	ecj
BuildRequires:	ecj
BuildRequires:	jpackage-utils
BuildRequires:	unzip
BuildRequires:	zip

%description java
This package adds support for compiling Java(tm) programs and
bytecode into native code.

%files java
%{_bindir}/aot-compile
%{_bindir}/gc-analyze
%{_bindir}/gcj
%{_bindir}/gcj-dbtool
%{_bindir}/gcjh
%{_bindir}/gjavah
%{_bindir}/gjar
%{_bindir}/gjarsigner
%if %{without java_bootstrap}
%{_bindir}/gjdoc
%endif
%{_bindir}/gnative2ascii
%{_bindir}/grmic
%{_bindir}/gserialver
%{_bindir}/jcf-dump
%{_bindir}/jv-convert
%{_bindir}/rebuild-gcj-db
%{_mandir}/man1/aot-compile.1*
%{_mandir}/man1/gc-analyze.1*
%{_mandir}/man1/gcj.1*
%{_mandir}/man1/gcj-dbtool.1*
%{_mandir}/man1/gcjh.1*
%{_mandir}/man1/gjar.1*
%{_mandir}/man1/gjarsigner.1*
%{_mandir}/man1/gjavah.1*
%{_mandir}/man1/gjdoc.1*
%{_mandir}/man1/gnative2ascii.1*
%{_mandir}/man1/grmic.1*
%{_mandir}/man1/gserialver.1*
%{_mandir}/man1/jcf-dump.1*
%{_mandir}/man1/jv-convert.1*
%{_mandir}/man1/rebuild-gcj-db.1*
%{_infodir}/gcj.info*
%{_infodir}/cp-tools.info*
%{_bindir}/gcj-%{ver}
%{_bindir}/%{_target_platform}-gcj
%{_bindir}/%{_target_platform}-gcj-%{ver}
%{_bindir}/%{_target_platform}-gcjh
%{gcclibexecdir}/jc1
%{gcclibexecdir}/ecj1
%{gcclibexecdir}/jvgenmain
%if %{build_doc}
%doc %{_docdir}/gcc-java
%endif

#-----------------------------------------------------------------------

%package -n %{libgcj}
Summary:	Java runtime library for gcc (platform dependent parts)
Group:		System/Libraries
Provides:	libgcj = %{EVRD}
%if %{build_multilib}
# for compatibility and/or make updates clean
Provides:	libgcj%{gcj_major} = %{EVRD}
%endif
Requires:	zip >= 2.1
Requires:	libgcj-java >= %{EVRD}
%if %{without java_bootstrap}
# We need antlr
BuildRequires:	antlr-tool
%endif
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libart-2.0)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	spec-helper >= 0.31.10

%description -n %{libgcj}
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%files -n %{libgcj}
%dir %{_libdir}/gcj-%{ver}-%{gcj_major}
%{_libdir}/gcj-%{ver}-%{gcj_major}/*.so
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_libdir}/gcj-%{ver}-%{gcj_major}/classmap.db
%{_libdir}/libgcj.so.%{gcj_major}*
%{_libdir}/libgcj-tools.so.%{gcj_major}*
%{_libdir}/libgij.so.%{gcj_major}*

#-----------------------------------------------------------------------

%package -n %{libgcj_bc}
Summary:	Java runtime library for gcc
Group:		System/Libraries
%if %{build_multilib}
Provides:	libgcj_bc%{gcj_bc_major} = %{EVRD}
%endif
Conflicts:	%{_lib}gcj13 < 4.7.3_2012.10-4
Conflicts:	%{_lib}gcj15 < 4.9.1_2014.05-2

%description -n %{libgcj_bc}
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%files -n %{libgcj_bc}
%{_libdir}/libgcj_bc.so.%{gcj_bc_major}*

#-----------------------------------------------------------------------

%package -n libgcj-java
Summary:	Java runtime library for gcc (Java parts)
Group:		System/Libraries
Conflicts:	%{_lib}gcj13 < 4.7.3_2012.10-4
Requires:	%{libgcj} = %{EVRD}

%description -n libgcj-java
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%files -n libgcj-java
%{_javadir}/libgcj*.jar

#-----------------------------------------------------------------------

%package -n gcj-tools
Summary:	Tools needed to use applications in the GCJ Java runtime
Group:		System/Libraries
Requires:	%{libgcj} = %{EVRD}
Requires:	zip >= 2.1

%description -n gcj-tools
Tools needed to run applications in the GCJ Java(tm) runtime. You will
need this package to run your Java programs in the Java Virtual Machine
(JVM) provided by the GNU Compiler Collection (gcj).

%files -n gcj-tools
%{_bindir}/gappletviewer
%{_bindir}/gij
%{_bindir}/grmid
%{_bindir}/grmiregistry
%{_bindir}/gtnameserv
%{_bindir}/gkeytool
%{_bindir}/gorbd
%{_mandir}/man1/gappletviewer.1*
%{_mandir}/man1/gij.1*
%{_mandir}/man1/grmiregistry.1*
%{_mandir}/man1/gkeytool.1*
%{_mandir}/man1/gorbd.1*
%{_mandir}/man1/grmid.1*
%{_mandir}/man1/gtnameserv.1*
%{_libdir}/logging.properties
%{_libdir}/security
%if %{build_pdf}
%doc %{_docdir}/libjava
%endif

#-----------------------------------------------------------------------

%package -n %{libgcj_devel}
Summary:	Libraries for Java development using GCC
Group:		Development/Java
Requires:	%{libgcj} = %{EVRD}
Requires:	%{libgcj_bc} = %{EVRD}
Requires:	awk
Requires:	pkgconfig(zlib)
Provides:	libgcj-devel = %{EVRD}
Provides:	gcj-devel = %{EVRD}

%description -n %{libgcj_devel}
The Java(tm) static libraries and C header files. You will need this
package to compile your Java programs using the GCC Java compiler (gcj).

%files -n %{libgcj_devel}
%{gccdir}/include/gcj
%{gccdir}/include/jawt*.h
%{gccdir}/include/jni*.h
%{gccdir}/include/jvm*.h
%{py_puresitedir}/libjava
%{_libdir}/pkgconfig/libgcj-%{branch}.pc
%{_libdir}/libgcj*.spec
%{_libdir}/libgcj*.so
%{_libdir}/libgij.so

#-----------------------------------------------------------------------

%package -n libgcj%{gcj_major}-src
Summary:	Java library sources
Group:		Development/Java
Requires:	%{libgcj} = %{EVRD}
Provides:	libgcj-src = %{EVRD}

%description -n libgcj%{gcj_major}-src
The Java(tm) runtime library sources.

%files -n libgcj%{gcj_major}-src
%{_javadir}/src-%{ver}.zip

#-----------------------------------------------------------------------
# build java
%endif

########################################################################
%if %{build_objc}
#-----------------------------------------------------------------------

%package objc
Summary:	Objective-C support for GCC
Group:		Development/Other
Requires:	%{name} = %{EVRD}
Requires:	%{libobjc_devel} = %{EVRD}

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%files objc
%{gcclibexecdir}/cc1obj

#-----------------------------------------------------------------------

%package -n %{libobjc}
Summary:	Objective-C runtime
Group:		System/Libraries
Provides:	libobjc = %{EVRD}

%description -n %{libobjc}
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%files -n %{libobjc}
%{_libdir}/libobjc.so.%{objc_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibobjc}
Summary:	Objective-C runtime
Group:		System/Libraries
Provides:	libobjc = %{EVRD}
Conflicts:	%{libobjc} < 4.6.2-11

%description -n %{multilibobjc}
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%files -n %{multilibobjc}
%{multilibdir}/libobjc.so.%{objc_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libobjc_devel}
Summary:	Objective-C development libraries
Group:		Development/Other
Requires:	%{libobjc} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibobjc} = %{EVRD}
%endif
Provides:	libobjc-devel = %{EVRD}
Provides:	objc-devel = %{EVRD}

%description -n %{libobjc_devel}
This package includes libraries and support files for compiling
Objective-C programs.

%files -n %{libobjc_devel}
%{_libdir}/libobjc.so
%{gccdir}/include/objc
%if %{build_multilib}
%{multilibdir}/libobjc.so
%endif

#-----------------------------------------------------------------------

%package -n %{libobjc_static_devel}
Summary:	Static Objective-C libraries
Group:		Development/Other
Requires:	%{libobjc_devel} = %{EVRD}
Provides:	libobjc-static-devel = %{EVRD}
Provides:	objc-static-devel = %{EVRD}

%description -n %{libobjc_static_devel}
This package contains static Objective-C libraries.

%files -n %{libobjc_static_devel}
%{_libdir}/libobjc.*a
%if %{build_multilib}
%{multilibdir}/libobjc.*a
%endif
#-----------------------------------------------------------------------
# build objc
%endif

########################################################################
%if %{build_objcxx}
#-----------------------------------------------------------------------

%package objc++
Summary:	Objective-C++ support for GCC
Group:		Development/Other
Requires:	gcc-objc = %{EVRD}

%description objc++
gcc++-objc provides Objective-C++ support for the GCC.

%files objc++
%{gcclibexecdir}/cc1objplus
#-----------------------------------------------------------------------
# build objcxx
%endif

########################################################################
%if %{package_ffi}
#-----------------------------------------------------------------------

%package -n %{libffi}
Summary:	GCC support library for FFI
Group:		System/Libraries
Provides:	libffi = %{EVRD}

%description -n %{libffi}
This package contains GCC shared support library which is needed
for FFI support.

%files -n %{libffi}
%{_libdir}/libffi.so.%{ffi_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibffi}
Summary:	GCC support library for FFI
Group:		System/Libraries
Conflicts:	%{libffi} < 4.6.2-11

%description -n %{multilibffi}
This package contains GCC shared support library which is needed
for FFI support.

%files -n %{multilibffi}
%{multirootlibdir}/libffi.so.%{ffi_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libffi_devel}
Summary:	GCC development for FFI
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libffi} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibffi} = %{EVRD}
%endif
Provides:	libffi-devel = %{EVRD}
Provides:	ffi-devel = %{EVRD}

%description -n %{libffi_devel}
This package contains GCC development which is needed
to compile FFI support.

%files -n %{libffi_devel}
%{_libdir}/libffi.so
%if %{build_multilib}
%{multilibdir}/libffi.so
%endif
%{_mandir}/man3/*.3*

#-----------------------------------------------------------------------

%package -n %{libffi_static_devel}
Summary:	GCC FFI static library
Group:		Development/C
Requires:	%{libffi_devel} = %{EVRD}
Provides:	libffi-static-devel = %{EVRD}
Provides:	ffi-static-devel = %{EVRD}

%description -n %{libffi_static_devel}
This package contains GCC static libraries which are needed
to compile FFI support.

%files -n %{libffi_static_devel}
%{_libdir}/libffi.*a
%if %{build_multilib}
%{multilibdir}/libffi.*a
%endif

#-----------------------------------------------------------------------
# package ffi
%endif

########################################################################
%if %{build_quadmath}
#-----------------------------------------------------------------------

%package -n %{libquadmath}
Summary:	GCC __float128 shared support library
Group:		System/Libraries
Provides:	libquadmath = %{EVRD}

%description -n %{libquadmath}
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%files -n %{libquadmath}
%{_libdir}/libquadmath.so.%{quadmath_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibquadmath}
Summary:	GCC __float128 shared support library
Group:		System/Libraries
Conflicts:	%{libquadmath} < 4.6.2-11

%description -n %{multilibquadmath}
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%files -n %{multilibquadmath}
%{multilibdir}/libquadmath.so.%{quadmath_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libquadmath_devel}
Summary:	GCC __float128 support
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libquadmath} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibquadmath} = %{EVRD}
%endif
Provides:	libquadmath-devel = %{EVRD}
Provides:	quadmath-devel = %{EVRD}

%description -n %{libquadmath_devel}
This package contains support for building Fortran programs using
REAL*16 and programs using __float128 math.

%files -n %{libquadmath_devel}
%{_libdir}/libquadmath.so
%if %{build_multilib}
%{multilibdir}/libquadmath.so
%endif
%{_infodir}/libquadmath.info*
%{gccdir}/include/quadmath*.h
%if %{build_pdf}
%doc %{_docdir}/libquadmath
%endif

#-----------------------------------------------------------------------

%package -n %{libquadmath_static_devel}
Summary:	Static libraries for __float128 support
Group:		Development/C
Requires:	%{libquadmath_devel} = %{EVRD}
Provides:	libquadmath-static-devel = %{EVRD}
Provides:	quadmath-static-devel = %{EVRD}

%description -n %{libquadmath_static_devel}
This package contains static libraries for building Fortran programs
using REAL*16 and programs using __float128 math.

%files -n %{libquadmath_static_devel}
%{_libdir}/libquadmath.*a
%if %{build_multilib}
%{multilibdir}/libquadmath.*a
%endif

#-----------------------------------------------------------------------
# build quadmath
%endif

########################################################################
%if %{build_gomp}
#-----------------------------------------------------------------------

%package -n %{libgomp}
Summary:	GCC OpenMP v3.0 shared support library
Group:		System/Libraries
Provides:	libgomp = %{EVRD}

%description -n %{libgomp}
This package contains GCC shared library which is needed
for OpenMP v3.0 support.

%files -n %{libgomp}
/%{_lib}/libgomp.so.%{gomp_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibgomp}
Summary:	GCC OpenMP v3.0 shared support library
Group:		System/Libraries
Provides:	libgomp = %{EVRD}
Conflicts:	%{libgomp} < 4.6.2-11

%description -n %{multilibgomp}
This package contains GCC shared library which is needed
for OpenMP v3.0 support.

%files -n %{multilibgomp}
%{multirootlibdir}/libgomp.so.%{gomp_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libgomp_devel}
Summary:	GCC OpenMP v3.0 development support
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libgomp} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibgomp} = %{EVRD}
%endif
Provides:	libgomp-devel = %{EVRD}
Provides:	gomp-devel = %{EVRD}

%description -n %{libgomp_devel}
This package contains GCC development which is needed
to compile OpenMP v3.0 support.

%files -n %{libgomp_devel}
%{_libdir}/libgomp.so
%{_libdir}/libgomp.spec
%if %{build_multilib}
%{multilibdir}/libgomp.so
%{multilibdir}/libgomp.spec
%endif
%{_infodir}/libgomp.info*
%{gccdir}/include/omp*.h
%if %{build_pdf}
%doc %{_docdir}/libgomp
%endif

#-----------------------------------------------------------------------

%package -n %{libgomp_static_devel}
Summary:	GCC OpenMP v3.0 static library
Group:		Development/C
Requires:	%{libgomp_devel} = %{EVRD}
Provides:	libgomp-static-devel = %{EVRD}
Provides:	gomp-static-devel = %{EVRD}

%description -n %{libgomp_static_devel}
This package contains GCC static libraries which are needed
to compile OpenMP v3.0 support.

%files -n %{libgomp_static_devel}
%{_libdir}/libgomp.*a
%if %{build_multilib}
%{multilibdir}/libgomp.*a
%endif

#-----------------------------------------------------------------------
# build gomp
%endif

########################################################################
%if %{build_ssp}
#-----------------------------------------------------------------------

%package -n %{libssp}
Summary:	GCC SSP shared support library
Group:		System/Libraries
Provides:	libssp = %{EVRD}

%description -n %{libssp}
This package contains GCC shared support library which is needed
for SSP support.

%files -n %{libssp}
%{_libdir}/libssp.so.%{ssp_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibssp}
Summary:	GCC SSP shared support library
Group:		System/Libraries
Provides:	libssp = %{EVRD}
Conflicts:	%{libssp} < 4.6.2-11

%description -n %{multilibssp}
This package contains GCC shared support library which is needed
for SSP support.

%files -n %{multilibssp}
%{multilibdir}/libssp.so.%{ssp_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libssp_devel}
Summary:	GCC SSP development support
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libssp} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibssp} = %{EVRD}
%endif
Provides:	libssp-devel = %{EVRD}
Provides:	ssp-devel = %{EVRD}

%description -n %{libssp_devel}
This package contains GCC libraries which are needed
to compile SSP support.

%files -n %{libssp_devel}
%{_libdir}/libssp.so
%if %{build_multilib}
%{multilibdir}/libssp.so
%endif
%{gccdir}/include/ssp

#-----------------------------------------------------------------------

%package -n %{libssp_static_devel}
Summary:	GCC SSP static libraries
Group:		Development/C
Requires:	%{libssp_devel} = %{EVRD}
Provides:	libssp-static-devel = %{EVRD}
Provides:	ssp-static-devel = %{EVRD}

%description -n %{libssp_static_devel}
This package contains GCC static libraries which are needed
to compile SSP support.

%files -n %{libssp_static_devel}
%{_libdir}/libssp.*.*a
%if %{build_multilib}
%{multilibdir}/libssp.*.*a
%endif

#-----------------------------------------------------------------------
# build ssp
%endif

########################################################################
%if %{build_itm}
#-----------------------------------------------------------------------

%package -n %{libitm}
Summary:	GCC Transactional Memory support library
Group:		System/Libraries
Provides:	libitm = %{EVRD}

%description -n %{libitm}
This package contains GCC's Transactional Memory support library.

%files -n %{libitm}
%{_libdir}/libitm.so.%{itm_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibitm}
Summary:	GCC Transactional Memory support library
Group:		System/Libraries
Provides:	libitm = %{EVRD}

%description -n %{multilibitm}
This package contains GCC's Transactional Memory support library.

%files -n %{multilibitm}
%{multilibdir}/libitm.so.%{itm_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libitm_devel}
Summary:	GCC Transactional Memory development support
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libitm} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibitm} = %{EVRD}
%endif
Provides:	libitm-devel = %{EVRD}
Provides:	itm-devel = %{EVRD}

%description -n %{libitm_devel}
This package contains GCC libraries which are needed
to use Transactional Memory features.

%files -n %{libitm_devel}
%{_libdir}/libitm.so
%{_libdir}/libitm.spec
%if %{build_multilib}
%{multilibdir}/libitm.so
%{multilibdir}/libitm.spec
%endif
%{_infodir}/libitm.info*

#-----------------------------------------------------------------------

%package -n %{libitm_static_devel}
Summary:	GCC Transactional Memory static libraries
Group:		Development/C
Requires:	%{libitm_devel} = %{EVRD}
Provides:	libitm-static-devel = %{EVRD}
Provides:	itm-static-devel = %{EVRD}

%description -n %{libitm_static_devel}
This package contains GCC static libraries which are needed
to compile Transactional Memory support.

%files -n %{libitm_static_devel}
%{_libdir}/libitm.a
%if %{build_multilib}
%{multilibdir}/libitm.a
%endif

#-----------------------------------------------------------------------
# build itm
%endif

%if %{build_asan}
#-----------------------------------------------------------------------
# Address Sanitizer
#-----------------------------------------------------------------------
%package -n %{libasan}
Summary:	GCC Address Sanitizer library
Group:		Development/C

%description -n %{libasan}
GCC Address Sanitizer Library.

%files -n %{libasan}
%{_libdir}/libasan.so.%{asan_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibasan}
Summary:	GCC Address Sanitizer library
Group:		Development/C

%description -n %{multilibasan}
GCC Address Sanitizer Library.

%files -n %{multilibasan}
%{multilibdir}/libasan.so.%{asan_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libasan_devel}
Summary:	GCC Address Sanitizer development support
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libasan} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibasan} = %{EVRD}
%endif
Provides:	libasan-devel = %{EVRD}
Provides:	asan-devel = %{EVRD}

%description -n %{libasan_devel}
This package contains GCC libraries which are needed
to use Address Sanitizer features.

%files -n %{libasan_devel}
%{_libdir}/libasan.so
%{_libdir}/libasan_preinit.o
%if %{build_multilib}
%{multilibdir}/libasan.so
%{multilibdir}/libasan_preinit.o
%endif

#-----------------------------------------------------------------------

%package -n %{libasan_static_devel}
Summary:	Static libasan
Group:		Development/C
Requires:	%{libasan_devel} = %{EVRD}

%description -n %{libasan_static_devel}
Static libasan.

%files -n %{libasan_static_devel}
%{_libdir}/libasan.a
%if %{build_multilib}
%{multilibdir}/libasan.a
%endif
%endif

#-----------------------------------------------------------------------
# Thread Sanitizer
#-----------------------------------------------------------------------
%ifarch x86_64
%package -n %{libtsan}
Summary:	GCC Thread Sanitizer library
Group:		Development/C

%description -n %{libtsan}
GCC Address Sanitizer Library.

%files -n %{libtsan}
%{_libdir}/libtsan.so.%{tsan_major}*

#-----------------------------------------------------------------------

%package -n %{libtsan_devel}
Summary:	GCC Thread Sanitizer development support
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libtsan} = %{EVRD}
Provides:	libtsan-devel = %{EVRD}
Provides:	tsan-devel = %{EVRD}

%description -n %{libtsan_devel}
This package contains GCC libraries which are needed
to use Thread Sanitizer features.

%files -n %{libtsan_devel}
%{_libdir}/libtsan.so

#-----------------------------------------------------------------------

%package -n %{libtsan_static_devel}
Summary:	Static libtsan
Group:		Development/C
Requires:	%{libtsan_devel} = %{EVRD}

%description -n %{libtsan_static_devel}
Static libtsan.

%files -n %{libtsan_static_devel}
%{_libdir}/libtsan.a
%endif

#-----------------------------------------------------------------------
# Atomic operations
#-----------------------------------------------------------------------
%package -n %{libatomic}
Summary:	GCC Atomic operations library
Group:		Development/C

%description -n %{libatomic}
GCC Atomic operations Library.

%files -n %{libatomic}
%{_libdir}/libatomic.so.%{atomic_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibatomic}
Summary:	GCC Atomic optimizer library
Group:		Development/C

%description -n %{multilibatomic}
GCC Atomic optimizer Library.

%files -n %{multilibatomic}
%{_prefix}/lib/libatomic.so.%{atomic_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libatomic_devel}
Summary:	GCC Atomic optimizer development support
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libatomic} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibatomic} = %{EVRD}
%endif
Provides:	libatomic-devel = %{EVRD}
Provides:	atomic-devel = %{EVRD}

%description -n %{libatomic_devel}
This package contains GCC libraries which are needed
to use Atomic optimizer features.

%files -n %{libatomic_devel}
%{_libdir}/libatomic.so
%if %{build_multilib}
%{multilibdir}/libatomic.so
%endif

#-----------------------------------------------------------------------

%package -n %{libatomic_static_devel}
Summary:	Static libatomic
Group:		Development/C
Requires:	%{libatomic_devel} = %{EVRD}

%description -n %{libatomic_static_devel}
Static libatomic.

%files -n %{libatomic_static_devel}
%{_libdir}/libatomic.a
%if %{build_multilib}
%{multilibdir}/libatomic.a
%endif

########################################################################
# Intel CILK
########################################################################
%ifarch %{ix86} x86_64
%package -n %{libcilkrts}
Summary:	CILK (multithreading programming language) runtime
Group:		Development/C

%description -n %{libcilkrts}
CILK (multithreading programming language) runtime.

%files -n %{libcilkrts}
%{_libdir}/libcilkrts.so.%{cilk_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibcilkrts}
Summary:	CILK (multithreading programming language) runtime
Group:		Development/C

%description -n %{multilibcilkrts}
CILK (multithreading programming language) runtime.

%files -n %{multilibcilkrts}
%{_prefix}/lib/libcilkrts.so.%{cilk_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libcilkrts_devel}
Summary:	Development files for the CILK multithreading programming language
Group:		Development/C
Requires:	%{libcilkrts} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibcilkrts} = %{EVRD}
%endif
Provides:	libcilkrts-devel = %{EVRD}
Provides:	cilkrts-devel = %{EVRD}

%description -n %{libcilkrts_devel}
Development files for the CILK multithreading programming language.

%files -n %{libcilkrts_devel}
%{_libdir}/libcilkrts.so
%{_libdir}/libcilkrts.spec
%if %{build_multilib}
%{_prefix}/lib/libcilkrts.so
%{_prefix}/lib/libcilkrts.spec
%endif
%{gccdir}/include/cilk

#-----------------------------------------------------------------------

%package -n %{libcilkrts_static_devel}
Summary:	Static libcilkrts
Group:		Development/C
Requires:	%{libcilkrts_devel} = %{EVRD}

%description -n %{libcilkrts_static_devel}
Static libcilkrts.

%files -n %{libcilkrts_static_devel}
%{_libdir}/libcilkrts.a
%if %{build_multilib}
%{multilibdir}/libcilkrts.a
%endif
%endif

########################################################################
# VTV (VTable Verification)
########################################################################
%ifarch %{ix86} x86_64
%package -n %{libvtv}
Summary:	VTable Verification library
Group:		Development/C

%description -n %{libvtv}
VTable Verification library.

%files -n %{libvtv}
%{_libdir}/libvtv.so.%{vtv_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibvtv}
Summary:	VTable Verification library
Group:		Development/C

%description -n %{multilibvtv}
VTable Verification library.

%files -n %{multilibvtv}
%{_prefix}/lib/libvtv.so.%{vtv_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libvtv_devel}
Summary:	GCC VTable Verification development support
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libvtv} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibvtv} = %{EVRD}
%endif
Provides:	libvtv-devel = %{EVRD}
Provides:	vtv-devel = %{EVRD}

%description -n %{libvtv_devel}
This package contains GCC libraries which are needed
to use VTable Verification features.

%files -n %{libvtv_devel}
%{_libdir}/libvtv.so
%if %{build_multilib}
%{_prefix}/lib/libvtv.so
%endif

#-----------------------------------------------------------------------

%package -n %{libvtv_static_devel}
Summary:	Static libvtv
Group:		Development/C
Requires:	%{libvtv_devel} = %{EVRD}

%description -n %{libvtv_static_devel}
Static libvtv

%files -n %{libvtv_static_devel}
%{_libdir}/libvtv.a
%if %{build_multilib}
%{multilibdir}/libvtv.a
%endif
%endif

########################################################################
# UBSan (Undefined Behavior Sanitizer)
########################################################################
%package -n %{libubsan}
Summary:	Undefined Behavior Sanitizer library
Group:		Development/C

%description -n %{libubsan}
Undefined Behavior Sanitizer library.

%files -n %{libubsan}
%{_libdir}/libubsan.so.%{ubsan_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibubsan}
Summary:	Undefined Behavior Sanitizer library
Group:		Development/C

%description -n %{multilibubsan}
Undefined Behavior Sanitizer library.

%files -n %{multilibubsan}
%{_prefix}/lib/libubsan.so.%{ubsan_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libubsan_devel}
Summary:	GCC Undefined Behavior Sanitizer development support
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libubsan} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibubsan} = %{EVRD}
%endif
Provides:	libubsan-devel = %{EVRD}
Provides:	ubsan-devel = %{EVRD}

%description -n %{libubsan_devel}
This package contains GCC libraries which are needed
to use Undefined Behavior Sanitizer features.

%files -n %{libubsan_devel}
%{_libdir}/libubsan.so
%{_libdir}/libsanitizer.spec
%if %{build_multilib}
%{_prefix}/lib/libubsan.so
%{_prefix}/lib/libsanitizer.spec
%endif

#-----------------------------------------------------------------------

%package -n %{libubsan_static_devel}
Summary:	Static libubsan
Group:		Development/C
Requires:	%{libubsan_devel} = %{EVRD}

%description -n %{libubsan_static_devel}
Static libubsan.

%files -n %{libubsan_static_devel}
%{_libdir}/libubsan.a
%if %{build_multilib}
%{multilibdir}/libubsan.a
%endif

########################################################################
# LSan (Leak Sanitizer)
########################################################################
%ifarch x86_64
%package -n %{liblsan}
Summary:	Leak Sanitizer library
Group:		Development/C

%description -n %{liblsan}
Leak Sanitizer library.

%files -n %{liblsan}
%{_libdir}/liblsan.so.%{lsan_major}*

#-----------------------------------------------------------------------

%package -n %{liblsan_devel}
Summary:	GCC Leak Sanitizer development support
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{liblsan} = %{EVRD}
Provides:	liblsan-devel = %{EVRD}
Provides:	lsan-devel = %{EVRD}

%description -n %{liblsan_devel}
This package contains GCC libraries which are needed
to use Leak Sanitizer features.

%files -n %{liblsan_devel}
%{_libdir}/liblsan.so

#-----------------------------------------------------------------------

%package -n %{liblsan_static_devel}
Summary:	Static liblsan
Group:		Development/C
Requires:	%{liblsan_devel} = %{EVRD}

%description -n %{liblsan_static_devel}
Static liblsan.

%files -n %{liblsan_static_devel}
%{_libdir}/liblsan.a
%endif

########################################################################
%prep
%if "%{linaro}" != ""
%if "%{linaro_spin}" != ""
  %setup -q -n gcc-linaro-%{branch}-%{linaro}-%{linaro_spin}
%else
  %setup -q -n gcc-linaro-%{branch}-%{linaro}
%endif
%else
%if %{official}
  %setup -q -n gcc-%{version}%{snapshot}
%else
  %setup -q -n gcc-%{branch}%{snapshot}
%endif
%endif

%patch0 -p1 -b .uclibc~
%patch1 -p1 -b .java~
%patch2 -p1 -b .aarch64~
%patch3 -p1 -b .linux32~
%patch4 -p1 -b .execstack~
%patch5 -p1 -b .deptrack~
%patch6 -p1 -b .ac269~
%patch7 -p1 -b .plugindet~
# Breaks the build, see comment on bug 33763
#patch8 -p1 -b .ext_inline~
#patch9 -p1 -b .android~
#patch10 -p1 -b .texi50~
%patch11 -p1 -b .buildfix~
%patch12 -p1 -b .compare~
%patch13 -p1 -b .short

aclocal -I config
autoconf

echo %{vendor} > gcc/DEV-PHASE
%if !%{official}
    sed -i -e 's/4\.8\..*/%{version}/' gcc/BASE-VER
%endif

%if %{with java_bootstrap}
    tar xjf %{SOURCE6}
%endif

%if %{with x32_bootstrap}
    pushd gcc
        tar -xf %{SOURCE7}
        mkdir gnu
        ln -s /usr/include/gnu/stubs-64.h gnu/stubs-x32.h
    popd
%endif

#-----------------------------------------------------------------------
%build
# The -gdwarf-4 removal is a workaround for gcc bug #52420
OPT_FLAGS=`echo %{optflags} | \
    sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g' \
    -e 's/-m\(31\|32\|64\)//g' \
    -e 's/-fstack-protector//g' \
    -e 's/--param=ssp-buffer-size=4//' \
    -e 's/-gdwarf-4/-g/' \
    -e 's/-pipe//g'`
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`

# FIXME debugedit
[ ! -z "$TMP" ] && export TMP=`echo $TMP | sed -e 's|/$||'`
[ ! -z "x$TMPDIR" ] && export TMPDIR=`echo $TMPDIR | sed -e 's|/$||'`

LANGUAGES=c
%if %{build_ada}
    LANGUAGES="$LANGUAGES,ada"
%endif
%if %{build_cxx}
    LANGUAGES="$LANGUAGES,c++"
%endif
%if %{build_fortran}
    LANGUAGES="$LANGUAGES,fortran"
%endif
%if %{build_go}
    LANGUAGES="$LANGUAGES,go"
%endif
%if %{build_java}
    LANGUAGES="$LANGUAGES,java"
%endif
%if %{build_lto}
    LANGUAGES="$LANGUAGES,lto"
%endif
%if %{build_objc}
    LANGUAGES="$LANGUAGES,objc"
%endif
%if %{build_objcxx}
    LANGUAGES="$LANGUAGES,obj-c++"
%endif

BOOTSTRAP=bootstrap
%ifarch %{ix86} x86_64
    %if %{system_compiler}
        BOOSTRAP=profiledbootstrap
    %endif
%endif

mkdir BUILD
cd BUILD

CC=%{__cc} \
CFLAGS="$OPT_FLAGS" \
CXXFLAGS="$OPT_FLAGS" \
GCJFLAGS="$OPT_FLAGS" \
TCFLAGS="$OPT_FLAGS" \
XCFLAGS="$OPT_FLAGS" \
../configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
%if !%{build_java}
        --disable-libgcj \
%else
        --disable-libjava-multilib \
        --with-java-home=%{_jvmdir}/java-1.5.0-gcj-1.5.0.0/jre \
        --with-ecj-jar=%{_datadir}/java/eclipse-ecj.jar \
        --enable-java-awt=gtk \
        --enable-gtk-cairo \
%endif
%if !%{build_cloog}
        --without-cloog \
        --without-ppl \
%else
        --with-cloog \
        --with-ppl \
        --enable-cloog-backend=isl \
        --disable-cloog-version-check \
%endif
%if !%{build_ffi}
        --disable-libffi \
%endif
%if !%{build_gomp}
        --disable-libgomp \
%endif
%if !%{build_quadmath}
        --disable-libquadmath \
  %if %{build_fortran}
        --disable-libquadmath-support \
  %endif
%endif
%if !%{build_ssp}
        --disable-libssp \
%endif
        --disable-libunwind-exceptions \
        --disable-werror \
        --enable-__cxa_atexit \
        --enable-gold=default \
        --with-plugin-ld=%{_bindir}/ld \
%if %{system_compiler}
        --enable-bootstrap \
%endif
        --enable-checking=release \
        --enable-gnu-unique-object \
        --enable-languages="$LANGUAGES" \
        --enable-linker-build-id \
%if !%{build_plugin}
        --disable-plugin \
%else
        --enable-plugin \
        --enable-lto \
%endif
        --enable-shared \
%if !%{system_compiler}
        --disable-static \
%endif
        --enable-threads=posix \
        --with-system-zlib \
        --with-bugurl=%{bugurl} \
%ifarch %{ix86} x86_64
        --with-tune=generic \
%endif
%ifarch %{ix86}
        --with-arch=i586 \
%endif
%ifarch x86_64
  %if %{build_multilib}
        --with-arch_32=i586 \
    %if %{with x32_boostrap}
        --with-multilib-list=m32,m64,mx32 \
    %else
        --with-multilib-list=m32,m64 \
    %endif
  %else
        --disable-multilib \
  %endif
%endif
%ifarch armv5te
        --with-arch=armv5te \
%endif
%ifarch armv7l armv7hl
        --without-multilib \
        --disable-multilib \
        --with-cpu=cortex-a8 \
        --with-tune=cortex-a8 \
        --with-arch=armv7-a \
        --with-mode=thumb \
  %ifarch armv7l
        --with-float=softfp \
  %else
        --with-float=hard \
  %endif
        --with-fpu=vfpv3-d16 \
        --with-abi=aapcs-linux \
%endif
        --host=%{_target_platform} \
        --build=%{_build} \
        --target=%{_target_platform}

GCJFLAGS="$OPT_FLAGS" \
%make BOOT_CFLAGS="$OPT_FLAGS" $BOOTSTRAP
# GNATMAKE=gnatmake GNATBIND=gnatbind

%if %{build_pdf}
    %make pdf || :
%endif

%if %{build_doc}
    pushd host-%{_target_platform}/gcc
        %make html || :
        %if %{build_pdf}
            %make pdf || :
        %endif
    popd
%endif

%if %{with java_build_tar}
find libjava -name \*.h -type f | \
    xargs grep -l '// DO NOT EDIT THIS FILE - it is machine generated' \
    > libjava-classes.list
find libjava -name \*.class -type f >> libjava-classes.list
find libjava/testsuite -name \*.jar -type f >> libjava-classes.list
tar cf - -T libjava-classes.list | bzip2 -9 \
    > %{make_rpmlint_happy_sourcedir}/libjava-classes-%{version}-%{release}.tar.bz2
%endif

#-----------------------------------------------------------------------

%if %{build_check}
%check
echo ====================TESTING=========================
%{_bindir}/time %make -k check || true
echo "XXX check time above XXX"
contrib/test_summary > test_summary.log
echo ====================TESTING END=====================
install -D -m644 test_summary.log %{buildroot}%{_docdir}/gcc/test_summary.log
%endif

#-----------------------------------------------------------------------

%install
%makeinstall_std -C BUILD

%if %{build_java}
    %make -C BUILD \
        DESTDIR=%{buildroot} \
        JAR=$PWD/BUILD/%{_target_platform}/libjava/scripts/jar \
        -C %{_target_platform}/libjava \
        install-src.zip
%endif

# configure python dir option does not cover libstdc++ and needs to remove
# /usr prefix for libjava
mkdir -p %{buildroot}%{py_puresitedir}
if [ -d %{buildroot}%{_datadir}/gcc-%{ver}/python ]; then
    mv -f %{buildroot}%{_datadir}/gcc-%{ver}/python/* \
        %{buildroot}%{py_puresitedir}
    rm -fr %{buildroot}%{_datadir}/gcc-%{ver}
    %if %{build_java}
    perl -pi -e 's|%{_datadir}/gcc-%{ver}/python|%{py_puresitedir}|;' \
        %{buildroot}%{_bindir}/aot-compile
    %endif
fi

pushd %{buildroot}%{_bindir}
%if %{system_compiler}
    mkdir -p %{buildroot}/lib
    ln -sf %{_bindir}/cpp %{buildroot}/lib/cpp
    install -m 0755 %{SOURCE4} %{SOURCE5} %{buildroot}%{_bindir}
    ln -sf %{_target_platform}-gcc-%{ver} cc
%else
    rm -f %{buildroot}%{_bindir}/cpp
%endif
    PROGRAMS="gcc"
    %if %{build_cxx}
        PROGRAMS="$PROGRAMS g++"
    %endif
    %if %{build_go}
        PROGRAMS="$PROGRAMS gccgo"
    %endif
    %if %{build_java}
        PROGRAMS="$PROGRAMS gcj"
    %endif
    %if %{build_fortran}
        PROGRAMS="$PROGRAMS gfortran"
    %endif
    for prog in $PROGRAMS; do
        if [ -f %{_target_platform}-$prog ]; then
            mv -f %{_target_platform}-$prog{,-%{ver}}
        fi
        rm -f $prog
        ln -sf %{_target_platform}-$prog-%{ver} $prog-%{ver}
        %if %{system_compiler}
            ln -sf %{_target_platform}-$prog-%{ver} $prog
            ln -sf %{_target_platform}-$prog-%{ver} %{_target_platform}-$prog
        %endif
    done
%if %{build_cxx}
    rm -f c++ %{_target_platform}-c++{,-%{ver}}
    ln -sf %{_target_platform}-g++-%{ver} c++-%{ver}
    %if %{system_compiler}
        ln -sf %{_target_platform}-g++-%{ver} c++
        ln -sf %{_target_platform}-g++-%{ver} %{_target_platform}-c++
    %endif
    mkdir -p %{buildroot}%{_datadir}/gdb/auto-load%{_libdir}
    mv -f %{buildroot}%{_libdir}/libstdc++.so.*.py \
        %{buildroot}%{_datadir}/gdb/auto-load%{_libdir}
    perl -pi -e 's|%{_datadir}/gcc-%{ver}/python|%{py_puresitedir}|;' \
        %{buildroot}%{_datadir}/gdb/auto-load%{_libdir}/libstdc++.*.py

    mkdir -p %{buildroot}/%{_lib}
    mv %{buildroot}%{_libdir}/libstdc++.so.%{stdcxx_major}* \
        %{buildroot}/%{_lib}
    ln -srf %{buildroot}/%{_lib}/libstdc++.so.%{stdcxx_major}.*.* \
        %{buildroot}%{_libdir}/libstdc++.so

    %if %{build_multilib}
        mkdir -p %{buildroot}%{_datadir}/gdb/auto-load%{multilibdir}
        mv -f %{buildroot}%{multilibdir}/libstdc++.so.*.py \
        %{buildroot}%{_datadir}/gdb/auto-load%{multilibdir}
        perl -pi -e 's|%{_datadir}/gcc-%{ver}/python|%{py_puresitedir}|;' \
            %{buildroot}%{_datadir}/gdb/auto-load%{multilibdir}/libstdc++.*.py

        mkdir -p %{buildroot}%{multirootlibdir}
        mv %{buildroot}%{multilibdir}/libstdc++.so.%{stdcxx_major}* \
            %{buildroot}%{multirootlibdir}
        ln -srf %{buildroot}%{multirootlibdir}/libstdc++.so.%{stdcxx_major}.*.* \
            %{buildroot}%{multilibdir}/libstdc++.so
    %endif
%endif
%if %{build_java}
    ln -sf gcjh %{_target_platform}-gcjh
    # For some reason, the .so file is a real file, not a symlink
    ln -sf libgcj_bc.so.1.0.0 %{buildroot}%{_libdir}/libgcj_bc.so
%endif
popd

%if %{build_gomp}
    mkdir -p %{buildroot}/%{_lib}
    mv %{buildroot}%{_libdir}/libgomp.so.%{gomp_major}* \
        %{buildroot}/%{_lib}
    ln -srf %{buildroot}/%{_lib}/libgomp.so.%{gomp_major}.*.* \
        %{buildroot}%{_libdir}/libgomp.so

    %if %{build_multilib}
        mkdir -p %{buildroot}%{multirootlibdir}
        mv %{buildroot}%{multilibdir}/libgomp.so.%{gomp_major}* \
            %{buildroot}%{multirootlibdir}
        ln -srf %{buildroot}%{multirootlibdir}/libgomp.so.%{gomp_major}.*.* \
            %{buildroot}%{multilibdir}/libgomp.so
    %endif
%endif

%if %{system_compiler}
    mkdir -p %{buildroot}/%{_lib}
    mv %{buildroot}%{_libdir}/libgcc_s.so.%{gcc_major} \
        %{buildroot}/%{_lib}
    ln -srf %{buildroot}/%{_lib}/libgcc_s.so.%{gcc_major} \
        %{buildroot}%{_libdir}/libgcc_s.so

    %if %{build_multilib}
        mkdir -p %{buildroot}%{multirootlibdir}
        mv %{buildroot}%{multilibdir}/libgcc_s.so.%{gcc_major} \
            %{buildroot}%{multirootlibdir}
        ln -srf %{buildroot}%{multirootlibdir}/libgcc_s.so.%{gcc_major} \
            %{buildroot}%{multilibdir}/libgcc_s.so
    %endif
%endif

%if %{shared_libgnat}
    %if %{build_ada}
        for lib in libgnarl libgnat; do
            rm -f %{buildroot}%{_libdir}/$lib.so
            rm -f %{buildroot}%{gccdir}/adalib/$lib.so
            mv -f %{buildroot}%{gccdir}/adalib/$lib-%{branch}.so \
                    %{buildroot}%{_libdir}/$lib-%{branch}.so.1
            ln -sf $lib-%{branch}.so.1 %{buildroot}%{_libdir}/$lib-%{branch}.so
            ln -sf $lib-%{branch}.so.1 %{buildroot}%{_libdir}/$lib.so
            %if %{build_multilib}
                rm -f %{buildroot}%{multilibdir}/$lib.so
                rm -f %{buildroot}%{multigccdir}/adalib/$lib.so
                mv -f %{buildroot}%{multigccdir}/adalib/$lib-%{branch}.so \
                        %{buildroot}%{multilibdir}/$lib-%{branch}.so.1
                ln -sf $lib-%{branch}.so.1 %{buildroot}%{multilibdir}/$lib-%{branch}.so
                ln -sf $lib-%{branch}.so.1 %{buildroot}%{multilibdir}/$lib.so
            %endif
        done
    %endif
%endif

mv -f %{buildroot}%{gccdir}/include{-fixed,}/syslimits.h
mv -f %{buildroot}%{gccdir}/include{-fixed,}/limits.h
rm -fr %{buildroot}%{gccdir}/include-fixed
rm -fr %{buildroot}%{gccdir}/install-tools/include

%if !%{system_compiler}
    rm -fr %{buildroot}%{_infodir}
    rm -fr %{buildroot}%{_mandir}
    rm -fr %{buildroot}%{_localedir}
    rm -f %{buildroot}%{_bindir}/gcov
    rm -f %{buildroot}%{_libdir}/libgcc_s.so
    %if %{build_multilib}
        rm -f %{buildroot}%{multilibdir}/libgcc_s.so
    %endif
    %if !%{build_libgcc}
        rm -f %{buildroot}%{_libdir}/libgcc_s.so.*
        %if %{build_multilib}
            rm -f %{buildroot}%{multilibdir}/libgcc_s.so.*
        %endif
    %endif
%endif
rm -f %{buildroot}%{_libdir}/libiberty.a
rm -f %{buildroot}%{multilibdir}/libiberty.a

%if !%{package_ffi}
    rm -f %{buildroot}%{_libdir}/libffi.*
    rm -f %{buildroot}%{multilibdir}/libffi.*
    rm -f %{buildroot}%{_mandir}/man3/ffi*
%else
    mkdir -p %{buildroot}/%{_lib}
    mv %{buildroot}%{_libdir}/libffi.so.%{ffi_major}* \
        %{buildroot}/%{_lib}
    ln -srf %{buildroot}/%{_lib}/libffi.so.%{ffi_major}.*.* \
        %{buildroot}%{_libdir}/libffi.so

    %if %{build_multilib}
        mkdir -p %{buildroot}%{multirootlibdir}
        mv %{buildroot}%{multilibdir}/libffi.so.%{ffi_major}* \
            %{buildroot}%{multirootlibdir}
        ln -srf %{buildroot}%{multirootlibdir}/libffi.so.%{ffi_major}.*.* \
            %{buildroot}%{multilibdir}/libffi.so
    %endif
%endif

cd BUILD

%if %{build_doc}
    %if %{build_cxx}
    mkdir -p %{buildroot}%{_docdir}/libstdc++
    cp -far libstdc++-v3/doc/html %{buildroot}%{_docdir}/libstdc++
    %endif
    pushd host-%{_target_platform}/gcc/HTML/gcc-%{ver}
        mkdir -p %{buildroot}%{_docdir}/gcc/html
        for doc in gcc gccinstall gccint; do
            cp -far $doc %{buildroot}%{_docdir}/gcc/html
        done
        %if %{system_compiler}
            mkdir -p %{buildroot}%{_docdir}/gcc-cpp/html
            for doc in cpp cppinternals; do
                cp -far $doc %{buildroot}%{_docdir}/gcc-cpp/html
            done
        %endif
        %if %{build_fortran}
            mkdir -p %{buildroot}%{_docdir}/gcc-gfortran/html
            cp -far gfortran %{buildroot}%{_docdir}/gcc-gfortran/html
        %endif
        %if %{build_go}
            mkdir -p %{buildroot}%{_docdir}/gcc-go/html
            cp -far go %{buildroot}%{_docdir}/gcc-go/html
        %endif
        %if %{build_java}
            mkdir -p %{buildroot}%{_docdir}/gcc-java/html
            cp -far java %{buildroot}%{_docdir}/gcc-java/html
        %endif
    popd
    %if %{build_pdf}
    pushd host-%{_target_platform}/gcc/doc
        for doc in gcc.pdf gccinstall.pdf gccint.pdf; do
            install -m 0644 $doc %{buildroot}%{_docdir}/gcc/$doc
        done
        %if %{system_compiler}
            for doc in cpp.pdf cppinternals.pdf; do
                install -m 0644 $doc %{buildroot}%{_docdir}/gcc-cpp/$doc
            done
        %endif
        %if %{build_ada}
            mkdir -p %{buildroot}%{_docdir}/gcc-gnat
            for doc in gnat_ugn.pdf gnat_rm.pdf gnat-style.pdf; do
                install -m 0644 $doc %{buildroot}%{_docdir}/gcc-gnat/$doc
            done
        %endif
        %if %{build_fortran}
            for doc in gfc-internals.pdf gfortran.pdf; do
                install -m 0644 $doc %{buildroot}%{_docdir}/gcc-gfortran/$doc
            done
        %endif
        %if %{build_go}
            install -m 0644 -D gccgo.pdf %{buildroot}%{_docdir}/gcc-go/gccgo.pdf
        %endif
        %if %{build_java}
            install -m 0644 -D gcj.pdf %{buildroot}%{_docdir}/gcc-java/gcj.pdf
        %endif
    popd
    pushd %{_target_platform}
        %if %{build_gomp}
            install -m 0644 -D libgomp/libgomp.pdf %{buildroot}%{_docdir}/libgomp/libgomp.pdf
        %endif
        %if %{build_quadmath}
            install -m 0644 -D libquadmath/libquadmath.pdf %{buildroot}%{_docdir}/libquadmath/libquadmath.pdf
        %endif
        %if %{build_java}
            install -m 0644 -D libjava/classpath/doc/cp-tools.pdf %{buildroot}%{_docdir}/libjava/cp-tools.pdf
        %endif
    popd
    %endif
%endif

cd ..

%if %{build_java}
# Workaround for all gcj related tools
# somehow getting the same build ID
strip --strip-unneeded \
	%{buildroot}%{_bindir}/gc-analyze \
	%{buildroot}%{_bindir}/gappletviewer \
	%{buildroot}%{_bindir}/gjar \
	%{buildroot}%{_bindir}/gij \
	%{buildroot}%{_bindir}/gjavah \
	%{buildroot}%{_bindir}/gjarsigner \
	%{buildroot}%{_bindir}/gkeytool \
	%{buildroot}%{_bindir}/gorbd \
	%{buildroot}%{_bindir}/grmic \
	%{buildroot}%{_bindir}/grmid \
	%{buildroot}%{_bindir}/gnative2ascii \
	%{buildroot}%{_bindir}/gserialver \
	%{buildroot}%{_bindir}/grmiregistry \
	%{buildroot}%{_bindir}/jv-convert \
	%{buildroot}%{_bindir}/gtnameserv \
	%{buildroot}%{_bindir}/gcjh
%endif
