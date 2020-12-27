#!/usr/bin/env python3

from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
#from ..core.mattack import MaskAttack
from ..core.jtrhash import jtr_hashes
import re


from fineprint.status import print_status, print_successful, print_failure

class Search(Controller):
    class Meta:
        label='search'
        sensitive=False #no sensitive search

    @ex(
        help="Search by a hash format",
        arguments=[
            (["pattern"],
            {'help':'Search an hash with a pattern',
             'action':'store'}),
            (["--jtr"],
            {'help':'Search a john the ripper hash',
             'action':'store_true'}),
            (["--hc"],
            {'help':'Search a hashcat hash',
             'action':'store_true'})
        ]
    )
    def search(self):
        print("Running search subcommand")
        print(f"pattern: {self.app.pargs.pattern}")
        if self.app.pargs.pattern:
            pattern = self.app.pargs.pattern
            if not self.Meta.sensitive:
                hashPattern = re.compile(rf"\w*{pattern}\w*", re.IGNORECASE)
            else:
                hashPattern = re.compile(rf"\w*{pattern}\w*")
                
            print_status(f"Posible hashes(Pattern: *{pattern}*):")
            if self.app.pargs.jtr:
                for hashFormat in jtr_hashes:
                    if hashPattern.search(hashFormat):
                        print_successful(hashFormat)
            elif self.app.pargs.hc:
                pass    # search for an hash of hashcat
        else:
            print_failure("No pattern given.")