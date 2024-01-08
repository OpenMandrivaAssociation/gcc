# Listed targets are short form and will be expanded by rpm
# gnueabihf variants etc. are inserted by rpm into long_targets
%ifarch %{riscv}
# Still missing a few deps...
%global targets aarch64-linux armv7hnl-linux x86_64-linux x32-linux riscv64-linux aarch64-linuxmusl armv7hnl-linuxmusl i686-linuxmusl x86_64-linuxmusl x32-linuxmusl riscv64-linuxmusl
%else
%ifarch %{arm}
# Also missing a few deps...
%global targets aarch64-linux armv7hnl-linux x32-linux riscv64-linux aarch64-linuxmusl armv7hnl-linuxmusl i686-linuxmusl x32-linuxmusl riscv64-linuxmusl i686-linux
%global bootstraptargets aarch64-linuxuclibc armv7hnl-linuxuclibc i686-linuxuclibc x86_64-linuxuclibc x32-linuxuclibc riscv64-linuxuclibc ppc64-linuxuclibc ppc64le-linuxuclibc ppc64-linuxmusl ppc64-linux ppc64le-linux ppc64le-linuxmusl x86_64-linux x86_64-linuxmusl
# FIXME determine why Windoze crosscompilers don't compile on arm32
# i686-mingw32 x86_64-mingw32
%else
%ifarch %{ix86}
# FIXME at some point, we need to figure out why x86_32 to
# x86_64-mingw crosscompilers are broken
%global targets aarch64-linux armv7hnl-linux x32-linux riscv64-linux i686-mingw32
%global bootstraptargets i686-linux aarch64-linuxuclibc armv7hnl-linuxuclibc i686-linuxuclibc riscv64-linuxuclibc ppc64-linux ppc64le-linux x86_64-linux aarch64-linuxmusl armv7hnl-linuxmusl i686-linuxmusl x86_64-linuxmusl x32-linuxmusl riscv64-linuxmusl
%else
%global targets aarch64-linux armv7hnl-linux x86_64-linux x32-linux riscv64-linux aarch64-linuxmusl armv7hnl-linuxmusl i686-linuxmusl x86_64-linuxmusl x32-linuxmusl riscv64-linuxmusl i686-mingw32 x86_64-mingw32 i686-linux ppc64le-linux ppc64le-linuxmusl ppc64-linux ppc64-linuxmusl
%global bootstraptargets aarch64-linuxuclibc armv7hnl-linuxuclibc i686-linuxuclibc x86_64-linuxuclibc x32-linuxuclibc riscv64-linuxuclibc ppc64-linuxuclibc ppc64le-linuxuclibc
%endif
%endif
%endif
# Once bionic is built, add: aarch64-android armv7l-android armv8l-android
%global long_targets %(
        for i in %{targets}; do
                CPU=$(echo $i |cut -d- -f1)
                OS=$(echo $i |cut -d- -f2)
                echo -n "$(rpm --target=${CPU}-${OS} -E %%{_target_platform}) "
        done
)
%global long_bootstraptargets %(
        for i in %{bootstraptargets}; do
                CPU=$(echo $i |cut -d- -f1)
                OS=$(echo $i |cut -d- -f2)
                echo -n "$(rpm --target=${CPU}-${OS} -E %%{_target_platform}) "
        done
)
%bcond_without crosscompilers

# functions with printf format attribute but with special parser and also
# receiving non constant format strings
%define		Werror_cflags			%{nil}

# avoid failures when testing if compiler used to build gcc can generate
# shared objects (regardless of unresolved symbols)
%define		_disable_ld_no_undefined	1

# avoid build failure due to configure built with different autoconf version
%define		_disable_libtoolize		1
# -flto in compiler flags breaks things, but --with-build-config=bootstrap-lto
# does the right thing
%define		_disable_lto			1

# (tpg) optimize it a bit
%global optflags %{optflags} -O3
#-----------------------------------------------------------------------

%define nof_arches		noarch
%define biarches		%{x86_64} mips64 mips64el mips mipsel

%define	system_gcc		1

%if %{system_gcc}
%define cross_prefix		%{nil}
%define cross_program_prefix	%{nil}
%define package_suffix		%{nil}
%define program_prefix		%{nil}
%define program_suffix		%{nil}
%define	program_long_suffix	-%{version}
%else
%define cross_prefix		%{nil}
%define cross_program_prefix	%{nil}
%define package_suffix		%{branch}
%define program_prefix		%{nil}
%define program_suffix		%{branch}
%define program_long_suffix	%{branch}
%endif

# Define GCC target platform, and arch we built for
%define arch			%(echo %{_target_cpu}|sed -e "s/\\(i.86\\|athlon\\)/i386/" -e "s/amd64/x86_64/")
%define	target_cpu		%{arch}
%define gcc_target_platform	%{_target_platform}
%define isarch()		%(case " %* " in (*" %{arch} "*) echo 1;; (*) echo 0;; esac)

%if %isarch %{x86_64}
%define multilib_32_arch	i686
%endif
%if %isarch mips64
%define	multilib_32_arch	mips
%endif
%if %isarch mips64el
%define	multilib_32_arch	mipsel
%endif
%if %isarch %{biarches}
%define gcc32_target_platform	%{multilib_32_arch}-%{_target_vendor}-%{_target_os}%{?_gnu}
%endif

%define		default_compiler	0
%define		majorver		%(echo %{version} |cut -d. -f1)
%define		branch			13.2
%define		ver			%{branch}.1
%define		prerelease		20240106
#define		beta			%{nil}
%define		gcclibexecdirparent	%{_libexecdir}/gcc/%{gcc_target_platform}/
%define		gcclibexecdir		%{gcclibexecdirparent}/%{ver}
%define		gccdirparent		%{_libdir}/gcc/%{gcc_target_platform}/
%define		gccdir			%{gccdirparent}/%{ver}
%define		multigccdir		%{_libdir}/gcc/%{gcc_target_platform}/%{ver}/32
%define		multigccdirn32		%{_libdir}/gcc/%{gcc_target_platform}/%{ver}/n32
%define		multigccdir64		%{_libdir}/gcc/%{gcc_target_platform}/%{ver}/64
%define		multilibdir		%{_prefix}/lib

#-----------------------------------------------------------------------
%define		gcc_major		1
%define		libgcc			%mklibname gcc %{gcc_major}
%define		multilibgcc		libgcc%{gcc_major}
%define		libx32gcc		libx32gcc%{gcc_major}
%define		libgcc_devel		%mklibname gcc -d
%define		libgcc_static_devel	%mklibname gcc -d -s
%define		stdcxx_major		6
%define		libstdcxx		%mklibname stdc++ %{stdcxx_major}
%define		libstdcxx_devel		%mklibname stdc++ -d
%define		libstdcxx_static_devel	%mklibname stdc++ -d -s
%define		multilibstdcxx		libstdc++%{stdcxx_major}
%define		d_major			2
%define		libgdruntime		%mklibname gdruntime %{d_major}
%define		libgdruntime_devel	%mklibname gdruntime -d
%define		libgdruntime_static_devel	%mklibname gdruntime -d -s
%define		multilibgdruntime	libgdruntime%{d_major}
%define		gfortran_major		5
%define		libgfortran		%mklibname gfortran %{gfortran_major}
%define		libgfortran_devel	%mklibname gfortran -d
%define		libgfortran_static_devel %mklibname gfortran -d -s
%define		multilibgfortran	libgfortran%{gfortran_major}
%define		ffi_major		4
%define		libffi			%mklibname ffi %{ffi_major}
%define		libffi_devel		%mklibname ffi -d
%define		libffi_static_devel	%mklibname ffi -d -s
%define		multilibffi		libffi%{ffi_major}
%define		mpx_major		2
%define		libmpx			%mklibname mpx %{mpx_major}
%define		libmpx_devel		%mklibname mpx -d
%define		libmpx_static_devel	%mklibname mpx -d -s
%define		multilibmpx		libmpx%{mpx_major}
%define		mpxwrappers_major	2
%define		libmpxwrappers		%mklibname mpxwrappers %{mpxwrappers_major}
%define		libmpxwrappers_devel	%mklibname mpxwrappers -d
%define		libmpxwrappers_static_devel	%mklibname mpxwrappers -d -s
%define		multilibmpxwrappers	libmpxwrappers%{mpxwrappers_major}
%define		gnat_major		1
%define		libgnat			%mklibname gnat %{gnat_major}
%define		libgnat_devel		%mklibname gnat -d
%define		libgnat_static_devel	%mklibname gnat -d -s
%define		multilibgnat		libgnat%{gnat_major}
%define		go_major		19
%define		libgo			%mklibname go %{go_major}
%define		libgo_devel		%mklibname go -d
%define		libgo_static_devel	%mklibname go -d -s
%define		multilibgo		libgo%{go_major}
%define		cc1_major		0
%define		libcc1			%mklibname cc1 %{cc1_major}
%define		libcc1_devel		%mklibname cc1 -d
%define		libcc1_static_devel	%mklibname cc1 -d -s
%define		gomp_major		1
%define		libgomp			%mklibname gomp %{gomp_major}
%define		libgomp_devel		%mklibname gomp -d
%define		libgomp_static_devel	%mklibname gomp -d -s
%define		multilibgomp		libgomp%{gomp_major}
%define		objc_major		4
%define		libobjc			%mklibname objc %{objc_major}
%define		libobjc_devel		%mklibname gccobjc -d
%define		libobjc_static_devel	%mklibname gccobjc -d -s
%define		multilibobjc		libgccobjc%{objc_major}
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
%define		asan_major		8
%define		libasan			%mklibname asan %{asan_major}
%define		libasan_devel		%mklibname asan -d
%define		libasan_static_devel	%mklibname asan -d -s
%define		multilibasan		libasan%{asan_major}
%define		tsan_major		2
%define		libtsan			%mklibname tsan %{tsan_major}
%define		libtsan_devel		%mklibname tsan -d
%define		libtsan_static_devel	%mklibname tsan -d -s
%define		atomic_major		1
%define		libatomic		%mklibname atomic %{atomic_major}
%define		libatomic_devel		%mklibname atomic -d
%define		libatomic_static_devel	%mklibname atomic -d -s
%define		multilibatomic		libatomic%{atomic_major}
%define		ubsan_major		1
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
# FIXME This should be re-enabled, for a yet undetermined reason
# "make install" fails on broken *.Po files when building gcc
# 12.0-20220313 with gcc 11.2.1
%define		build_d			0
%define		build_lto		1
%define		build_atomic		1
%define		build_objc		0
%define		build_objcxx		0
%define		build_rust		0
%define		build_quadmath		0
%define		build_ssp		0
%define		build_ubsan		%{system_gcc}
%if %isarch %{ix86} %{x86_64} %{arm}
%define		build_itm		1
%else
# aarch64 libitm support not implemented yet
%define		build_itm		0
%endif
%define		build_cloog		%{system_gcc}
%define		build_cxx		%{system_gcc}
%define		build_doc		0
%define		build_ffi		%{system_gcc}
%define		build_fortran		%{system_gcc}
%define		build_gomp		%{system_gcc}
# need to build if major does not conflict with current system_gcc
%define		build_libgcc		%{system_gcc}
%define		build_pdf		%{build_doc}
%define		build_plugin		%{system_gcc}
%if %isarch %{x86_64} %{armx}
  %define	build_tsan		%{system_gcc}
  %define	build_lsan		%{system_gcc}

