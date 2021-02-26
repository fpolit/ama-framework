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

#Argument = namedtuple('Argument', ['value', 'required', 'description'])
