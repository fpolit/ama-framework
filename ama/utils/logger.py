#!/usr/bin/env python3

import logging
from cmd2 import Cmd

class Logger(logging.Logger):
    def __init__(self, name, logfile, logformat, level=logging.WARNING):
        super().__init__(name, level)
        self.logfile = logfile
        self.logformat = logformat
        self.setLevel(level)
        self.level = level

    def add_handler(self, handler_type, logformat=None, level=None, logfile:str=None):
        try:
            if handler_type is logging.StreamHandler:
                handler = logging.StreamHandler()
            elif handler_type is logging.FileHandler:
                if logfile:
                    handler = logging.FileHandler(logfile)
                else:
                    handler = logging.FileHandler(self.logfile)
            else:
                raise Exception("Unsupported handler type")

            if level:
                handler.setLevel(level)
            else:
                handler.setLevel(self.level)

            if logformat:
                formatter = logging.Formatter(logformat)
                handler.setFormatter(formatter)
            else:
                formatter = logging.Formatter(self.logformat)
                handler.setFormatter(formatter)

            self.addHandler(handler)

        except Exception as error:
            print(error)
            #Cmd.pexcept(error)
