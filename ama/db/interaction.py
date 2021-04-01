#!/usr/bin/env python3
#
# interaction with ama database
#
# Date: Feb 18 2021
# Maintainer: glozanoa <glozanoa@uni.pe>


import os
import json
import psycopg2

from ama.config import AMA_HOME
from ama.core.files import Path
from ama.core.modules.auxiliary.hashes.hashes_status import HashesStatus

from fineprint.status import print_failure

def dbCreds(dbconfig: Path):
    dbconfig_file = Path(dbconfig)
    dbconfig_file = dbconfig_file.expanduser()
    permission = [os.R_OK]
    Path.access(permission, dbconfig_file)

    db_credentials = None
    with open(dbconfig_file, 'r') as credentials_json:
        db_credentials = json.load(credentials_json)

    return db_credentials

def insert_hashes(hashes_file: Path, workspace: str, creds_file: Path):
    cur = db_conn = None
    try:
        import pdb;pdb.set_trace()
        hashesStatus = HashesStatus(hashes_file=hashes_file)
        hashes_status = hashesStatus.run(quiet=True)
        cracked_hashes = hashes_status['cracked']

        db_credentials = dbCreds(creds_file)
        db_conn = psycopg2.connect(**db_credentials)

        insert_cracked_hash = (
            f"""
            INSERT INTO hashes_{workspace} (hash, type, cracker, password)
            VALUES (%s, %s, %s, %s)
            """
        )

        cur = db_conn.cursor()
        cur.executemany(insert_cracked_hash, cracked_hashes)
        db_conn.commit()
        cur.close()

    except Exception as error:
        print_failure(error)

    finally:
        if cur is not None:
            cur.close()

        if db_conn is not None:
            db_conn.close()
