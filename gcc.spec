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
%define		branch			4.7
%define		ver			%branch.3
%define		linaro			2013.01
%define		alternatives		/usr/sbin/update-alternatives
%define		remove_alternatives	0
%define		obsolete_devmajor	0
%if %mdkversion <= 201200
  %if %{system_compiler}
    %define	remove_alternatives	1
    %define	obsolete_devmajor	1
  %endif
%endif
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
%define		libstdcxx_devel		%mklibname -d stdc++
%define		libstdcxx_static_devel	%mklibname -d -s stdc++
%define		multilibstdcxx		libstdc++%{stdcxx_major}
%define		gcj_major		13
%define		libgcj			%mklibname gcj %{gcj_major}
%define		libgcj_devel		%mklibname -d gcj
%define		libgcj_static_devel	%mklibname -d -s gcj
%define		gcj_bc_major		1
%define		libgcj_bc		%mklibname gcj_bc %{gcj_bc_major}
# gcj multilib explicitly disabled
%define		gfortran_major		3
%define		libgfortran		%mklibname gfortran %{gfortran_major}
%define		libgfortran_devel	%mklibname -d gfortran
%define		libgfortran_static_devel %mklibname -d -s gfortran
%define		multilibgfortran	libgfortran%{gfortran_major}
%define		ffi_major		4
%define		libffi			%mklibname ffi %{ffi_major}
%define		libffi_devel		%mklibname -d ffi
%define		libffi_static_devel	%mklibname -d -s ffi
%define		multilibffi		libffi%{ffi_major}
%define		gnat_major		1
%define		libgnat			%mklibname gnat %{gnat_major}
%define		libgnat_devel		%mklibname -d gnat
%define		libgnat_static_devel	%mklibname -d -s gnat
%define		multilibgnat		libgnat%{gnat_major}
%define		go_major		0
%define		libgo			%mklibname go %{go_major}
%define		libgo_devel		%mklibname -d go
%define		libgo_static_devel	%mklibname -d -s go
%define		multilibgo		libgo%{go_major}
%define		gomp_major		1
%define		libgomp			%mklibname gomp %{gomp_major}
%define		libgomp_devel		%mklibname -d gomp
%define		libgomp_static_devel	%mklibname -d -s gomp
%define		multilibgomp		libgomp%{gomp_major}
%define		mudflap_major		0
%define		libmudflap		%mklibname mudflap %{mudflap_major}
%define		libmudflap_devel	%mklibname -d mudflap
%define		libmudflap_static_devel %mklibname -d -s mudflap
%define		multilibmudflap		libmudflap%{mudflap_major}
%define		objc_major		4
%define		libobjc			%mklibname objc %{objc_major}
%define		libobjc_devel		%mklibname -d objc
%define		libobjc_static_devel	%mklibname -d -s objc
%define		multilibobjc		libobjc%{objc_major}
%define		quadmath_major		0
%define		libquadmath		%mklibname quadmath %{quadmath_major}
%define		libquadmath_devel	%mklibname -d quadmath
%define		libquadmath_static_devel %mklibname -d -s quadmath
%define		multilibquadmath	libquadmath%{quadmath_major}
%define		ssp_major		0
%define		libssp			%mklibname ssp %{ssp_major}
%define		libssp_devel		%mklibname -d ssp
%define		libssp_static_devel	%mklibname -d -s ssp
%define		multilibssp		libssp%{ssp_major}
%define		itm_major		1
%define		libitm			%mklibname itm %{itm_major}
%define		libitm_devel		%mklibname -d itm
%define		libitm_static_devel	%mklibname -d -s itm
%define		multilibitm		libitm%{itm_major}

#-----------------------------------------------------------------------
%define		build_ada		0
%define		build_check		0
%define		build_multilib		0
%define		build_go		0
%define		build_lto		1
%define		build_objc		0
%define		build_objcxx		0
%define		build_quadmath		0
%define		build_ssp		0
%define		build_itm		1
%define		build_cloog		%{system_compiler}
%define		build_cxx		%{system_compiler}
%define		build_doc		0
%define		build_ffi		%{system_compiler}
%define		build_fortran		%{system_compiler}
%define		build_gomp		%{system_compiler}
# system_compiler && build_ffi
%define		build_java		%{system_compiler}
# need to build if major does not conflict with current system_compiler
%define		build_libgcc		%{system_compiler}
%define		build_mudflap		%{system_compiler}
%define		build_pdf		%{build_doc}
%define		build_plugin		%{system_compiler}
%ifarch x86_64
  %define	build_multilib		%{system_compiler}
%endif
%ifarch %{ix86} x86_64
  %define	build_ada		%{system_compiler}
  %define	build_quadmath		%{system_compiler}
  %define	build_doc		%{system_compiler}
# system_compiler && build_cxx
  %define	build_go		%{system_compiler}
%endif
%ifarch %{ix86} x86_64 %{arm}
  %define	build_objc		%{system_compiler}
  %define	build_objcxx		%{system_compiler}
%endif

%define		build_doc		0
%define		build_pdf		0

%define		package_ffi		0

# Adapted from fedora procedure:
#   If there is no usable gcc-java neither libgcj for the arch,
# on an arch that has it, run:
#	rpmbuild -bc --define "_topdir `pwd`" --with java_build_tar SPECS/gcc.spec
# which creates libjava-classes-@{version}-@{release}.tar.bz2
#   With the tarball on the new arch, run:
#	rpmbuild -ba --define "_topdir `pwd`" -v --with java_bootstrap SPECS/gcc.spec
%bcond_with	java_build_tar
%bcond_with	java_bootstrap

#-----------------------------------------------------------------------
%if %{system_compiler}
Name:		gcc
%else
Name:		gcc%branch
%endif
Release:	1
#ExclusiveArch:	x86_64
Summary:	GNU Compiler Collection
License:	GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group:		Development/C
URL:		http://gcc.gnu.org/
%if "%linaro" != ""
Version:	%{ver}_%linaro
Source0:	http://cbuild.validation.linaro.org/snapshots/gcc-linaro-%branch-%linaro.tar.bz2
%else
Version:	%ver
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

Source100:	%name.rpmlintrc

%if %{system_compiler}
Requires:	gcc-cpp >= %{version}-%{release}
Requires:	libgcc >= %{version}-%{release}
Requires:	libgomp >= %{version}-%{release}
Obsoletes:	manbo-mandriva-files-gcc < %{version}-%{release}
Obsoletes:	manbo-mandriva-files-gcc4.4 < %{version}-%{release}
# versioned and non versioned files
Conflicts:	manbo-mandriva-files-gcc4.2 < %{version}-%{release}
%endif
%ifarch armv7l armv7hl
# find-provides fail to provide devel(libgcc_s) because it is a linker script
Provides:	devel(libgcc_s) = %{version}-%{release}
%endif
BuildRequires:	binutils >= 2.20.51.0.2
Requires:	binutils >= 2.20.51.0.2
BuildRequires:	elfutils-devel >= 0.147

