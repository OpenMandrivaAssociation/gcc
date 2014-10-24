if [ -f /etc/sysconfig/gcc ]; then
    . /etc/sysconfig/gcc
fi
if [ -z "$GCC_COLORS" ]; then
	export GCC_COLORS=auto
    else
	export GCC_COLORS=$GCC_COLORS
fi
