#!/usr/bin/env python3

from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
import re

from fineprint.status import print_status, print_successful, print_failure


import os

class Status(Controller):
    class Meta:
        label='status'
    
    @ex(
        help="Check if a hash was cracked",
        arguments=[
            (['-s','--hash'],
            {'help':'hash to check status',
             'action':'store'}
            ),
            (['-f','--hashFile'],
            {'help':'hash file to check status',
             'action':'store'})
        ]
    )
    def status(self):
        """
            Check status of the hash (it is cracked or no)
            It hash is cracked when it is in the ~/.john/john.pot file
            otherwise it isn't cracked
        """
        if self.app.pargs.hash:
            hash = self.app.pargs.hash
            crackedPattern = re.compile(rf"(\w|\W|\s)*{hash}(\w|\W|\s)*")
            homeUser = os.path.expanduser("~")
            johnPotPath = os.path.join(homeUser, ".john/john.pot")
            with open(johnPotPath, 'r') as johnPotFile:
                while   crackedHash := johnPotFile.readline().rstrip():
                    if(crackedPattern.fullmatch(crackedHash)):
                        print_successful(f"{hash} hash was cracked")
                        break
            print_failure(f"{hash} hash wans't cracked")
        
        elif self.app.pargs.hashFile:
            pass #write me
        else:
            print_failure("No hash supplied to check status.")