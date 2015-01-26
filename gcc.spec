# functions with printf format attribute but with special parser and also
# receiving non constant format strings
%define		Werror_cflags			%{nil}

# avoid failures when testing if compiler used to build gcc can generate
# shared objects (regardless of unresolved symbols)
%define		_disable_ld_no_undefined	1

# avoid build failure due to configure built with different autoconf version
%define		_disable_libtoolize		1

#-----------------------------------------------------------------------

%define nof_arches		noarch
%define lsb_arches		i386 x86_64
%define biarches		x86_64 mips64 mips64el mips mipsel

%define		system_compiler		1

%define		official		1
%if %{official}
  %define	snapshot		%{nil}
%else
  %define	snapshot		-20120413
%endif

# Define if building a cross compiler
# FIXME: assume user does not define both cross and cross_bootstrap variables
%define build_cross		0
%define build_cross_bootstrap	0
%{expand: %{?cross:		%%global build_cross 1}}
%{expand: %{?cross_bootstrap:	%%global build_cross_bootstrap 1}}


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
%define	program_long_suffix	-%{version}
%else
%if %{build_cross}
%define	_build_pkgcheck_set /usr/bin/rpmlint -T -f %{_sourcedir}/gcc.rpmlintrc
%define	_build_pkgcheck_srpm /usr/bin/rpmlint -T -f %{_sourcedir}/gcc.rpmlintrc
%define alternative_priority	10%{branch_tag}
%define cross_prefix		cross-%{target_cpu}-
%global	target_platform		%(rpm --macros %%{_usrlibrpm}/macros:%%{_usrlibrpm}/platform/%{target_cpu}-%{_target_os}/macros --target=%{target_cpu} -E %%{_target_platform})
%define cross_program_prefix	%{target_platform}-
%define package_suffix		%{nil}
%define program_prefix		%{target_platform}-
%define program_suffix		%{nil}
%define program_long_suffix	-%{ver}
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

# Define GCC target platform, and arch we built for
%if %{build_cross}
%define biarches		noarch
%define arch			%{target_cpu}
%define gcc_target_platform	%{target_platform}
%define target_prefix		%{_prefix}/%{gcc_target_platform}
%global	target_lib		%(rpm --macros %%{_usrlibrpm}/macros:%%{_usrlibrpm}/platform/%{target_cpu}-%{_target_os}/macros --target=%{target_cpu} -E %%{_lib})
%define target_libdir		%{target_prefix}/%{target_lib}
%define target_slibdir		%{target_prefix}/%{target_lib}
%define target_slibdir32	%{target_prefix}/lib
%else
%define arch			%(echo %{_target_cpu}|sed -e "s/\\(i.86\\|athlon\\)/i386/" -e "s/amd64/x86_64/")
%define	target_cpu		%{arch}
%define gcc_target_platform	%{_target_platform}
%define target_prefix		%{_prefix}
%define target_libdir		%{_libdir}
%define target_slibdir		/%{_lib}
%define target_slibdir32	/lib
%endif
%define isarch()		%(case " %* " in (*" %{arch} "*) echo 1;; (*) echo 0;; esac)

%if %isarch x86_64
%define multilib_32_arch	i586
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
%define		branch			4.9
%define		ver			%{branch}.3
%define		linaro			2015.01
%define		linaro_spin		%{nil}
%define		alternatives		/usr/sbin/update-alternatives
%define		gcclibexecdirparent	%{_libexecdir}/gcc/%{gcc_target_platform}/
%define		gcclibexecdir		%{gcclibexecdirparent}/%{ver}
%define		gccdirparent		%{_libdir}/gcc/%{gcc_target_platform}/
%define		gccdir			%{gccdirparent}/%{ver}
%define		multigccdir		%{_libdir}/gcc/%{gcc_target_platform}/%{ver}/32
%define		multigccdirn32		%{_libdir}/gcc/%{gcc_target_platform}/%{ver}/n32
%define		multigccdir64		%{_libdir}/gcc/%{gcc_target_platform}/%{ver}/64
%define		multilibdir		%{target_prefix}/lib
%if %build_cross
%define		multirootlibdir		%{multilibdir}
%else
%define		multirootlibdir		/lib
%endif

#-----------------------------------------------------------------------
%define		gcc_major		1
%define		libgcc			%{?cross_prefix}%mklibname gcc %{gcc_major}
%define		multilibgcc		%{?cross_prefix}libgcc%{gcc_major}
%define		stdcxx_major		6
%define		libstdcxx		%{?cross_prefix}%mklibname stdc++ %{stdcxx_major}
%define		libstdcxx_devel		%{?cross_prefix}%mklibname stdc++ -d
%define		libstdcxx_static_devel	%{?cross_prefix}%mklibname stdc++ -d -s
%define		multilibstdcxx		libstdc++%{stdcxx_major}
%define		gcj_major		15
%define		libgcj			%{?cross_prefix}%mklibname gcj %{gcj_major}
%define		libgcj_devel		%{?cross_prefix}%mklibname gcj -d
%define		libgcj_static_devel	%{?cross_prefix}%mklibname gcj -d -s
%define		gcj_bc_major		1
%define		libgcj_bc		%{?cross_prefix}%mklibname gcj_bc %{gcj_bc_major}
# gcj multilib explicitly disabled
%define		gfortran_major		3
%define		libgfortran		%{?cross_prefix}%mklibname gfortran %{gfortran_major}
%define		libgfortran_devel	%{?cross_prefix}%mklibname gfortran -d
%define		libgfortran_static_devel %{?cross_prefix}%mklibname gfortran -d -s
%define		multilibgfortran	%{?cross_prefix}libgfortran%{gfortran_major}
%define		ffi_major		4
%define		libffi			%{?cross_prefix}%mklibname ffi %{ffi_major}
%define		libffi_devel		%{?cross_prefix}%mklibname ffi -d
%define		libffi_static_devel	%{?cross_prefix}%mklibname ffi -d -s
%define		multilibffi		%{?cross_prefix}libffi%{ffi_major}
%define		gnat_major		1
%define		libgnat			%{?cross_prefix}%mklibname gnat %{gnat_major}
%define		libgnat_devel		%{?cross_prefix}%mklibname gnat -d
%define		libgnat_static_devel	%{?cross_prefix}%mklibname gnat -d -s
%define		multilibgnat		%{?cross_prefix}libgnat%{gnat_major}
%define		go_major		5
%define		libgo			%{?cross_prefix}%mklibname go %{go_major}
%define		libgo_devel		%{?cross_prefix}%mklibname go -d
%define		libgo_static_devel	%{?cross_prefix}%mklibname go -d -s
%define		multilibgo		%{?cross_prefix}libgo%{go_major}
%define		gomp_major		1
%define		libgomp			%{?cross_prefix}%mklibname gomp %{gomp_major}
%define		libgomp_devel		%{?cross_prefix}%mklibname gomp -d
%define		libgomp_static_devel	%{?cross_prefix}%mklibname gomp -d -s
%define		multilibgomp		%{?cross_prefix}libgomp%{gomp_major}
%define		objc_major		4
%define		libobjc			%{?cross_prefix}%mklibname objc %{objc_major}
%define		libobjc_devel		%{?cross_prefix}%mklibname objc -d
%define		libobjc_static_devel	%{?cross_prefix}%mklibname objc -d -s
%define		multilibobjc		%{?cross_prefix}libobjc%{objc_major}
%define		quadmath_major		0
%define		libquadmath		%{?cross_prefix}%mklibname quadmath %{quadmath_major}
%define		libquadmath_devel	%{?cross_prefix}%mklibname quadmath -d
%define		libquadmath_static_devel %{?cross_prefix}%mklibname quadmath -d -s
%define		multilibquadmath	%{?cross_prefix}libquadmath%{quadmath_major}
%define		ssp_major		0
%define		libssp			%{?cross_prefix}%mklibname ssp %{ssp_major}
%define		libssp_devel		%{?cross_prefix}%mklibname ssp -d
%define		libssp_static_devel	%{?cross_prefix}%mklibname ssp -d -s
%define		multilibssp		%{?cross_prefix}libssp%{ssp_major}
%define		itm_major		1
%define		libitm			%{?cross_prefix}%mklibname itm %{itm_major}
%define		libitm_devel		%{?cross_prefix}%mklibname itm -d
%define		libitm_static_devel	%{?cross_prefix}%mklibname itm -d -s
%define		multilibitm		%{?cross_prefix}libitm%{itm_major}
%define		asan_major		1
%define		libasan			%{?cross_prefix}%mklibname asan %{asan_major}
%define		libasan_devel		%{?cross_prefix}%mklibname asan -d
%define		libasan_static_devel	%{?cross_prefix}%mklibname asan -d -s
%define		multilibasan		%{?cross_prefix}libasan%{asan_major}
%define		tsan_major		0
%define		libtsan			%{?cross_prefix}%mklibname tsan %{tsan_major}
%define		libtsan_devel		%{?cross_prefix}%mklibname tsan -d
%define		libtsan_static_devel	%{?cross_prefix}%mklibname tsan -d -s
%define		atomic_major		1
%define		libatomic		%{?cross_prefix}%mklibname atomic %{atomic_major}
%define		libatomic_devel		%{?cross_prefix}%mklibname atomic -d
%define		libatomic_static_devel	%{?cross_prefix}%mklibname atomic -d -s
%define		multilibatomic		%{?cross_prefix}libatomic%{atomic_major}
%define		cilk_major		5
%define		libcilkrts		%{?cross_prefix}%mklibname cilkrts %{cilk_major}
%define		libcilkrts_devel	%{?cross_prefix}%mklibname cilkrts -d
%define		libcilkrts_static_devel	%{?cross_prefix}%mklibname cilkrts -d -s
%define		multilibcilkrts		%{?cross_prefix}libcilkrts%{cilk_major}
%define		ubsan_major		0
%define		libubsan		%{?cross_prefix}%mklibname ubsan %{ubsan_major}
%define		libubsan_devel		%{?cross_prefix}%mklibname ubsan -d
%define		libubsan_static_devel	%{?cross_prefix}%mklibname ubsan -d -s
%define		multilibubsan		%{?cross_prefix}libubsan%{ubsan_major}
%define		vtv_major		0
%define		libvtv			%{?cross_prefix}%mklibname vtv %{vtv_major}
%define		libvtv_devel		%{?cross_prefix}%mklibname vtv -d
%define		libvtv_static_devel	%{?cross_prefix}%mklibname vtv -d -s
%define		multilibvtv		%{?cross_prefix}libvtv%{vtv_major}
%define		lsan_major		0
%define		liblsan			%{?cross_prefix}%mklibname lsan %{lsan_major}
%define		liblsan_devel		%{?cross_prefix}%mklibname lsan -d
%define		liblsan_static_devel	%{?cross_prefix}%mklibname lsan -d -s

