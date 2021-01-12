#!/usr/bin/env python3

class NoArgumentProvided(Exception):
    def __init__(self):
        self.warningMsg = f"No Arguments Provided"
        super().__init__(self.warningMsg)
