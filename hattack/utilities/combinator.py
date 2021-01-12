#!/usr/bin/env python3
#
# combinate two wordlist and generate a combined wordlist
#
# Maintainer : glozanoa <glozanoa@uni.pe>


# combinator exceptions
class InvalidWordlistNumber(Exception):
    def __init__(self, wordlistNumber):
        self.wordlistNumber = wordlistNumber
        self.warningMsg = f"Invalid wordlist number: {self.wordlistNumber}"
        super().__init__(self.warningMsg)


from mpi4py import MPI
from ..base import FilePath

class Combinator:

    def wordlist(wordlists, combinedWordlist):
        """
        wordlists: list of path of wordlist to combine
        """

        wordlistNumber = len(wordlists)
        if wordlistNumber != 2:
            raise InvalidWordlistNumber(wordlistNumber)

        firstWordlist, secondWordlist = wordlists

        firstWordlistPath = FilePath(firstWordlist)
        secondWordlistPath = FilePath(secondWordlist)

        with open(firstWordlistPath, 'r') as _firstWordlist:
            # combine the wordlists


        combinedWordlistPath = FilePath(combinedWordlist)
        #write the combined words in the wordlist


        return combinedWordlistPath


    def hybridWMF(wordlist, maskFile):


    def hybridWM(wordlist, mask):
        """
        generate all the combination of the words in the wordlist and the generated words by the mask
        """


    def hybridWM(wordlist, mask):
        """
        generate all the combination of the generated words by the mask and the words in the wordlist
        """
