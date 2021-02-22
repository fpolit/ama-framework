#!/usr/bin/env python3
#
# Database Exception to manage connection errors generated in interelations with ama-framework db
#
# date: Feb 20 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

from psycopg2 import DatabaseError


class WorkspaceExistsError(DatabaseError):
    """
    No workspace name in workspaces table
    """
    def __init__(self, workspace):
        self.warning = f"No {workspace} workspace in workspaces table"
        super().__init__(self.warning)
