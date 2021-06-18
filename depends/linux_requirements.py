#!/usr/bin/env python3
#
# Install GNU/Linux packages needed to install cluster's packages
#
# Status: TESTED DISTRIBUTIONS = (centos 8, )
#
#
# Maintainer: glozanoa <glozanoa@uni.pe>


from sbash import Bash
from fineprint.status import print_status

requirements = {
    'centos':{
        "munge": ["openssl-devel.x86_64", "libevent-devel.x86_64", "zlib-devel.x86_64"],
        "pdsh": ["libssh.x86_64"],
        "pmix": ["libevent-devel.x86_64", "zlib-devel.x86_64"],
        "slurm": ["gtk2-devel.x86_64", "pam-devel.x86_64"]
    },

    'kali':{
        'munge': ['libevent-dev','libssl-dev'],
        'pdsh': [],
        'pmix': ['zlib1g-dev'],
        'slurm': [] # add package
    },

    'ubuntu':{
        'munge': ['libevent-dev','libssl-dev'],
        'pdsh': [],
        'pmix': ['zlib1g-dev'],
        'slurm': [] # add package
    },
    'arch':{
        "munge": ['openssl', 'libevent', 'zlib'],
        "pdsh": ['libssh'],
        "pmix": ['libevent', 'zlib'],
        "slurm": ['gtk2','pam']
    },
}

build_requirements = {
    'centos':{
        'group': ["'Development Tools'"],
        'package': ['make.x86_64', 'wget.x86_64']
    },
    'kali':{
        'package': ['python3-venv'] #add autoconf package
    },
    'ubuntu':{
        'package': ['python3-venv'] #add autoconf package
    },
    'arch':{
        'package': ['base-devel', 'wget']
    }
}

def install_requirements(distro_id):
    #import pdb; pdb.set_trace()
    print_status("Installing build requirements")
    for requirement_type, require in build_requirements[distro_id].items():
        if require:
            if requirement_type == "group":
                if distro_id == "centos":
                    Bash.exec(f"sudo yum -y group install {' '.join(require)}")

            elif requirement_type == "package":
                if distro_id == "centos":
                    Bash.exec(f"sudo yum -y install {' '.join(require)}")

                elif distro_id in ["kali", "ubuntu"]:
                    Bash.exec(f"sudo apt -y install {' '.join(require)}")

                elif distro_id == "arch":
                    Bash.exec(f"sudo pacman -S {' '.join(require)} --noconfirm")


    print_status("Installing package requirements")
    for pkg, require in requirements[distro_id].items():
        if require:
            print_status(f"Installing {pkg}'s {distro_id} dependencies")
            if distro_id == "centos":
                Bash.exec(f"sudo yum -y install {' '.join(require)}")
            elif distro_id in ["kali", "ubuntu"]:
                Bash.exec(f"sudo apt -y install {' '.join(require)}")
            elif distro_id == "arch":
                Bash.exec(f"sudo pacman -S {' '.join(require)} --noconfirm")
