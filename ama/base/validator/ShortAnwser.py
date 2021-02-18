#!/usr/bin/env python3
#
# Validator
#
# Date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


class Validator:

    #Ensure that response of a show question is y or n
    # return True if response is "y" and False if not
    def shortAnwser(answer):
        response = input(answer)
        while response not in ["y", "Y", "n", "N"]:
            response = input(answer)

        if response in ["y", "Y"]:
            return True
        else:
            return False
