#!/usr/bin/env python3
#
# Shell class to execute shell commands
#
# Status:
#
# Maintainer: glozanoa <glozanoa@uni.pe>


import sys
import shlex
from subprocess import Popen


class Shell:
    @staticmethod
    def exec(cmd, *args, **kwargs):
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)

        kwargs['stdout'] = sys.stdout
        kwargs['stderr'] = sys.stdout
        proc = Popen(cmd, *args, **kwargs)
        proc.wait()

        return proc
