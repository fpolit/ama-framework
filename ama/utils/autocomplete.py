#!/usr/bin/env python3
#
# Auto complete for ama commands
#
# Status:
#
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse
import argcomplete
from cmd2 import Cmd

from ama.modules.base import Module
from ama.utils import with_argparser

def autocomplete_setv(module:Module):
	module_options = module.options

	def setv()
	setv_parser = argparse.ArgumentParser(prog='setv')
	setv_parser.add_argument("option", choices=module_options.keys(),
							 help="Module option")


	def	choice_values(prefix, parsed_args):
		choices = module_options[parsed_args.option]
		if choices:
			return (choice for choice in choices if choice.startwith(prefix))
		else:
			return []


	setv_parser.add_argument("value", help="Option value").completer = choice_values
	setv_parser.add_argument('-q',"--quiet", action='store_true',
                         help="Option value")

	extra_modules = setv_parser.add_mutually_exclusive_group()
	extra_modules.add_argument('-pre', '--pre-module', dest='pre_module',
						   action='store_true', help='Set pre module option')
	extra_modules.add_argument('-post', '--post-module', dest='post_module',
						   action='store_true', help='Set post module option')

	argcomplete.autocomplete(setv_parser)

	args = setb_parser.parse_args()

	#import pdb; pdb.set_trace()

	#@with_argparser(setv_parser)
	#def do_setv(args=None):
	print(f"args: {args}")

	return
