#!/usr/bin/env python3
#
# combinate two wordlist and generate a combined wordlist
#
# Maintainer : glozanoa <glozanoa@uni.pe>

#from mpi4py import MPI
import shutil
from fineprint.status import print_successful

# base modules imports
from ..base.Mask import Mask
from ..base.FilePath import FilePath

from ..base.MaskExceptions import InvalidMaskSymbol
from ..base.MaskExceptions import MaskError


# utilities exceptions
from ..utilities.utilitiesExceptions import InvalidArgumentsGiven
from ..utilities.utilitiesExceptions import InvalidWordlistNumber
from ..utilities.utilitiesExceptions import NoOutputFileSupplied
from ..utilities.utilitiesExceptions import InvalidCombinationAction


class Combinator:
    actions = {0: 'Wordlists combination',
               1: 'Wordlist + Masks file or mask',
               2: 'Masks file or mask + Wordlist'}

    @staticmethod
    def selectAction(*, wordlists=None, masksFiles=None, mask=None, action, output):
        #import pdb; pdb.set_trace()

        if action == 0:
            wordlistNumber = len(wordlists)
            if wordlistNumber != 2:
                raise InvalidWordlistNumber(wordlistNumber)

            Combinator.wordlist(wordlists, output)

        elif action == 1:
            if mask and len(wordlists) == 1 and output:
                wordlist = wordlists[0]
                with open(output, 'w') as outputFile:
                    Combinator.genHybridWM(wordlist, mask, outputFile, inverse=False)

                print_successful(f"Combinated mask and wordlist was generated: {output}")


            elif len(wordlists) == 1 and len(masksFiles) == 1 and output:
                wordlist = wordlists[0]
                masksFile = masksFiles[0]
                Combinator.hybridMFW(wordlist = wordlist,
                                     masksFile = masksFile,
                                     output = output)

            elif not (len(wordlists) == 1 and len(masksFiles) == 1):
                raise InvalidArgumentsGiven({'wordlists':wordlists, 'masksFiles': masksFiles})

            if not output:
                raise NoOutputFileSupplied

        elif action == 2:
            if mask and len(wordlists) == 1 and output:
                wordlist = wordlists[0]
                with open(output, 'w') as outputFile:
                    Combinator.genHybridWM(wordlist, mask, outputFile, inverse=True)
                print_successful(f"Combinated wordlist and mask was generated: {output}")

            elif len(wordlists) == 1 and len(masksFiles) == 1 and output:
                wordlist = wordlists[0]
                masksFile = masksFiles[0]
                Combinator.hybridWMF(wordlist = wordlist,
                                     masksFile = masksFile,
                                     output = output)

            elif not (len(wordlists) == 1 and len(masksFiles) == 1):
                raise InvalidArgumentsGiven({'wordlists':wordlists, 'masksFiles': masksFiles})

            if not output:
                raise NoOutputFileSupplied

        else:
            raise InvalidCombinationAction(action)


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


        print_successful(f"Combinated wordlist generated: {combinedWordlist}")


    @staticmethod
    def hybridWMF(*, wordlist, masksFile, output):

        with open(output, 'w') as outputFile:
            with open(masksFile, 'r') as masks:
                while mask := masks.readline().rstrip():
                    Combinator.genHybridWM(wordlist, mask, outputFile, inverse=False)

        print_successful(f"Combinated masks file and wordlist was generated: {output}")

    @staticmethod
    def hybridMFW(*, masksFile, wordlist, output):
        """
        generate all the combination of the generated words by the mask and the words in the wordlist
        """

        with open(output, 'w') as outputFile:
            with open(masksFile, 'r') as masks:
                while mask := masks.readline().rstrip():
                    Combinator.genHybridWM(wordlist, mask, outputFile, inverse=True)

        print_successful(f"Combinated masks file and wordlist was generated: {output}")


    @staticmethod
    def expand(words, maskSymbol, *, inverse=False):
        # genWords variable store the combination of
        #word (of words list) + maskSymbol(["?l" (abc...z) or "?u" or ... or "?a"])
        # if inverser=True: it will combine maskSymbol + word
        genWords = []
        if maskSymbol in Mask.charset:
            if inverse:
                for word in words:
                    for character in Mask.charset[maskSymbol]:
                        genWords.append(character + word)
                return genWords

            else:
                for word in words:
                    for character in Mask.charset[maskSymbol]:
                        genWords.append(word + character)
                return genWords

        else:
            raise InvalidMaskSymbol(maskSymbol)


    @staticmethod
    def genHybridWM(wordsFile, mask, outputFile, *, inverse=False):
        """
        generate all the posible combination of words + mask
        if inverse is True, it combine mask + words (in that order)
        """

        if Mask.isMask(mask):
            with open(wordsFile, 'r') as words:
                while word := words.readline().rstrip():
                    genWords = [word]
                    for maskSymbol in Mask._genIterMask(mask, inverse):
                        genWords = Combinator.expand(genWords, maskSymbol, inverse = inverse)

                    for combinedWord in genWords:
                        outputFile.write(f"{combinedWord}\n")
        else:
            raise MaskError(mask)
