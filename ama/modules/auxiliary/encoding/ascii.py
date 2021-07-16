#!/usr/bin/env python3
#
# Ascii encoding
#
# State:
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from password_generator import PasswordGenerator as RandomPasswordGenerator
import string

from ama.modules.base import Auxiliary

from ama.utils import Argument
from ama.utils.color import ColorStr
from ama.utils.fineprint import (
    print_failure,
    print_status,
    print_successful
)

class AsciiEncoding(Auxiliary):
    """
    Ascii encoding
    """
    DESCRIPTION = "Ascii encoding"
    MNAME = "auxiliary/encoding/ascii"
    MTYPE, MSUBTYPE, NAME = MNAME.split("/")
    AUTHORS = [
        "glozanoa <glozanoa@uni.pe>"
    ]

    FULLDESCRIPTION = (
        """

        """
    )

    REFERENCES = [
        "https://en.wikipedia.org/wiki/Binary-to-text_encoding"
    ]

    def __init__(self, text:str):

        auxiliary_options = {
            'TEXT': Argument(text, True, "Text to encode"),
            'JOB_NAME': Argument('encoding-%j', True, "Job name"),
            'ROUTPUT': Argument('ama-%j.out', True, "Redirection output file")
        }

        init_options = {
            'mname': AsciiEncoding.MNAME,
            'authors': AsciiEncoding.AUTHORS,
            'description': AsciiEncoding.DESCRIPTION,
            'fulldescription': AsciiEncoding.FULLDESCRIPTION,
            'references': AsciiEncoding.REFERENCES,
            'auxiliary_options': auxiliary_options
        }

        super().__init__(**init_options)

    def run(self, quiet=False):
        """
        Ascii encoding
        """
        #import pdb; pdb.set_trace()
        try:

            text = self.options['TEXT'].value

            encode_text = text.encode(encoding='ascii')

            print("[*] Encode text: {encode_text}")

            return encode_text


        except Exception as error:
            print(error) # print_failure