#-----------------------------------------------------------------------
%define		build_ada		0
%define		build_asan		0
%define		build_check		0
%define		build_multilib		0
%define		build_go		0
%define		build_lto		1
%define		build_atomic		1
%define		build_objc		0
%define		build_objcxx		0
%define		build_quadmath		0
%define		build_ssp		0
%if %isarch aarch64
# ubsan doesn't exist for aarch64 yet
%define		build_ubsan		0
%else
%define		build_ubsan		%{system_compiler}
%endif
%if %isarch %{ix86} x86_64 %{arm}
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
%if %isarch %{ix86} x86_64 %{arm}
  %define	build_java		%{system_compiler}
%else
  %define	build_java		0
%endif
# need to build if major does not conflict with current system_compiler
%define		build_libgcc		%{system_compiler}
%define		build_pdf		%{build_doc}
%define		build_plugin		%{system_compiler}
%if %isarch x86_64
  %define	build_tsan		%{system_compiler}
  %define	build_lsan		%{system_compiler}

  %define	build_multilib		%{system_compiler}
%endif
%if %isarch %{ix86} x86_64
  %define	build_cilkrts		%{system_compiler}
  %define	build_quadmath		%{system_compiler}
  %define	build_doc		1
# system_compiler && build_cxx
  %define	build_go		%{system_compiler}
  %define	build_vtv		%{system_compiler}
%endif
%if %isarch %{ix86} x86_64
  %define	build_ada		%{system_compiler}
%endif
%if %isarch %{ix86} x86_64 %{armx}
  %define	build_objc		%{system_compiler}
  %define	build_objcxx		%{system_compiler}
%if %isarch %{ix86} x86_64 %{arm}
  %define	build_asan		%{system_compiler}
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

# (proyvind): TODO
# This is a cheap knockoff of the former monolithic build, hastily thrown
# together to get non-bootstrap cross build without unnecessary complexity
# of package libification etc.
# Returning it to it's former state will require rearranging the spec layout
# with all %%files sections collected together at the end, reverting back to
# what earlier was before pcpa cleaned it out (at a time of cross build being
# broken, thus build support for removed).
# Unless any loud objections from pcpa or anyone else, I intend to do so
# eventually, this would not only improve and make the cross compiler support
# easier to maintain, but also easier to maintain package in general as it
# would make it easier to share efforts with Mageia.
%define		build_monolithic	0


%if %{build_cross_bootstrap}
%define		build_minimal		1
%define		libc_shared		0
%endif

%if %{build_cross}
%define		build_monolithic	1
%define		build_ada		0
%define		build_asan		1
%define		build_check		0
%define		build_cxx		1
%define		build_doc		0
%define		build_gomp		1
%define		build_itm		1
%define		build_java		0
%define		build_libgcc		1
%define		package_ffi		0
%define		build_ssp		1
%define		build_ubsan		1
%endif

%if %{build_minimal}
%define		build_ada		0
%define		build_asan		0
%define		build_atomic		0
%define		build_check		0
%define		build_cilkrts		0
%define		build_go		0
%define		build_lto		0
%define		build_lsan		0
%define		build_objc		0
%define		build_objcxx		0
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
%define		build_java		0
%define		build_libgcc		0
%define		build_pdf		0
%define		build_plugin		0
%define		package_ffi		0
%define		shared_libgnat		0
%endif


# Adapted from fedora procedure:
#   If there is no usable gcc-java neither libgcj for the arch,
# on an arch that has it, run:
#	rpmbuild -bc --define "_topdir `pwd`" --with java_build_tar SPECS/gcc.spec
# which creates libjava-classes-@{version}-@{release}.tar.bz2
#   With the tarball on the new arch, run:
#	rpmbuild -ba --define "_topdir `pwd`" -v --with java_bootstrap SPECS/gcc.spec
%bcond_with	java_build_tar
%bcond_with	java_bootstrap

%if 0
%define		x32_bootstrap	1
%endif

#-----------------------------------------------------------------------

Summary:	GNU Compiler Collection
%if %{system_compiler}
Name:		gcc
%else
Name:		%{cross_prefix}gcc%{package_suffix}
%endif
Release:	3
License:	GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group:		Development/C
Url:		http://gcc.gnu.org/
%if "%{linaro}" != ""
Version:	%{ver}_%{linaro}
%if "%{linaro_spin}" != ""
Source0:	http://abe.tcwglab.linaro.org/snapshots/gcc-linaro-%{branch}-%{linaro}-%{linaro_spin}.tar.xz
%else
Source0:	http://abe.tcwglab.linaro.org/snapshots/gcc-linaro-%{branch}-%{linaro}.tar.xz
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
Source8:	libc-x32-seed.tar.xz

# environment variables for enabling/disabling colorized gcc output
Source10:	gcc.sysconfig
Source11:	gcc.sh
Source12:	gcc.csh

