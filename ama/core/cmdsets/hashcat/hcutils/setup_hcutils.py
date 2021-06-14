#!/usr/bin/env python3

from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension(name="hcutils", sources=["pyhcutils.pyx",
                                         "combinator.c",
                                         "combipow.c",
                                         "combinator3.c"])
setup(ext_modules=cythonize(ext))