# Ensure https://qa.mandriva.com/show_bug.cgi?id=62943
# have been addressed if using an older version
Requires:	glibc-devel >= 2.13

BuildRequires:	dejagnu
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gdb
BuildRequires:	gettext
BuildRequires:	gmp-devel, mpfr-devel, libmpc-devel
BuildRequires:	sharutils
BuildRequires:	texinfo
%if %{build_doc}
BuildRequires:	texi2html
%endif
%if %{build_pdf}
BuildRequires:	texlive
%endif
BuildRequires:	zlib-devel
%if %{build_cloog}
BuildRequires:	ppl-devel >= 0.11
BuildRequires:	pwl-devel >= 0.11
BuildRequires:	ppl_c-devel >= 0.11
#BuildRequires:	cloog-ppl-devel >= 0.16.1
BuildRequires:	cloog-devel isl-devel
%endif
%if %{remove_alternatives}
Requires(pre):	update-alternatives
%endif
Obsoletes:	gcc-doc < %{version}-%{release}

Patch0:		gcc-4.7.1-uclibc-ldso-path.patch
Patch1:		gcc-4.6.0-java-nomulti.patch
Patch2:		gcc-4.6.0-make-pdf.patch
Patch3:		gcc-4.7.1-linux32.patch
Patch4:		gnatmake-execstack.patch
Patch5:		gcc-4.7.1-linker-selection.patch
Patch6:		gcc-4.7.1-autoconf-2.69.patch
Patch7:		gcc-4.7.1-linker-plugin-detect.patch
Patch8:		gcc-4.7.1-extern-inline-not-inlined.patch
# Patch for Android compatibility (creating Linux->Android crosscompilers etc)
Patch9:		gcc-4.7-androidcompat.patch

%description
The gcc package contains the GNU Compiler Collection version %{branch}.

%if %{remove_alternatives}
%pre
if [ -f %{_bindir}/gcc ]; then %{alternatives} --remove-all gcc; fi
%endif

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
%{gccdir}/cc1
%{gccdir}/collect2
%{gccdir}/*.o
%{gccdir}/libgcc*.a
%{gccdir}/libgcov.a
%if %{build_lto}
%{gccdir}/lto*
%{gccdir}/liblto*
%endif
%dir %{gccdir}/include
%{gccdir}/include/*.h
%if %{build_java}
%exclude %{gccdir}/include/jawt*.h
%exclude %{gccdir}/include/jni*.h
%exclude %{gccdir}/include/jvm*.h
%endif
%{gccdir}/install-tools
%if %{build_quadmath}
%exclude %{gccdir}/include/quadmath*.h
%endif
%if %{build_gomp}
%exclude %{gccdir}/include/omp*.h
%endif
%if %{build_mudflap}
%exclude %{gccdir}/include/mf-runtime.h
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
%package	-n %{libgcc}
Summary:	GNU C library
Group:		System/Libraries
%if "%libgcc" != "libgcc"
Provides:	libgcc = %{version}-%{release}
%endif
%if %mdkversion <= 201200
Obsoletes:	libgcc3.0 < %{version}-%{release}
Obsoletes:	libgcc3.2 < %{version}-%{release}
Obsoletes:	libgcc4.5 < %{version}-%{release}
%endif

%description	-n %{libgcc}
The %{libgcc} package contains GCC shared libraries for gcc %{branch}

%files		-n %{libgcc}
/%{_lib}/libgcc_s.so.%{gcc_major}

#-----------------------------------------------------------------------
%if %{build_multilib}
%package	-n %{multilibgcc}
Summary:	GNU C library
Group:		System/Libraries
Conflicts:	%{libgcc} < 4.6.2-11

%description	-n %{multilibgcc}
The %{multilibgcc} package contains GCC shared libraries for gcc %{branch}

%files		-n %{multilibgcc}
%{multirootlibdir}/libgcc_s.so.%{gcc_major}
%endif
#-----------------------------------------------------------------------
# build libgcc
%endif

########################################################################
%if %{build_plugin}
#-----------------------------------------------------------------------
%package	plugin-devel
Summary:	Headers to build gcc plugins
Group:		Development/C
Obsoletes:	gcc-plugins <= 4.5.2
Requires:	%{name} = %{version}-%{release}
Requires:	gmp-devel
Requires:	mpfr-devel
Requires:	libmpc-devel
Requires:	ppl-devel
Requires:	ppl_c-devel

%description	plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%files		plugin-devel
%{gccdir}/gengtype
%{gccdir}/gtype.state
%{gccdir}/plugin
#-----------------------------------------------------------------------
# build_plugin
%endif

########################################################################
%if %{system_compiler}
#-----------------------------------------------------------------------
%package	cpp
Summary:	The C Preprocessor
Group:		Development/C
Provides:	cpp = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
%if %{remove_alternatives}
Requires(pre):	update-alternatives
%endif

%description	cpp
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

%if %{remove_alternatives}
%pre		cpp
if [ -f %{_bindir}/cpp ]; then %{alternatives} --remove-all cpp; fi
%endif

%files		cpp
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
%package	c++
Summary:	C++ support for gcc
Group:		Development/C++
Requires:	%{name} = %{version}-%{release}
%if %{system_compiler}
Requires:	%{libstdcxx_devel} = %{version}
Obsoletes:	manbo-mandriva-files-g++ < %{version}-%{release}
Obsoletes:	manbo-mandriva-files-g++4.4 < %{version}-%{release}
Obsoletes:	manbo-mandriva-files-gcc-c++ < %{version}-%{release}
Obsoletes:	manbo-mandriva-files-gcc-c++4.2 < %{version}-%{release}
%endif
%if %{remove_alternatives}
Requires(pre):	update-alternatives
%endif

%description	c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%if %{remove_alternatives}
%pre		c++
if [ -f %{_bindir}/c++ ]; then %{alternatives} --remove-all c++; fi
if [ -f %{_bindir}/g++ ]; then %{alternatives} --remove-all g++; fi
%endif

%files		c++
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
%{gccdir}/cc1plus

#-----------------------------------------------------------------------
%package	-n %{libstdcxx}
Summary:	GNU Standard C++ library
Group:		System/Libraries
%if "%libstdcxx" != "libstdc++"
Provides:	libstdc++ = %{version}-%{release}
%endif
%if %{build_doc}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif

%description	-n %{libstdcxx}
The libstdc++ package contains a rewritten standard compliant
GCC Standard C++ Library.

%files		-n %{libstdcxx}
/%{_lib}/libstdc++.so.%{stdcxx_major}
/%{_lib}/libstdc++.so.%{stdcxx_major}.*
%if %{system_compiler}
%{_localedir}/*/LC_MESSAGES/libstdc++.mo
%endif

#-----------------------------------------------------------------------
%if %{build_multilib}
%package	-n %{multilibstdcxx}
Summary:	GNU Standard C++ library
Group:		System/Libraries
Conflicts:	%{libstdcxx} < 4.6.2-11

%description	-n %{multilibstdcxx}
The libstdc++ package contains a rewritten standard compliant
GCC Standard C++ Library.

