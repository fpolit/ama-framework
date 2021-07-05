#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/r3nt0n/bopscrk
# bopscrk - script opts and presentation

import sys, os, datetime

from modules.args import Arguments
from modules.config import Config
from modules.auxiliars import clear
from modules import banners
from modules.color import color
from modules.transforms import leet_transforms, case_transforms, artist_space_transforms, lyric_space_transforms, multithread_transforms, take_initials
from modules.combinators import combinator, add_common_separators
from modules.excluders import remove_by_lengths, remove_duplicates, multithread_exclude


from ama.core.plugins.auxiliary import Auxiliary
from ama.core.files import Path

class Bopscrk(Auxiliary):
    MAINNAME =  'bopscrk'
    __author__ = 'r3nt0n'
    __version__ = '2.3.1'
    __status__ = 'Development'

    DEFAULT_MIN = 4
    DEFAULT_MAX = 12
    DEFAULT_N_WORDS = 2
    DEFAULT_OUTPUT_FILE = 'tmp.txt'
    DEFAULT_CFG_FILE = 'bopscrk.cfg'

    def __init__(self, cfg_file: Path = Path(Bopscrk.DEFAULT_CFG_FILE)):
        self.Config = Config(cfg_file)
        self.Config.setup()
        self.args = Arguments()
        self.args.cfg_file = cfg_file
        super().__init__(["bopscrk"], version=Bopscrk.__version__, search_exec=False)

    def interactive(self, quiet:bool = quiet, output:Path = Path(Bopscrk.DEFAULT_OUTPUT_FILE)):
        clear()
        banners.bopscrk_banner()
        banners.help_banner()
        banners.banner(name, Bopscrk.__version__, Bopscrk.__author__)

        self.args.outfile = output
        self.args.set_interactive_options()

        self.gen_wordlist()

        return output


    def combine(self, words:List[str],
                artists:List[str] = [], n_words:int = Bopscrk.DEFAULT_N_WORDS,
                min_length:int = Bopscrk.DEFAULT_MIN, max_length:int = Bopscrk.DEFAULT_MAX,
                leet:bool = False, case:bool = False,
                exclude_wordlists:List[str] = [],
                output:Path = Path(Bopscrk.DEFAULT_OUTPUT_FILE)):

        banners.bopscrk_banner()
        banners.help_banner()
        banners.banner(name, __version__, __author__)
        #self.args.set_cli_options()

        self.args.base_wordlist = []
        if words:
            self.args.base_wordlist += [word.lower() for word in words]
            #[self.base_wordlist.append(word.lower()) for word in ((self.args.words).split(','))]
        self.args.min_length = min_length
        self.args.max_length = max_length
        self.args.leet = leet
        self.args.case = case
        self.args.n_words = n_words
        self.args.artists = artists
        self.args.outfile = output
        self.args.exclude_wordlists = exclude_wordlists
        if self.args.exclude_wordlists:
            #self.exclude_wordlists = self.exclude_wordlists.split(',')
            for wl_path in self.args.exclude_wordlists:
                if not os.path.isfile(wl_path):
                    print('  {}[!]{} {} not found'.format(color.RED, color.END, wl_path))
                    sys.exit(4)

        self.gen_wordlist()

        return output


    def gen_wordlist(self):

        # Initial timestamp
        start_time = datetime.datetime.now().time().strftime('%H:%M:%S')

        # Inserting original values into final_wordlist
        base_wordlist = self.args.base_wordlist
        print('  {}[+]{} Appending words provided (base wordlist length: {})...'.format(color.BLUE, color.END, len(base_wordlist)))
        final_wordlist = base_wordlist[:]  # Copy to preserve the original

        # SEARCH FOR LYRICS
        if self.args.artists:
            print('  {}[+]{} Appending artist names   (base wordlist length: {})...'.format(color.BLUE, color.END,(len(base_wordlist)+len(self.args.artists))))
            for artist in self.args.artists:
                # Add IN BASE WORDLIST artist name as a word
                base_wordlist.append(artist)

                # Add artist name with all space transformed configured (and enabled) into a specific charset
                if not (self.Config.SPACE_REPLACEMENT_CHARSET and self.Config.ARTIST_SPACE_REPLACEMENT):
                    print('  {}[!]{} Any space-replacement charset specified in {}'.format(color.ORANGE, color.END, self.args.cfg_file))
                    print('  {}[!]{} Spaces inside artists names won\'t be replaced\n'.format(color.ORANGE, color.END))
                elif self.Config.ARTIST_SPACE_REPLACEMENT:
                    print('  {}[+]{} Producing new words replacing any space in {}...'.format(color.BLUE, color.END,artist))
                    final_wordlist += artist_space_transforms(artist)

                # Search lyrics if it meets dependencies for lyricpass
                try:
                    from modules.lyricpass import lyricpass
                    print('\n{}     -- Starting lyricpass module (by initstring) --\n'.format(color.GREY))
                    print('  {}[*]{} Looking for {}\'s lyrics...'.format(color.CYAN, color.END, artist.title()))
                    lyrics = lyricpass.lyricpass(artist)
                    #lyrics = [s.decode("utf-8") for s in lyfinder.lyrics]
                    print('\n  {}[*] {}{}{} phrases found'.format(color.CYAN, color.GREEN, len(lyrics), color.END))
                    print('\n{}     -- Stopping lyricpass module --\n'.format(color.GREY))

                    # First we remove all the parenthesis in the phrases (if enabled)
                    if Config.REMOVE_PARENTHESIS:
                        lyrics = ([s.replace('(', '') for s in lyrics])
                        lyrics = ([s.replace(')', '') for s in lyrics])

                    # Add the phrases to BASE wordlist
                    lyrics = remove_by_lengths(lyrics, self.args.min_length, self.args.max_length)
                    print('  {}[+]{} Removing by min and max length range ({} phrases remain)...'.format(color.BLUE, color.END,len(lyrics)))
                    final_wordlist += lyrics

                    # Take just the initials on each phrase and add as a new word to FINAL wordlist
                    if self.Config.TAKE_INITIALS:
                        base_lyrics = lyrics[:]
                        ly_initials_wordlist = multithread_transforms(take_initials, base_lyrics)
                        final_wordlist += ly_initials_wordlist

                    # Make space transforms and add it too
                    if not (self.Config.SPACE_REPLACEMENT_CHARSET and self.Config.LYRIC_SPACE_REPLACEMENT):
                        print('  {}[!]{} Any spaces-replacement charset specified in {}'.format(color.ORANGE, color.END, self.args.cfg_file))
                        print('  {}[!]{} Spaces inside lyrics won\'t be replaced\n'.format(color.ORANGE,color.END))
                    elif self.Config.LYRIC_SPACE_REPLACEMENT:
                        print('  {}[+]{} Producing new words replacing spaces in {} phrases...'.format(color.BLUE, color.END, len(lyrics)))
                        base_lyrics = lyrics[:]
                        space_transformed_lyrics = multithread_transforms(lyric_space_transforms, base_lyrics)
                        final_wordlist += space_transformed_lyrics

                except ImportError:
                    print('  {}[!]{} missing dependencies, only artist names will be added and transformed'.format(color.RED, color.END))

        # WORD COMBINATIONS
        if ((self.args.n_words > 1)):
            print('  {}[+]{} Creating all posible combinations between words...'.format(color.BLUE, color.END))
            i = 1
            while ((i < self.args.n_words) and (len(base_wordlist) > i)):
                i += 1
                final_wordlist += combinator(base_wordlist, i)
                print('  {}[*]{} Combining {} words using {} words (words produced: {})...'.format(color.CYAN,color.END,len(base_wordlist),i, len(final_wordlist)))
                #print('\n')



        # WORD COMBINATIONS (WITH COMMON SEPARATORS)
        if self.Config.EXTRA_COMBINATIONS:
            if self.Config.SEPARATORS_CHARSET:
                print('  {}[+]{} Creating extra combinations (separators charset in {}{}{})...'.format(color.BLUE, color.END,color.CYAN, self.args.cfg_file,color.END))
                final_wordlist += add_common_separators(base_wordlist)
            else:
                print('  {}[!]{} Any separators charset specified in {}{}'.format(color.ORANGE, color.END, self.args.cfg_file,color.END))


        # Remove words by min-max length range established
        final_wordlist = remove_by_lengths(final_wordlist, self.args.min_length, self.args.max_length)
        # (!) Check for duplicates (is checked before return in combinator() and add_common_separators())
        #final_wordlist = remove_duplicates(final_wordlist)

        # LEET TRANSFORMS
        if self.args.leet:
            if not self.Config.LEET_CHARSET:
                print('  {}[!]{} Any leet charset specified in {}'.format(color.ORANGE, color.END, self.args.cfg_file))
                print('  {}[!]{} Skipping leet transforms...'.format(color.ORANGE, color.END, self.args.cfg_file))
            else:
                recursive_msg = ''
                if self.Config.RECURSIVE_LEET:
                    print('\n  {}[!] WARNING: Recursive leet is enabled, depending on the words\n'
                          '      max-length configured (now is {}{}{}) and the size of your\n'
                          '      wordlist at this point (now contains {}{}{} words), this process\n'
                          '      could take several minutes{}\n'.format(color.ORANGE,color.END,self.args.max_length,color.ORANGE,color.END,len(final_wordlist),color.ORANGE,color.END))
                    recursive_msg = '{}recursive{} '.format(color.RED,color.END)
                print('  {}[+]{} Applying {}leet transforms to {} words...'.format(color.BLUE, color.END, recursive_msg,len(final_wordlist)))
                #print(final_wordlist)
                temp_wordlist = []
                temp_wordlist += multithread_transforms(leet_transforms, final_wordlist)
                final_wordlist += temp_wordlist

        # CASE TRANSFORMS
        if self.args.case:
            print('  {}[+]{} Applying case transforms to {} words...'.format(color.BLUE, color.END, len(final_wordlist)))
            temp_wordlist = []
            temp_wordlist += multithread_transforms(case_transforms, final_wordlist)
            final_wordlist += temp_wordlist

        # EXCLUDE FROM OTHER WORDLISTS
        if self.args.exclude_wordlists:
            # For each path to wordlist provided
            for wl_path in self.args.exclude_wordlists:
                print('  {}[+]{} Excluding wordlist {}...'.format(color.BLUE, color.END, os.path.basename(wl_path)))
                # Open the file
                with open(wl_path, 'r') as x_wordlist_file:
                    # Read line by line in a loop
                    while True:
                        word_to_exclude = x_wordlist_file.readline()
                        if not word_to_exclude: break  # breaks the loop when file ends
                        final_wordlist = multithread_exclude(word_to_exclude, final_wordlist)

        # re-check for duplicates
        final_wordlist = remove_duplicates(final_wordlist)

        # SAVE WORDLIST TO FILE
        ############################################################################
        with open(self.args.outfile, 'w') as f:
            for word in final_wordlist:
                f.write(word + '\n')

        # Final timestamps
        end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        total_time = (datetime.datetime.strptime(end_time, '%H:%M:%S') -
                      datetime.datetime.strptime(start_time, '%H:%M:%S'))

        # PRINT RESULTS
        ############################################################################
        print('\n  {}[+]{} Time elapsed:\t{}'.format(color.GREEN, color.END, total_time))
        print('  {}[+]{} Output file:\t{}{}{}{}'.format(color.GREEN, color.END, color.BOLD, color.BLUE, self.args.outfile, color.END))
        print('  {}[+]{} Words generated:\t{}{}{}\n'.format(color.GREEN, color.END, color.RED, len(final_wordlist), color.END))
