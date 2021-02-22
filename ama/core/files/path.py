#!/usr/bin/env python3
#
# class to check properties of files and directories paths
#
# date: feb 22 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import os

# cmd2 imports
import cmd2

class Path:
    @staticmethod
    def access(permissions=[], *paths):
        """
        Check if each path in paths have the permissions from permissions list
        Return True if all the paths have the necesary permissions otherwise return false
        """
        permissionCheck = True # True: all the paths have the necesary permissions
        invalidPermission = {'read': [], 'write':[], 'execution':[]}
        for permission in permissions:
            for path in paths:
                if os.path.exists(path):
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
                            cmd2.Cmd.pwarning(f"{path} haven't execution permission")
                            permissionCheck = False
                            invalidPermission['execution'].append(path)
                else:
                    cmd2.Cmd.pwarning(f"{path} path doesn't exist")
                    permissionCheck = False

        if not permissionCheck:
            raise PermissionError(f"Permission Error: {**invalidPermission}")

        return permissionCheck