%files		-n %{multilibstdcxx}
%{multirootlibdir}/libstdc++.so.%{stdcxx_major}
%{multirootlibdir}/libstdc++.so.%{stdcxx_major}.*
%endif

#-----------------------------------------------------------------------
%package	-n %{libstdcxx_devel}
Summary:	Header files and libraries for C++ development
Group:		Development/C++
Requires:	%{libstdcxx} = %{version}-%{release}
%if %{build_multilib}
Requires:	%{multilibstdcxx} = %{version}-%{release}
%endif
%if "%libstdcxx_devel" != "libstdc++-devel"
Provides:	libstdc++-devel = %{version}-%{release}
%endif
Provides:	stdc++-devel = %{version}-%{release}
%if "%ver" != "%version"
# 4.7.2_2010.10 should provide 4.7.2 so clang can pick up the dep
%if "%libstdcxx_devel" != "libstdc++-devel"
Provides:	%libstdcxx_devel = %ver-%release
%endif
Provides:	libstdc++-devel = %ver-%release
Provides:	stdc++-devel = %ver-%release
%endif
%if %{obsolete_devmajor}
Obsoletes:	libstdc++4.5-devel < %{version}-%{release}
Obsoletes:	libstdc++6-devel < %{version}-%{release}
%endif
# We don't want to pull in an entire Python environment just because of
# libstdc++'s python based gdb plugin...
%define __noautoreq '.*python.*'

%description	-n %{libstdcxx_devel}
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%files		-n %{libstdcxx_devel}
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
%package	-n %{libstdcxx_static_devel}
Summary:	Static libraries for the GNU standard C++ library
Group:		Development/C++
Requires:	%{libstdcxx_devel} = %{version}-%{release}
%if "%libstdcxx_static_devel" != "libstdc++-static-devel"
Provides:	libstdc++-static-devel = %{version}-%{release}
%endif
Provides:	stdc++-static-devel = %{version}-%{release}
%if %{obsolete_devmajor}
Obsoletes:	libstdc++4.5-static-devel < %{version}-%{release}
Obsoletes:	libstdc++%{stdcxx_major}-static-devel < %{version}-%{release}
%endif

%description	-n %{libstdcxx_static_devel}
Static libraries for the GNU standard C++ library.

%files		-n %{libstdcxx_static_devel}
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
%package	gnat
Summary:	Ada 95 support for gcc
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Requires:	%{libgnat_devel} = %{version}-%{release}
# no bootstrap support
BuildRequires:	gcc-gnat >= 3.1, libgnat >= 3.1

%description	gnat
GNAT is a GNU Ada 95 front-end to GCC. This package includes development
tools, the documents and Ada 95 compiler.

%files		gnat
%{_bindir}/gnat*
%if %{build_java}
%exclude %{_bindir}/gnative2ascii
%endif
%{gccdir}/gnat1
%{_infodir}/gnat*
%if %{build_doc}
%doc %{_docdir}/gcc-gnat
%endif

#-----------------------------------------------------------------------
%package	-n %{libgnat}
Summary:	GNU Ada 95 runtime libraries
Group:		System/Libraries
Provides:	libgnat = %{version}-%{release}
Obsoletes:	gnat-runtime < %{version}-%{release}

%description	-n %{libgnat}
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared
libraries, which are required to run programs compiled with the GNAT.

%files		-n %{libgnat}
%{_libdir}/libgnat-%{branch}.so.%{gnat_major}
%{_libdir}/libgnarl-%{branch}.so.%{gnat_major}

#-----------------------------------------------------------------------
%if %{build_multilib}
%package	-n %{multilibgnat}
Summary:	GNU Ada 95 runtime libraries
Group:		System/Libraries
Conflicts:	%{libgnat} < 4.6.2-11

%description	-n %{multilibgnat}
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared
libraries, which are required to run programs compiled with the GNAT.

%files		-n %{multilibgnat}
%{multilibdir}/libgnat-%{branch}.so.%{gnat_major}
%{multilibdir}/libgnarl-%{branch}.so.%{gnat_major}
%endif

#-----------------------------------------------------------------------
%package	-n %{libgnat_devel}
Summary:	GNU Ada 95 libraries
Group:		Development/Other
Requires:	%{libgnat} = %{version}-%{release}
%if %{build_multilib}
Requires:	%{multilibgnat} = %{version}-%{release}
%endif
Provides:	libgnat-devel = %{version}-%{release}
Provides:	gnat-devel = %{version}-%{release}

%description	-n %{libgnat_devel}
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared
libraries, which are required to compile with the GNAT.

%files		-n %{libgnat_devel}
%{_libdir}/libgnat*.so
%{_libdir}/libgnarl*.so
%{gccdir}/adalib
%{gccdir}/adainclude
%exclude %{gccdir}/adalib/lib*.a
%if %{build_multilib}
%{multilibdir}/libgnat*.so
%{multilibdir}/libgnarl*.so
%{multigccdir}/adalib
%{multigccdir}/adainclude
%exclude %{multigccdir}/adalib/lib*.a
%endif

#-----------------------------------------------------------------------
%package	-n %{libgnat_static_devel}
Summary:	GNU Ada 95 static libraries
Group:		Development/Other
Requires:	%{libgnat_devel} = %{version}-%{release}
Provides:	libgnat-static-devel = %{version}-%{release}
Provides:	gnat-static-devel = %{version}-%{release}

%description	-n %{libgnat_static_devel}
GNAT is a GNU Ada 95 front-end to GCC. This package includes static
libraries.

%files		-n %{libgnat_static_devel}
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
%package	gfortran
Summary:	Fortran 95 support for gcc
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Requires:	%{libgfortran_devel} = %{version}-%{release}
Obsoletes:	manbo-mandriva-files-gfortran < %{version}-%{release}
Obsoletes:	manbo-mandriva-files-gfortran4.4 < %{version}-%{release}
Obsoletes:	manbo-mandriva-files-gcc-gfortran < %{version}-%{release}
Obsoletes:	manbo-mandriva-files-gcc-gfortran4.2 < %{version}-%{release}

%description	gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%files		gfortran
%{_bindir}/gfortran
%{_bindir}/gfortran-%{ver}
%{_bindir}/%{_target_platform}-gfortran
%{_bindir}/%{_target_platform}-gfortran-%{ver}
%{_infodir}/gfortran.info*
%{_mandir}/man1/gfortran.1*
%{gccdir}/f951
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
%package	-n %{libgfortran}
Summary:	Fortran 95 runtime libraries
Group:		System/Libraries
%if %{build_quadmath}
Requires:	%{libquadmath} = %{version}-%{release}
%endif
Provides:	libgfortran = %{version}-%{release}
%if %{build_multilib}
Provides:	%{multilibgfortran} = %{version}-%{release}
%endif
%if %mdkversion <= 201200
Obsoletes:	libgfortran4.5 < %{version}-%{release}
%endif

%description	-n %{libgfortran}
This package contains Fortran 95 shared library which is needed to run
Fortran 95 dynamically linked programs.

