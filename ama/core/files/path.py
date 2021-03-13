#!/usr/bin/env python3
#
# class to check properties of files and directories paths
#
# date: feb 22 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import os

# cmd2 imports
import cmd2

# fineprint imports
from fineprint.status import (
    print_status,
    print_failure
)

class Path:
    @staticmethod
    def access(permissions=[], *paths):
        """
        Check if each path in paths have the permissions from permissions list
        Return True if all the paths have the necesary permissions otherwise return false
        """

        #import pdb; pdb.set_trace()
        permissionCheck = True # True: all the paths have the necesary permissions
        exist_all = True

        no_exist_files = []
        invalidPermission = {'read': [], 'write':[], 'execution':[]}
        for permission in permissions:
            for path in paths:
                if (path is not None) and os.path.exists(path):
                    if not os.access(path, permission):
                        if permission == os.R_OK:
                            cmd2.Cmd.pwarning(f"{path} haven't read permission")
                            permissionCheck = False
                            invalidPermission['read'].append(path)

                        elif permission == os.W_OK:
                            cmd2.Cmd.pwarning(f"{path} haven't write permission")
                            permissionCheck = False
                            invalidPermission['write'].append(path)

                        elif permission == os.X_OK:
                            #cmd2.Cmd.pwarning(f"{path} haven't execution permission")
                            print_failure(f"{path} haven't execution permission")
                            permissionCheck = False
                            invalidPermission['execution'].append(path)
                else:
                    if path:
                        #cmd2.Cmd.pwarning(f"{path} path doesn't exist")
                        print_failure(f"{path} path doesn't exist")
                        exist_all = False
                        no_exist_files.append(path)

                    else: #path = None
                        #cmd2.Cmd.pwarning(f"No path supplied (path:None)")
                        print_failure(f"No path supplied (path:None)")

        if not permissionCheck:
            raise PermissionError(f"Permission Error: {invalidPermission}")

        if not exist_all:
            raise FileNotFoundError(f"Files that don't exist: {no_exist_files}")
