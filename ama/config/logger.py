#!/usr/bin/env python3

import logging
from cmd2 import Cmd

class Logger(logging.Logger):
    def __init__(self, name, filelog, formatlog, level=logging.WARNING):
        super().__init__(name, level)
        self.filelog = filelog
        self.formatlog = formatlog
        self.setLevel(level)
        self.level = level

    def add_handler(self, handler_type, formatlog=None, level=None, filelog:str=None):
        try:
            if handler_type is logging.StreamHandler:
                handler = logging.StreamHandler()
            elif handler_type is logging.FileHandler:
                if filelog:
                    handler = logging.FileHandler(filelog)
                else:
                    handler = logging.FileHandler(self.filelog)
            else:
                raise Exception("Unsupported handler type")

            if level:
                handler.setLevel(level)
            else:
                handler.setLevel(self.level)

            if formatlog:
                formatter = logging.Formatter(formatlog)
                handler.setFormatter(formatter)
            else:
                formatter = logging.Formatter(self.formatlog)
                handler.setFormatter(formatter)

            self.addHandler(handler)
        except Exception as error:
            print(error)
            #Cmd.pexcept(error)