Source100:	gcc.rpmlintrc

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
# Alias -Oz to -Os for compatibility with clang's -Oz flag
Patch14:	gcc-4.9-add-Oz-for-clang-compatibility.patch
# Fix build with ISL 0.13
Patch15:	https://raw.githubusercontent.com/archlinuxcn/repo/master/gcc-multilib-x32/gcc-4.9-isl-0.13-hack.patch
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
# Fix for fileline_fn callback being NULL in libbacktrace sometimes
Patch17:	gcc-4.9.1-libbacktrace-fix-null-callback.patch

# From Google's tree
# 539bbad457e7161f89fd4db3017b4abf478466f4
Patch100:	gcc-4.9-libstdc++-clang-c++11.patch
# 771c2f9542b4e84b08c107060319603d12ec8867
Patch101:	gcc-4.9-neon-alignment.patch
# d7c9c7963a79b60e2247bd5a41decc80938023f4
Patch102:	gcc-4.9-libstdc++-clang.patch
# 331e362574142e4c1d9d509533d1c96b6dc54d13
Patch104:	gcc-4.9-simplify-got.patch

# Patches 1001 and 1007 disabled until they're committed
# slibdir is either /lib or /lib64
Patch1001:	gcc33-pass-slibdir.patch
# pass libdir around
Patch1007:	gcc-4.6.2-multi-do-libdir.patch

BuildRequires:	%{cross_prefix}binutils >= 2.20.51.0.2
%if !%{build_cross_bootstrap}
BuildRequires:	%{cross_prefix}glibc-devel
%endif
BuildRequires:	dejagnu
BuildRequires:	elfutils-devel >= 0.147
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gdb
BuildRequires:	gettext
BuildRequires:	sharutils
BuildRequires:	texinfo
# For py_puresitedir
%if !(%{build_cross} || %{build_minimal})
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

%if %{system_compiler}
Requires:	%{name}-cpp >= %{EVRD}
Requires:	%{libgcc} >= %{EVRD}
Requires:	%{libgomp} >= %{EVRD}
# as gcc now has it's own output color support, let's obsolete the old
# colorgcc with it's perl wrapper script which is slightly buggy with it's
# it's output redirection anyways...
Obsoletes:	colorgcc <= 1.3.2-17
%endif
Requires:	%{cross_prefix}binutils >= 2.20.51.0.2
# Ensure https://qa.mandriva.com/show_bug.cgi?id=62943
# have been addressed if using an older version
%if !%{build_cross_bootstrap}
Requires:	%{cross_prefix}glibc-devel >= 2.13
%endif

Obsoletes:	%{_lib}mudflap0 < 4.9.1_2014.05
Obsoletes:	%{_lib}mudflap-devel < 4.9.1_2014.05
Obsoletes:	%{_lib}mudflap-static-devel < 4.9.1_2014.05
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description
The gcc package contains the GNU Compiler Collection version %{branch}.