%files		-n %{libgfortran}
%{_libdir}/libgfortran.so.%{gfortran_major}
%{_libdir}/libgfortran.so.%{gfortran_major}.*

#-----------------------------------------------------------------------
%if %{build_multilib}
%package	-n %{multilibgfortran}
Summary:	Fortran 95 runtime libraries
Group:		System/Libraries
%if %{build_quadmath}
Requires:	%{multilibquadmath} = %{version}-%{release}
%endif
Conflicts:	%{libgfortran} < 4.6.2-11

%description	-n %{multilibgfortran}
This package contains Fortran 95 shared library which is needed to run
Fortran 95 dynamically linked programs.

%files		-n %{multilibgfortran}
%{multilibdir}/libgfortran.so.%{gfortran_major}
%{multilibdir}/libgfortran.so.%{gfortran_major}.*
%endif

#-----------------------------------------------------------------------
%package	-n %{libgfortran_devel}
Summary:	Fortran 95 libraries
Group:		System/Libraries
Requires:	%{libgfortran} = %{version}-%{release}
%if %{build_multilib}
Requires:	%{multilibgfortran} = %{version}-%{release}
%endif
%if %{build_quadmath}
Requires:	%{libquadmath_devel} = %{version}-%{release}
%endif
Provides:	libgfortran-devel = %{version}-%{release}
Provides:	gfortran-devel = %{version}-%{release}

%description	-n %{libgfortran_devel}
This package contains Fortran 95 shared library which is needed to
compile Fortran 95 programs.

%files		-n %{libgfortran_devel}
%{_libdir}/libgfortran.so
%{_libdir}/libgfortran.spec
%if %{build_multilib}
%{multilibdir}/libgfortran.so
%{multilibdir}/libgfortran.spec
%endif

#-----------------------------------------------------------------------
%package	-n %{libgfortran_static_devel}
Summary:	Fortran 95 static libraries
Group:		System/Libraries
Requires:	%{libgfortran_devel} = %{version}-%{release}
Provides:	libgfortran-static-devel = %{version}-%{release}
Provides:	gfortran-static-devel = %{version}-%{release}

%description	-n %{libgfortran_static_devel}
This package contains Fortran 95 static library which is needed to
compile Fortran 95 programs.

%files		-n %{libgfortran_static_devel}
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
%package	go
Summary:	Go support for gcc
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Requires:	%{libgo_devel} = %{version}-%{release}

%description	go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%files		go
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
%{gccdir}/go1
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
%package	-n %{libgo}
Summary:	Go runtime libraries
Group:		System/Libraries
Provides:	libgo = %{version}-%{release}

%description	-n %{libgo}
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%files		-n %{libgo}
%{_libdir}/libgo.so.%{go_major}
%{_libdir}/libgo.so.%{go_major}.*

#-----------------------------------------------------------------------
%if %{build_multilib}
%package	-n %{multilibgo}
Summary:	Go runtime libraries
Group:		System/Libraries
Conflicts:	%{libgo} < 4.6.2-11

%description	-n %{multilibgo}
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%files		-n %{multilibgo}
%{multilibdir}/libgo.so.%{go_major}
%{multilibdir}/libgo.so.%{go_major}.*
%endif

#-----------------------------------------------------------------------
%package	-n %{libgo_devel}
Summary:	Go development libraries
Group:		Development/Other
Requires:	%{libgo} = %{version}-%{release}
%if %{build_multilib}
Requires:	%{multilibgo} = %{version}-%{release}
%endif
Provides:	libgo-devel = %{version}-%{release}
Provides:	go-devel = %{version}-%{release}

%description	-n %{libgo_devel}
This package includes libraries and support files for compiling
Go programs.

%files		-n %{libgo_devel}
%{_libdir}/libgo.so
%if %{build_multilib}
%{multilibdir}/libgo.so
%endif

#-----------------------------------------------------------------------
%package	-n %{libgo_static_devel}
Summary:	Static Go libraries
Group:		Development/Other
Requires:	%{libgo_devel} = %{version}-%{release}
Provides:	libgo-static-devel = %{version}-%{release}
Provides:	go-static-devel = %{version}-%{release}

%description	-n %{libgo_static_devel}
This package contains static Go libraries.

%files		-n %{libgo_static_devel}
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
%package	java
Summary:	Java support for GCC
Group:		Development/Java
Requires:	%{name} = %{version}-%{release}
Requires:	%{libgcj_devel} = %{version}-%{release}
Requires:	eclipse-ecj
BuildRequires:	eclipse-ecj
BuildRequires:	jpackage-utils
BuildRequires:	unzip
BuildRequires:	zip
Obsoletes:	manbo-mandriva-files-java < %{version}-%{release}
Obsoletes:	manbo-mandriva-files-java4.4 < %{version}-%{release}
Obsoletes:	manbo-mandriva-files-gcc-java < %{version}-%{release}
Obsoletes:	manbo-mandriva-files-gcc-java4.2 < %{version}-%{release}

%description	java
This package adds support for compiling Java(tm) programs and
bytecode into native code.

%files		java
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
%{gccdir}/jc1
%{gccdir}/ecj1
%{gccdir}/jvgenmain
%if %{build_doc}
%doc %{_docdir}/gcc-java
%endif

#-----------------------------------------------------------------------
%package	-n %{libgcj}
Summary:	Java runtime library for gcc
Group:		System/Libraries
Provides:	libgcj = %{version}-%{release}
Provides:	%{libgcj_bc} = %{version}-%{release}
%if %{build_multilib}
# for compatibility and/or make updates clean
Provides:	libgcj%{gcj_major} = %{version}-%{release}
Provides:	libgcj_bc%{gcj_bc_major} = %{version}-%{release}
%endif
%if %mdkversion <= 201200
Provides:	libgcj%{gcj_major}-base = %{version}-%{release}
Provides:	%{libgcj}-base = %{version}-%{release}
Obsoletes:	gcc-libgcj < %{version}-%{release}
Obsoletes:	libgcj4.5 < %{version}-%{release}
Obsoletes:	gcj4.5-tools < %{version}-%{release}
Obsoletes:	gcj-tools <= 4.5.2
%define		libgcj11 %{mklibname gcj 11}
Obsoletes:	%{libgcj11} < %{version}-%{release}
Obsoletes:	%{libgcj11}-base < %{version}-%{release}
%endif
Requires:	zip >= 2.1
%if %{without java_bootstrap}
BuildRequires:	antlr-java
%endif
BuildRequires:	gtk2-devel >= 2.4.0
BuildRequires:	glib2-devel >= 2.4.0
BuildRequires:	libart_lgpl-devel >= 2.1.0
BuildRequires:	pkgconfig(alsa)
BuildRequires:	libxtst-devel
BuildRequires:	libxt-devel
BuildRequires:	spec-helper >= 0.31.10

