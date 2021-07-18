#!/usr/bin/env python3
#
# RedirectOutput class to redirect stdout to a file
#
# Status:
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import sys

class RedirectOutput:
    def __init__(self, filename, mode='w'):
        self.filename = filename
        self.mode = mode
        self.stdout = sys.stdout
        self.outfile = None

    def __enter__(self):
        self.outfile = open(self.filename, self.mode)
        sys.stdout = self.outfile

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        sys.stdout = self.stdout
        if self.outfile:
            self.outfile.close()
