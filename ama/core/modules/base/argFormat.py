#!/usr/bin/env python3
#
# argument format supplied to ama modules (attack and auxiliary)
#
# date: Feb 24 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from collections import namedtuple

Argument = namedtuple('Argument', ['value', 'required', 'description'])