%description	-n %{libgcj}
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%files		-n %{libgcj}
%{_javadir}/libgcj*.jar
%dir %{_libdir}/gcj-%{ver}-%{gcj_major}
%{_libdir}/gcj-%{ver}-%{gcj_major}/*.so
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_libdir}/gcj-%{ver}-%{gcj_major}/classmap.db
%{_libdir}/libgcj.so.%{gcj_major}
%{_libdir}/libgcj.so.%{gcj_major}.*
%{_libdir}/libgcj-tools.so.%{gcj_major}
%{_libdir}/libgcj-tools.so.%{gcj_major}.*
%{_libdir}/libgcj_bc.so.%{gcj_bc_major}
%{_libdir}/libgcj_bc.so.%{gcj_bc_major}.*
%{_libdir}/libgij.so.%{gcj_major}
%{_libdir}/libgij.so.%{gcj_major}.*

#-----------------------------------------------------------------------
%package	-n gcj-tools
Summary:	Tools needed to use applications in the GCJ Java runtime
Group:		System/Libraries
Requires:	%{libgcj} = %{version}-%{release}
Requires:	zip >= 2.1

%description	-n gcj-tools
Tools needed to run applications in the GCJ Java(tm) runtime. You will
need this package to run your Java programs in the Java Virtual Machine
(JVM) provided by the GNU Compiler Collection (gcj).

%files		-n gcj-tools
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
%package	-n %{libgcj_devel}
Summary:	Libraries for Java development using GCC
Group:		Development/Java
Requires:	%{libgcj} = %{version}-%{release}
Requires:	zlib-devel
Requires:	awk
Provides:	libgcj-devel = %{version}-%{release}
Provides:	gcj-devel = %{version}-%{release}
# libgcj and friends are no longer built statically for 4.7.x
Obsoletes:	%{libgcj_static_devel} < {version}-%{release}

%description	-n %{libgcj_devel}
The Java(tm) static libraries and C header files. You will need this
package to compile your Java programs using the GCC Java compiler (gcj).

%files		-n %{libgcj_devel}
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
%package	-n libgcj%{gcj_major}-src
Summary:	Java library sources
Group:		Development/Java
Requires:	%{libgcj} = %{version}-%{release}
Provides:	libgcj-src = %{version}-%{release}

%description	-n libgcj%{gcj_major}-src
The Java(tm) runtime library sources.

%files	-n libgcj%{gcj_major}-src
%{_javadir}/src-%{ver}.zip
#-----------------------------------------------------------------------
# build java
%endif

########################################################################
%if %{build_objc}
#-----------------------------------------------------------------------
%package	objc
Summary:	Objective-C support for GCC
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}
Requires:	%{libobjc_devel} = %{version}-%{release}

%description	objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%files		objc
%{gccdir}/cc1obj

#-----------------------------------------------------------------------
%package	-n %{libobjc}
Summary:	Objective-C runtime
Group:		System/Libraries
Provides:	libobjc = %{version}-%{release}
%if %mdkversion <= 201200
Obsoletes:	libobjc3.0 < %{version}-%{release}
Obsoletes:	libobjc3.1 < %{version}-%{release}
%endif

%description	-n %{libobjc}
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%files		-n %{libobjc}
%{_libdir}/libobjc.so.%{objc_major}
%{_libdir}/libobjc.so.%{objc_major}.*

#-----------------------------------------------------------------------
%if %{build_multilib}
%package	-n %{multilibobjc}
Summary:	Objective-C runtime
Group:		System/Libraries
Provides:	libobjc = %{version}-%{release}
%if %mdkversion <= 201200
Obsoletes:	libobjc3.0 < %{version}-%{release}
Obsoletes:	libobjc3.1 < %{version}-%{release}
%endif
Conflicts:	%{libobjc} < 4.6.2-11

%description	-n %{multilibobjc}
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%files		-n %{multilibobjc}
%{multilibdir}/libobjc.so.%{objc_major}
%{multilibdir}/libobjc.so.%{objc_major}.*
%endif

#-----------------------------------------------------------------------
%package	-n %{libobjc_devel}
Summary:	Objective-C development libraries
Group:		Development/Other
Requires:	%{libobjc} = %{version}-%{release}
%if %{build_multilib}
Requires:	%{multilibobjc} = %{version}-%{release}
%endif
Provides:	libobjc-devel = %{version}-%{release}
Provides:	objc-devel = %{version}-%{release}

%description	-n %{libobjc_devel}
This package includes libraries and support files for compiling
Objective-C programs.

%files		-n %{libobjc_devel}
%{_libdir}/libobjc.so
%{gccdir}/include/objc
%if %{build_multilib}
%{multilibdir}/libobjc.so
%endif

#-----------------------------------------------------------------------
%package	-n %{libobjc_static_devel}
Summary:	Static Objective-C libraries
Group:		Development/Other
Requires:	%{libobjc_devel} = %{version}-%{release}
Provides:	libobjc-static-devel = %{version}-%{release}
Provides:	objc-static-devel = %{version}-%{release}

%description	-n %{libobjc_static_devel}
This package contains static Objective-C libraries.

%files		-n %{libobjc_static_devel}
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
%package	objc++
Summary:	Objective-C++ support for GCC
Group:		Development/Other
Requires:	gcc-objc = %{version}-%{release}

%description	objc++
gcc++-objc provides Objective-C++ support for the GCC.

%files		objc++
%{gccdir}/cc1objplus
#-----------------------------------------------------------------------
# build objcxx
%endif

########################################################################
%if %{package_ffi}
#-----------------------------------------------------------------------
%package	-n %{libffi}
Summary:	GCC support library for FFI
Group:		System/Libraries
Provides:	libffi = %{version}-%{release}

%description	-n %{libffi}
This package contains GCC shared support library which is needed
for FFI support.

%files		-n %{libffi}
%{_libdir}/libffi.so.%{ffi_major}
%{_libdir}/libffi.so.%{ffi_major}.*

#-----------------------------------------------------------------------
%if %{build_multilib}
%package	-n %{multilibffi}
Summary:	GCC support library for FFI
Group:		System/Libraries
Conflicts:	%{libffi} < 4.6.2-11

%description	-n %{multilibffi}
This package contains GCC shared support library which is needed
for FFI support.

%files		-n %{multilibffi}
%{multirootlibdir}/libffi.so.%{ffi_major}
%{multirootlibdir}/libffi.so.%{ffi_major}.*
%endif

#-----------------------------------------------------------------------
%package	-n %{libffi_devel}
Summary:	GCC development for FFI
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libffi} = %{version}-%{release}
%if %{build_multilib}
Requires:	%{multilibffi} = %{version}-%{release}
%endif
Provides:	libffi-devel = %{version}-%{release}
Provides:	ffi-devel = %{version}-%{release}
%if %{obsolete_devmajor}
Obsoletes:	libffi4-devel < %{version}-%{release}
%endif

%description	-n %{libffi_devel}
This package contains GCC development which is needed
to compile FFI support.

%files		-n %{libffi_devel}
%{_libdir}/libffi.so
%if %{build_multilib}
%{multilibdir}/libffi.so
%endif
%{_mandir}/man3/*.3*

#-----------------------------------------------------------------------
%package	-n %{libffi_static_devel}
Summary:	GCC FFI static library
Group:		Development/C
Requires:	%{libffi_devel} = %{version}-%{release}
Provides:	libffi-static-devel = %{version}-%{release}
Provides:	ffi-static-devel = %{version}-%{release}

%description	-n %{libffi_static_devel}
This package contains GCC static libraries which are needed
to compile FFI support.

%files		-n %{libffi_static_devel}
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
%package	-n %{libquadmath}
Summary:	GCC __float128 shared support library
Group:		System/Libraries
Provides:	libquadmath = %{version}-%{release}

%description	-n %{libquadmath}
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%files		-n %{libquadmath}
%{_libdir}/libquadmath.so.%{quadmath_major}
%{_libdir}/libquadmath.so.%{quadmath_major}.*

#-----------------------------------------------------------------------
%if %{build_multilib}
%package	-n %{multilibquadmath}
Summary:	GCC __float128 shared support library
Group:		System/Libraries
Conflicts:	%{libquadmath} < 4.6.2-11

%description	-n %{multilibquadmath}
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%files		-n %{multilibquadmath}
%{multilibdir}/libquadmath.so.%{quadmath_major}
%{multilibdir}/libquadmath.so.%{quadmath_major}.*
%endif

#-----------------------------------------------------------------------
%package	-n %{libquadmath_devel}
Summary:	GCC __float128 support
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libquadmath} = %{version}-%{release}
%if %{build_multilib}
Requires:	%{multilibquadmath} = %{version}-%{release}
%endif
Provides:	libquadmath-devel = %{version}-%{release}
Provides:	quadmath-devel = %{version}-%{release}

%description	-n %{libquadmath_devel}
This package contains support for building Fortran programs using
REAL*16 and programs using __float128 math.

%files		-n %{libquadmath_devel}
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
%package	-n %{libquadmath_static_devel}
Summary:	Static libraries for __float128 support
Group:		Development/C
Requires:	%{libquadmath_devel} = %{version}-%{release}
Provides:	libquadmath-static-devel = %{version}-%{release}
Provides:	quadmath-static-devel = %{version}-%{release}

%description	-n %{libquadmath_static_devel}
This package contains static libraries for building Fortran programs
using REAL*16 and programs using __float128 math.

%files		-n %{libquadmath_static_devel}
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
%package	-n %{libgomp}
Summary:	GCC OpenMP v3.0 shared support library
Group:		System/Libraries
Provides:	libgomp = %{version}-%{release}

%description	-n %{libgomp}
This package contains GCC shared library which is needed
for OpenMP v3.0 support.

%files		-n %{libgomp}
/%{_lib}/libgomp.so.%{gomp_major}
/%{_lib}/libgomp.so.%{gomp_major}.*

#-----------------------------------------------------------------------
%if %{build_multilib}
%package	-n %{multilibgomp}
Summary:	GCC OpenMP v3.0 shared support library
Group:		System/Libraries
Provides:	libgomp = %{version}-%{release}
Conflicts:	%{libgomp} < 4.6.2-11

%description	-n %{multilibgomp}
This package contains GCC shared library which is needed
for OpenMP v3.0 support.

%files		-n %{multilibgomp}
%{multirootlibdir}/libgomp.so.%{gomp_major}
%{multirootlibdir}/libgomp.so.%{gomp_major}.*
%endif

#-----------------------------------------------------------------------
%package	-n %{libgomp_devel}
Summary:	GCC OpenMP v3.0 development support
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libgomp} = %{version}-%{release}
%if %{build_multilib}
Requires:	%{multilibgomp} = %{version}-%{release}
%endif
Provides:	libgomp-devel = %{version}-%{release}
Provides:	gomp-devel = %{version}-%{release}

%description	-n %{libgomp_devel}
This package contains GCC development which is needed
to compile OpenMP v3.0 support.

%files		-n %{libgomp_devel}
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
%package	-n %{libgomp_static_devel}
Summary:	GCC OpenMP v3.0 static library
Group:		Development/C
Requires:	%{libgomp_devel} = %{version}-%{release}
Provides:	libgomp-static-devel = %{version}-%{release}
Provides:	gomp-static-devel = %{version}-%{release}

%description	-n %{libgomp_static_devel}
This package contains GCC static libraries which are needed
to compile OpenMP v3.0 support.

%files		-n %{libgomp_static_devel}
%{_libdir}/libgomp.*a
%if %{build_multilib}
%{multilibdir}/libgomp.*a
%endif
#-----------------------------------------------------------------------
# build gomp
%endif

########################################################################
%if %{build_mudflap}
#-----------------------------------------------------------------------
%package	-n %{libmudflap}
Summary:	GCC mudflap shared support libraries
Group:		System/Libraries
Provides:	libmudflap = %{version}-%{release}

%description	-n %{libmudflap}
This package contains GCC shared libraries which are needed
for mudflap support.

For front-ends that support it (C and C++), instrument all risky
pointer/array dereferencing operations, some standard library
string/heap functions, and some other associated constructs with
range/validity tests.  Modules so instrumented should be immune to
buffer overflows, invalid heap use, and some other classes of C/C++
programming errors.

%files		-n %{libmudflap}
%{_libdir}/libmudflap.so.%{mudflap_major}
%{_libdir}/libmudflap.so.%{mudflap_major}.*
%{_libdir}/libmudflapth.so.%{mudflap_major}
%{_libdir}/libmudflapth.so.%{mudflap_major}.*

#-----------------------------------------------------------------------
%if %{build_multilib}
%package	-n %{multilibmudflap}
Summary:	GCC mudflap shared support libraries
Group:		System/Libraries
Conflicts:	%{libmudflap} < 4.6.2-11

%description	-n %{multilibmudflap}
This package contains GCC shared libraries which are needed
for mudflap support.

For front-ends that support it (C and C++), instrument all risky
pointer/array dereferencing operations, some standard library
string/heap functions, and some other associated constructs with
range/validity tests.  Modules so instrumented should be immune to
buffer overflows, invalid heap use, and some other classes of C/C++
programming errors.

%files		-n %{multilibmudflap}
%{multilibdir}/libmudflap.so.%{mudflap_major}
%{multilibdir}/libmudflap.so.%{mudflap_major}.*
%{multilibdir}/libmudflapth.so.%{mudflap_major}
%{multilibdir}/libmudflapth.so.%{mudflap_major}.*
%endif

#-----------------------------------------------------------------------
%package	-n %{libmudflap_devel}
Summary:	GCC mudflap development support
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libmudflap} = %{version}-%{release}
%if %{build_multilib}
Requires:	%{multilibmudflap} = %{version}-%{release}
%endif
%if "%libmudflap_devel" != "libmudflap-devel"
Provides:	libmudflap-devel = %{version}-%{release}
%endif
Provides:	mudflap-devel = %{version}-%{release}

%description	-n %{libmudflap_devel}
This package contains GCC libraries which are needed
to compile mudflap support.

%files		-n %{libmudflap_devel}
%{_libdir}/libmudflap.so
%{_libdir}/libmudflapth.so
%if %{build_multilib}
%{multilibdir}/libmudflap.so
%{multilibdir}/libmudflapth.so
%endif
%{gccdir}/include/mf-runtime.h

#-----------------------------------------------------------------------
%package	-n %{libmudflap_static_devel}
Summary:	GCC mudflap static libraries
Group:		Development/C
Requires:	%{libmudflap_devel} = %{version}-%{release}
Provides:	libmudflap-static-devel = %{version}-%{release}
Provides:	mudflap-static-devel = %{version}-%{release}

%description	-n %{libmudflap_static_devel}
This package contains GCC static libraries which are needed
to compile mudflap support.

%files		-n %{libmudflap_static_devel}
%{_libdir}/libmudflap.*a
%{_libdir}/libmudflapth.*a
%if %{build_multilib}
%{multilibdir}/libmudflap.*a
%{multilibdir}/libmudflapth.*a
%endif
#-----------------------------------------------------------------------
# build mudflap
%endif

########################################################################
%if %{build_ssp}
#-----------------------------------------------------------------------
%package	-n %{libssp}
Summary:	GCC SSP shared support library
Group:		System/Libraries
Provides:	libssp = %{version}-%{release}

%description	-n %{libssp}
This package contains GCC shared support library which is needed
for SSP support.

%files		-n %{libssp}
%{_libdir}/libssp.so.%{ssp_major}
%{_libdir}/libssp.so.%{ssp_major}.*

#-----------------------------------------------------------------------
%if %{build_multilib}
%package	-n %{multilibssp}
Summary:	GCC SSP shared support library
Group:		System/Libraries
Provides:	libssp = %{version}-%{release}
Conflicts:	%{libssp} < 4.6.2-11

%description	-n %{multilibssp}
This package contains GCC shared support library which is needed
for SSP support.

%files		-n %{multilibssp}
%{multilibdir}/libssp.so.%{ssp_major}
%{multilibdir}/libssp.so.%{ssp_major}.*
%endif

#-----------------------------------------------------------------------
%package	-n %{libssp_devel}
Summary:	GCC SSP development support
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libssp} = %{version}-%{release}
%if %{build_multilib}
Requires:	%{multilibssp} = %{version}-%{release}
%endif
Provides:	libssp-devel = %{version}-%{release}
Provides:	ssp-devel = %{version}-%{release}

%description	-n %{libssp_devel}
This package contains GCC libraries which are needed
to compile SSP support.

%files		-n %{libssp_devel}
%{_libdir}/libssp.so
%if %{build_multilib}
%{multilibdir}/libssp.so
%endif
%{gccdir}/include/ssp

#-----------------------------------------------------------------------
%package	-n %{libssp_static_devel}
Summary:	GCC SSP static libraries
Group:		Development/C
Requires:	%{libssp_devel} = %{version}-%{release}
Provides:	libssp-static-devel = %{version}-%{release}
Provides:	ssp-static-devel = %{version}-%{release}

%description	-n %{libssp_static_devel}
This package contains GCC static libraries which are needed
to compile SSP support.

%files		-n %{libssp_static_devel}
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
%package	-n %{libitm}
Summary:	GCC Transactional Memory support library
Group:		System/Libraries
Provides:	libitm = %{version}-%{release}

%description	-n %{libitm}
This package contains GCC's Transactional Memory support library.

%files		-n %{libitm}
%{_libdir}/libitm.so.%{itm_major}
%{_libdir}/libitm.so.%{itm_major}.*

#-----------------------------------------------------------------------
%if %{build_multilib}
%package	-n %{multilibitm}
Summary:	GCC Transactional Memory support library
Group:		System/Libraries
Provides:	libitm = %{version}-%{release}

%description	-n %{multilibitm}
This package contains GCC's Transactional Memory support library.

%files		-n %{multilibitm}
%{multilibdir}/libitm.so.%{itm_major}
%{multilibdir}/libitm.so.%{itm_major}.*
%endif

#-----------------------------------------------------------------------
%package	-n %{libitm_devel}
Summary:	GCC Transactional Memory development support
Group:		Development/C
Requires:	%{name} = %{version}-%{release}
Requires:	%{libitm} = %{version}-%{release}
%if %{build_multilib}
Requires:	%{multilibitm} = %{version}-%{release}
%endif
Provides:	libitm-devel = %{version}-%{release}
Provides:	itm-devel = %{version}-%{release}

%description	-n %{libitm_devel}
This package contains GCC libraries which are needed
to use Transactional Memory features.

%files		-n %{libitm_devel}
%{_libdir}/libitm.so
%{_libdir}/libitm.spec
%if %{build_multilib}
%{multilibdir}/libitm.so
%{multilibdir}/libitm.spec
%endif
%_infodir/libitm.info*

#-----------------------------------------------------------------------
%package	-n %{libitm_static_devel}
Summary:	GCC Transactional Memory static libraries
Group:		Development/C
Requires:	%{libitm_devel} = %{version}-%{release}
Provides:	libitm-static-devel = %{version}-%{release}
Provides:	itm-static-devel = %{version}-%{release}

%description	-n %{libitm_static_devel}
This package contains GCC static libraries which are needed
to compile Transactional Memory support.

%files		-n %{libitm_static_devel}
%{_libdir}/libitm.a
%if %{build_multilib}
%{multilibdir}/libitm.a
%endif
#-----------------------------------------------------------------------
# build itm
%endif

########################################################################
%prep
%if "%linaro" != ""
  %setup -q -n gcc-linaro-%branch-%linaro
%else
%if %{official}
  %setup -q -n gcc-%{version}%{snapshot}
%else
  %setup -q -n gcc-%{branch}%{snapshot}
%endif
%endif

%patch0 -p1 -b .uclibc~
%patch1 -p1 -b .java~
%patch2 -p1 -b .pdf~
%patch3 -p1 -b .linux32~
%patch4 -p1 -b .execstack~
%patch5 -p1 -b .linker-selection~
%patch6 -p1 -b .ac269~
%patch7 -p1 -b .plugindet~
# Breaks the build, see comment on bug 33763
#patch8 -p1 -b .ext_inline~
%patch9 -p1 -b .android~

aclocal -I config
autoconf

echo %{vendor} > gcc/DEV-PHASE
%if !%{official}
    sed -i -e 's/4\.7\..*/%{version}/' gcc/BASE-VER