%if %isarch %{x86_64}
  %define	build_multilib		%{system_gcc}
%endif
%endif
%if %isarch %{ix86} %{x86_64}
  %define	build_quadmath		%{system_gcc}
  %define	build_doc		1
  %define	build_vtv		%{system_gcc}
%endif
%if %isarch %{ix86} %{x86_64}
  %define	build_ada		%{system_gcc}
%endif
%if %isarch %{ix86} %{x86_64} %{armx}
  %define	build_objc		%{system_gcc}
  %define	build_objcxx		%{system_gcc}
  #define	build_rust		%{system_gcc}
# FIXME restore go when it's fixed
# As of 12.0: No rule to make target '../libbacktrace/libbacktrace.la', needed by 'libgo.la'.
  %define	build_go		0
%if %isarch %{ix86} %{x86_64} %{arm} %{aarch64} %{riscv}
  %define	build_asan		%{system_gcc}
%else
  %define	build_asan		0
%endif
%endif

%define		build_doc		0
%define		build_pdf		0

%define		package_ffi		0

# Some versions of gcc build shared libgnat/libgnarl, some don't...
%define		shared_libgnat		1

# Define C library to use
%define		libc			glibc
%define		libc_shared		1

%define		build_minimal		0

%if %{build_minimal}
%define		build_ada		0
%define		build_asan		0
%define		build_atomic		0
%define		build_check		0
%define		build_go		0
%define		build_d			0
%define		build_lto		0
%define		build_lsan		0
%define		build_objc		0
%define		build_objcxx		0
%define		build_rust		0
%define		build_quadmath		0
%define		build_ssp		0
%define		build_tsan		0
%define		build_ubsan		0
%define		build_vtv		0
%define		build_itm		0
%define		build_cloog		0
%define		build_cxx		0
%define		build_doc		0
%define		build_ffi		0
%define		build_fortran		0
%define		build_gomp		0
%define		build_libgcc		0
%define		build_pdf		0
%define		build_plugin		0
%define		package_ffi		0
%define		shared_libgnat		0
%endif

#-----------------------------------------------------------------------

Summary:	GNU Compiler Collection
%if %{system_gcc}
Name:		gcc
%else
Name:		gcc%{package_suffix}
%endif
License:	GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group:		Development/C
Url:		http://gcc.gnu.org/
%if "%{prerelease}" != ""
Version:	%{ver}
Release:	0.%(echo %{prerelease} |sed -e 's,-,_,g').1
%define srcname gcc-%{?beta:%{version}}%{!?beta:%{majorver}}-%{?beta:%{beta}-}%{prerelease}
Source0:	http://mirror.koddos.net/gcc/snapshots/%{?beta:%{version}}%{!?beta:%{majorver}}-%{?beta:%{beta}-}%{prerelease}/%{srcname}.tar.xz
Source1:	http://mirror.koddos.net/gcc/snapshots/%{?beta:%{version}}%{!?beta:%{majorver}}-%{?beta:%{beta}-}%{prerelease}/sha512.sum
%else
Version:	%{ver}
Release:	1
# http://www.gnu.org/prep/ftp.html ...
Source0:	http://mirror.koddos.net/gcc/releases/gcc-%{version}/gcc-%{version}.tar.xz
Source1:	http://mirror.koddos.net/gcc/releases/gcc-%{version}/sha512.sum
%define srcname gcc-%{version}
%endif
Source4:	c89
Source5:	c99

# environment variables for enabling/disabling colorized gcc output
Source10:	gcc.sysconfig
Source11:	gcc.sh
Source12:	gcc.csh

Source100:	gcc.rpmlintrc

Patch0:		gcc-4.7.1-uclibc-ldso-path.patch
Patch1:		libstdc++-pthread-linkage.patch
Patch2:		gcc-13.1.0-crosscompiler-lld-mold.patch
#Patch3:		gcc-4.7.1-linux32.patch
Patch4:		gnatmake-execstack.patch
Patch5:		gcc-20231125-fix-unused-variables.patch
#Patch6:		gcc-9-20190706-use-bfd-ld-with-lto.patch
Patch7:		gcc-4.7.1-linker-plugin-detect.patch
Patch8:		gcc-4.7.1-extern-inline-not-inlined.patch
# Patch for Android compatibility (creating Linux->Android crosscompilers etc)
Patch9:		gcc-4.7-androidcompat.patch
# https://github.com/llvm/llvm-project/issues/50248
# Affects building chromium with the clang/libstdc++ combo
Patch10:	libstdc++-workaround-clang-bug-50248.patch
# Seems to be still required on armv7hnl
Patch12:	gcc-4.8-non-fatal-compare-failure.patch
# https://bugs.launchpad.net/gcc-linaro/+bug/1225317
Patch13:	Gcc-4.8.2-arm-thumb2-CASE_VECTOR_SHORTEN_MODE.patch
# FIXME this is ***evil***
# Without this patch, we get an Exec format error every time cc1plus is run inside qemu.
# A notable difference:
# Without the patch:
# $ file except.o
# except.o: ELF 64-bit LSB relocatable, ARM aarch64, version 1 (SYSV), not stripped
# With the patch:
# except.o: ELF 64-bit LSB relocatable, ARM aarch64, version 1 (GNU/Linux), not stripped
# Apparently, the kernel or glibc can't handle Linux specific object files in
# qemu?
# This needs further debugging (and preferrably testing on real hardware), but
# for now, the evil patch allows us to continue building.
Patch16:	gcc-4.9-aarch64-evil-exception-workaround.patch

# Provide functions from compiler-rt in libgcc
Patch17:	gcc-6.3-libgcc-__muloti4.patch

# MUSL Support
Patch18:	gcc-5.1.0-libstdc++-musl.patch

Patch20:	gcc-6.3-libgcc-musl-workaround.patch

# From Google's tree
# 331e362574142e4c1d9d509533d1c96b6dc54d13
Patch104:	gcc-4.9-simplify-got.patch

# MUSL support
Patch203:	0003-musl-unwind.patch
Patch205:	0005-musl-config-revert.patch
Patch206:	0006-musl-config.patch
Patch207:	0007-musl-gcc.patch
Patch208:	0008-musl-mips.patch
Patch209:	0009-musl-x86.patch

# Patches 1001 and 1007 disabled until they're committed
# slibdir is either /lib or /lib64
Patch1001:	gcc33-pass-slibdir.patch
# pass libdir around
Patch1007:	gcc-4.6.2-multi-do-libdir.patch

# Fix build of libstdc++ for mingw crosscompilers
Patch1008:	libstdc++-12.0-mingw-crosscompilers.patch
# Fix linking the stage-1 ADA compiler
Patch1009:	gcc-12-fix-stage1-ada-linkage.patch

%ifarch %{x86_64}
# 32-bit glibc needed for 32-bit libstdc++ and friends
BuildRequires:	libc6
%endif
BuildRequires:	binutils >= 2.20.51.0.2
BuildRequires:	dejagnu
BuildRequires:	elfutils-devel >= 0.147
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gdb
BuildRequires:	gettext
BuildRequires:	sharutils
BuildRequires:	diffutils
BuildRequires:	texinfo
BuildRequires:	locales-en
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	locales-extra-charsets
# For py_puresitedir
%if ! %{build_minimal}
BuildRequires:	python >= 3.4
%endif
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

%if %{system_gcc}
Requires:	%{name}-cpp >= %{EVRD}
Requires:	%{libgcc} >= %{EVRD}
Requires:	%{libgcc_devel} >= %{EVRD}
Requires:	%{libgomp} >= %{EVRD}
Requires:	%{libcc1} >= %{EVRD}
# as gcc now has it's own output color support, let's obsolete the old
# colorgcc with it's perl wrapper script which is slightly buggy with it's
# it's output redirection anyways...
Obsoletes:	colorgcc <= 1.3.2-17
%endif
Requires:	binutils >= 2.20.51.0.2

