#!/usr/bin/env python3
#
# argument format for ama modules (attack and auxiliary) arguments
#
# date: Feb 25 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

class Argument:
    """
    Argument for ama modules
    """
    def __init__(self, value, required:bool, description:str, *, value_type=None, choices=None):
        self.value = Argument.parse(value, value_type)
        self.value_type = value_type
        self.choices = choices
        self.required = required
        self.description = description

    def set_value(self, value):
        import pdb; pdb.set_trace()
        self.value = Argument.parse(value, self.value_type)

    def get_attributes(self):
        """
        Return attributes value, required and description in a list
        """
        return [self.value, self.required, self.description]

    @staticmethod
    def parse(value, value_type):
        """
        Try to parse string value to a value with value_type type
        """
        parsed_value = None
        if (value is None) or (value_type is None) or isinstance(value, value_type):
            parsed_value = value

        else:
            if value_type == bool:
                if isinstance(value, int):
                    if value == 0:
                        parsed_value = False
                    else:
                        parsed_value = True
                elif isinstance(value, str):
                    valid_true_values = ["True", "true", "1", 1]
                    valid_false_values = ["False", "false", "0", 0]

                    if self.value not in [*valid_true_values, *valid_false_values]:
                        raise Exception(f"Invalid value for a boolean argument")

                    parsed_value = True if value in valid_true_values else False

            elif value_type == int:
                try:
                    parsed_value = int(value)
                except ValueError as error: #self.value isn't a number
                    raise Exception(f"Invalid value for a integer argument")
            elif value_type == str:
                parsed_value = str(value) # self.value is already a string

        return parsed_value

    @staticmethod
    def get_empty():
        EMPTY = Argument(None, required=False, decription=None)
        return EMPTY

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