%endif

%if %{with java_bootstrap}
    tar xjf %{SOURCE6}
%endif

#-----------------------------------------------------------------------
%build
# The -gdwarf-4 removal is a workaround for gcc bug #52420
OPT_FLAGS=`echo %{optflags} |					\
	sed	-e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'	\
		-e 's/-m\(31\|32\|64\)//g'			\
		-e 's/-fstack-protector//g'			\
		-e 's/--param=ssp-buffer-size=4//'		\
		-e 's/-gdwarf-4/-g/'				\
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

# FIXME: Replace
#	--with-multilib-list=m32,m64
# with	--with-multilib-list=m32,m64,mx32
# once the build process is fixed.
# Currently, it barfs while linking x32/libgcc_s.so.1 (incompatible target)

CC=%{__cc}							\
CFLAGS="$OPT_FLAGS"						\
CXXFLAGS="$OPT_FLAGS"						\
GCJFLAGS="$OPT_FLAGS"						\
TCFLAGS="$OPT_FLAGS"						\
XCFLAGS="$OPT_FLAGS"						\
%configure2_5x							\
%if !%{build_java}
	--disable-libgcj					\
%else
	--disable-libjava-multilib				\
	--with-java-home=%{_jvmdir}/java-1.5.0-gcj-1.5.0.0/jre	\
	--with-ecj-jar=%{_datadir}/java/eclipse-ecj.jar		\
	--enable-java-awt=gtk					\
	--enable-gtk-cairo					\
%endif
%if !%{build_cloog}
	--without-cloog						\
	--without-ppl						\
%else
	--with-cloog						\
	--with-ppl						\
	--enable-cloog-backend=isl				\
	--disable-cloog-version-check				\
%endif
%if !%{build_ffi}
	--disable-libffi					\
%endif
%if !%{build_gomp}
	--disable-libgomp					\
%endif
%if !%{build_quadmath}
	--disable-libquadmath					\
  %if %{build_fortran}
	--disable-libquadmath-support				\
  %endif
%endif
%if !%{build_mudflap}
	--disable-libmudflap					\
%endif
%if !%{build_ssp}
	--disable-libssp					\
%endif
	--disable-libunwind-exceptions				\
	--disable-werror					\
	--enable-__cxa_atexit					\
	--enable-gold=default					\
	--with-plugin-ld=%_bindir/ld				\
%if %{system_compiler}
	--enable-bootstrap					\
%endif
	--enable-checking=release				\
	--enable-gnu-unique-object				\
	--enable-languages="$LANGUAGES"				\
	--enable-linker-build-id				\
%if !%{build_plugin}
	--disable-plugin					\
%else
	--enable-plugin						\
	--enable-lto						\
%endif
	--enable-shared						\
%if !%{system_compiler}
	--disable-static					\
%endif
	--enable-threads=posix					\
	--with-system-zlib					\
	--with-bugurl=https://qa.mandriva.com/			\
%ifarch %{ix86} x86_64
	--with-tune=generic					\
%endif
%ifarch %{ix86}
	--with-arch=i586					\
%endif
%ifarch x86_64
  %if %{build_multilib}
	--with-arch_32=i586					\
	--with-multilib-list=m32,m64				\
  %else
	--disable-multilib					\
  %endif
%endif
%ifarch armv5te
	--with-arch=armv5te					\
%endif
%ifarch armv7l armv7hl
	--with-cpu=cortex-a8					\
	--with-tune=cortex-a8					\
	--with-arch=armv7-a					\
	--with-mode=thumb					\
  %ifarch armv7l
	--with-float=softfp					\
  %else
	--with-float=hard					\
  %endif
	--with-fpu=vfpv3-d16					\
	--with-abi=aapcs-linux					\
%endif
	--host=%{_target_platform}				\
	--target=%{_target_platform}

GCJFLAGS="$OPT_FLAGS"						\
%make BOOT_CFLAGS="$OPT_FLAGS" $BOOTSTRAP

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
find libjava -name \*.h -type f |					\
    xargs grep -l '// DO NOT EDIT THIS FILE - it is machine generated'	\
    > libjava-classes.list
find libjava -name \*.class -type f >> libjava-classes.list
find libjava/testsuite -name \*.jar -type f >> libjava-classes.list
tar cf - -T libjava-classes.list | bzip2 -9				\
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
%makeinstall_std

%if %{build_java}
    %make							\
	DESTDIR=%{buildroot}					\
	JAR=$PWD/%{_target_platform}/libjava/scripts/jar	\
	-C %{_target_platform}/libjava				\
	install-src.zip
%endif

# configure python dir option does not cover libstdc++ and needs to remove
# /usr prefix for libjava
mkdir -p %{buildroot}%{py_puresitedir}
if [ -d %{buildroot}%{_datadir}/gcc-%{ver}/python ]; then
    mv -f %{buildroot}%{_datadir}/gcc-%{ver}/python/*		\
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
    mv -f %{buildroot}%{_libdir}/libstdc++.so.*.py		\
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
	mv -f %{buildroot}%{multilibdir}/libstdc++.so.*.py		\
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
    ln -sf libgcj_bc.so.1.0.0 %buildroot%_libdir/libgcj_bc.so
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

%if %{build_ada}
    for lib in libgnarl libgnat; do
	rm -f	%{buildroot}%{_libdir}/$lib.so
	rm -f	%{buildroot}%{gccdir}/adalib/$lib.so
	mv -f	%{buildroot}%{gccdir}/adalib/$lib-%{branch}.so		\
		%{buildroot}%{_libdir}/$lib-%{branch}.so.1
	ln -sf	$lib-%{branch}.so.1 %{buildroot}%{_libdir}/$lib-%{branch}.so
	ln -sf	$lib-%{branch}.so.1 %{buildroot}%{_libdir}/$lib.so
    %if %{build_multilib}
	rm -f %{buildroot}%{multilibdir}/$lib.so
	rm -f	%{buildroot}%{multigccdir}/adalib/$lib.so
	mv -f	%{buildroot}%{multigccdir}/adalib/$lib-%{branch}.so	\
		%{buildroot}%{multilibdir}/$lib-%{branch}.so.1
	ln -sf	$lib-%{branch}.so.1 %{buildroot}%{multilibdir}/$lib-%{branch}.so
	ln -sf	$lib-%{branch}.so.1 %{buildroot}%{multilibdir}/$lib.so
    %endif
    done
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

# https://qa.mandriva.com/show_bug.cgi?id=63587
%if %{build_plugin}
    pushd host-%{_target_platform}
	cp -fpa gcc/build/gengtype %{buildroot}%{gccdir}
	cp -fpa gcc/gtype.state %{buildroot}%{gccdir}
    popd
%endif

# Not needed on cooker (but on ROSA 2012 and backports, and
# can't hurt)
rm -f %buildroot%_libdir/libitm.la \
      %buildroot%_prefix/lib/libitm.la \
      %buildroot%_libdir/gcj-*/*.la

%if 1
# Workaround for all gcj related tools
# somehow getting the same build ID
strip --strip-unneeded \
	%buildroot%_bindir/gc-analyze \
	%buildroot%_bindir/gappletviewer \
	%buildroot%_bindir/gjar \
	%buildroot%_bindir/gij \
	%buildroot%_bindir/gjavah \
	%buildroot%_bindir/gjarsigner \
	%buildroot%_bindir/gkeytool \
	%buildroot%_bindir/gjdoc \
	%buildroot%_bindir/gorbd \
	%buildroot%_bindir/grmic \
	%buildroot%_bindir/grmid \
	%buildroot%_bindir/gnative2ascii \
	%buildroot%_bindir/gserialver \
	%buildroot%_bindir/grmiregistry \
	%buildroot%_bindir/jv-convert \
	%buildroot%_bindir/gtnameserv \
	%buildroot%_bindir/gcjh
%endif
