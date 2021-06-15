# Python wrapper for hashcat-utils
#
# Maintainer: glozanoa<glozanoa@uni.pe>

# combinator - hashcat utils
cpdef int pycombinator2stdout(char* wl1, char* wl2)
cpdef int pycombinator(char* wl1, char* wl2, char* out)

# combipow - hashcat utils0
cpdef int pycombipow2stdout(char* wl)
cpdef int pycombipow(char* wl, char* out)

# combinator3 - hashcat utils
cpdef int pycombinator32stdout(char* wl1, char* wl2, char* wl3)
cpdef int pycombinator3(char* wl1, char* wl2, char* wl3, char* out)
