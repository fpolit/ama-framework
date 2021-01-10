#!/usr/bin/env python3

"""
# Hashcat class
# Jan 9 2021 - Implementation of Hashcat class
                (using core module of pyhashcat python package)
#
# Maintainer: glozanoa <glozanoa@uni.pe>
"""



import os
from os.path import dirname
from sbash.core import Bash
from fineprint.status import print_status, print_failure

# cracker modules
from .PasswordCracker import PasswordCracker
from ..hashes.hc import hashes

# base modules
from ..base.FilePath import FilePath

# importing PasswordCracker exceptions
from .PasswordCrackerExceptions import CrackerDisableError
from .PasswordCrackerExceptions import AttackModeError
from .PasswordCrackerExceptions import CrackerHashError

class Hashcat(PasswordCracker):
    hashes = hashes
    attackMode = {  0:"Wordlist",
                    1:"Combination",
                    3:"Mask Attack",
                    6:"Hybrid Wordlist + Mask",
                    7:"Hybrid Mask + Wordlist"}

    def __init__(self):
        super().__init__(name=['hashcat', 'hc'])


    @staticmethod
    def benchmark():
        cracker = Hashcat()
        if cracker.checkStatus():
            benchmark = f"{cracker.mainexec} -b"
            print_status(f"Running: {benchmark}")
            Bash.exec(benchmark)
        else:
            raise CrackerDisableError("Hashcat")

    @staticmethod
    def checkAttackMode(attack):
        if not (attack in Hashcat.attackMode):
            raise AttackModeError(attack)


    @staticmethod
    def checkHashType(hashType):
        """ Check if the hash type is correct

        Args:
            hashType (str): hash type

        Raises:
            HashcatHashError: Error if the given hash isn't a valid hash type
        """

        if not (hashType in Hashcat.hashes):
            raise HashcatHashError(hashType)


    # @staticmethod
    # def checkAttackArgs(*,
    #                     _hashType=None,
    #                     _hashFile,
    #                     _wordlist=None,
    #                     _maskFile=None):

    #     # validation of existence and read access of input file arguments
    #     for inputFile in [_hashFile, _wordlist, _maskFile]:
    #         if inputFile:
    #             inputFilePath = FilePath(inputFile)
    #             if not inputFilePath.checkReadAccess():
    #                 print_failure(f"No read permission in {inputFilePath} file")
    #                 raise PermissionError

    #     Hashcat.checkHashType(_hashType)


    @staticmethod
    def checkAttackArgs(*,
                        _hashType=None,
                        _hashFile=None,
                        _wordlist=None,
                        _maskFile=None):
        PasswordCracker.checkAttackArgs(__hashFile = _hashFile,
                                        __wordlist = _wordlist,
                                        __maskFile = _maskFile)

        Hashcat.checkHashType(_hashType)


    @staticmethod
    def selectAttack(*, 
                attackMode=None,
                hashType=None,
                hashFile=None, 
                wordlist=[],
                maskFile=None, 
                ):

        # contruction of hashcat cmd to execute
        Hashcat.checkAttackMode(attackMode)
        if attackMode == 0:   # wordlist attack
            Hashcat.checkAttackArgs(_hashType=hashType,
                                    _hashFile=hashFile,
                                    _wordlist=wordlist)
            hc = Hashcat()
            print_status(f"Attacking {hashFile} with {wordlist} in straigth mode.")
            cmd =   f"{hc.mainexec} -a {attackMode} -m {hashType} {hashFile} {wordlist}"

        elif attackMode==1: #combination attack

            # self._validate_args(_hash_type=hash_type, 
            #                     _hash_file=hash_file, 
            #                     _wordlist=wordlist)

            # if type(wordlist) is list:
            #     wordlists = shlex.join(wordlist)
            # else:
            #     wordlists = wordlist
                                
            # print_status(f"Attacking {hash_file} with {wordlists} in combinator mode.")
            # cmd = f"{self.mainexec} -a {attack_mode} -m {hash_type} {hash_file} {wordlists}"
            # cmd = shlex.split(cmd)

        elif attackMode == 3:   #mask attack
            pass

        elif attackMode == 6:   #hybrid attack (word + mask)

    
    
        ##adding --force flag to the command 
        if force:
            cmd.append("--force")
            
        return cmd

    

    # def crack(self, *, attack_mode=None, hash_type=None, hash_file=None, 
    #         wordlist=[], mask=None, mask_file=None, force=False, **kwargs):
    #     """[summary]

    #     Args:
    #         hash_type ([type], optional): [description]. Defaults to None.
    #         hash_file ([type], optional): [description]. Defaults to None.
    #         attack_mode ([type], optional): [description]. Defaults to None.
    #         wordlist ([type], optional): [description]. Defaults to None.
    #         force (bool, optional): [description]. Defaults to False.
            
    #     Raises:
    #         Exception: Hashcat Pluging Disable
    #     """     
        
    #     self._validate_status()
        
    #     #generate hashcat command
    #     cmd = self._gencmd(attack_mode=attack_mode,
    #                         hash_type=hash_type,
    #                         hash_file=hash_file,
    #                         wordlist=wordlist,
    #                         mask=mask,
    #                         mask_file=mask_file,
    #                         force=force)
    #     process = Popen(cmd, stdout=PIPE, stderr=PIPE, encoding='utf-8')
    #     pid = process.pid
    #     cp = CrackProcess(process=process, status="Running", cmd=cmd)
    #     self.process[pid] = cp
    #     print_status(f"Runing attack in process {pid}")

    
    # def show_attack_mode(self):
    #     title=f"{'#':>3} | {'Mode':>2}"
    #     print(title)
    #     print("-"*len(title))
    #     for attack_id , attack_info in self.attack_mode.items():
    #         print(f"{attack_id:>3} | {attack_info:>2}")
            
    # def search_hash(self, search=None, *, sensitive=False):
    #     if search:
    #         if not sensitive:
    #             hash_pattern = re.compile(rf"\w*{search}\w*", re.IGNORECASE)
    #         else:
    #             hash_pattern = re.compile(rf"\w*{search}\w*")
                
    #         posible_hashes = []
    #         for hash_id, hash_info in self.hash_hashcat.items():
    #             if hash_pattern.search(hash_info["Name"]):
    #                 posible_hashes.append({'#':hash_id, **hash_info})
            
    #         print_successful("Posible hashcat hashes.")
    #         print(tabulate(posible_hashes, headers="keys"))
    #     else:
    #         print_failure("No pattern given.")
              
    
    
    # def _update_all_process(self):
    #     for crack_process in self.process.values():
    #         crack_process.update_status()
    
    # def show_process(self):
        
    #     title = f"{'pid':>5} | {'status':>8} | {'cmd'}"
    #     print(title)
    #     print(f"{'-'*len(title):>5}")
    #     for pid, crack_process in self.process.items():
    #         join_cmd = shlex.join(crack_process.cmd)
    #         print(f"{pid:>3} | {crack_process.status:>8} | {join_cmd}")
        
            
    




