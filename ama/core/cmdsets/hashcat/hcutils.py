#!/usr/bin/env python3
#
# hashcat-utils commands (these commands are inside 'hashcat' command sets)
#
# Implementation - date: Apr 5 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

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
    parser_combinator.add_argument('outfile', completer=Cmd.path_complete,
                                   help='Ouput wordlist')

    @with_argparser(parser_combinator)
    def do_combinator(self, args):
        """
        Hashcat-Utils combinator
        """
        pass

    parser_combinator3 = Cmd2ArgumentParser()
    parser_combinator3.add_argument('wordlists', nargs=3, completer=Cmd.path_complete,
                                    help='Wordlist files')
    parser_combinator3.add_argument('outfile', completer=Cmd.path_complete,
                                    help='Ouput wordlist')
    @with_argparser(parser_combinator3)
    def do_combinator3(self, args):
        """
        Hashcat-Utils combinator3
        """
        pass

    parser_combipow = Cmd2ArgumentParser()
    parser_combipow.add_argument('wordlist', completer=Cmd.path_complete,
                                 help='Wordlist file')
    parser_combipow.add_argument('outfile', completer=Cmd.path_complete,
                                 help='Ouput wordlist')
    @with_argparser(parser_combipow)
    def do_combipow(self, args):
        """
        Hashcat-Utils combipow
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

    parser_mli2 = Cmd2ArgumentParser()
    parser_mli2.add_argument('infile', completer=Cmd.path_complete,
                             help='Input wordlist')
    parser_mli2.add_argument('mergefile', completer=Cmd.path_complete,
                             help='Merge wordlist')
    parser_mli2.add_argument('outfile', completer=Cmd.path_complete,
                             help='Ouput wordlist')
    @with_argparser(parser_mli2)
    def do_mli2(self, args):
        """
        Hashcat-Utils mli2
        """
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
        Hashcat-Utils rli
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
