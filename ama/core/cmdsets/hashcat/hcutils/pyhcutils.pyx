# Python wrapper for hashcat-utils
#
# Maintainer: glozanoa<glozanoa@uni.pe>

# combinator - hashcat utils
cdef extern from "combinator.h":
   int combinator2stdout(char* wl1, char* wl2)
   int combinator(char* wl1, char* wl2, char* out)

cpdef int pycombinator2stdout(char* wl1, char* wl2):
   combinator2stdout(wl1, wl2)

cpdef int pycombinator(char* wl1, char* wl2, char* out):
   combinator(wl1, wl2, out)

# combinator3 - hashcat utils
cdef extern from "combinator3.h":
   int combinator32stdout(char* wl1, char* wl2, char* wl3)
   int combinator3(char* wl1, char* wl2, char* wl3, char* out)

cpdef int pycombinator32stdout(char* wl1, char* wl2, char* wl3):
   combinator32stdout(wl1, wl2, wl3)

cpdef int pycombinator3(char* wl1, char* wl2, char* wl3, char* out):
   combinator3(wl1, wl2, wl3, out)


# combipow - hashcat utils
cdef extern from "combipow.h":
   int combipow2stdout(char* wl)
   int combipow(char* wl, char* out)

cpdef int pycombipow2stdout(char* wl):
   combipow2stdout(wl)

cpdef int pycombipow(char* wl, char* out):
   combipow(wl, out)
