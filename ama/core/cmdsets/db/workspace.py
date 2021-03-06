#!/usr/bin/env python3
#
# database commands set from ama-framework (Database Commands Category)
#
#
# debug - date: Feb 27 2021
#
# debugged functions:
# do_workspace, existWorkspace, exist,
# switch, init, delete, deleteall, rename
#
#
# date: Feb 21 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import argparse
from tabulate import tabulate

#fineprint imports
from fineprint.status import (
    print_failure,
    print_status,
    print_successful
)

from fineprint.color import ColorStr

# import db connection modules
from getpass import getpass
import psycopg2

# version import
from ama.core.version import get_version

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
from ama.core.validator import Answer

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

    #debugged - date: Feb 27 2021
    @with_argparser(workspace_parser)
    def do_workspace(self, args):
        """
        Manager of ama-framework workspaces
        """
        if self._cmd.db_conn is None:
            #cmd2.Cmd.pwarning("Database not connected")
            print_failure("Database not connected")
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
                self._cmd.workspace = Workspace.delete(deleteWorkspce, self._cmd.workspace,
                                                       **self._cmd.db_creds)

            elif args.deleteall:
                Workspace.deleteall(**self._cmd.db_creds)
                self._cmd.workspace = "default"

            elif args.rename:
                oldWorkspace = args.rename[0]
                newWorkspace = args.rename[1]
                Workspace.rename(oldWorkspace, newWorkspace, **self._cmd.db_creds)

            else: #show the availables workspaces
                try:
                    cur = self._cmd.db_conn.cursor()
                    cur.execute("SELECT name FROM workspaces")
                    self._cmd.db_conn.commit()

                    workspaces = []
                    for workspace, *_ in cur.fetchall():
                        if workspace == self._cmd.workspace:
                            selectedWorkspace = ColorStr(f"{workspace}*").ForeRED
                            workspaces.append([selectedWorkspace])
                        else:
                            workspaces.append([workspace])

                    print(tabulate(workspaces, headers=["Workspace"]))
                    cur.close()

                except Exception as error:
                    print_failure(error)

    #debugged - date: Feb 27 2021
    @staticmethod
    def existWorkspace(workspace=None, *, database="ama", user="attacker", host='localhost', password=None):
        """
        Check if a workspace exist or not
        """

        #import pdb; pdb.set_trace()

        if workspace:
            cur = None
            dbCredential = {'database': database, 'user': user, 'host': host, 'password': password}
            conn = None
            try:
                conn = psycopg2.connect(**dbCredential)
                cur = conn.cursor()

                cur.execute("SELECT name FROM workspaces")
                conn.commit()

                for workspaceName, *_ in cur.fetchall():
                    if workspaceName == workspace:
                        return True
                return False

            except (Exception, psycopg2.DatabaseError) as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)
                return False

            finally:
                if cur is not None:
                    cur.close()
                if conn is not None:
                    conn.close()
                    del dbCredential

        else:
            #cmd2.Cmd.pwarning("No workspace selected")
            print_failure("No workspace selected")
            return False

    #debugged - date: Feb 27 2021
    def exist(self, workspace=None):
        """
        Check if a workspace exist or not

        Return:
          return True if workspace exist otherwise return False
        """
        #import pdb; pdb.set_trace()
        if workspace:
            cur = None
            try:
                # checking if switch workspace exist
                cur = self._cmd.db_conn.cursor()
                cur.execute("SELECT name FROM workspaces")
                self._cmd.db_conn.commit()

                for workspaceName, *_ in cur.fetchall():
                    if workspaceName == workspace:
                        return True
                return False

            except (Exception, psycopg2.DatabaseError) as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)
                return False #check if this return work or if it's useless

            finally:
                if cur is not None:
                    cur.close()
        else:
            #cmd2.Cmd.pwarning("No workspace selected")
            print_failure("No workspace selected")
            return False

    #debugged - date: Feb 27 2021
    def switch(self, workspace=None):
        """
        Switch between workspaces
        """
        #import pdb; pdb.set_trace()
        if workspace:
            try:
                if self.exist(workspace):
                    self._cmd.workspace = workspace
                else:
                    raise WorkspaceExistsError(workspace)

                #self._cmd.workspace = switchWorkspace
                #cmd2.Cmd.poutput(f"Workspace: {switchWorkspace}")
                print_status(f"Current workspace: {workspace}")

            except (Exception, psycopg2.DatabaseError) as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)
        else:
            #cmd2.Cmd.pwarning("No workspace selected")
            print_failure("No workspace selected")

    #debugged - date: Feb 27 2021
    @staticmethod
    def init(workspace=None, *, database="ama", user="attacker", host='localhost', password=None):
        """
        Workspace initialization (creation of hash and service tables)
        """
        #import pdb; pdb.set_trace()
        if not password:
            password = getpass(prompt=f"Password of {user} role: ")

        dbCredential = {'host': host, 'database': database, 'user': user, 'password': password}

        cmdsTables = (
            f"""
            CREATE TABLE IF NOT EXISTS hashes_{workspace} (
            hash VARCHAR (100) UNIQUE NOT NULL,
            type VARCHAR (20),
            cracker VARCHAR (20) NOT NULL,
            password VARCHAR (32) NOT NULL
            )
            """,

            f"""
            CREATE TABLE IF NOT EXISTS services_{workspace} (
            service VARCHAR (20) NOT NULL,
            target VARCHAR (15) NOT NULL,
            service_user VARCHAR (20) NOT NULL,
            password VARCHAR (32) NOT NULL
            )
            """
        )

        valueInsert = (
                """
                INSERT INTO workspaces (name)
                VALUES (%s);
                """
            )


        conn = None
        cur = None
        try:
            conn = psycopg2.connect(**dbCredential)
            cur = conn.cursor()

            for cmd in cmdsTables:
                cur.execute(cmd)

            conn.commit()

            # adding new workspace to workspaces table in database
            cur.execute(valueInsert, (workspace ,))
            conn.commit()
            cur.close()
            #cmd2.Cmd.poutput(f"Added workspace: {workspace}")
            print_successful(f"Added workspace: {workspace}")

        except (Exception, psycopg2.DatabaseError) as error:
            #cmd2.Cmd.pexcept(error)
            print_failure(error)

        finally:
            if cur is not None:
                cur.close()

            if conn is not None:
                conn.close()

    #debugged - date: Feb 27 2021
    @staticmethod
    def delete(workspace=None, selectedWorkspace=None, *, database="ama", user="attacker", host='localhost'):
        """
        Delete a workspace and return the name of workspace in use
        """
        #import pdb; pdb.set_trace()
        password = getpass(prompt=f"Password of {user} role: ")
        dbCredential = {'host': host, 'database': database, 'user': user, 'password': password}

        if Workspace.existWorkspace(workspace, **dbCredential):
            conn = None
            cur = None
            try:
                if workspace == selectedWorkspace: # workspace is in current use
                    forceDelete = Answer.shortAnwser(f"Workspace {workspace} is in current use. Do you want to delete it(y/n)? ") # y: True and n: False
                    if not forceDelete:
                        print_status("Be carefully you can lose your data")
                        return selectedWorkspace

                conn = psycopg2.connect(**dbCredential)
                cur = conn.cursor()
                workspace_tables = ["hashes", "services"]
                for table in workspace_tables:
                    cur.execute(f"DROP TABLE IF EXISTS {table}_{workspace}")

                #delete workspace name from workspaces table
                deleteWorkspace = (
                    f"""
                    DELETE FROM workspaces
                    WHERE name = '{workspace}'
                    """
                )
                cur.execute(deleteWorkspace, (workspace, ))
                conn.commit()
                #cmd2.Cmd.poutput(f"Workspace {workspace} was deleted")
                print_status(f"Workspace {workspace} was deleted")

                defaultWorkspace = "default"

                if workspace == selectedWorkspace:
                    print_status(f"Current workspace: {defaultWorkspace}")

                if workspace == defaultWorkspace:
                    Workspace.init(workspace, **dbCredential)
                    return workspace

                else:
                    if not Workspace.existWorkspace(defaultWorkspace, **dbCredential):
                        Workspace.init(defaultWorkspace, **dbCredential)
                    return defaultWorkspace

            except (Exception, psycopg2.DatabaseError) as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)

            finally:
                if cur is not None:
                    cur.close()

                if conn is not None:
                    conn.close()

        else:
            #cmd2.Cmd.pwarning(f"Workspace {workspace} doesn't exist")
            print_failure(f"Workspace {workspace} doesn't exist")

    #debugged - date: Feb 27 2021
    @staticmethod
    def deleteall(*, database="ama", user="attacker", host='localhost'):
        """
        Delete all workspaces from workspaces table
        """
        #import pdb; pdb.set_trace()

        delete = Answer.shortAnwser("Do you want to delete all your workspaces(y/n)? ")
        if delete:
            password = getpass(prompt=f"Password of {user} role: ")
            dbCredential = {'host': host, 'database': database, 'user': user, 'password': password}

            conn = None
            cur = None
            try:
                conn = psycopg2.connect(**dbCredential)
                cur = conn.cursor()

                cur.execute("SELECT name FROM workspaces")
                conn.commit()

                workspaces =  cur.fetchall()
                workspace_tables = ["hashes", "services"]
                for workspace, *_  in workspaces:
                    for table in workspace_tables:
                        cur.execute(f"DROP TABLE IF EXISTS {table}_{workspace}")

                    #delete workspace name from workspaces table
                    deleteWorkspace = (
                        f"""
                        DELETE FROM workspaces
                        WHERE name = '{workspace}'
                        """
                    )
                    cur.execute(deleteWorkspace, (workspace, ))
                    conn.commit()

                print_status(f"Workspaces were deleted")

                defaultWorkspace = "default"
                Workspace.init(defaultWorkspace, **dbCredential)

            except (Exception, psycopg2.DatabaseError) as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)

            finally:
                if cur is not None:
                    cur.close()

                if conn is not None:
                    conn.close()

        else:
            #cmd2.Cmd.poutput("Be carefully you could lose all your data.")
            print_status("Be carefully you could lose all your data.")

    #debugged - date: Feb 27 2021
    @staticmethod
    def rename(oldWorkspace, newWorkspace, *, database="ama", user="attacker", host='localhost'):
        """
        Rename a workspace
        """
        import pdb; pdb.set_trace()
        password = getpass(prompt=f"Password of {user} role: ")
        dbCredential = {'host': host, 'database': database, 'user': user, 'password': password}
        if Workspace.existWorkspace(oldWorkspace, **dbCredential):
            conn = None
            cur = None
            try:
                conn = psycopg2.connect(**dbCredential)
                cur = conn.cursor()
                renameWorkspace = \
                    f"""
                    UPDATE workspaces
                    SET name = '{newWorkspace}'
                    WHERE name = '{oldWorkspace}'
                    """
                cur.execute(renameWorkspace, (newWorkspace, oldWorkspace, ))
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
                    cur.execute(renameTable, (newWorkspace, oldWorkspace, ))
                    conn.commit()

                cur.close()
                #cmd2.Cmd.poutput(f"Workspace {oldWorkspace} rename to {newWorkspace}")
                print_status(f"Workspace {oldWorkspace} rename to {newWorkspace}")

            except (Exception, psycopg2.DatabaseError) as error:
                #cmd2.Cmd.pexcept(error)
                print_failure(error)

            finally:
                if cur is not None:
                    cur.close()

                if conn is not None:
                    conn.close()

        else:
            #cmd2.Cmd.pwarning(f"Workspace {oldWorkspace} doesn't exist")
            print_failure(f"Workspace {oldWorkspace} doesn't exist")

