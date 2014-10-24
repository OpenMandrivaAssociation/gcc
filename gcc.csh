if ( -f /etc/sysconfig/gcc ) then
    eval `sed -n 's/^\([^#]*\)=\([^#]*\)/set \1=\2;/p' < /etc/sysconfig/gcc`
endif
if ( ${?GCC_COLORS} ) then
	setenv GCC_COLORS $GCC_COLORS
    else
	setenv GCC_COLORS auto
endif