%if %{system_compiler}
%files -f gcc.lang
%else
%files
%endif
%if %{system_compiler} || %{build_cross}
%{_bindir}/%{gcc_target_platform}-gcc
%{_bindir}/%{gcc_target_platform}-gcc-ar
%{_bindir}/%{gcc_target_platform}-gcc-nm
%{_bindir}/%{gcc_target_platform}-gcc-ranlib
%endif
%if %{build_cross}
%{_bindir}/%{gcc_target_platform}-gcov
%endif
%if %{system_compiler}
%config(noreplace) %{_sysconfdir}/sysconfig/gcc
%{_sysconfdir}/profile.d/90gcc.sh
%{_sysconfdir}/profile.d/90gcc.csh
%{_bindir}/gcc
%{_bindir}/gcc-ar
%{_bindir}/gcc-nm
%{_bindir}/gcc-ranlib
%{_bindir}/gcov
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man7/*
%{_infodir}/gcc.info*
%{_infodir}/gccint.info*
%{_infodir}/gccinstall.info*
%{target_libdir}/libgcc_s.so
%if %{build_multilib}
%{multilibdir}/libgcc_s.so
%endif
%if %isarch mips mipsel
%{target_libdir}32/libgcc_s.so
%{target_libdir}64/libgcc_s.so
%endif
%endif
%if !%{build_cross}
%{_bindir}/gcc-%{ver}
%endif
%{_bindir}/%{gcc_target_platform}-gcc-%{ver}
%dir %{gccdirparent}
%dir %{gccdir}
%dir %{gcclibexecdirparent}
%dir %{gcclibexecdir}
%{gcclibexecdir}/cc1
%{gcclibexecdir}/collect2
%{gccdir}/*.o
%{gccdir}/libgcc*.a
%{gccdir}/libgcov.a
%{gcclibexecdir}/lto*
%if %{build_lto}
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
%if %{build_gomp} && !%{build_monolithic}
%exclude %{gccdir}/include/omp*.h
%endif
%if %{build_multilib}
%if %isarch mips mipsel
%dir %{multigccdirn32}
%{multigccdirn32}/*.o
%{multigccdirn32}/libgcc*.a
%{multigccdirn32}/libgcov.a
%dir %{multigccdir64}
%{multigccdir64}/*.o
%{multigccdir64}/libgcc*.a
%{multigccdir64}/libgcov.a
%else
%dir %{multigccdir}
%{multigccdir}/*.o
%{multigccdir}/libgcc*.a
%{multigccdir}/libgcov.a
%endif
%endif
%if %{build_doc}
%doc %{_docdir}/gcc
%endif
%if %{build_check}
%doc %{_docdir}/gcc/test_summary.log
%endif
%if %{build_monolithic}
%if %{build_atomic}
%{target_libdir}/libatomic.a
%{target_libdir}/libatomic.so
%{target_libdir}/libatomic.so.%{atomic_major}*
%endif
%if %{build_gomp}
%{target_libdir}/libgomp.a
%{target_libdir}/libgomp.so
%{target_libdir}/libgomp.so.%{gomp_major}*
%{target_libdir}/libgomp.spec
%endif
%if %{build_libgcc}
%{target_libdir}/libgcc_s.so
%{target_libdir}/libgcc_s.so.%{gcc_major}
%endif
%if %{build_ssp}
%dir %{gccdir}/include/ssp
%{gccdir}/include/ssp/*.h
%{target_libdir}/libssp.so.%{ssp_major}*
%{target_libdir}/libssp.so
%{target_libdir}/libssp.a
%{target_libdir}/libssp_nonshared.a
%endif
%endif


########################################################################
%if %{build_libgcc} && !%{build_monolithic}
#-----------------------------------------------------------------------

%package -n %{libgcc}
Summary:	GNU C library
Group:		System/Libraries
%if "%{libgcc}" != "libgcc"
Provides:	%{cross_prefix}libgcc = %{EVRD}
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif
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
%if %{system_compiler} || %{build_cross}
#-----------------------------------------------------------------------

%package cpp
Summary:	The C Preprocessor
Group:		Development/C
Requires:	%{name} = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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

%if %{system_compiler}
%files cpp -f cpplib.lang
%else
%files cpp
%endif
%{_bindir}/%{cross_program_prefix}cpp
%if %{system_compiler}
/lib/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%if %{build_doc}
%doc %{_docdir}/gcc-cpp
%endif
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%files c++
%if %{system_compiler}
%{_bindir}/g++
%{_mandir}/man1/g++.1*
%endif
%if %{system_compiler} || %{build_cross}
%{_bindir}/%{gcc_target_platform}-c++
%{_bindir}/%{gcc_target_platform}-g++
%endif
%if !%{build_cross}
%{_bindir}/c++-%{ver}
%{_bindir}/g++-%{ver}
%endif
%{_bindir}/%{gcc_target_platform}-g++-%{ver}
%{gcclibexecdir}/cc1plus
%if %{build_monolithic}
%{target_slibdir}/libstdc++.a
%{target_slibdir}/libstdc++.so
%{target_slibdir}/libstdc++.so.%{stdcxx_major}*
%{target_slibdir}/libsupc++.a
%{target_prefix}/include/c++/%{ver}
%if %{build_itm}
%{target_libdir}/libitm.so.%{itm_major}*
%{target_libdir}/libitm.so
%{target_libdir}/libitm.spec
%{target_libdir}/libitm.a
%endif
%if %{build_asan}
%{target_libdir}/libasan.so.%{asan_major}*
%{target_libdir}/libasan.so
%{target_libdir}/libasan_preinit.o
%{target_libdir}/libasan.a
%endif
%if %{build_ubsan}
%{target_libdir}/libubsan.so.%{ubsan_major}*
%{target_libdir}/libubsan.so
%{target_libdir}/libsanitizer.spec
%{target_libdir}/libubsan.a
%endif
%else

#-----------------------------------------------------------------------

%package -n %{libstdcxx}
Summary:	GNU Standard C++ library
Group:		System/Libraries
%if "%{libstdcxx}" != "libstdc++"
Provides:	%{cross_prefix}libstdc++ = %{EVRD}
%endif
%if %{build_doc}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libstdcxx}
The libstdc++ package contains a rewritten standard compliant
GCC Standard C++ Library.

%if %{system_compiler}
%files -n %{libstdcxx} -f libstdc++.lang
%else
%files -n %{libstdcxx}
%endif
%{target_slibdir}/libstdc++.so.%{stdcxx_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibstdcxx}
Summary:	GNU Standard C++ library
Group:		System/Libraries
Conflicts:	%{libstdcxx} < 4.6.2-11
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
Provides:	%{cross_prefix}libstdc++-devel = %{ver}-%{release}
Provides:	%{cross_prefix}stdc++-devel = %{ver}-%{release}
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
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
%{target_libdir}/libstdc++.so
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
Provides:	%{cross_prefix}libstdc++-static-devel = %{EVRD}
%endif
Provides:	%{cross_prefix}stdc++-static-devel = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libstdcxx_static_devel}
Static libraries for the GNU standard C++ library.

%files -n %{libstdcxx_static_devel}
%{target_libdir}/libstdc++.*a
%{target_libdir}/libsupc++.*a
%if %{build_multilib}
%{multilibdir}/libstdc++.*a
%{multilibdir}/libsupc++.*a
%endif

%endif
#-----------------------------------------------------------------------
# build_monolithic


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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgnat}
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared
libraries, which are required to run programs compiled with the GNAT.

%files -n %{libgnat}
%{target_libdir}/libgnat-%{branch}.so.%{gnat_major}
%{target_libdir}/libgnarl-%{branch}.so.%{gnat_major}

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibgnat}
Summary:	GNU Ada 95 runtime libraries
Group:		System/Libraries
Conflicts:	%{libgnat} < 4.6.2-11
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgnat_devel}
GNAT is a GNU Ada 95 front-end to GCC. This package includes shared
libraries, which are required to compile with the GNAT.

%files -n %{libgnat_devel}
%if %{shared_libgnat}
%{target_libdir}/libgnat*.so
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%files gfortran
%{_bindir}/gfortran
%{_bindir}/gfortran-%{ver}
%{_bindir}/%{gcc_target_platform}-gfortran
%{_bindir}/%{gcc_target_platform}-gfortran-%{ver}
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
Provides:	%{cross_prefix}libgfortran = %{EVRD}
%if %{build_multilib}
Provides:	%{multilibgfortran} = %{EVRD}
%endif
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgfortran}
This package contains Fortran 95 shared library which is needed to run
Fortran 95 dynamically linked programs.

%files -n %{libgfortran}
%{target_libdir}/libgfortran.so.%{gfortran_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibgfortran}
Summary:	Fortran 95 runtime libraries
Group:		System/Libraries
%if %{build_quadmath}
Requires:	%{multilibquadmath} = %{EVRD}
%endif
Conflicts:	%{libgfortran} < 4.6.2-11
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
Provides:	%{cross_prefix}gfortran-devel = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgfortran_devel}
This package contains Fortran 95 shared library which is needed to
compile Fortran 95 programs.

%files -n %{libgfortran_devel}
%{target_libdir}/libgfortran.so
%{target_libdir}/libgfortran.spec
%if %{build_multilib}
%{multilibdir}/libgfortran.so
%{multilibdir}/libgfortran.spec
%endif

#-----------------------------------------------------------------------

%package -n %{libgfortran_static_devel}
Summary:	Fortran 95 static libraries
Group:		System/Libraries
Requires:	%{libgfortran_devel} = %{EVRD}
Provides:	%{cross_prefix}gfortran-static-devel = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgfortran_static_devel}
This package contains Fortran 95 static library which is needed to
compile Fortran 95 programs.

%files -n %{libgfortran_static_devel}
%{target_libdir}/libgfortran.*a
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%files go
%{_bindir}/gccgo
%{_bindir}/%{gcc_target_platform}-gccgo
%dir %{_libdir}/go
%if %{build_multilib}
%dir %{multilibdir}/go
%endif
%{_infodir}/gccgo.info*
%{_mandir}/man1/gccgo.1*
%{_bindir}/gccgo-%{ver}
%{_bindir}/%{gcc_target_platform}-gccgo-%{ver}
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgo}
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%files -n %{libgo}
%{target_libdir}/libgo.so.%{go_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibgo}
Summary:	Go runtime libraries
Group:		System/Libraries
Conflicts:	%{libgo} < 4.6.2-11
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgo_devel}
This package includes libraries and support files for compiling
Go programs.

%files -n %{libgo_devel}
%{target_libdir}/libgo.so
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgo_static_devel}
This package contains static Go libraries.

%files -n %{libgo_static_devel}
%{target_libdir}/libgo.*a
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
%{_bindir}/%{gcc_target_platform}-gcj
%{_bindir}/%{gcc_target_platform}-gcj-%{ver}
%{_bindir}/%{gcc_target_platform}-gcjh
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgcj}
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%files -n %{libgcj}
%dir %{target_libdir}/gcj-%{ver}-%{gcj_major}
%{target_libdir}/gcj-%{ver}-%{gcj_major}/*.so
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{target_libdir}/gcj-%{ver}-%{gcj_major}/classmap.db
%{target_libdir}/libgcj.so.%{gcj_major}*
%{target_libdir}/libgcj-tools.so.%{gcj_major}*
%{target_libdir}/libgij.so.%{gcj_major}*

#-----------------------------------------------------------------------

%package -n %{libgcj_bc}
Summary:	Java runtime library for gcc
Group:		System/Libraries
%if %{build_multilib}
Provides:	libgcj_bc%{gcj_bc_major} = %{EVRD}
%endif
Conflicts:	%{_lib}gcj13 < 4.7.3_2012.10-4
Conflicts:	%{_lib}gcj15 < 4.9.1_2014.05-2
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgcj_bc}
The Java(tm) runtime library. You will need this package to run your Java
programs compiled using the Java compiler from GNU Compiler Collection (gcj).

%files -n %{libgcj_bc}
%{target_libdir}/libgcj_bc.so.%{gcj_bc_major}*

#-----------------------------------------------------------------------

%package -n libgcj-java
Summary:	Java runtime library for gcc (Java parts)
Group:		System/Libraries
Conflicts:	%{_lib}gcj13 < 4.7.3_2012.10-4
Requires:	%{libgcj} = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgcj_devel}
The Java(tm) static libraries and C header files. You will need this
package to compile your Java programs using the GCC Java compiler (gcj).

%files -n %{libgcj_devel}
%{gccdir}/include/gcj
%{gccdir}/include/jawt*.h
%{gccdir}/include/jni*.h
%{gccdir}/include/jvm*.h
%{py_puresitedir}/libjava
%{target_libdir}/pkgconfig/libgcj-%{branch}.pc
%{target_libdir}/libgcj*.spec
%{target_libdir}/libgcj*.so
%{target_libdir}/libgij.so

#-----------------------------------------------------------------------

%package -n libgcj%{gcj_major}-src
Summary:	Java library sources
Group:		Development/Java
Requires:	%{libgcj} = %{EVRD}
Provides:	libgcj-src = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libobjc}
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%files -n %{libobjc}
%{target_libdir}/libobjc.so.%{objc_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibobjc}
Summary:	Objective-C runtime
Group:		System/Libraries
Provides:	libobjc = %{EVRD}
Conflicts:	%{libobjc} < 4.6.2-11
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libobjc_devel}
This package includes libraries and support files for compiling
Objective-C programs.

%files -n %{libobjc_devel}
%{target_libdir}/libobjc.so
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libobjc_static_devel}
This package contains static Objective-C libraries.

%files -n %{libobjc_static_devel}
%{target_libdir}/libobjc.*a
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libffi}
This package contains GCC shared support library which is needed
for FFI support.

%files -n %{libffi}
%{target_libdir}/libffi.so.%{ffi_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibffi}
Summary:	GCC support library for FFI
Group:		System/Libraries
Conflicts:	%{libffi} < 4.6.2-11
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libffi_devel}
This package contains GCC development which is needed
to compile FFI support.

%files -n %{libffi_devel}
%{target_libdir}/libffi.so
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libffi_static_devel}
This package contains GCC static libraries which are needed
to compile FFI support.

%files -n %{libffi_static_devel}
%{target_libdir}/libffi.*a
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libquadmath}
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%files -n %{libquadmath}
%{target_libdir}/libquadmath.so.%{quadmath_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibquadmath}
Summary:	GCC __float128 shared support library
Group:		System/Libraries
Conflicts:	%{libquadmath} < 4.6.2-11
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libquadmath_devel}
This package contains support for building Fortran programs using
REAL*16 and programs using __float128 math.

%files -n %{libquadmath_devel}
%{target_libdir}/libquadmath.so
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libquadmath_static_devel}
This package contains static libraries for building Fortran programs
using REAL*16 and programs using __float128 math.

%files -n %{libquadmath_static_devel}
%{target_libdir}/libquadmath.*a
%if %{build_multilib}
%{multilibdir}/libquadmath.*a
%endif

#-----------------------------------------------------------------------
# build quadmath
%endif

########################################################################
%if %{build_gomp} && !%{build_monolithic}
#-----------------------------------------------------------------------

%package -n %{libgomp}
Summary:	GCC OpenMP v3.0 shared support library
Group:		System/Libraries
Provides:	libgomp = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgomp_devel}
This package contains GCC development which is needed
to compile OpenMP v3.0 support.

%files -n %{libgomp_devel}
%{target_libdir}/libgomp.so
%{target_libdir}/libgomp.spec
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libgomp_static_devel}
This package contains GCC static libraries which are needed
to compile OpenMP v3.0 support.

%files -n %{libgomp_static_devel}
%{target_libdir}/libgomp.*a
%if %{build_multilib}
%{multilibdir}/libgomp.*a
%endif

#-----------------------------------------------------------------------
# build gomp
%endif

########################################################################
%if %{build_ssp} && !%{build_monolithic}
#-----------------------------------------------------------------------

%package -n %{libssp}
Summary:	GCC SSP shared support library
Group:		System/Libraries
Provides:	libssp = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libssp}
This package contains GCC shared support library which is needed
for SSP support.

%files -n %{libssp}
%{target_libdir}/libssp.so.%{ssp_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibssp}
Summary:	GCC SSP shared support library
Group:		System/Libraries
Provides:	libssp = %{EVRD}
Conflicts:	%{libssp} < 4.6.2-11
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libssp_devel}
This package contains GCC libraries which are needed
to compile SSP support.

%files -n %{libssp_devel}
%{target_libdir}/libssp.so
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libssp_static_devel}
This package contains GCC static libraries which are needed
to compile SSP support.

%files -n %{libssp_static_devel}
%{target_libdir}/libssp.*.*a
%if %{build_multilib}
%{multilibdir}/libssp.*.*a
%endif

#-----------------------------------------------------------------------
# build ssp
%endif

########################################################################
%if %{build_itm} && !%{build_monolithic}
#-----------------------------------------------------------------------

%package -n %{libitm}
Summary:	GCC Transactional Memory support library
Group:		System/Libraries
Provides:	libitm = %{EVRD}

%description -n %{libitm}
This package contains GCC's Transactional Memory support library.

%files -n %{libitm}
%{target_libdir}/libitm.so.%{itm_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibitm}
Summary:	GCC Transactional Memory support library
Group:		System/Libraries
Provides:	libitm = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libitm_devel}
This package contains GCC libraries which are needed
to use Transactional Memory features.

%files -n %{libitm_devel}
%{target_libdir}/libitm.so
%{target_libdir}/libitm.spec
%if %{build_multilib}
%{multilibdir}/libitm.so
%{multilibdir}/libitm.spec
%endif
%if %{system_compiler}
%{_infodir}/libitm.info*
%endif

#-----------------------------------------------------------------------

%package -n %{libitm_static_devel}
Summary:	GCC Transactional Memory static libraries
Group:		Development/C
Requires:	%{libitm_devel} = %{EVRD}
Provides:	libitm-static-devel = %{EVRD}
Provides:	itm-static-devel = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libitm_static_devel}
This package contains GCC static libraries which are needed
to compile Transactional Memory support.

%files -n %{libitm_static_devel}
%{target_libdir}/libitm.a
%if %{build_multilib}
%{multilibdir}/libitm.a
%endif

#-----------------------------------------------------------------------
# build itm
%endif

%if %{build_asan} && !%{build_monolithic}
#-----------------------------------------------------------------------
# Address Sanitizer
#-----------------------------------------------------------------------
%package -n %{libasan}
Summary:	GCC Address Sanitizer library
Group:		Development/C
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libasan}
GCC Address Sanitizer Library.

%files -n %{libasan}
%{target_libdir}/libasan.so.%{asan_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibasan}
Summary:	GCC Address Sanitizer library
Group:		Development/C
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libasan_devel}
This package contains GCC libraries which are needed
to use Address Sanitizer features.

%files -n %{libasan_devel}
%{target_libdir}/libasan.so
%{target_libdir}/libasan_preinit.o
%if %{build_multilib}
%{multilibdir}/libasan.so
%{multilibdir}/libasan_preinit.o
%endif

#-----------------------------------------------------------------------

%package -n %{libasan_static_devel}
Summary:	Static libasan
Group:		Development/C
Requires:	%{libasan_devel} = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libasan_static_devel}
Static libasan.

%files -n %{libasan_static_devel}
%{target_libdir}/libasan.a
%if %{build_multilib}
%{multilibdir}/libasan.a
%endif
%endif

#-----------------------------------------------------------------------
# Thread Sanitizer
#-----------------------------------------------------------------------
%if %isarch x86_64
%if %{build_tsan}
%package -n %{libtsan}
Summary:	GCC Thread Sanitizer library
Group:		Development/C
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libtsan}
GCC Address Sanitizer Library.

%files -n %{libtsan}
%{target_libdir}/libtsan.so.%{tsan_major}*

#-----------------------------------------------------------------------

%package -n %{libtsan_devel}
Summary:	GCC Thread Sanitizer development support
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libtsan} = %{EVRD}
Provides:	libtsan-devel = %{EVRD}
Provides:	tsan-devel = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libtsan_devel}
This package contains GCC libraries which are needed
to use Thread Sanitizer features.

%files -n %{libtsan_devel}
%{target_libdir}/libtsan.so

#-----------------------------------------------------------------------

%package -n %{libtsan_static_devel}
Summary:	Static libtsan
Group:		Development/C
Requires:	%{libtsan_devel} = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libtsan_static_devel}
Static libtsan.

%files -n %{libtsan_static_devel}
%{target_libdir}/libtsan.a
%endif
%endif

#-----------------------------------------------------------------------
# Atomic operations
#-----------------------------------------------------------------------
%if %{build_atomic} && !%{build_monolithic}
%package -n %{libatomic}
Summary:	GCC Atomic operations library
Group:		Development/C
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libatomic}
GCC Atomic operations Library.

%files -n %{libatomic}
%{target_libdir}/libatomic.so.%{atomic_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibatomic}
Summary:	GCC Atomic optimizer library
Group:		Development/C
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libatomic_devel}
This package contains GCC libraries which are needed
to use Atomic optimizer features.

%files -n %{libatomic_devel}
%{target_libdir}/libatomic.so
%if %{build_multilib}
%{multilibdir}/libatomic.so
%endif

#-----------------------------------------------------------------------

%package -n %{libatomic_static_devel}
Summary:	Static libatomic
Group:		Development/C
Requires:	%{libatomic_devel} = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libatomic_static_devel}
Static libatomic.

%files -n %{libatomic_static_devel}
%{target_libdir}/libatomic.a
%if %{build_multilib}
%{multilibdir}/libatomic.a
%endif
%endif

########################################################################
# Intel CILK
########################################################################
%if %isarch %{ix86} x86_64
%if %{build_cilkrts}
%package -n %{libcilkrts}
Summary:	CILK (multithreading programming language) runtime
Group:		Development/C
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libcilkrts}
CILK (multithreading programming language) runtime.

%files -n %{libcilkrts}
%{target_libdir}/libcilkrts.so.%{cilk_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibcilkrts}
Summary:	CILK (multithreading programming language) runtime
Group:		Development/C
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{multilibcilkrts}
CILK (multithreading programming language) runtime.

%files -n %{multilibcilkrts}
%{multilibdir}/libcilkrts.so.%{cilk_major}*
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libcilkrts_devel}
Development files for the CILK multithreading programming language.

%files -n %{libcilkrts_devel}
%{target_libdir}/libcilkrts.so
%{target_libdir}/libcilkrts.spec
%if %{build_multilib}
%{multilibdir}/libcilkrts.so
%{multilibdir}/libcilkrts.spec
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
%{target_libdir}/libcilkrts.a
%if %{build_multilib}
%{multilibdir}/libcilkrts.a
%endif
%endif
%endif

########################################################################
# VTV (VTable Verification)
########################################################################
%if %isarch %{ix86} x86_64
%if %{build_vtv}
%package -n %{libvtv}
Summary:	VTable Verification library
Group:		Development/C
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libvtv}
VTable Verification library.

%files -n %{libvtv}
%{target_libdir}/libvtv.so.%{vtv_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibvtv}
Summary:	VTable Verification library
Group:		Development/C
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libvtv_devel}
This package contains GCC libraries which are needed
to use VTable Verification features.

%files -n %{libvtv_devel}
%{target_libdir}/libvtv.so
%if %{build_multilib}
%{multilibdir}/libvtv.so
%endif

#-----------------------------------------------------------------------

%package -n %{libvtv_static_devel}
Summary:	Static libvtv
Group:		Development/C
Requires:	%{libvtv_devel} = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libvtv_static_devel}
Static libvtv

%files -n %{libvtv_static_devel}
%{target_libdir}/libvtv.a
%if %{build_multilib}
%{multilibdir}/libvtv.a
%endif
%endif
%endif

########################################################################
# UBSan (Undefined Behavior Sanitizer)
########################################################################
%if %{build_ubsan} && !%{build_monolithic}
%package -n %{libubsan}
Summary:	Undefined Behavior Sanitizer library
Group:		Development/C
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libubsan}
Undefined Behavior Sanitizer library.

%files -n %{libubsan}
%{target_libdir}/libubsan.so.%{ubsan_major}*

#-----------------------------------------------------------------------

%if %{build_multilib}
%package -n %{multilibubsan}
Summary:	Undefined Behavior Sanitizer library
Group:		Development/C
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libubsan_devel}
This package contains GCC libraries which are needed
to use Undefined Behavior Sanitizer features.

%files -n %{libubsan_devel}
%{target_libdir}/libubsan.so
%{target_libdir}/libsanitizer.spec
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
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{libubsan_static_devel}
Static libubsan.

%files -n %{libubsan_static_devel}
%{target_libdir}/libubsan.a
%if %{build_multilib}
%{multilibdir}/libubsan.a
%endif
%endif

########################################################################
# LSan (Leak Sanitizer)
########################################################################
%if %isarch x86_64
%if %{build_lsan}
%package -n %{liblsan}
Summary:	Leak Sanitizer library
Group:		Development/C
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{liblsan}
Leak Sanitizer library.

%files -n %{liblsan}
%{target_libdir}/liblsan.so.%{lsan_major}*

#-----------------------------------------------------------------------

%package -n %{liblsan_devel}
Summary:	GCC Leak Sanitizer development support
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{liblsan} = %{EVRD}
Provides:	liblsan-devel = %{EVRD}
Provides:	lsan-devel = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{liblsan_devel}
This package contains GCC libraries which are needed
to use Leak Sanitizer features.

%files -n %{liblsan_devel}
%{target_libdir}/liblsan.so

#-----------------------------------------------------------------------

%package -n %{liblsan_static_devel}
Summary:	Static liblsan
Group:		Development/C
Requires:	%{liblsan_devel} = %{EVRD}
%if %{build_cross}
AutoReq:	false
AutoProv:	false
%endif

%description -n %{liblsan_static_devel}
Static liblsan.

%files -n %{liblsan_static_devel}
%{target_libdir}/liblsan.a
%endif
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
%patch14 -p1 -b .Oz~
#patch15 -p1 -b .isl~
%patch16 -p1 -b .EVILaarch64~
%patch17 -p1 -b .libbacktrace~

%patch100 -p2 -b .google1~
%patch101 -p2 -b .google2~
%patch102 -p2 -b .google3~
%patch104 -p1 -b .google5~

%patch1001 -p1 -b .pass_slibdir~
%patch1007 -p1 -b .multi-do-libdir~

aclocal -I config
autoconf

echo %{vendor} > gcc/DEV-PHASE
%if !%{official}
    sed -i -e 's/4\.8\..*/%{version}/' gcc/BASE-VER
