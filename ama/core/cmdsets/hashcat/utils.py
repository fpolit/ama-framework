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
    CommandSet,
    with_default_category,
    with_argparser
)


@with_default_category(Category.HASHCAT)
class HashcatUtils(CommandSet):
    """
    Hashcat-utils commands
    """

    def __init__(self):
        super().__init__()

    parser_combinator = argparse.ArgumentParser()
    parser_combinator.add_argument('wordlists', nargs=2, help='Wordlist files')
    parser_combinator.add_argument('outfile', help='Ouput wordlist')
    def do_combinator(self, args):
        """
        Hashcat-Utils combinator
        """
        pass

    parser_combinator3 = argparse.ArgumentParser()
    parser_combinator3.add_argument('wordlists', nargs=3, help='Wordlist files')
    parser_combinator3.add_argument('outfile', help='Ouput wordlist')
    def do_combinator3(self, args):
        """
        Hashcat-Utils combinator3
        """
        pass

    parser_combipow = argparse.ArgumentParser()
    parser_combipow.add_argument('wordlist', help='Wordlist file')
    parser_combipow.add_argument('outfile', help='Ouput wordlist')
    def do_combipow(self, args):
        """
        Hashcat-Utils combipow
        """
        pass

    parser_len = argparse.ArgumentParser()
    parser_len.add_argument('min', help='Minimun password length')
    parser_len.add_argument('max', help='Maximun password length')
    parser_len.add_argument('infile', help='Input wordlist')
    parser_len.add_argument('outfile', help='Ouput wordlist')
    def do_len(self, args):
        """
        Hashcat-Utils len
        """
        pass

    parser_mli2 = argparse.ArgumentParser()
    parser_mli2.add_argument('infile', help='Input wordlist')
    parser_mli2.add_argument('mergefile', help='Merge wordlist')
    parser_mli2.add_argument('outfile', help='Ouput wordlist')
    def do_mli2(self, args):
        """
        Hashcat-Utils mli2
        """
        pass

    parser_rli = argparse.ArgumentParser()
    parser_rli.add_argument('infile', help='Input wordlist')
    parser_rli.add_argument('outfile', help='Ouput wordlist')
    parser_rli.add_argument('removefile', help='Remove wordlist')
    def do_rli(self, args):
        """
        Hashcat-Utils rli
        """
        pass

    parser_splitlen = argparse.ArgumentParser()
    parser_splitlen.add_argument('infile', help='Input wordlist')
    parser_splitlen.add_argument('outfile', help='Ouput wordlist')
    def do_splitlen(self, args):
        """
        Hashcat-Utils splitlen
        """
        pass