Obsoletes:	%{_lib}mudflap0 < 4.9.1_2014.05
Obsoletes:	%{_lib}mudflap-devel < 4.9.1_2014.05
Obsoletes:	%{_lib}mudflap-static-devel < 4.9.1_2014.05

# Presence of a previous cross-mingw toolchain results in libstdc++
# linking against libgcc from that toolchain, potentially causing ABI
# issues.
BuildConflicts:	cross-i686-w64-mingw32-gcc
BuildConflicts:	cross-x86_64-w64-mingw32-gcc

# Allow "lazy dependencies" (without having to check if a needed
# compiler is a cross-compiler or native). Obviously a native
# compiler is a "cross-compiler" to its own architecture.
Provides:	cross-%{gcc_target_platform}-gcc = %{EVRD}
Provides:	cross-%{gcc_target_platform}-gcc-bootstrap = %{EVRD}

%description
The gcc package contains the GNU Compiler Collection version %{branch}.

%if %{system_gcc}
%files -f gcc.lang
%else
%files
%endif
%{_bindir}/%{gcc_target_platform}-gcc
%{_bindir}/%{gcc_target_platform}-gcc-ar
%{_bindir}/%{gcc_target_platform}-gcc-nm
%{_bindir}/%{gcc_target_platform}-gcc-ranlib
%{_bindir}/lto-dump
%(
	if [ -n "$(echo %{gcc_target_platform} |cut -d- -f4-)" ]; then
		shortplatform="$(echo %{gcc_target_platform} |cut -d- -f1)-$(echo %{gcc_target_platform} |cut -d- -f3-)"
		echo "%%optional %{_bindir}/${shortplatform}-gcc"
		echo "%%optional %{_bindir}/${shortplatform}-gcc-%{ver}"
		echo "%%optional %{_bindir}/${shortplatform}-gcc-ar"
		echo "%%optional %{_bindir}/${shortplatform}-gcc-nm"
		echo "%%optional %{_bindir}/${shortplatform}-gcc-ranlib"
	fi
)
%config(noreplace) %{_sysconfdir}/sysconfig/gcc
%{_sysconfdir}/profile.d/90gcc.sh
%{_sysconfdir}/profile.d/90gcc.csh
%if %{default_compiler}
%{_bindir}/c++
%{_bindir}/c89
%{_bindir}/c99
%{_bindir}/cc
%endif
%{_bindir}/gcc
%{_bindir}/gcc-ar
%{_bindir}/gcc-nm
%{_bindir}/gcc-ranlib
%{_bindir}/gcov
%{_bindir}/gcov-dump
%{_bindir}/gcov-tool
%doc %{_mandir}/man1/gcc.1*
%doc %{_mandir}/man1/gcov.1*
%doc %{_mandir}/man1/gcov-dump.1*
%doc %{_mandir}/man1/gcov-tool.1*
%doc %{_mandir}/man1/lto-dump.1*
%doc %{_mandir}/man7/*
%doc %{_infodir}/gcc.info*
%doc %{_infodir}/gccint.info*
%doc %{_infodir}/gccinstall.info*
# Marked optional because of weird failure on armv7hnl
%optional %doc %{_infodir}/libquadmath.info*
%{_bindir}/gcc-%{ver}
%{_bindir}/%{gcc_target_platform}-gcc-%{ver}
%dir %{_libdir}/gcc
%if "%{_lib}" != "lib"
%{_prefix}/lib/gcc
%endif
%dir %{gccdirparent}
%dir %{gccdir}
%dir %{gcclibexecdirparent}
%dir %{gcclibexecdir}
%{gcclibexecdir}/cc1
%{gcclibexecdir}/collect2
%{gccdir}/libgcov.a
%{_libdir}/libgcov.a
%{gcclibexecdir}/lto*
%if %{build_lto}
%{gcclibexecdir}/liblto*
%{_libdir}/bfd-plugins/liblto_plugin.so
%endif
%dir %{gccdir}/include
%{gccdir}/include/*.h
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
%if %isarch mips mipsel
%dir %{multigccdirn32}
%{multigccdirn32}/libgcov.a
%dir %{multigccdir64}
%{multigccdir64}/libgcov.a
%else
%dir %{multigccdir}
%{multigccdir}/libgcov.a
%endif
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
%{_libdir}/libgcc_s.so.%{gcc_major}

#-----------------------------------------------------------------------

%package -n %{libgcc_devel}
Summary:	Development files for libgcc
Group:		System/Libraries
Requires:	%{libgcc} = %{EVRD}

%description -n %{libgcc_devel}
The %{libgcc} package contains header files and object files needed to
build applications with libgcc.

%files -n %{libgcc_devel}
%{_libdir}/libgcc_s.so
%if %{build_multilib}
%{_prefix}/lib/libgcc_s.so
%endif
%{gccdir}/*.o
%{gccdir}/libgcc*.a
%{_libdir}/*.o
%{_libdir}/libgcc*.a
%if %{build_multilib}
%ifarch mips mipsel
%dir %{multigccdirn32}
%{multigccdirn32}/*.o
%{multigccdirn32}/libgcc*.a
%dir %{multigccdir64}
%{multigccdir64}/*.o
%{multigccdir64}/libgcc*.a
%else
%dir %{multigccdir}
%{multigccdir}/*.o
%{multigccdir}/libgcc*.a
%endif
%endif

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibgcc}
Summary:	GNU C library
Group:		System/Libraries
Conflicts:	%{libgcc} < 4.6.2-11

%description -n %{multilibgcc}
The %{multilibgcc} package contains GCC shared libraries for gcc %{branch}

%files -n %{multilibgcc}
%{_prefix}/lib/libgcc_s.so.%{gcc_major}
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
%if %{system_gcc}
#-----------------------------------------------------------------------

%package cpp
Summary:	The C Preprocessor
Group:		Development/C
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

%if %{system_gcc}
%files cpp -f cpplib.lang
%else
%files cpp
%endif
%{_bindir}/cpp
%{_bindir}/%{gcc_target_platform}-cpp
%{_bindir}/%{gcc_target_platform}-cpp-%{ver}
%(
	if [ -n "$(echo %{gcc_target_platform} |cut -d- -f4-)" ]; then
		shortplatform="$(echo %{gcc_target_platform} |cut -d- -f1)-$(echo %{gcc_target_platform} |cut -d- -f3-)"
		echo "%%optional %{_bindir}/${shortplatform}-cpp"
		echo "%%optional %{_bindir}/${shortplatform}-cpp-%{ver}"
	fi
)
%if %{system_gcc}
%{_prefix}/lib/cpp
%doc %{_mandir}/man1/cpp.1*
%doc %{_infodir}/cpp*
%if %{build_doc}
%doc %{_docdir}/gcc-cpp
%endif
%endif

#-----------------------------------------------------------------------
# system_gcc
%endif

########################################################################
%if %{build_cxx}
#-----------------------------------------------------------------------

%package c++
Summary:	C++ support for gcc
Group:		Development/C++
Requires:	%{name} = %{EVRD}
%if %{system_gcc}
Requires:	%{libstdcxx_devel} = %{version}
%endif

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%files c++
%if %{system_gcc}
%{_bindir}/g++
%doc %{_mandir}/man1/g++.1*
%endif
%if %{system_gcc}
%{_bindir}/%{gcc_target_platform}-c++
%{_bindir}/%{gcc_target_platform}-g++
%endif
%{_bindir}/c++-%{ver}
%{_bindir}/g++-%{ver}
%{_libexecdir}/gcc/%{gcc_target_platform}/%{ver}/g++-mapper-server
%{_bindir}/%{gcc_target_platform}-g++-%{ver}
%(
	if [ -n "$(echo %{gcc_target_platform} |cut -d- -f4-)" ]; then
		shortplatform="$(echo %{gcc_target_platform} |cut -d- -f1)-$(echo %{gcc_target_platform} |cut -d- -f3-)"
		echo "%%optional %{_bindir}/${shortplatform}-c++"
		echo "%%optional %{_bindir}/${shortplatform}-g++"
		echo "%%optional %{_bindir}/${shortplatform}-g++-%{ver}"
	fi
)
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

%if %{system_gcc}
%files -n %{libstdcxx} -f libstdc++.lang
%else
%files -n %{libstdcxx}
%endif
%{_libdir}/libstdc++.so.%{stdcxx_major}*

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
%{multilibdir}/libstdc++.so.%{stdcxx_major}*
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
%define __requires_exclude_from ^(%{py_puresitedir}|%{_datadir}/gdb/).*$

%description -n %{libstdcxx_devel}
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%files -n %{libstdcxx_devel}
%{_includedir}/c++/%{ver}
%{_libdir}/libstdc++.so
%if ! %{cross_compiling}
%{_datadir}/gdb/auto-load%{_libdir}/libstdc++.*.py
%endif
%if %{build_multilib}
%{multilibdir}/libstdc++.so
%if ! %{cross_compiling}
%{_datadir}/gdb/auto-load%{multilibdir}/libstdc++.*.py
%endif
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
%{_libdir}/libstdc++exp.*a
%{_libdir}/libstdc++fs.*a
%{_libdir}/libsupc++.*a
%if %{build_multilib}
%{multilibdir}/libstdc++.*a
%{multilibdir}/libstdc++exp.*a
%{multilibdir}/libstdc++fs.*a
%{multilibdir}/libsupc++.*a
%endif

#-----------------------------------------------------------------------
# build_cxx
%endif

########################################################################
%if %{build_d}
#-----------------------------------------------------------------------

%package d
Summary:	D support for gcc
Group:		Development/C++
Requires:	%{name} = %{EVRD}
%if %{system_gcc}
Requires:	%{libgdruntime_devel} = %{version}
%endif

%description d
This package adds D support to the GNU Compiler Collection.

%files d
%if %{system_gcc}
%{_bindir}/gdc
%doc %{_mandir}/man1/gdc.1*
%doc %{_infodir}/gdc.info*
%endif
%if %{system_gcc}
%{_bindir}/%{gcc_target_platform}-gdc
%endif
%(
	if [ -n "$(echo %{gcc_target_platform} |cut -d- -f4-)" ]; then
		shortplatform="$(echo %{gcc_target_platform} |cut -d- -f1)-$(echo %{gcc_target_platform} |cut -d- -f3-)"
		echo "%%optional %{_bindir}/${shortplatform}-gdc"
	fi
)
%{gcclibexecdir}/d21

#-----------------------------------------------------------------------

%package -n %{libgdruntime}
Summary:	D standard library
Group:		System/Libraries
%if "%{libgdruntime}" != "libgdruntime"
Provides:	libgdruntime = %{EVRD}
%endif

%description -n %{libgdruntime}
The libphobos package contains a version of the
D Standard Library.

%files -n %{libgdruntime}
%{_libdir}/libgdruntime.so.%{d_major}*
%{_libdir}/libgphobos.so.%{d_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibgdruntime}
Summary:	D Standard library
Group:		System/Libraries

%description -n %{multilibgdruntime}
The libphobos package contains a version of the
D Standard Library.

%files -n %{multilibgdruntime}
%{multilibdir}/libgdruntime.so.%{d_major}*
%{multilibdir}/libgphobos.so.%{d_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libgdruntime_devel}
Summary:	Header files and libraries for D development
Group:		Development/D
Requires:	%{libgdruntime} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibgdruntime} = %{EVRD}
%endif
%if "%{libgdruntime_devel}" != "libgdruntime-devel"
Provides:	libgdruntime-devel = %{EVRD}
%endif

%description -n %{libgdruntime_devel}
This is the GNU implementation of the D standard libraries.  This
package includes the header files and libraries needed for D
development.

%files -n %{libgdruntime_devel}
%{_libdir}/libgdruntime.so
%{_libdir}/libgphobos.so
%{_libdir}/libgphobos.spec
%{gccdir}/include/d
%if %{build_multilib}
%{multilibdir}/libgdruntime.so
%{multilibdir}/libgphobos.so
%{multilibdir}/libgphobos.spec
%endif

#-----------------------------------------------------------------------

%package -n %{libgdruntime_static_devel}
Summary:	Static libraries for the D standard library
Group:		Development/D
Requires:	%{libgdruntime_devel} = %{EVRD}
%if "%{libgdruntime_static_devel}" != "libgdruntime-static-devel"
Provides:	libgdruntime-static-devel = %{EVRD}
%endif
Provides:	gdruntime-static-devel = %{EVRD}

%description -n %{libgdruntime_static_devel}
Static libraries for the GNU standard D library.

%files -n %{libgdruntime_static_devel}
%{_libdir}/libgdruntime.*a
%{_libdir}/libgphobos.*a
%if %{build_multilib}
%{multilibdir}/libgdruntime.*a
%{multilibdir}/libgphobos.*a
%endif

#-----------------------------------------------------------------------
# build_d
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
%{gcclibexecdir}/gnat1
%doc %{_infodir}/gnat*
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
%{_libdir}/libgnat-%{majorver}.so.%{gnat_major}
%{_libdir}/libgnarl-%{majorver}.so.%{gnat_major}

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
%{multilibdir}/libgnat-%{majorver}.so.%{gnat_major}
%{multilibdir}/libgnarl-%{majorver}.so.%{gnat_major}
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
%{_libdir}/gcc/*/*/ada_target_properties
%if %{build_multilib}
%{_libdir}/gcc/*/*/32/ada_target_properties
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
%(
	if [ -n "$(echo %{gcc_target_platform} |cut -d- -f4-)" ]; then
		shortplatform="$(echo %{gcc_target_platform} |cut -d- -f1)-$(echo %{gcc_target_platform} |cut -d- -f3-)"
		echo "%%optional %{_bindir}/${shortplatform}-gfortran"
		echo "%%optional %{_bindir}/${shortplatform}-gfortran-%{ver}"
	fi
)
%doc %{_infodir}/gfortran.info*
%doc %{_mandir}/man1/gfortran.1*
%{gcclibexecdir}/f951
%{gccdir}/finclude
%{gccdir}/libcaf_single.a
%{_libdir}/libcaf_single.a
%if %{build_multilib}
%{multigccdir}/libcaf_single.a
%{multigccdir}/finclude
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
%if "%{libgfortran}" != "libgfortran"
Provides:	libgfortran = %{EVRD}
%endif
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
BuildRequires:	(gcc-go or golang-bin)

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%files go
%{_bindir}/go
%{_bindir}/gofmt
%{_bindir}/gccgo
%{_bindir}/%{gcc_target_platform}-gccgo
%(
	if [ -n "$(echo %{gcc_target_platform} |cut -d- -f4-)" ]; then
		shortplatform="$(echo %{gcc_target_platform} |cut -d- -f1)-$(echo %{gcc_target_platform} |cut -d- -f3-)"
		echo "%%optional %{_bindir}/${shortplatform}-gccgo"
		echo "%%optional %{_bindir}/${shortplatform}-gccgo-%{ver}"
	fi
)
%{_libexecdir}/gcc/*/*/cgo
%{_libdir}/%{name}/bin/%{name}
%dir %{_libdir}/go
%if %{build_multilib}
%dir %{multilibdir}/go
%endif
%doc %{_infodir}/gccgo.info*
%doc %{_mandir}/man1/gccgo.1*
%{_bindir}/gccgo-%{ver}
%{_bindir}/%{gcc_target_platform}-gccgo-%{ver}
%{gcclibexecdir}/go1
%{gcclibexecdir}/buildid
%{gcclibexecdir}/test2json
%{gcclibexecdir}/vet
%{_libdir}/go/%{ver}
%{_libdir}/libgobegin.a
%{_libdir}/libgolibbegin.a
%if %{build_multilib}
%{multilibdir}/go/%{ver}
%{multilibdir}/libgobegin.a
%{multilibdir}/libgolibbegin.a
%endif
%if %{build_doc}
%doc %{_docdir}/gcc-go
%endif
%doc %{_mandir}/man1/go.1*
%doc %{_mandir}/man1/gofmt.1*

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
%{multilibdir}/libffi.so.%{ffi_major}*
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
#-----------------------------------------------------------------------
%if 0
%package -n %{libmpx}
Summary:	GCC support library for MPX
Group:		System/Libraries
Provides:	libmpx = %{EVRD}

