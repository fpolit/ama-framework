#!/usr/bin/env python3
#
# argument format supplied to ama modules (attack and auxiliary)
#
# date: Feb 25 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

class Argument:
    """
    Argument for ama modules
    """

    def __init__(self, value, required, description):
        self.value = value
        self.required = required
        self.description = description

    def getAttributes(self):
        """
        Return attributes value, required and description in a list
        """
        return [self.value, self.required, self.description]

    def __repr__(self):
        return f"Argument(value={self.value}, required={self.required}, description={self.description})"

    def __eq__(self, other):
        if isinstance(other, Argument):
            return self.value == other.value
        else:
            return self.value == other

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if isinstance(other, Argument):
            return self.value < other.value
        else:
            return self.value < other

    def __gt__(self, other):
        if isinstance(other, Argument):
            return self.value > other.value
        else:
            return self.value > other

    def __le__(self, other):
        if isinstance(other, Argument):
            return self.value < other.value or self.value == other.value
        else:
            return self.value < other or self.value == other

    def __ge__(self, other):
        if isinstance(other, Argument):
            return self.value > other.value or self.value == other.value
        else:
            return self.value > other or self.value == other


#Argument = namedtuple('Argument', ['value', 'required', 'description'])
