#!/usr/bin/env python3

import logging

class Logger(Logging.Logger):
    def __init__(self, name, filelog, level=logging.WARNING, formatlog:None):
        super().__init__(name, level)
        self.filelog = filelog
        self.formatlog = formatlog
        self.setLevel(level)
        self.level = level

    def add_handler(handler_type, formatlog=None, level=None, filelog:str=None):
        if isinstance(handler_type, logging.StreamHandler):
            handler = logging.StreamHandler()
        elif isinstance(handler_type, logging.FileHandler):
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
            handler.setFormatter(self.formatter)

        self.addHandler(handler)
