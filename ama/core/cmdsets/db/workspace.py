#!/usr/bin/env python3
#
# database commands set from ama-framework (Database Commands Category)
#
# date: Feb 21 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse

# import db connection modules
from getpass import getpass
import psycopg2

# version import
from ...version import get_version

# commandset categories
from ..category import CmdsetCategory as Category

# cmd2 imports
import cmd2
from cmd2 import (
    CommandSet,
    with_default_category,
    with_argparser
)

# db exceptions
from ama.db.exceptions import WorkspaceExistsError

# valiadator imports
from ...validator import Answer


@with_default_category(Category.DB)
class Workspace(CommandSet):
    """
    Database command set category related to workspace connection
    command sets: workspace
    """
    def __init__(self):
        super().__init__()

    workspace_parser = argparse.ArgumentParser()
    workspace_parser.add_argument('-s', '--switch',
                                  help='Switch workspace')
    workspace_parser.add_argument('-a', '--add',
                                  help='Add workspace')
    workspace_parser.add_argument('-as', dest='addswitch',
                                  help='Add workspace and switch to it')
    workspace_parser.add_argument('-d', '--delete',
                                  help='Delete workspace')
    workspace_parser.add_argument('-D', dest='deleteall', action='store_true',
                                  help='Delete all workspaces')
    workspace_parser.add_argument('-r', '--rename', nargs=2,
                                  help='Rename workspace')

    @with_argparser(workspace_parser)
    def do_workspace(self, args):
        """
        Manager of ama-framework workspaces
        """
        if self._cmd.db_conn is None:
            cmd2.Cmd.pwarning("Database not connected")
        else:
            if args.switch:
                switchWorkspace = args.switch
                self.switch(switchWorkspace)

            elif args.add or args.addswitch:
                newWorkspace = args.addswitch or args.add
                Workspace.init(newWorkspace, **self._cmd.db_creds)

                if args.addswitch:
                    self.switch(newWorkspace)

            elif args.delete:
                deleteWorkspce = args.delete
                Workspace.delete(deleteWorkspce, **self._cmd.db_creds)

            elif args.deleteall:
                Workspace.deleteall(**self._cmd.db_creds)

            elif args.rename:
                oldWorkspace = args.rename[0]
                newWorkspace = args.rename[1]
                Workspace.rename(oldWorkspace, newWorkspace, **self._cmd.db_creds)


    def existWorkspace(self, workspace=None):
        """
        Check if a workspace exist or not
        """
        if workspace:
            try:
                # checking if switch workspace exist
                cur = self._cmd.db_conn.cursor()
                cur.execute("SELECT name FROM workspaces")
                self._cmd.db_conn.commit()
                cur.close()

                if workspace in cur.fetchall():
                    return True
                else:
                    return False

            except (Exception, psycopg2.DatabaseError) as error:
                cmd2.Cmd.pexcept(error)
                return False #check if this return work or if it's useless
        else:
            cmd2.Cmd.pwarning("No workspace selected")
            return False

    @staticmethod
    def existWorkspace(workspace=None, *, database="ama", user="attacker", host='localhost', password=None):
        """
        Check if a workspace exist or not
        """
        if workspace:
            dbCredential = {'database': database, 'user': user, 'host': host, 'password': password}
            conn = None
            try:
                conn = psycopg2.connect(**dbCredential)
                cur = conn.cursor()

                cur.execute("SELECT name FROM workspaces")
                conn.commit()

                if workspace in cur.fetchall():
                    cur.close()
                    return True
                else:
                    cur.close()
                    return False

            except (Exception, psycopg2.DatabaseError) as error:
                cmd2.Cmd.pexcept(error)
                return False

            finally:
                if conn is not None:
                    conn.close()
                    del dbCredential

        else:
            cmd2.Cmd.pwarning("No workspace selected")
            return False

    def switch(self, workspace=None):
        """
        Switch between workspaces
        """
        if workspace:
            try:
                if self.existWorkspace(workspace):
                    self._cmd.workspace = workspace
                else:
                    raise WorkspaceExistsError(workspace)

                self._cmd.workspace = switchWorkspace
                cmd2.Cmd.poutput(f"Workspace: {switchWorkspace}")

            except (Exception, psycopg2.DatabaseError) as error:
                cmd2.Cmd.pexcept(error)
        else:
            cmd2.Cmd.pwarning("No workspace selected")

    @staticmethod
    def init(workspace=None, *, database="ama", user="attacker", host='localhost'):
        """
        Workspace initialization (creation of hash and service tables)
        """
        password = getpass(prompt=f"Password of {user} role: ")
        dbCredential = {'host': host, 'database': database, 'user': user, 'password': password}

        cmdsTables = (
            f"""
            CREATE TABLE IF NOT EXIST hashes_{workspace} (
            hash VARCHAR (100) UNIQUE NOT NULL,
            type VARCHAR (20),
            cracker VARCHAR (20) NOT NULL,
            password VARCHAR (32) NOT NULL
            )
            """,

            f"""
            CREATE TABLE IF NOT EXIST services_{workspace} (
            service VARCHAR (20) NOT NULL,
            target INET NOT NULL,
            user VARCHAR (20) NOT NULL,
            password VARCHAR (32) NOT NULL
            )
            """
        )

        conn = None
        try:
            conn = psycopg2.connect(**dbCredential)
            cur = conn.cursor()

            for cmd in cmdsTables:
                cur.execute(cmd)

            conn.commit()
            cur.close()
            cmd2.Cmd.poutput(f"Added workspace: {workspace}")

        except (Exception, psycopg2.DatabaseError) as error:
            cmd2.Cmd.pexcept(error)

        finally:
            if conn is not None:
                conn.close()

    @staticmethod
    def delete(workspace=None, *, database="ama", user="attacker", host='localhost'):
        """
        Delete a workspace
        """
        password = getpass(prompt=f"Password of {user} role: ")
        dbCredential = {'host': host, 'database': database, 'user': user, 'password': password}

        if Workspace.existWorkspace(workspace, **dbCredential):
            conn = None
            try:
                conn = psycopg2.connect(**dbCredential)
                cur = conn.cursor()
                workspace_tables = ["hashes", "services"]
                for table in workspace_tables:
                    cur.execute(f"DROP TABLE IF EXISTS table_{workspace}}")

                    #delete workspace name from workspaces table
                    deleteWorkspace = (
                        f"""
                        DROP FROM workspaces
                        WHERE name == {workspace}
                        """
                    )
                    cur.execute(deleteWorkspace)
                    conn.commit()
                    cur.close()
                    cmd2.Cmd.poutput(f"Workspace {workspace} was deleted")

            except (Exception, psycopg2.DatabaseError) as error:
                cmd2.Cmd.pexcept(error)
        else:
            cmd2.Cmd.pwarning(f"Workspace {workspace} doesn't exist")

    @staticmethod
    def deleteall(*, database="ama", user="attacker", host='localhost'):
        """
        Delete all workspaces from workspaces table
        """
        delete = Answer("Do you want to delete all your workspaces(y/n)? ")
        if delete:
            password = getpass(prompt=f"Password of {user} role: ")
            dbCredential = {'host': host, 'database': database, 'user': user, 'password': password}

            conn = None
            try:
                conn = psycopg2.connect(**dbCredential)
                cur = conn.cursor()

                cur.execute("SELECT name FROM workspaces")
                conn.commit()

                workspaces =  cur.fetchall()
                workspace_tables = ["hashes", "services"]
                for workspace  in workspaces:
                    for table in workspace_tables:
                        cur.execute(f"DROP TABLE IF EXISTS table_{workspace}}")

                    #delete workspace name from workspaces table
                    deleteWorkspace = (
                        f"""
                        DROP FROM workspaces
                        WHERE name == {workspace}
                        """
                    )
                    cur.execute(deleteWorkspace)
                    conn.commit()

                cur.close()
                cmd2.Cmd.poutput(f"Workspaces were deleted")

            except (Exception, psycopg2.DatabaseError) as error:
                cmd2.Cmd.pexcept(error)

        else:
            cmd2.Cmd.poutput("Be carefully you could lose all your data.")

    @staticmethod
    def rename(oldWorkspace, newWorkspace, *, database="ama", user="attacker", host='localhost'):
        """
        Rename a workspace
        """
        password = getpass(prompt=f"Password of {user} role: ")
        dbCredential = {'host': host, 'database': database, 'user': user, 'password': password}
        if Workspace.existWorkspace(oldWorkspace, **dbCredential):
            conn = None
            try:
                conn = psycopg2.connect(**dbCredential)
                cur = conn.cursor()
                renameWorkspace = \
                    f"""
                    UPDATE workspaces
                    SET name = {newWorkspace}
                    WHERE name == {oldworkspace}
                    """
                cur.execute(renameWorkspace)
                conn.commit()

                renameWorkspaceTables = (
                    f"""
                    ALTER TABLE hashes_{oldWorkspace}
                    RENAME TO hashes_{newWorkspace}
                    """,
                    f"""
                    ALTER TABLE services_{oldWorkspace}
                    RENAME TO services_{newWorkspace}
                    """
                )
                for renameTable in renameWorkspaceTables:
                    cur.execute(renameTable)
                    conn.commit()

                cur.close()
                cmd2.Cmd.poutput(f"Workspace {oldWorkspace} rename to {newWorkspace}")

            except (Exception, psycopg2.DatabaseError) as error:
                cmd2.Cmd.pexcept(error)

        else:
            cmd2.Cmd.pwarning(f"Workspace {oldWorkspace} doesn't exist")

