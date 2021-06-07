#!/usr/bin/env python3
#
# Install CentOS packages needed to install cluster's packages

from sbash import Bash
from fineprint.status import print_status

if __name__=="__main__":

    requirements = {
        "munge": ["openssl-devel.x86_64", "libevent-devel.x86_64", "zlib-devel.x86_64", "make.x86_64", "wget.x86_64"],
        "pdsh": ["libssh.x86_64",  "make.x86_64", "wget.x86_64"],
        "pmix": ["libevent-devel.x86_64", "zlib-devel.x86_64",  "make.x86_64", "wget.x86_64"],
        "slurm": ["gtk2-devel.x86_64", "pam-devel.x86_64", "make.x86_64", "wget.x86_64"]
    }
    
    for pkg, require in requirements.items():
        print_status(f"Installing {pkg}'s CentOS dependencies")
        #import pdb; pdb.set_trace()
        yum_install_cmd = "sudo yum -y install " + " ".join(require)
        Bash.exec(yum_install_cmd)
