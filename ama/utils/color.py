#!/usr/bin/env python3
#
# String that support coloration
#
# Maintainer: glozanoa <glozanoa@uni.pe>


from colorama import Fore, Back, Style

class ColorStr(str):
    def __init__(self, string):
        """
        String that support coloration
        Args:
            string (str): String value
        """
        super().__init__()
        self.value = string

        # Funcionalities of Fore (colorama)
        self.ForeBLACK = f"{Fore.BLACK}{self.value}{Fore.RESET}"
        self.ForeRED = f"{Fore.RED}{self.value}{Fore.RESET}"
        self.ForeGREEN = f"{Fore.GREEN}{self.value}{Fore.RESET}"
        self.ForeYELLOW = f"{Fore.YELLOW}{self.value}{Fore.RESET}"
        self.ForeMAGENTA = f"{Fore.MAGENTA}{self.value}{Fore.RESET}"
        self.ForeCYAN = f"{Fore.CYAN}{self.value}{Fore.RESET}"
        self.ForeWHITE = f"{Fore.WHITE}{self.value}{Fore.RESET}"

        # Funcionalities of Fore (colorama)
        self.BackBLACK = f"{Back.BLACK}{self.value}{Back.RESET}"
        self.BackRED = f"{Back.RED}{self.value}{Back.RESET}"
        self.BackGREEN = f"{Back.GREEN}{self.value}{Back.RESET}"
        self.BackYELLOW = f"{Back.YELLOW}{self.value}{Back.RESET}"
        self.BackMAGENTA = f"{Back.MAGENTA}{self.value}{Back.RESET}"
        self.BackCYAN = f"{Back.CYAN}{self.value}{Back.RESET}"
        self.BackWHITE = f"{Back.WHITE}{self.value}{Back.RESET}"


        # Functionalities of Style (colorama)
        self.StyleDIM = f"{Style.DIM}{self.value}{Style.RESET_ALL}"
        self.StyleNORMAL = f"{Style.NORMAL}{self.value}{Style.RESET_ALL}"
        self.StyleBRIGHT = f"{Style.BRIGHT}{self.value}{Style.RESET_ALL}"

        def __repr__(self):
            return self.value


    # Fore(colorama) Functions to permit anidation of syles

    @staticmethod
    def ForeBLACK(string):
        return ColorStr(f"{Fore.BLACK}{string}{Fore.RESET}")

    @staticmethod
    def ForeRED(string):
        return ColorStr(f"{Fore.RED}{string}{Fore.RESET}")

    @staticmethod
    def ForeGREEN(string):
        return ColorStr(f"{Fore.GREEN}{string}{Fore.RESET}")

    @staticmethod
    def ForeYELLOW(string):
        return ColorStr(f"{Fore.YELLOW}{string}{Fore.RESET}")

    @staticmethod
    def ForeMAGENTA(string):
        return ColorStr(f"{Fore.MAGENTA}{string}{Fore.RESET}")

    @staticmethod
    def ForeCYAN(string):
        return ColorStr(f"{Fore.CYAN}{string}{Fore.RESET}")

    @staticmethod
    def ForeWHITE(string):
        return ColorStr(f"{Fore.WHITE}{string}{Fore.RESET}")


    # Black(colorama) Functions to permit anidation of syles
    @staticmethod
    def BackBLACK(string):
        return ColorStr(f"{Back.BLACK}{string}{Back.RESET}")

    @staticmethod
    def BackRED(string):
        return ColorStr(f"{Back.RED}{string}{Back.RESET}")

    @staticmethod
    def BackGREEN(string):
        return ColorStr(f"{Back.GREEN}{string}{Back.RESET}")

    @staticmethod
    def BackYELLOW(string):
        return ColorStr(f"{Back.YELLOW}{string}{Back.RESET}")

    @staticmethod
    def BackMAGENTA(string):
        return ColorStr(f"{Back.MAGENTA}{string}{Back.RESET}")

    @staticmethod
    def BackCYAN(string):
        return ColorStr(f"{Back.CYAN}{string}{Back.RESET}")

    @staticmethod
    def BackWHITE(string):
        return ColorStr(f"{Back.WHITE}{string}{Back.RESET}")


    # Style(colorama) Functions to permit anidation of syles

    @staticmethod
    def StyleDIM(string):
        return ColorStr(f"{Style.DIM}{string}{Style.RESET_ALL}")

    @staticmethod
    def StyleNORMAL(string):
        return ColorStr(f"{Style.NORMAL}{string}{Style.RESET_ALL}")

    @staticmethod
    def StyleBRIGHT(string):
        return ColorStr(f"{Style.BRIGHT}{string}{Style.RESET_ALL}")
