#!/usr/bin/env python3
#
# Script to automatize hpc dependencies (pmix, munge, slurm)
#
# Maintainer: glozanoa <glozanoa@uni.pe>


from munge import Munge
from slurm import Slurm
from pmix import Pmix

def install_hpc_depends():
    munge_pkg = Munge(
        source="https://github.com/dun/munge/archive/refs/tags/munge-0.5.14.tar.gz",
        pkgver="0.5.14"
    )

    slurm_pkg = Slurm(
        source="https://download.schedmd.com/slurm/slurm-20.11.7.tar.bz2",
        pkver="20.11.7"
    )

    pmix_pkg = Pmix(
        source="https://github.com/openpmix/openpmix/releases/download/v3.2.3/pmix-3.2.3.tar.gz",
        pkver="3.2.3"
    )

    hpc_depends = [munge_pkg, pmix_pkg, slurm_pkg] # order is important


    for hpc_pkg in hpc_depends:
        hpc_pkg.doall()

if __name__=="__main__":
    install_hpc_depends()
