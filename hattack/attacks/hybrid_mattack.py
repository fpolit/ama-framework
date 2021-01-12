#!/usr/bin/env python3

from mpi4py import MPI
from .core import MaskAttack
from sbash.core import Bash



def readBlock(maskFile, blockSize):
    masks = [maskFile.readline().rstrip() for k in range(blockSize)]
    return masks

def isCracked(vstatus):
    """
        vstatus: vector status (True: cracked, False: uncracked) (of each processor)
    """
    for cracked in vstatus:
        if cracked:
            return True
    return False

def hybridAttack(maskFile, hashType, hashFile):

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        N=10    # number of mask for each processor
        with open(maskFile, 'r') as masks:
            cracked = [False]*size  # hash is uncracked (for all the processors)
            while masks := readBlock(masks, N*size):
                cracked = comm.gather()
                if not cracked: # hash is uncracked
                    pass
    else:
        masks = comm.recv(source=0, tag=1) # we use tag=1 to send masks and tag=10 to send the status of the processors (True)
        for mask in masks:
            mask_attack = f"hashcat -a 3 -m {hashType} {hashFile} {mask}"
            Bash.exec(mask_attack)
        
        comm.send()



