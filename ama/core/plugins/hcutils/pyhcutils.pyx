# Python wrapper for hashcat-utils
#
# Maintainer: glozanoa<glozanoa@uni.pe>


# combinator - hashcat utils
cdef extern from "combinator.h":
   int combinator2stdout(char* wl1, char* wl2)
   int combinator(char* wl1, char* wl2, char* out)

cpdef int pycombinator2stdout(char* wl1, char* wl2):
   return combinator2stdout(wl1, wl2)

cpdef int pycombinator(char* wl1, char* wl2, char* out):
   return combinator(wl1, wl2, out)



# combinator3 - hashcat utils
cdef extern from "combinator3.h":
   int combinator32stdout(char* wl1, char* wl2, char* wl3)
   int combinator3(char* wl1, char* wl2, char* wl3, char* out)

cpdef int pycombinator32stdout(char* wl1, char* wl2, char* wl3):
   return combinator32stdout(wl1, wl2, wl3)

cpdef int pycombinator3(char* wl1, char* wl2, char* wl3, char* out):
   return combinator3(wl1, wl2, wl3, out)



# combipow - hashcat utils
cdef extern from "combipow.h":
   int combipow2stdout(char* wl)
   int combipow(char* wl, char* out)

cpdef int pycombipow2stdout(char* wl):
   return combipow2stdout(wl)

cpdef int pycombipow(char* wl, char* out):
   return combipow(wl, out)



# mli2 - hashcat utils
# cdef extern from "mli2.h":
#   int mli2stdout(char* infile, char* mergefile)

# cpdef int pymli2stdout(char* infile , char* mergefile):
#    return mli2stdout(infile, mergefile)




# # len - hashcat utils
# cdef extern from "len.h":
#    int len(int min, int max, char* infile)

# cpdef int pylen(int min, int max, char* wl):
#    return len(min, max, wl)
