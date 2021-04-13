#!/usr/bin/env python3

from .path import Path

def line_counter(file_name: Path):
    count = sum(1 for line in open(file_name))
    return count