def _report_result(process, report_file):
    _validate_write_file(report_file)
    try:
        stdout , stderr = process.comunicate()
        if type(stdout) is bytes:
            stdout.decode('utf-8')
            stderr.decode('utf-8')

            print_status(f"stderr: {stderr}")
            with open(report_file, 'r') as report:
                report.write(stdout)

    except Exception as error:
        print_failure(error)


class HCAttacks:
    @staticmethod
    def wordlist(*, attackMode=0, hashType, hashFile, wordlist):
        PasswordCracker.checkAttackArgs(_hashType=hashType,
                                        _hashFile=hashFile,
                                        _wordlist=wordlist)
        hc = Hashcat()
        print_status(f"Attacking {hashFile} with {wordlist} in straigth mode.")
        wordlistAttack =   f"{hc.mainexec} -a {attackMode} -m {hashType} {hashFile} {wordlist}"  
        Bash.exec(wordlistAttack)

    @staticmethod
    def combination(*, attackMode=1, hashType, hashFile, wordlists=[]):
        self._validate_args(_hash_type=hash_type,
                            _hash_file=hash_file,
                            _wordlist=wordlist)

        if type(wordlist) is list:
            wordlists = shlex.join(wordlist)
        else:
            wordlists = wordlist
                            
        print_status(f"Attacking {hash_file} with {wordlists} in combinator mode.")
        cmd = f"{self.mainexec} -a {attack_mode} -m {hash_type} {hash_file} {wordlists}"
        cmd = shlex.split(cmd)

    @staticmethod
    def maskAttack(*, attackMode=3, hashType, hashFile, wordlist):

        # if mask and mask_file:
        #         raise Exception(f"{mask} mask and {mask_file} masks file supplied.")
        
        # elif mask_file:
        #     self._validate_args(_hash_type=hash_type, 
        #                         _hash_file=hash_file, 
        #                         _mask_file=mask_file)
        #     print_status(f"Attacking {hash_file} with {mask_file} masks file in Brute-Force mode.")
        #     cmd = f"{self.mainexec} -a {attack_mode} -m {hash_type} {hash_file} {mask_file}"
        #     cmd = shlex.split(cmd)
        # elif mask:
        #     self._validate_args(_hash_type=hash_type, 
        #                         _hash_file=hash_file, 
        #                         _mask=mask)
        #     print_status(f"Attacking {hash_file} with {mask} in Brute-Force mode.")
        #     cmd = f"{self.mainexec} -a {attack_mode} -m {hash_type} {hash_file} {mask}"
        #     cmd = shlex.split(cmd)
        # else:
        #     raise Exception(f"No {mask} mask or {mask_file} masks file supplied.")
    
    @staticmethod
    def hybridWordMask(*, attackMode=6, hashType, hashFile, wordlist):
        pass

    @staticmethod
    def hybridMaskWord(*, attackMode=7, hashType, hashFile, wordlist):
        pass