%description -n %{libmpx}
This package contains GCC shared support library which is needed
for MPX support.

%files -n %{libmpx}
%{_libdir}/libmpx.so.%{mpx_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibmpx}
Summary:	GCC support library for MPX
Group:		System/Libraries
Conflicts:	%{libmpx} < 4.6.2-11

%description -n %{multilibmpx}
This package contains GCC shared support library which is needed
for MPX support.

%files -n %{multilibmpx}
%{multilibdir}/libmpx.so.%{mpx_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libmpx_devel}
Summary:	GCC development for MPX
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libmpx} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibmpx} = %{EVRD}
%endif
Provides:	libmpx-devel = %{EVRD}
Provides:	mpx-devel = %{EVRD}

%description -n %{libmpx_devel}
This package contains GCC development which is needed
to compile MPX support.

%files -n %{libmpx_devel}
%{_libdir}/libmpx.so
%{_libdir}/libmpx.spec
%if %{build_multilib}
%{multilibdir}/libmpx.so
%{multilibdir}/libmpx.spec
%endif

#-----------------------------------------------------------------------

%package -n %{libmpx_static_devel}
Summary:	GCC MPX static library
Group:		Development/C
Requires:	%{libmpx_devel} = %{EVRD}
Provides:	libmpx-static-devel = %{EVRD}
Provides:	mpx-static-devel = %{EVRD}

%description -n %{libmpx_static_devel}
This package contains GCC static libraries which are needed
to compile MPX support.

%files -n %{libmpx_static_devel}
%{_libdir}/libmpx.*a
%if %{build_multilib}
%{multilibdir}/libmpx.*a
%endif

#-----------------------------------------------------------------------
# package mpxwrappers

%package -n %{libmpxwrappers}
Summary:	GCC support library for MPX
Group:		System/Libraries
Provides:	libmpxwrappers = %{EVRD}

%description -n %{libmpxwrappers}
This package contains GCC shared support library which is needed
for MPX support.

%files -n %{libmpxwrappers}
%{_libdir}/libmpxwrappers.so.%{mpxwrappers_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibmpxwrappers}
Summary:	GCC support library for MPX
Group:		System/Libraries
Conflicts:	%{libmpxwrappers} < 4.6.2-11

%description -n %{multilibmpxwrappers}
This package contains GCC shared support library which is needed
for MPX support.

%files -n %{multilibmpxwrappers}
%{multilibdir}/libmpxwrappers.so.%{mpxwrappers_major}*
%endif

#-----------------------------------------------------------------------