%endif

%if %{with java_bootstrap}
    tar xjf %{SOURCE6}
%endif

%if %{?x32_bootstrap}0
    pushd gcc
        tar -xf %{SOURCE7}
        mkdir gnu
        ln -s /usr/include/gnu/stubs-64.h gnu/stubs-x32.h
    popd
%endif

# Setup files for cross-compilation
# XXX embed uClibc / dietlibc sources? [ia64 checks for __GLIBC__]
%if %{build_cross}
sysroot=%{_prefix}/%{gcc_target_platform}
%endif
if [[ -n "$sysroot" ]]; then
mkdir sysroot
cd sysroot
[[ -d $sysroot/bin ]] &&
ln -s $sysroot/bin bin
[[ -f $sysroot/lib/crti.o ]] &&
ln -s $sysroot/lib lib
[[ -f $sysroot/lib64/crti.o ]] &&
ln -s $sysroot/lib64 lib64
[[ -f $sysroot/lib32/crti.o ]] &&
ln -s $sysroot/lib32 lib32
cd ../
fi

%if %{build_cross}
perl -pi -e '/^DRIVER_DEFINES/ .. /^gcc/ and s/(\@TARGET_SYSTEM_ROOT_DEFINE\@)/-DSYSROOT_SPEC="\\"\\"" \1/' gcc/Makefile.in
%endif

