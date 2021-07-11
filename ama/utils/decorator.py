#!/usr/bin/env python3
#
# Decorators used in ama
#
# Status:
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import argparse

def	with_argparser(parser:argparse.ArgumentParser):
	"""
	Parse argument parser and pass parsed arguments to a function

	Usage:

	parser = argparse.ArgumentParser(...)
	...

	@with_argparser(parser)
	def f(args):
	    do_something
	"""
	def wrapper(func):
		#print("was called Wrapper?")
		pargs = None
		try:
		    pargs = parser.parse_args()
		except Exception as error:
			print(error)

		return func(pargs)

	return wrapper
