#!/usr/bin/env python3

class NoArgumentProvided(Exception):
    def __init__(self):
        self.warningMsg = f"No Arguments Provided"
        super().__init__(self.warningMsg)


# Combinator utility exceptions
class InvalidArgumentsGiven(Exception):
    def __init__(self, **args):
        self.warning = "Invalid Arguments Given\n"
        for arg, argValue in args.items():
            self.warning += "{arg} : {argValue}\n"

        super().__init__(self.warning)

class InvalidWordlistNumber(Exception):
    def __init__(self, wordlistNumber):
        self.wordlistNumber = wordlistNumber
        self.warningMsg = f"Invalid wordlist number: {self.wordlistNumber}"
        super().__init__(self.warningMsg)



class NoOutputFileSupplied(Exception):
    def __init__(self):
        super().__init__("No output file supplied")


class InvalidCombinationAction(Exception):
    def __init__(self, action):
        self.warning = f"Invalid Combination Acction: {action}"
        super().__init__(self.warning)