%package -n %{libmpxwrappers_devel}
Summary:	GCC development for MPX
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libmpxwrappers} = %{EVRD}
%if %{build_multilib}
Requires:	%{multilibmpxwrappers} = %{EVRD}
%endif
Provides:	libmpxwrappers-devel = %{EVRD}
Provides:	mpxwrappers-devel = %{EVRD}

%description -n %{libmpxwrappers_devel}
This package contains GCC development which is needed
to compile MPX support.

%files -n %{libmpxwrappers_devel}
%{_libdir}/libmpxwrappers.so
%if %{build_multilib}
%{multilibdir}/libmpxwrappers.so
%endif

#-----------------------------------------------------------------------

%package -n %{libmpxwrappers_static_devel}
Summary:	GCC MPX static library
Group:		Development/C
Requires:	%{libmpxwrappers_devel} = %{EVRD}
Provides:	libmpxwrappers-static-devel = %{EVRD}
Provides:	mpxwrappers-static-devel = %{EVRD}

%description -n %{libmpxwrappers_static_devel}
This package contains GCC static libraries which are needed
to compile MPX support.

%files -n %{libmpxwrappers_static_devel}
%{_libdir}/libmpxwrappers.*a
%if %{build_multilib}
%{multilibdir}/libmpxwrappers.*a
%endif

#-----------------------------------------------------------------------
# package mpxwrappers
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
#-----------------------------------------------------------------------

%if ! %{build_minimal}
%package -n %{libcc1}
Summary:	GCC parsing shared library
Group:		System/Libraries

%description -n %{libcc1}
This package contains the gcc parsing library

%files -n %{libcc1}
%{_libdir}/libcc1.so.%{cc1_major}*

#-----------------------------------------------------------------------

%package -n %{libcc1_devel}
Summary:	GCC parser library development support
Group:		Development/C
Requires:	%{libcc1} = %{EVRD}

%description -n %{libcc1_devel}
Development files for gcc's parser library

%files -n %{libcc1_devel}
%{_libdir}/libcc1.so

#-----------------------------------------------------------------------

%package -n %{libcc1_static_devel}
Summary:	Static library containing the gcc parser
Group:		Development/C
Requires:	%{libcc1_devel} = %{EVRD}
Provides:	libcc1-static-devel = %{EVRD}

%description -n %{libcc1_static_devel}
Static library containing the gcc parser

%files -n %{libcc1_static_devel}
%{_libdir}/libcc1.a
%endif

#-----------------------------------------------------------------------
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
%{_libdir}/libgomp.so.%{gomp_major}*

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
%{multilibdir}/libgomp.so.%{gomp_major}*
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
%doc %{_infodir}/libgomp.info*
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
%if %{system_gcc}
%doc %{_infodir}/libitm.info*
%endif

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
%optional %{_libdir}/libhwasan.so.0*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibasan}
Summary:	GCC Address Sanitizer library
Group:		Development/C

%description -n %{multilibasan}
GCC Address Sanitizer Library.

%files -n %{multilibasan}
%{multilibdir}/libasan.so.%{asan_major}*
%optional %{multilibdir}/libhwasan.so.0*
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
%optional %{_libdir}/libhwasan.so
%optional %{_libdir}/libhwasan_preinit.o
%if %{build_multilib}
%{multilibdir}/libasan.so
%{multilibdir}/libasan_preinit.o
%optional %{multilibdir}/libhwasan.so
%optional %{multilibdir}/libhwasan_preinit.o
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
%optional %{_libdir}/libhwasan.a
%if %{build_multilib}
%{multilibdir}/libasan.a
%optional %{multilibdir}/libhwasan.a
%endif
%endif

#-----------------------------------------------------------------------
# Thread Sanitizer
#-----------------------------------------------------------------------
%if %isarch %{x86_64} aarch64
%if %{build_tsan}
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
%{_libdir}/libtsan_preinit.o

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
%endif

#-----------------------------------------------------------------------
# Atomic operations
#-----------------------------------------------------------------------
%if %{build_atomic}
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
%{multilibdir}/libatomic.so.%{atomic_major}*
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
%endif

########################################################################
# VTV (VTable Verification)
########################################################################
%if 0
%if %{build_vtv}
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
%{multilibdir}/libvtv.so.%{vtv_major}*
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
%{multilibdir}/libvtv.so
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
%endif

%if %{build_rust}
%package rust
Summary:	Rust support for gcc
Group:		Development/Other
Requires:	%{name} = %{EVRD}

%description rust
Rust front-end to GCC.

