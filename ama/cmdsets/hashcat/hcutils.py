#!/usr/bin/env python3
#
# hashcat-utils commands (these commands are inside 'hashcat' command sets)
#
# Implementation - date: Apr 5 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

import sys
import argparse

# commandset categories
from ..category import CmdsetCategory as Category

# cmd2 imports
import cmd2
from cmd2 import (
    Cmd,
    CommandSet,
    with_default_category,
    with_argparser,
    Cmd2ArgumentParser
)

# python wrapper of hashcat utils
from ama.core.plugins.hcutils import pyhcutils

@with_default_category(Category.HASHCAT)
class HashcatUtils(CommandSet):
    """
    Hashcat-utils commands
    """

    def __init__(self):
        super().__init__()


    parser_combinator = Cmd2ArgumentParser()
    parser_combinator.add_argument('wordlists', nargs=2, completer=Cmd.path_complete,
                                   help='Wordlist files')
    parser_combinator.add_argument('-o', '--output', default = None, completer=Cmd.path_complete,
                                   help='Output file')

    @with_argparser(parser_combinator)
    def do_combinator(self, args):
        """
        Combinate the words of 2 wordlists
        """
        wl1 = bytes(args.wordlists[0], 'utf-8')
        wl2 = bytes(args.wordlists[1], 'utf-8')

        if args.output:
            out = bytes(args.output, 'utf-8')
            pyhcutils.pycombinator(wl1, wl2, out)
        else:
            pyhcutils.pycombinator2stdout(wl1, wl2)


    parser_combinator3 = Cmd2ArgumentParser()
    parser_combinator3.add_argument('wordlists', nargs=3, completer=Cmd.path_complete,
                                    help='Wordlist files')
    parser_combinator3.add_argument('-o','--output', default=None, completer=Cmd.path_complete,
                                    help='Ouput file')
    @with_argparser(parser_combinator3)
    def do_combinator3(self, args):
        """
        Combinate the words of 3 wordlists
        """
        wl1 = bytes(args.wordlists[0], 'utf-8')
        wl2 = bytes(args.wordlists[1], 'utf-8')
        wl3 = bytes(args.wordlists[2], 'utf-8')

        if args.output:
            out = bytes(args.output, 'utf-8')
            pyhcutils.pycombinator3(wl1, wl2, wl3, out)
        else:
            pyhcutils.pycombinator32stdout(wl1, wl2, wl3)



    parser_combipow = Cmd2ArgumentParser()
    parser_combipow.add_argument('wordlist', completer=Cmd.path_complete,
                                 help='Wordlist file')
    parser_combipow.add_argument('-o', '--output', default=None, completer=Cmd.path_complete,
                                 help='Ouput file')
    @with_argparser(parser_combipow)
    def do_combipow(self, args):
        """
        Produces all unique combinations of a wordlist
        """

        wl = bytes(args.wordlist, 'utf-8')

        if args.output:
            out = bytes(args.output, 'utf-8')
            pyhcutils.pycombipow(wl, out)
        else:
            pyhcutils.pycombipow2stdout(wl)



    parser_mli2 = Cmd2ArgumentParser()
    parser_mli2.add_argument('wordlists', nargs=2, completer=Cmd.path_complete,
                                    help='Sorted Wordlist Files')
    parser_mli2.add_argument('-o', '--output', default=None, completer=Cmd.path_complete,
                             help='Ouput file')
    @with_argparser(parser_mli2)
    def do_mli2(self, args):
        """
         Merge 2 sorted wordlists
        """
        wl1 = bytes(args.wordlists[0], 'utf-8')
        wl2 = bytes(args.wordlists[1], 'utf-8')

        if args.output:
            out = bytes(args.output, 'utf-8')
            #pyhcutils.(wl1, wl2, out)
        else:
            #pyhcutils.pymli2stdout(wl1, wl2)
            pass



    parser_rli = Cmd2ArgumentParser()
    parser_rli.add_argument('infile', completer=Cmd.path_complete,
                            help='Input wordlist')
    parser_rli.add_argument('outfile', completer=Cmd.path_complete,
                            help='Ouput wordlist')
    parser_rli.add_argument('removefile', completer=Cmd.path_complete,
                            help='Remove wordlist')
    @with_argparser(parser_rli)
    def do_rli(self, args):
        """
        Compare a single file against another file(s) and removes all duplicates
        """
        pass



    parser_len = Cmd2ArgumentParser()
    parser_len.add_argument('min', help='Minimun password length')
    parser_len.add_argument('max', help='Maximun password length')
    parser_len.add_argument('infile', completer=Cmd.path_complete,
                            help='Input wordlist')
    parser_len.add_argument('outfile', completer=Cmd.path_complete,
                            help='Ouput wordlist')
    @with_argparser(parser_len)
    def do_len(self, args):
        """
        Hashcat-Utils len
        """
        pass


    parser_splitlen = Cmd2ArgumentParser()
    parser_splitlen.add_argument('infile', completer=Cmd.path_complete,
                                 help='Input wordlist')
    parser_splitlen.add_argument('outfile', completer=Cmd.path_complete,
                                 help='Ouput wordlist')
    @with_argparser(parser_splitlen)
    def do_splitlen(self, args):
        """
        Hashcat-Utils splitlen
        """
        pass