# Force a seperate object dir
mkdir obj-%{gcc_target_platform}

#-----------------------------------------------------------------------
%build
# FIXME: extra tools needed
export PATH=$PATH:$PWD/bin
export sysroot=%{target_prefix}
#_prefix}/%{gcc_target_platform}

# The -gdwarf-4 removal is a workaround for gcc bug #52420
OPT_FLAGS=`echo %{optflags} | \
    sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g' \
    -e 's/-m\(31\|32\|64\)//g' \
    -e 's/-fstack-protector//g' \
    -e 's/--param=ssp-buffer-size=4//' \
    -e 's/-gdwarf-4/-g/' \
    -e 's/-pipe//g'`
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`

%if %{build_cross}
OPT_FLAGS="-O2 -g -pipe"
%endif

# don't build crt files with -fasynchronous-unwind-tables
case " $OPT_FLAGS " in
*" -fasynchronous-unwind-tables "*)
  sed -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables /' -i gcc/Makefile.in
  ;;
esac

# Force a seperate object dir
pushd obj-%{gcc_target_platform}

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
PROGRAM_SUFFIX=""
%if "%{program_suffix}" != ""
PROGRAM_SUFFIX="--program-suffix=%{program_suffix}"
%endif
PROGRAM_PREFIX=""
%if "%{program_prefix}" != ""
PROGRAM_PREFIX="--program-prefix=%{program_prefix}"
%endif
%if %{build_cross}
CROSS_FLAGS="--with-build-sysroot=$sysroot --with-native-system-header-dir=/include --with-headers --disable-nls"
%endif
%if %{build_cross_bootstrap}
CROSS_FLAGS="--disable-threads"
%if %isarch %{lsb_arches}
# we have embedded the LSB 3.1 headers, so we can build the unwinding stuff too (ia64)
CROSS_FLAGS="$CROSS_FLAGS --with-build-sysroot=$sysroot --with-headers"
%endif
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
LIBC_FLAGS="$LIBC_FLAGS --enable-shared --enable-static"
%else
LIBC_FLAGS="$LIBC_FLAGS --disable-shared --enable-static"
%endif
# target specific flags (don't %ifarch for cross compilers)
case %{target_cpu} in
x86_64)		TARGET_FLAGS="--with-cpu=generic %{?build_multilib:--with-arch_32=i586 --with-multilib-list=m32,m64}%{?x32_bootstrap:,mx32}";;
i?86|athlon)	TARGET_FLAGS="--with-arch=i586 --with-cpu=generic";;
mips64|mips64el) TARGET_FLAGS="--enable-long-long --with-abi=64 --enable-targets=all";;
mips32|mips32el) TARGET_FLAGS="--enable-long-long --with-abi=n32 --enable-targets=all";;
mips|mipsel) TARGET_FLAGS="--enable-long-long --enable-targets=all --enable-multiarch";;
esac

BOOTSTRAP=bootstrap
%if %isarch %{ix86} x86_64
    %if %{system_compiler}
        BOOSTRAP=profiledbootstrap
    %endif
%endif

# We can't currently compile gcc with clang, even
# though that would be great for bootstrapping
CC=gcc \
CXX=g++ \
CFLAGS="$OPT_FLAGS" \
CXXFLAGS="$OPT_FLAGS" \
GCJFLAGS="$OPT_FLAGS" \
TCFLAGS="$OPT_FLAGS" \
XCFLAGS="$OPT_FLAGS" \
%if ! %{build_cross} && ! %{build_cross_bootstrap}
ORIGINAL_NM_FOR_TARGET="%{_bindir}/binutils-nm" \
NM_FOR_TARGET="%{_bindir}/binutils-nm" \
%endif
../configure \
        --prefix=%{_prefix} \
        --libexecdir=%{_libexecdir} \
	--libdir=%{_libdir} \
	--with-slibdir=%{target_slibdir} \
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
        --disable-libunwind-exceptions \
        --disable-werror \
        --enable-__cxa_atexit \
%if !%isarch %{mipsx}
        --enable-gold=default \
%endif
        --with-plugin-ld=%{_bindir}/%{gcc_target_platform}-ld \
%if %{system_compiler}
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
%if %isarch armv7l armv7hl
        --without-multilib \
        --disable-multilib \
        --with-cpu=cortex-a8 \
        --with-tune=cortex-a8 \
        --with-arch=armv7-a \
        --with-mode=thumb \
  %if %isarch armv7l
        --with-float=softfp \
  %else
        --with-float=hard \
  %endif
        --with-fpu=vfpv3-d16 \
        --with-abi=aapcs-linux \
%endif
        --host=%{_target_platform} \
	--build=%{_target_platform} \
	$CROSS_FLAGS \
	$TARGET_FLAGS

%if %{?x32_bootstrap}0
mkdir -p %{_target_platform}/x32/libgcc
pushd %{_target_platform}/x32/libgcc
tar -Jxf %{SOURCE8}
popd
%endif

%if %{build_cross}
%make
%else
GCJFLAGS="$OPT_FLAGS" \
%make BOOT_CFLAGS="$OPT_FLAGS" $BOOTSTRAP
# GNATMAKE=gnatmake GNATBIND=gnatbind
%endif

%if %{build_pdf}
    %make pdf || :
%endif

%if %{build_doc}
    pushd host-%{gcc_target_platform}/gcc
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
%makeinstall_std -C obj-%{gcc_target_platform}

%if %{build_java}
    %make -C obj-%{gcc_target_platform} \
        DESTDIR=%{buildroot} \
        JAR=$PWD/obj-%{gcc_target_platform}/%{gcc_target_platform}/libjava/scripts/jar \
        -C %{gcc_target_platform}/libjava \
        install-src.zip
%endif

%if %{build_cross} && !%{build_cross_bootstrap}
%makeinstall_std -C obj-%{gcc_target_platform}/%{gcc_target_platform}/libgcc
%endif

# configure python dir option does not cover libstdc++ and needs to remove
# /usr prefix for libjava
%if !%{build_cross}
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
%else
    rm -rf %{buildroot}%{_datadir}/gcc-%{ver}/python
%endif

pushd %{buildroot}%{_bindir}
%if %{system_compiler}
    mkdir -p %{buildroot}/lib
    ln -sf %{_bindir}/cpp %{buildroot}/lib/cpp
    install -m 0755 %{SOURCE4} %{SOURCE5} %{buildroot}%{_bindir}
    ln -sf %{gcc_target_platform}-gcc-%{ver} cc
%else
    %if !%{build_cross}
	rm %{buildroot}%{_bindir}/cpp
    %endif
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
        if [ -f %{gcc_target_platform}-$prog ]; then
            mv -f %{gcc_target_platform}-$prog{,-%{ver}}
        fi
        rm -f $prog
	%if %{build_cross}
            ln -sf %{gcc_target_platform}-$prog-%{ver} %{gcc_target_platform}-$prog
	%else
            ln -sf %{gcc_target_platform}-$prog-%{ver} $prog-%{ver}
	%endif
        %if %{system_compiler}
            ln -sf %{gcc_target_platform}-$prog-%{ver} $prog
            ln -sf %{gcc_target_platform}-$prog-%{ver} %{gcc_target_platform}-$prog
        %endif
    done
%if %{build_cxx}
    rm -f c++ %{gcc_target_platform}-c++{,-%{ver}}
    %if !%{build_cross}
	ln -sf %{gcc_target_platform}-g++-%{ver} c++-%{ver}
    %endif
    %if %{system_compiler}
        ln -sf %{gcc_target_platform}-g++-%{ver} c++
    %endif
    %if %{system_compiler} || %{build_cross}
        ln -sf %{gcc_target_platform}-g++-%{ver} %{gcc_target_platform}-c++
    %endif

    %if %{build_cross} && !%{build_cross_bootstrap}
	rm -f %{buildroot}%{target_libdir}/libstdc++.so.%{stdcxx_major}*-gdb.py
	%if %isarch mips mipsel
	    rm -f %{buildroot}%{target_libdir}32/libstdc++.so.%{stdcxx_major}*-gdb.py
	    rm -f %{buildroot}%{target_libdir}64/libstdc++.so.%{stdcxx_major}*-gdb.py
	%endif
        rm -rf %{buildroot}%{py_puresitedir}/libstdcxx
    %else
	mkdir -p %{buildroot}%{_datadir}/gdb/auto-load%{_libdir}
	mv -f %{buildroot}%{_libdir}/libstdc++.so.*.py \
	    %{buildroot}%{_datadir}/gdb/auto-load%{_libdir}
	perl -pi -e 's|%{_datadir}/gcc-%{ver}/python|%{py_puresitedir}|;' \
	    %{buildroot}%{_datadir}/gdb/auto-load%{_libdir}/libstdc++.*.py

    mkdir -p %{buildroot}/%{target_slibdir}
    mv %{buildroot}%{target_libdir}/libstdc++.so.%{stdcxx_major}* \
        %{buildroot}/%{target_slibdir}
    ln -srf %{buildroot}/%{target_slibdir}/libstdc++.so.%{stdcxx_major}.*.* \
        %{buildroot}%{target_libdir}/libstdc++.so

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
%endif
%if %{build_java}
    ln -sf gcjh %{gcc_target_platform}-gcjh
    # For some reason, the .so file is a real file, not a symlink
    ln -sf libgcj_bc.so.1.0.0 %{buildroot}%{_libdir}/libgcj_bc.so
%endif
popd

%if %{build_gomp} && !%{build_cross}
    mkdir -p %{buildroot}%{target_slibdir}
    mv %{buildroot}%{target_libdir}/libgomp.so.%{gomp_major}* \
        %{buildroot}%{target_slibdir}
    ln -srf %{buildroot}%{target_slibdir}/libgomp.so.%{gomp_major}.*.* \
        %{buildroot}%{target_libdir}/libgomp.so

    %if %{build_multilib}
        mkdir -p %{buildroot}%{multirootlibdir}
        mv %{buildroot}%{multilibdir}/libgomp.so.%{gomp_major}* \
            %{buildroot}%{multirootlibdir}
        ln -srf %{buildroot}%{multirootlibdir}/libgomp.so.%{gomp_major}.*.* \
            %{buildroot}%{multilibdir}/libgomp.so
    %endif
%endif

%if %{system_compiler}
    mkdir -p %{buildroot}/%{target_slibdir}
    mv %{buildroot}%{target_libdir}/libgcc_s.so.%{gcc_major} \
        %{buildroot}/%{target_slibdir}
    ln -srf %{buildroot}/%{target_slibdir}/libgcc_s.so.%{gcc_major} \
        %{buildroot}%{target_libdir}/libgcc_s.so

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
            rm -f %{buildroot}%{target_libdir}/$lib.so
            rm -f %{buildroot}%{gccdir}/adalib/$lib.so
            mv -f %{buildroot}%{gccdir}/adalib/$lib-%{branch}.so \
                    %{buildroot}%{target_libdir}/$lib-%{branch}.so.1
            ln -sf $lib-%{branch}.so.1 %{buildroot}%{target_libdir}/$lib-%{branch}.so
            ln -sf $lib-%{branch}.so.1 %{buildroot}%{target_libdir}/$lib.so
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

%if %{build_cross_bootstrap}
# libgcc_eh.a is needed for glibc _but_ it is not built at this stage
# (disabled-shared)
# workaround by symlinking to libgcc. The other possibility would be to
# workaround at glibc level but it would be more painfull.
ln -srf %{buildroot}%{gccdir}/libgcc.a \
	%{buildroot}%{gccdir}/libgcc_eh.a
%if %isarch mips mipsel
ln -srf %{buildroot}%{gccdir}/n32/libgcc.a \
	%{buildroot}%{gccdir}/n32/libgcc_eh.a
ln -srf %{buildroot}%{gccdir}/64/libgcc.a \
	%{buildroot}%{gccdir}/64/libgcc_eh.a
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
    %if %{build_libgcc} && %{build_cross}
        mv %{buildroot}%{_libdir}/libgcc_s.so %{buildroot}%{target_libdir}/
        mv %{buildroot}%{_libdir}/libgcc_s.so.* %{buildroot}%{target_libdir}/
    %else
        rm -f %{buildroot}%{_libdir}/libgcc_s.so
        %if %{build_multilib}
            rm -f %{buildroot}%{multilibdir}/libgcc_s.so
        %endif
        %if !%{build_libgcc}
             rm -f %{buildroot}%{target_libdir}/libgcc_s.so.*
             %if %{build_multilib}
                 rm -f %{buildroot}%{multilibdir}/libgcc_s.so.*
             %endif
        %endif
    %endif
%endif
rm -f %{buildroot}%{_libdir}/libiberty.a
rm -f %{buildroot}%{multilibdir}/libiberty.a

%if !%{build_ubsan}
    rm -f %{buildroot}%{target_libdir}/libubsan*
    %if %{build_multilib}
        rm -f %{buildroot}%{multilibdir}/libubsan*
    %endif
    rm -f %{buildroot}%{target_libdir}/libsanitizer.spec
%endif

%if !%{build_asan}
    rm -f %{buildroot}%{target_libdir}/libasan*
    %if %{build_multilib}
        rm -f %{buildroot}%{multilibdir}/libasan*
    %endif
%endif

%if !%{build_itm}
    rm -f %{buildroot}%{target_libdir}/libitm* %{buildroot}%{_infodir}/libitm.info*
    %if %{build_multilib}
        rm -f %{buildroot}%{multilibdir}/libitm*
    %endif
%else
    %if !%{system_compiler}
        rm -f %{buildroot}%{_infodir}/libitm.info*
    %endif
%endif

%if !%{package_ffi}
    rm -f %{buildroot}%{target_libdir}/libffi.*
    rm -f %{buildroot}%{multilibdir}/libffi.*
    rm -f %{buildroot}%{_mandir}/man3/ffi*
%else
    mkdir -p %{buildroot}%{target_slibdir}
    mv %{buildroot}%{target_libdir}/libffi.so.%{ffi_major}* \
        %{buildroot}%{target_slibdir}
    ln -srf %{buildroot}%{target_slibdir}/libffi.so.%{ffi_major}.*.* \
        %{buildroot}%{target_libdir}/libffi.so

    %if %{build_multilib}
        mkdir -p %{buildroot}%{multirootlibdir}
        mv %{buildroot}%{multilibdir}/libffi.so.%{ffi_major}* \
            %{buildroot}%{multirootlibdir}
        ln -srf %{buildroot}%{multirootlibdir}/libffi.so.%{ffi_major}.*.* \
            %{buildroot}%{multilibdir}/libffi.so
    %endif
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
    pushd host-%{gcc_target_platform}/gcc/doc
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
    pushd %{gcc_target_platform}
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

%if ! %{default_compiler}
# Leave the cc, c89, c++, ... symlinks to clang
# or whatever other compiler is the default
rm -f \
	%{buildroot}%{_bindir}/cc \
	%{buildroot}%{_bindir}/c89 \
	%{buildroot}%{_bindir}/c99 \
	%{buildroot}%{_bindir}/c++
%endif

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

%if %{system_compiler}
install -m644 %{SOURCE10} -D %{buildroot}%{_sysconfdir}/sysconfig/gcc
install -m644 %{SOURCE11} -D %{buildroot}%{_sysconfdir}/profile.d/90gcc.sh
install -m644 %{SOURCE12} -D %{buildroot}%{_sysconfdir}/profile.d/90gcc.csh
%endif

%if %{system_compiler}
%find_lang cpplib
%find_lang gcc
%if %{build_cxx}
%find_lang libstdc++
%endif
%endif