%files rust
%{_bindir}/gccrs
%{_bindir}/*-gccrs
%{gcclibexecdir}/rust1
%endif

########################################################################
# UBSan (Undefined Behavior Sanitizer)
########################################################################
%if %{build_ubsan}
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
%{multilibdir}/libubsan.so.%{ubsan_major}*
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
%{multilibdir}/libubsan.so
%{multilibdir}/libsanitizer.spec
%endif
%optional %{gccdir}/include/sanitizer

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
%endif

########################################################################
# LSan (Leak Sanitizer)
########################################################################
%if %isarch %{x86_64} aarch64
%if %{build_lsan}
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
%{_libdir}/liblsan_preinit.o

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
%endif

########################################################################
%prep
export LC_ALL=en_US.UTF-8
%setup -q -n %{srcname}
%if 0
%patch0 -p1 -b .uclibc~
%patch1 -p1 -b .pthreadlinkage~
#patch3 -p1 -b .linux32~
%patch4 -p1 -b .execstack~
#patch6 -p1 -b .ltobfd~
%patch7 -p1 -b .plugindet~
# Breaks the build, see comment on bug 33763
#patch8 -p1 -b .ext_inline~
#patch9 -p1 -b .android~
%patch12 -p1 -b .compare~
%patch13 -p1 -b .short
%ifarch aarch64
%patch16 -p1 -b .EVILaarch64~
%endif
%patch17 -p1 -b .compilerRt~
%patch18 -p1 -b .musl1~
%patch20 -p1 -b .musllibgcc~

#patch104 -p1 -b .google5~

%patch203 -p1 -b .musl4~
#patch205 -p1 -b .musl6~
#patch206 -p1 -b .musl7~
#patch207 -p1 -b .musl8~
#patch208 -p1 -b .musl9~

%patch1001 -p1 -b .pass_slibdir~
%patch1007 -p1 -b .multi-do-libdir~
%endif
%patch1008 -p1 -b .mingw32~
%patch1009 -p1 -b .fixadabuild~

%patch2 -p1 -b .xclld~
%patch5 -p1 -b .unused~
%patch10 -p1 -b .clang50248~

# Allow building with current autoconf
find . -name "*.m4" |xargs sed -i -e 's,2\.69,2.71,g'

# FIXME running autoconf here breaks crosscompiling
# for whatever reason. It seems to drop necessary flags
# when targeting a different --host
#aclocal -I config
#autoconf
# FIXME since we can't run autoconf, we have to fix 
# configure scripts here -- gcc_cv_objdump isn't set
# anywhere, breaking --host=X --target=X --build=Y
sed -i -e 's,\$gcc_cv_objdump,${target}-objdump,g' libcc1/configure

echo %{vendor} > gcc/DEV-PHASE
%if "%{snapshot}" != ""
echo %{version} > gcc/BASE-VER
%endif

# Let's get our flags right...
LANGUAGES=c
%if %{build_ada}
    LANGUAGES="$LANGUAGES,ada"
%endif
%if %{build_cxx}
    LANGUAGES="$LANGUAGES,c++"
%endif
%if %{build_d}
    LANGUAGES="$LANGUAGES,d"
%endif
%if %{build_fortran}
    LANGUAGES="$LANGUAGES,fortran"
%endif
%if %{build_go}
    LANGUAGES="$LANGUAGES,go"
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
%if %{build_rust}
    LANGUAGES="$LANGUAGES,rust"
%endif
PROGRAM_SUFFIX=""
%if "%{program_suffix}" != ""
PROGRAM_SUFFIX="--program-suffix=%{program_suffix}"
%endif
PROGRAM_PREFIX=""
%if "%{program_prefix}" != ""
PROGRAM_PREFIX="--program-prefix=%{program_prefix}"
%endif
case %{libc} in
glibc|musl)	LIBC_FLAGS="--enable-threads=posix";;
newlib)		LIBC_FLAGS="--with-newlib --with-headers --disable-threads";;
*)		echo "ERROR: unsupported %{libc} C library"; exit 1;;
esac
%if %{libc_shared}
LIBC_FLAGS="$LIBC_FLAGS --enable-shared --enable-static"
%else
LIBC_FLAGS="$LIBC_FLAGS --disable-shared --enable-static"
%endif
# target specific flags (don't %ifarch for cross compilers)
case %{target_cpu} in
x86_64)		TARGET_FLAGS="--with-cpu=generic %{?build_multilib:--with-arch_32=i686 --with-multilib-list=m32,m64,mx32}";;
znver1)		TARGET_FLAGS="--with-cpu=znver1 %{?build_multilib:--with-arch_32=i686 --with-multilib-list=m32,m64,mx32}";;
i?86|athlon)	TARGET_FLAGS="--with-arch=i686 --with-cpu=generic";;
mips64|mips64el) TARGET_FLAGS="--enable-long-long --with-abi=64 --enable-targets=all";;
mips32|mips32el) TARGET_FLAGS="--enable-long-long --with-abi=n32 --enable-targets=all";;
mips|mipsel) TARGET_FLAGS="--enable-long-long --enable-targets=all --enable-multiarch";;
armv7*) TARGET_FLAGS="--with-arch=armv7-a --with-tune=cortex-a15 ";;
esac

# Configure for building some key crosscompilers
%if %{cross_compiling}
for i in %{_target_platform}; do
%else
for i in %{long_bootstraptargets} %{long_targets}; do
%endif
	EXTRA_FLAGS=""
	CFLAGS_FOR_TARGET=""
	CXXFLAGS_FOR_TARGET=""
	mkdir -p obj-${i}
	cd obj-${i}
	if echo ${i} |grep -q x32; then
		EXTRA_FLAGS="--with-abi=mx32 --with-multilib-list=mx32"
		export CFLAGS_FOR_TARGET="-mx32"
		export CXXFLAGS_FOR_TARGET="-mx32"
	elif echo ${i} |grep -qE '(x86_64|znver1)'; then
		# FIXME add mx32 once X32 is bootstrapped far enough
		EXTRA_FLAGS="--with-multilib-list=m64,m32"
		if [ "%{gcc_target_platform}" != "$i" ]; then
			# We have separate crosscompilers for i686 and x32,
			# let's make sure we get a 64bit libgcc.a
			EXTRA_FLAGS="--with-abi=m64 --without-multilib --disable-multilib"
			export CFLAGS_FOR_TARGET="-m64"
			export CXXFLAGS_FOR_TARGET="-m64"
		fi
	elif echo ${i} |grep ppc64; then
		EXTRA_FLAGS="--without-multilib --disable-multilib"
		export CFLAGS_FOR_TARGET="-m64"
		export CXXFLAGS_FOR_TARGET="-m64"
	fi
	# https://sourceware.org/bugzilla/show_bug.cgi?id=26360
	# glibc on ppc64le assumes 128-bit long doubles, while gcc (when built
	# without glibc headers already present) assumes 64-bit long doubles.
	# Let's force glibc's view of the world to make it match.
	# While other libcs don't barf as badly, --with-long-double-128 makes
	# sense for all ppc64 targets.
	if echo ${i} |grep -qE '^(ppc|powerpc)64'; then
		EXTRA_FLAGS="$EXTRA_FLAGS --with-long-double-128 --with-abi=elfv2"
	fi
	if echo ${i} |grep -q -- '-gnu'; then
		# glibc target -- when bootstrapping, make sure we set defaults
		# for the right version anyway
		EXTRA_FLAGS="$EXTRA_FLAGS --with-glibc-version=2.37"
	fi
	if echo ${i} |grep -q musl; then
		# gcc sanitizers currently aren't compatible with musl
		# (too many hardcoded assumptions that match glibc/bionic behavior)
		EXTRA_FLAGS="$EXTRA_FLAGS --disable-libsanitizer"
		if echo ${i} |grep -qE '(i.86|x86_64|znver1)'; then
			# Incomplete struct _libc_fpstate on x86 musl
			# ../../../../libmpx/mpxrt/mpxrt.h:52:42: error: invalid application of ‘sizeof’ to incomplete type ‘struct _libc_fpstate’
			EXTRA_FLAGS="$EXTRA_FLAGS --disable-libmpx"
			if echo ${i} |grep -E '(x86_64|znver1)'; then
				# No multilib support in crosscompilers
				if echo ${i} |grep x32; then
					EXTRA_FLAGS="$EXTRA_FLAGS --with-abi=mx32 --with-multilib-list=mx32 --without-multilib --disable-multilib"
				else
					EXTRA_FLAGS="$EXTRA_FLAGS --with-abi=m64 --with-multilib-list=m64 --without-multilib --disable-multilib"
				fi
			fi
		fi
	fi
	if echo ${i} |grep -q riscv; then
		# RISC-V 32 is not yet supported
		EXTRA_FLAGS="$EXTRA_FLAGS --without-multilib --disable-multilib"
	elif echo ${i} |grep i686-w64; then
		# Despite the "64" in its name, i686-w64-mingw32 is a 32-bit,
		# non-multilib arch
		EXTRA_FLAGS="$EXTRA_FLAGS --without-multilib --disable-multilib"
	fi
	if [ "%{gcc_target_platform}" = "$i" ]; then
		echo "===== Building native $i compiler ====="
		# This is the native compiler...

		# We can't currently compile gcc with clang, even
		# though that would be great for bootstrapping
		# FIXME add
		#	--with-build-config=bootstrap-lto \
		# when it is fixed (currently breaks building go)
%if ! %{cross_compiling}
		CC=gcc \
		CXX=g++ \
		ORIGINAL_NM_FOR_TARGET="%{_bindir}/binutils-nm" \
		NM_FOR_TARGET="%{_bindir}/binutils-nm" \
%else
		ORIGINAL_NM_FOR_TARGET="%{_bindir}/%{_target_platform}-nm" \
		NM_FOR_TARGET="%{_bindir}/%{_target_platform}-nm" \
%endif
		CFLAGS="$OPT_FLAGS" \
		CXXFLAGS="$OPT_FLAGS" \
		TCFLAGS="$OPT_FLAGS" \
		XCFLAGS="$OPT_FLAGS" \
		../configure \
			--prefix=%{_prefix} \
			--libexecdir=%{_libexecdir} \
			--libdir=%{_libdir} \
			--with-slibdir=%{_libdir} \
			--mandir=%{_mandir} \
			--infodir=%{_infodir} \
%if !%{build_cloog}
			--without-cloog \
			--without-ppl \
%else
			--with-cloog \
			--with-ppl \
			--disable-libmpx \
			--enable-cloog-backend=isl \
			--disable-cloog-version-check \
			--disable-isl-version-check \
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
			--disable-werror \
			--enable-__cxa_atexit \
%if !%isarch %{mipsx}
			--enable-gold=default \
%endif
			--with-plugin-ld=%{_bindir}/%{gcc_target_platform}-ld.bfd \
%if %{system_gcc} && ! %{cross_compiling}
			--enable-bootstrap \
%endif
			--enable-checking=release \
			--enable-gnu-unique-object \
			--enable-gnu-indirect-function \
			--with-linker-hash-style=gnu \
			--enable-languages="$LANGUAGES" \
			$PROGRAM_PREFIX \
			--enable-linker-build-id \
%if !%{build_plugin}
			--disable-plugin \
%else
			--enable-plugin \
			--enable-shared \
			--enable-libcc1 \
			--enable-lto \
%endif
%if !%{build_lto}
			--disable-lto \
%endif
%if %{build_atomic}
			--enable-libatomic \
%else
			--disable-libatomic \
%endif
			$LIBC_FLAGS \
			--with-system-zlib \
			--with-bugurl=%{bugurl} \
%if !%{build_multilib}
			--disable-multilib \
%endif
%if %isarch armv5te
			--with-arch=armv5te \
%endif
%if %isarch armv7l armv7hl armv7hln armv7hnl armv8l armv8hl armv8hnl armv8hcnl
			--without-multilib \
			--disable-multilib \
			--with-mode=thumb \
%if %isarch armv7l armv8l
			--with-float=softfp \
%else
			--with-float=hard \
%endif
%if 0
		# should be be armv7hl only
			--with-fpu=vfpv3-d16 \
		# should be be armv7hln armv7hnl
%endif
%if %isarch armv7hl armv7hln armv7hnl armv8hl armv8hnl armv8hcnl
			--with-fpu=neon \
			--with-abi=aapcs-linux \
%endif
%endif
			--host=%{_target_platform} \
%if %{cross_compiling}
			--target=${i} \
%else
			--build=%{_target_platform} \
%endif
			$TARGET_FLAGS \
			$EXTRA_FLAGS

%if %{with crosscompilers}
	else
		if echo $i |grep -q '^arm'; then
			if echo $i |grep -q h; then
				EXTRA_FLAGS="$EXTRA_FLAGS --with-float=hard --with-abi=aapcs-linux"
			else
				EXTRA_FLAGS="$EXTRA_FLAGS --with-float=softfp --with-abi=aapcs-linux"
			fi
			if echo $i |grep -q n; then
				EXTRA_FLAGS="$EXTRA_FLAGS --with-fpu=neon"
			else
				EXTRA_FLAGS="$EXTRA_FLAGS --with-fpu=vfpv3"
			fi
		fi
		if ! echo $i |grep -q 'mingw'; then
			# We want --hash-stlye=gnu, but not on a non-ELF target
			EXTRA_FLAGS="$EXTRA_FLAGS --with-linker-hash-style=gnu"
		fi
		if echo "%{long_bootstraptargets}" |grep -q $i; then
			echo "===== Building %{gcc_target_platform} -> $i bootstrap crosscompiler ====="
			CC=gcc CXX=g++ LDFLAGS="-fuse-ld=bfd" ../configure \
				--prefix=%{_prefix} \
				--libexecdir=%{_libexecdir} \
				--libdir=%{_libdir} \
				--with-slibdir=%{_prefix}/${i}/lib \
				--mandir=%{_mandir} \
				--infodir=%{_infodir} \
				--without-cloog \
				--without-ppl \
				--disable-libffi \
				--disable-libgomp \
				--disable-libquadmath \
				--disable-libssp \
				--disable-werror \
				--enable-__cxa_atexit \
				--enable-gold=default \
				--with-plugin-ld=%{_bindir}/${i}-ld.bfd \
				--enable-checking=release \
				--enable-gnu-unique-object \
				--enable-gnu-indirect-function \
				--enable-languages=c \
				--program-prefix=${i}- \
				--enable-linker-build-id \
				--disable-plugin \
				--disable-lto \
				--disable-libatomic \
				--disable-shared \
				--enable-static \
				--with-system-zlib \
				--with-bugurl=https://issues.openmandriva.org \
				--disable-multilib \
				--disable-threads \
				--disable-libmpx \
				--target=${i} \
				$EXTRA_FLAGS
		else
			echo "===== Building %{gcc_target_platform} -> $i crosscompiler ====="
			CC=gcc CXX=g++ LDFLAGS="-fuse-ld=bfd" ../configure \
				--prefix=%{_prefix} \
				--libexecdir=%{_libexecdir} \
				--libdir=%{_libdir} \
				--with-slibdir=%{_prefix}/${i}/lib \
				--mandir=%{_mandir} \
				--infodir=%{_infodir} \
				--with-sysroot=%{_prefix}/${i} \
				--with-native-system-header-dir=/include \
				--enable-threads \
				--enable-shared \
				--enable-lto \
				--enable-plugin \
				--enable-languages=c,c++,fortran,lto,objc,obj-c++ \
				--target=${i} \
				--with-bugurl=https://issues.openmandriva.org \
				$EXTRA_FLAGS
		fi
%endif
	fi
	cd ..
done

#-----------------------------------------------------------------------
%build
# FIXME: extra tools needed
export PATH=$PATH:$PWD/bin
export sysroot=%{_prefix}
#_prefix}/%{gcc_target_platform}

# The -gdwarf-4 removal is a workaround for gcc bug #52420
OPT_FLAGS=`echo %{optflags} -fno-strict-aliasing | \
    sed -e 's/-Wall//g' -e 's/-all//g' \
    -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g' \
    -e 's/-m\(31\|32\|64\)//g' \
    -e 's/-mx32//g' \
    -e 's/-fstack-protector-strong//g' \
    -e 's/-fstack-protector//g' \
    -e 's/--param=ssp-buffer-size=4//' \
    -e 's/-gdwarf-4/-g/' \
    -e 's/-pipe//g'`
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`

# don't build crt files with -fasynchronous-unwind-tables
case " $OPT_FLAGS " in
*" -fasynchronous-unwind-tables "*)
  sed -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables /' -i gcc/Makefile.in
  ;;
esac
echo "Using OPT_FLAGS $OPT_FLAGS"

%if %{cross_compiling}
BOOTSTRAP=all
%else
BOOTSTRAP=bootstrap
%if %isarch %{ix86} %{x86_64}
    %if %{system_gcc}
        BOOTSTRAP=profiledbootstrap
    %endif
%endif
%endif

# FIXME debugedit
[ ! -z "$TMP" ] && export TMP=`echo $TMP | sed -e 's|/$||'`
[ ! -z "x$TMPDIR" ] && export TMPDIR=`echo $TMPDIR | sed -e 's|/$||'`

%if  %{cross_compiling}
for i in %{_target_platform}; do
%else
for i in %{long_bootstraptargets} %{long_targets}; do
%endif
	cd obj-${i}
	if [ "%{gcc_target_platform}" = "$i" ]; then
		# Native host compiler gets special treatment...

		if ! %make_build BOOT_CFLAGS="$OPT_FLAGS" $BOOTSTRAP; then
			# Let's try to get a better error message
			# (Workaround for builds working locally and failing in abf,
			# let's see where exactly it's failing)
			make -j1 BOOT_CFLAGS="$OPT_FLAGS" $BOOTSTRAP
		fi

%if %{build_pdf}
		%make_build pdf || :
%endif

%if %{build_doc}
		pushd host-%{gcc_target_platform}/gcc
		%make_build html || :
%if %{build_pdf}
		%make_build pdf || :
%endif
		popd
%endif

%if %{with crosscompilers}
	else
		%make
%endif
	fi
	cd ..
done

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
# There's a nasty bug in gcc Makefiles -- they go to fixincludes/ and run
# make install, but they don't actually create a Makefile there if the
# directory is empty.
for i in %{long_bootstraptargets} %{long_targets}; do
	if [ -d obj-${i}/fixincludes -a ! -e obj-${i}/fixincludes/Makefile ]; then
		cat >obj-${i}/fixincludes/Makefile <<'EOF'
install:
	echo No fixincludes to take care of
EOF
	fi
done

%if ! %{cross_compiling}
%if %{with crosscompilers}
# Install crosscompilers first so the native compiler can overwrite stuff
for i in %{long_bootstraptargets} %{long_targets}; do
	[ "%{gcc_target_platform}" = "$i" ] && continue
	%make_install -C obj-${i}
	# libgcc_s.so* is always installed in the wrong place
	# Using "%{_prefix}/lib*" to catch /usr/lib, /usr/lib64 and /usr/libx32
	# Failure allowed because bootstrap compilers don't have shared libraries
	mv %{buildroot}%{_prefix}/lib*/libgcc* %{buildroot}%{_prefix}/${i}/lib/ || :
