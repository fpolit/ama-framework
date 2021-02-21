#!/usr/bin/env python3
#
# Answer Validator
#
# Date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


class Answer:

    # Ensure that response of a show question is y or n
    # return True if response is "y" and False if not
    @staticmethod
    def shortAnwser(shortQuestion):
        """
         Ensure that response of a show question is y or n
         return True if response is "y" and False if not
        """
        response = input(shortQuestion)
        while response not in ["y", "Y", "n", "N"]:
            response = input(shortQuestion)

        if response in ["y", "Y"]:
            return True
        else:
            return False
