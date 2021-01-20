#!/usr/bin/env python3
#
# combinate two wordlist and generate a combined wordlist
#
# Maintainer : glozanoa <glozanoa@uni.pe>

#from mpi4py import MPI

# base modules imports
from ..base.Mask import Mask
from ..base.FilePath import FilePath

from ..base.MaskExceptions import InvalidMaskSymbol
from ..base.MaskExceptions import MaskError


# utilities exceptions
from ..utilities.utilitiesExceptions import InvalidArgumentsGiven
from ..utilities.utilitiesExceptions import InvalidWordlistNumber
from ..utilities.utilitiesExceptions import NoOutputFileSupplied


class Combinator:
    actions = {0: 'Wordlists combination',
               1: 'Masks file + Wordlist',
               2: 'Wordlist + Masks file'}

    @staticmethod
    def selectAction(*, wordlists=None, masksFiles=None, action, output):
        if action == 0:
            wordlistNumber = len(wordlists)
            if wordlistNumber != 2:
                raise InvalidWordlistNumber(wordlistNumber)

            Combinator.wordlist(wordlists, output)

        elif action == 1:
            if not (len(wordlists) == 1 and len(masksFiles) == 1):
                raise InvalidArgumentsGiven({'wordlists':wordlists, 'masksFiles': masksFiles})

            if not output:
                raise NoOutputFileSupplied

            Combinator.hybridWMF(wordlists, masksFiles, output)

        elif action == 2:
            if not (len(wordlists) == 1 and len(masksFiles) == 1):
                raise InvalidArgumentsGiven({'wordlists':wordlists, 'masksFiles': masksFiles})

            if not output:
                raise NoOutputFileSupplied

            Combinator.hybridMFW(masksFiles, wordlists, output)

    @staticmethod
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

        with open(combinedWordlist, 'w') as _combinedWordlist:
            with open(firstWordlistPath, 'r') as _firstWordlist:
                while word1w := _firstWordlist.readline().rstrip():
                    with open(secondWordlistPath, 'r') as _secondWordlist:
                        while word2w := _secondWordlist.readline().rstrip():
                            combinedWord = word1w + word2w
                            _combinedWordlist.write(f"{combinedWord}\n")


        print_successful(f"Combinated wordlist was generated: {combinedWordlist}")


    @staticmethod
    def hybridWMF(wordlist, masksFile, output):
        with open(masksFile, 'r') as masks:
            genwmf = [] #generated words of combination of wordlist + masks (of masksFile)
            while mask := masks.readline().rstrip():
                genwmf += genWords(wordlist, mask)

        # writing output with generated words
        with open(output, 'w') as outputFile:
            for generateWord in genwmf:
                outputFile.write(f"{generateWord}\n")

        print_successful(f"Combinated wordlist and masks file was generated: {output}")


    @staticmethod
    def hybridMFW(masksFile, wordlist, output):
        """
        generate all the combination of the generated words by the mask and the words in the wordlist
        """

        with open(masksFile, 'r') as masks:
            genmfw = [] #generated words of combination of masks(of masksFile) + wordlist
            while mask := masks.readline().rstrip():
                genmfw += genWords(wordlist, mask, inverse=True)

        # writing output with generated words
        with open(output, 'w') as outputFile:
            for generateWord in genwmf:
                outputFile.write(f"{generateWord}\n")

        print_successful(f"Combinated masks file and wordlist was generated: {output}")


    @staticmethod
    def expand(wordsFile, maskSymbol, *, inverse=False):
        # genWords variable store the combination of
        #word (of wordFile) + maskSymbol(["?l" (abc...z) or "?u" or ... or "?a"])
        # if inverser=True: it will combine maskSymbol + word
        genWords = []
        if maskSymbol in Mask.charset:
            if inverse:
                with open(wordsFile, 'r') as words:
                    while word := words.readline().rstrip():
                        for character in Mask.charset[maskSymbol]:
                            genWords.append(character + word)
                return genWords

            else:
                with open(wordFile, 'r') as words:
                    while word := words.readline().rstrip():
                        for character in Mask.charset[maskSymbol]:
                            genWords.append(word + character)
                return genWords

        else:
            raise InvalidMaskSymbol(maskSymbol)


    @staticmethod
    def genWords(words, mask, *, inverse=False):
        """
        generate all the posible combination of words + mask
        if inverse is True, it combine mask + words (in that order)
        """

        if Mask.isMask(mask):
            for word in words:
                for maskSymbol in Mask._genIterMask(mask, inverse):
                    words = Mask.expand(words, maskSymbol, inverse)
            return words
        else:
            raise MaskError(mask)