done
# *-mingw32 crosscompilers include a float.h file that hides
# mingw's own float.h, causing mingw-crt to fail
for i in %{buildroot}%{_libdir}/gcc/*mingw32/*/include/float.h; do
	[ -e "$i" ] || continue
	echo >>$i
	echo '#include_next <float.h>' >>$i
done
%endif
%endif

# Native compiler
%make_install -C obj-%{gcc_target_platform}

%if %{build_lto}
# Put the LTO plugin where ld can see it...
mkdir -p %{buildroot}%{_libdir}/bfd-plugins
ln -s ../../libexec/gcc/%{gcc_target_platform}/%{ver}/liblto_plugin.so %{buildroot}%{_libdir}/bfd-plugins/liblto_plugin.so
%endif

# Make cpp names crosscompiler friendly
ln -s cpp %{buildroot}%{_bindir}/%{gcc_target_platform}-cpp
ln -s cpp %{buildroot}%{_bindir}/%{gcc_target_platform}-cpp-%{ver}

# configure python dir option does not cover libstdc++
mkdir -p %{buildroot}%{py_puresitedir}
    if [ -d %{buildroot}%{_datadir}/gcc-%{ver}/python ]; then
        mv -f %{buildroot}%{_datadir}/gcc-%{ver}/python/* \
            %{buildroot}%{py_puresitedir}
        rm -fr %{buildroot}%{_datadir}/gcc-%{ver}
    fi

pushd %{buildroot}%{_bindir}
%if %{system_gcc}
    mkdir -p %{buildroot}%{_prefix}/lib
    ln -sf %{_bindir}/cpp %{buildroot}%{_prefix}/lib/cpp
    install -m 0755 %{SOURCE4} %{SOURCE5} %{buildroot}%{_bindir}
    ln -sf %{gcc_target_platform}-gcc-%{ver} cc
%else
    rm %{buildroot}%{_bindir}/cpp
%endif
    PROGRAMS="gcc"
    %if %{build_cxx}
        PROGRAMS="$PROGRAMS g++"
    %endif
    %if %{build_go}
        PROGRAMS="$PROGRAMS gccgo"
    %endif
    %if %{build_fortran}
        PROGRAMS="$PROGRAMS gfortran"
    %endif
    for prog in $PROGRAMS; do
        if [ -f %{gcc_target_platform}-$prog ]; then
            rm -f %{gcc_target_platform}-$prog-%{ver}
            mv -f %{gcc_target_platform}-$prog{,-%{ver}}
        fi
        rm -f $prog
        ln -sf %{gcc_target_platform}-$prog-%{ver} $prog-%{ver}
        %if %{system_gcc}
            ln -sf %{gcc_target_platform}-$prog-%{ver} $prog
            ln -sf %{gcc_target_platform}-$prog-%{ver} %{gcc_target_platform}-$prog
        %endif
    done
%if %{build_cxx}
    rm -f c++ %{gcc_target_platform}-c++{,-%{ver}}
    ln -sf %{gcc_target_platform}-g++-%{ver} c++-%{ver}
    %if %{system_gcc}
        ln -sf %{gcc_target_platform}-g++-%{ver} c++
    %endif
    %if %{system_gcc}
        ln -sf %{gcc_target_platform}-g++-%{ver} %{gcc_target_platform}-c++
    %endif

%if ! %{cross_compiling}
    mkdir -p %{buildroot}%{_datadir}/gdb/auto-load%{_libdir}
    mv -f %{buildroot}%{_libdir}/libstdc++.so.*.py \
        %{buildroot}%{_datadir}/gdb/auto-load%{_libdir}
    perl -pi -e 's|%{_datadir}/gcc-%{ver}/python|%{py_puresitedir}|;' \
        %{buildroot}%{_datadir}/gdb/auto-load%{_libdir}/libstdc++.*.py

    %if %{build_multilib}
        mkdir -p %{buildroot}%{_datadir}/gdb/auto-load%{multilibdir}
        mv -f %{buildroot}%{multilibdir}/libstdc++.so.*.py \
        %{buildroot}%{_datadir}/gdb/auto-load%{multilibdir}
        perl -pi -e 's|%{_datadir}/gcc-%{ver}/python|%{py_puresitedir}|;' \
            %{buildroot}%{_datadir}/gdb/auto-load%{multilibdir}/libstdc++.*.py
    %endif
%endif
%endif
popd

%if %{shared_libgnat}
    %if %{build_ada}
        for lib in libgnarl libgnat; do
            rm -f %{buildroot}%{_libdir}/$lib.so
            rm -f %{buildroot}%{gccdir}/adalib/$lib.so
            mv -f %{buildroot}%{gccdir}/adalib/$lib-%{majorver}.so \
                    %{buildroot}%{_libdir}/$lib-%{majorver}.so.%{gnat_major}
            ln -sf $lib-%{majorver}.so.%{gnat_major} %{buildroot}%{_libdir}/$lib-%{majorver}.so
            ln -sf $lib-%{majorver}.so.%{gnat_major} %{buildroot}%{_libdir}/$lib.so
            %if %{build_multilib}
                rm -f %{buildroot}%{multilibdir}/$lib.so
                rm -f %{buildroot}%{multigccdir}/adalib/$lib.so
                mv -f %{buildroot}%{multigccdir}/adalib/$lib-%{majorver}.so \
                        %{buildroot}%{multilibdir}/$lib-%{majorver}.so.%{gnat_major}
                ln -sf $lib-%{majorver}.so.%{gnat_major} %{buildroot}%{multilibdir}/$lib-%{majorver}.so
                ln -sf $lib-%{majorver}.so.%{gnat_major} %{buildroot}%{multilibdir}/$lib.so
            %endif
        done
    %endif
%endif

rm -fr %{buildroot}%{gccdir}/include-fixed
rm -fr %{buildroot}%{gccdir}/install-tools/include

%if !%{system_gcc}
    rm -fr %{buildroot}%{_infodir}
    rm -fr %{buildroot}%{_mandir}
    rm -fr %{buildroot}%{_localedir}
    rm -f %{buildroot}%{_bindir}/gcov
    rm -f %{buildroot}%{_libdir}/libgcc_s.so
    %if %{build_multilib}
        rm -f %{buildroot}%{multilibdir}/libgcc_s.so
        rm -f %{buildroot}%{_prefix}/libx32/libgcc_s.so
    %endif
    %if !%{build_libgcc}
         rm -f %{buildroot}%{_libdir}/libgcc_s.so.*
         %if %{build_multilib}
             rm -f %{buildroot}%{multilibdir}/libgcc_s.so.*
             rm -f %{buildroot}%{_prefix}/libx32/libgcc_s.so.*
         %endif
    %endif
%endif
rm -f %{buildroot}%{_libdir}/libiberty.a
rm -f %{buildroot}%{multilibdir}/libiberty.a

%if !%{build_ubsan}
    rm -f %{buildroot}%{_libdir}/libubsan*
    %if %{build_multilib}
        rm -f %{buildroot}%{multilibdir}/libubsan*
    %endif
    rm -f %{buildroot}%{_libdir}/libsanitizer.spec
%endif

%if !%{build_asan}
    rm -f %{buildroot}%{_libdir}/libasan*
    %if %{build_multilib}
        rm -f %{buildroot}%{multilibdir}/libasan*
    %endif
%endif

%if !%{build_itm}
    rm -f %{buildroot}%{_libdir}/libitm* %{buildroot}%{_infodir}/libitm.info*
    %if %{build_multilib}
        rm -f %{buildroot}%{multilibdir}/libitm*
    %endif
%else
    %if !%{system_gcc}
        rm -f %{buildroot}%{_infodir}/libitm.info*
    %endif
%endif

%if !%{package_ffi}
    rm -f %{buildroot}%{_libdir}/libffi.*
    rm -f %{buildroot}%{multilibdir}/libffi.*
    rm -f %{buildroot}%{_mandir}/man3/ffi*
%endif

pushd obj-%{gcc_target_platform}

%if %{build_doc}
    %if %{build_cxx}
    mkdir -p %{buildroot}%{_docdir}/libstdc++
    cp -far libstdc++-v3/doc/html %{buildroot}%{_docdir}/libstdc++
    %endif
    pushd host-%{gcc_target_platform}/gcc/HTML/gcc-%{ver}
        mkdir -p %{buildroot}%{_docdir}/gcc/html
        for doc in gcc gccinstall gccint; do
            cp -far $doc %{buildroot}%{_docdir}/gcc/html
        done
        %if %{system_gcc}
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
    popd
    %if %{build_pdf}
    pushd host-%{gcc_target_platform}/gcc/doc
        for doc in gcc.pdf gccinstall.pdf gccint.pdf; do
            install -m 0644 $doc %{buildroot}%{_docdir}/gcc/$doc
        done
        %if %{system_gcc}
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
    popd
    pushd %{gcc_target_platform}
        %if %{build_gomp}
            install -m 0644 -D libgomp/libgomp.pdf %{buildroot}%{_docdir}/libgomp/libgomp.pdf
        %endif
        %if %{build_quadmath}
            install -m 0644 -D libquadmath/libquadmath.pdf %{buildroot}%{_docdir}/libquadmath/libquadmath.pdf
        %endif
    popd
    %endif
%endif

cd ..

%if ! %{default_compiler}
# Leave the cc, c89, c++, ... symlinks to clang
# or whatever other compiler is the default
rm -f \
	%{buildroot}%{_bindir}/cc \
	%{buildroot}%{_bindir}/c89 \
	%{buildroot}%{_bindir}/c99 \
	%{buildroot}%{_bindir}/c++
%endif

%if %{system_gcc}
install -m644 %{SOURCE10} -D %{buildroot}%{_sysconfdir}/sysconfig/gcc
install -m644 %{SOURCE11} -D %{buildroot}%{_sysconfdir}/profile.d/90gcc.sh
install -m644 %{SOURCE12} -D %{buildroot}%{_sysconfdir}/profile.d/90gcc.csh
%endif
%if %{build_go}
mkdir -p %{buildroot}/%{_libdir}/%{name}/bin/
ln -s %{_bindir}/%{name} %{buildroot}/%{_libdir}/%{name}/bin/%{name}
%endif

%if %{with crosscompilers}
for i in %{long_bootstraptargets} %{long_targets}; do
	# aarch64-mandriva-linux-gnu and aarch64-linux-gnu are similar enough...
	longplatform=$(grep ^target_alias= obj-$i/Makefile |cut -d= -f2-)
	if [ -n "$(echo $i |cut -d- -f4-)" ]; then
		shortplatform="$(echo $i |cut -d- -f1)-$(echo $i |cut -d- -f3-)"
		cd %{buildroot}%{_bindir}
		for j in $longplatform-*; do
			[ -e $(echo $j |sed -e "s,$longplatform,$shortplatform,") ] || ln -s $j $(echo $j |sed -e "s,$longplatform,$shortplatform,")
		done
		cd -
	fi
	if [ "$longplatform" != "$i" ]; then
		cd %{buildroot}%{_bindir}
		for j in $longplatform-*; do
			[ -e $(echo $j |sed -e "s,$longplatform,$i,") ] || ln -s $j $(echo $j |sed -e "s,$longplatform,$i,")
		done
		cd -
	fi
done
%endif

%if "%{_lib}" != "lib"
# clang has a slightly strange way of detecting gcc cross toolchains.
# Let's be compatible with it.
mkdir -p %{buildroot}%{_prefix}/lib
ln -s ../%{_lib}/gcc %{buildroot}%{_prefix}/lib/gcc
%endif

# Not sure why this ends up in /usr as well as the crosscompiler
# directories... Doesn't belong there for sure
%ifarch %{aarch64} %{riscv}
rm -rf %{buildroot}%{_prefix}/libx32
%endif
%ifarch %{ix86}
# Not sure why ix86 would try to build multilib stuff?
rm -rf %{buildroot}%{_prefix}/{lib64,libx32}
%endif

%if %{system_gcc}
%find_lang cpplib
%find_lang gcc
%if %{build_cxx}
%find_lang libstdc++
%endif
%endif

%if ! %{cross_compiling}
# Symlink CRT files where other compilers can find them without
# having to guess too hard
cd %{buildroot}%{_libdir}
ln -s gcc/%{gcc_target_platform}/%{version}/*.{a,o} .
cd -

%if %{with crosscompilers}
%(
for i in %{long_bootstraptargets} %{long_targets}; do
	[ "$i" = "%{_target_platform}" ] && continue
	if echo "%{long_bootstraptargets}" |grep -q $i; then
		bootstrap=true
	else
		bootstrap=false
	fi
	if $bootstrap; then
		package=cross-${i}-gcc-bootstrap
	else
		package=cross-${i}-gcc
	fi
	cat <<EOF
%package -n ${package}
EOF
	if $bootstrap; then
		if echo $i |grep -q mingw; then
			echo "BuildRequires: cross-${i}-libc-bootstrap"
		fi
	else
		cat <<EOF
# Full compiler can also be used for bootstrapping...
%rename cross-${i}-gcc-bootstrap
BuildRequires: cross-${i}-libc
Recommends: cross-${i}-libc
EOF
		if ! echo $i |grep -q mingw; then
			cat <<EOF
BuildRequires: cross-${i}-kernel-release-headers
EOF
		fi
	fi
	cat <<EOF
Summary: Gcc for crosscompiling to ${i}
Group: Development/Other
BuildRequires: cross-${i}-binutils
Recommends: cross-${i}-binutils
AutoReqProv: no

%description -n ${package}
Gcc for crosscompiling to ${i}

%files -n ${package}
%{_bindir}/${i}-*
%{_mandir}/man?/${i}-*
%{_libdir}/gcc/${i}
%{_libexecdir}/gcc/${i}
EOF
	if ! $bootstrap; then
		cat <<EOF
%{_prefix}/${i}/include/*
%{_prefix}/${i}/lib*/*
EOF
	fi

	if [ -n "$(echo $i |cut -d- -f4-)" ]; then
		shortplatform="$(echo $i |cut -d- -f1)-$(echo $i |cut -d- -f3-)"
		echo "%{_bindir}/${shortplatform}-*"
	fi
	echo
done
)
%endif
%endif
