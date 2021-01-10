#!/usr/bin/env python3

"""
# John class
# Jan 9 2021 - Implementation of John class
                (using core module of john python package)
#
# Maintainer: glozanoa <glozanoa@uni.pe>
"""

import os
from sbash.core import Bash
from fineprint.status import  print_failure, print_status

# cracker modules
from .PasswordCracker import PasswordCracker

from .PasswordCrackerExceptions import CrackerHashError

# hashes modules
from ..hashes.jtr import hashes

# base module
from ..base.FilePath import FilePath


class John(PasswordCracker):
    hashes = hashes

    attackMode = {0:"single", 1:"wordlist", 2:"incremental", 3:"mask"}

    def __init__(self):
	super().__init__(name=["john"])

    @staticmethod
    def benchmark():
        """
        	Run john benchmark
                """
        cracker = John()
        if cracker.checkStatus():
            benchmark = f"{cracker.mainexec} -b"
            print_status(f"Running: {benchmark}")
            Bash.exec(benchmark)
        else:
            raise CrackerDisableError("John")



    @staticmethod
    def checkAttackMode(attack):
        if not (attack in John.attackMode):
            raise AttackModeError(attack)


    @staticmethod
    def checkHashType(hashType):
        """ Check if the hash type is correct

        Args:
            hashType (str): hash type

        Raises:
            CrackerHashError: Error if the given hash isn't a valid hash type
        """

        if not (hashType in John.hashes):
            raise CrackerHashError(John, hashType)


    @staticmethod
    def checkAttackArgs(*,
                        _hashType=None,
                        _hashFile=None,
                        _wordlist=None,
                        _maskFile=None):
        PasswordCracker.checkAttackArgs(__hashFile = _hashFile,
                                        __wordlist = _wordlist,
                                        __maskFile = _maskFile)

        John.checkHashType(_hashType)

    @staticmethod
    def selectAttack(*,
                attackMode=None,
                hashType=None,
                hashFile=None,
                wordlist=[],
                maskFile=None,
                ):

        # contruction of hashcat cmd to execute
        John.checkAttackMode(attackMode)
        if attackMode == 0:   # wordlist attack
            PasswordCracker.checkAttackArgs(_hashType=hashType,
                                            _hashFile=hashFile,
                                            _wordlist=wordlist)
            jtr = John()
            print_status(f"Attacking {hashFile} with {wordlist} in straigth mode.")
            Bash.exec(f"{jtr.mainexec} --format={hashType} -w={wordlist} {hashFile}")


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


    

def __init__(self):
        
        self.utilities = self._find_jtr_utilities()
        
    def crack(self, *, attack_mode=None, hash_type=None, hash_file=None, 
            wordlist=[], mask=None, mask_file=None, **kwargs):
        """[summary]

        Args:
            hash_type ([type], optional): [description]. Defaults to None.
            hash_file ([type], optional): [description]. Defaults to None.
            attack_mode ([type], optional): [description]. Defaults to None.
            wordlist ([type], optional): [description]. Defaults to None.
            force (bool, optional): [description]. Defaults to False.
            
        Raises:
            Exception: Hashcat Pluging Disable
        """     
        if not len(self.process):
            self._validate_status()
        
        #generate hashcat command
        cmd = self._gencmd(attack_mode=attack_mode,
                            hash_type=hash_type,
                            hash_file=hash_file,
                            wordlist=wordlist,
                            mask=mask,
                            mask_file=mask_file)
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        pid = process.pid
        cp = CrackProcess(process=process, status="Running", cmd=cmd)
        self.process[pid] = cp
        print_status(f"Runing attack in process {pid}")


    def _util2john(self, *, util_name=None, ifile=None, ofile=None):
        if util_name and ifile:
            util2john_exec = []
            utils2john_pattern = re.compile(rf"\w*{util_name}(\.exe)?")
            for util_exec in self.utilities:
                if utils2john_pattern.fullmatch(util_exec):
                    util2john_exec.append(util_exec)
            
            if util2john_exec:
                main_util2john_exec = util2john_exec[0]
                if not ofile:
                    ofile = util_name + ".hash"
                shell.cmd(f"{main_util2john_exec} {ifile} > {ofile}")
                print_successful(f"{ofile} generated by {util_name}")
                    
            else:
                print_failure(f"No {util_name} executable.")
        else:
            if not util_name:
                raise Exception("No john utils supplied.")
            else:
                raise Exception(f"No input file supplied to {util_name}")

    def zip2john(self, *, zip_file=None, output_file="zip.hash"):
        self._util2john(util_name="zip2john", ifile=zip_file, ofile=output_file)

    def rar2john(self, *, rar_file=None, output_file="rar.hash"):
        self._util2john(util_name="rar2john", ifile=rar_file, ofile=output_file)
        
    def gpg2john(self, *, gpg_file=None, output_file="gpg.hash"):
        self._util2john(util_name="gpg2john", ifile=gpg_file, ofile=output_file)
        
    #def rar2john(self, *, rar_file=None, output_file="rar.hash"):
    #    self._util2john(util_name="rar2john", ifile=rar_file, ofile=output_file)
    

    def benckmark(self):
        """
        Run the john benchmark
        """
        
        if not len(self.process):
            self._validate_status()
        print_status(f"Using {self.mainexec} as {self.name} executable")
        cmd = shlex.split(f"{self.mainexec} --test")
        
        process = Popen(cmd, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        pid = process.pid
        cp = CrackProcess(process=process, status="Running", cmd=cmd)
        self.process[pid] = cp
        print_status(f"Runing benckmark with pid {pid}")    
    
    def show_attack_mode(self):
        title=f"{'#':>3} | {'Mode':>2}"
        print(title)
        print("-"*len(title))
        for mode_id, mode in self.attack_mode.items():
            print(f"{mode_id:>3} | {mode:>2}")
            
    def show_mask_charset(self):
        print(tabulate(self.mask_charset, headers=["mask", "charset"]))


    def search_hash(self, search=None, *, sensitive=False):
        if search:
            if not sensitive:
                hash_pattern = re.compile(rf"\w*{search}\w*", re.IGNORECASE)
            else:
                hash_pattern = re.compile(rf"\w*{search}\w*")
                
            print_successful("Posible hashcat hashes.")
            title = f"{'#':>4} | {'Name':>7}"
            print(title)
            print("-"*len(title))
            idx = 0
            for hash_name in self.hash_formats:
                if hash_pattern.search(hash_name):
                    print(f"{idx:>4} | {hash_name:>7}")
                    idx += 1
                    
        else:
            print_failure("No pattern given.")
    
    def _find_jtr_utilities(self):
        if platform.system() == "Linux":
            #import pdb; pdb.set_trace()
            jtr_utils, stderr, returnshell = shell.cmd("locate *2john", capture=True, encoding='utf-8')
            if not returnshell:
                if stderr:
                    print_failure(f"Generated error when finding john utils:\n {stderr}")
                else:
                     print_successful("John the Ripper's utilities found.") 
                return jtr_utils.split('\n')

            else:
                raise Exception("Failed to find john utilities.")
        else:
            print_status("Do this if i am bored")

    def _gencmd(self, *, 
                attack_mode=None, 
                hash_type=None, 
                hash_file=None, 
                wordlist=[], 
                mask=None, 
                mask_file=None, 
                force=False):
        
        # contruction of hashcat cmd to execute
        self._validate_attack_mode(attack_mode)
        if attack_mode=="single":
            print_failure("Not implemented yet.")
            #self._validate_args(_hash_type=hash_type, 
            #                    _hash_file=hash_file, 
            #                    _wordlist=wordlist)
            
            #print_status(f"Attacking {hash_file} with {wordlist} in single mode.")
            #cmd =   f"{self.mainexec} --single {hash_file} "  
            #cmd = shlex.split(cmd)

        elif attack_mode=="wordlist":


            if type(wordlist) is list:
                wordlists = ", ".join(wordlist)
            else:
                wordlists = wordlist
                    
            if hash_type:
                self._validate_args(_hash_type=hash_type, 
                                    _hash_file=hash_file, 
                                    _wordlist=wordlist)
                cmd = f"{self.mainexec} -w={wordlists} --format={hash_type} {hash_file}"
            else:
                self._validate_args(_hash_file=hash_file, 
                                    _wordlist=wordlist)
                cmd = f"{self.mainexec} -w={wordlists} {hash_file}"
            
            print_status(f"Attacking {hash_file} with {wordlists} in {attack_mode} mode.")
            cmd = shlex.split(cmd)

        elif attack_mode=="mask":
            
            if mask and mask_file:
                raise Exception(f"{mask} mask and {mask_file} masks file supplied.")
            
            elif mask_file:
                if hash_type:
                    self._validate_args(_hash_type=hash_type, 
                                        _hash_file=hash_file, 
                                        _mask_file=mask_file)
                
                    cmd = f"{self.mainexec} --mask={mask_file} --format={hash_type} {hash_file}"
                else:
                    self._validate_args(_hash_file=hash_file, 
                                        _mask_file=mask_file)
                    cmd = f"{self.mainexec} --mask={mask_file} {hash_file}"
                    
                print_status(f"Attacking {hash_file} with {mask_file} masks file in Brute-Force mode.")
                cmd = shlex.split(cmd)
            elif mask:
                if hash_type:
                    self._validate_args(_hash_type=hash_type, 
                                        _hash_file=hash_file, 
                                        _mask=mask)
                    cmd = f"{self.mainexec} --mask={mask} --format={hash_type} {hash_file}"
                else:
                    self._validate_args( _hash_file=hash_file, 
                                        _mask=mask)
                    cmd = f"{self.mainexec} --mask={mask} {hash_file}"

                    print_status(f"Attacking {hash_file} with {mask} in Brute-Force mode.")
                    cmd = shlex.split(cmd)
    
            else:
                raise Exception(f"No {mask} mask or {mask_file} masks file supplied.")
    
        elif attack_mode=="incremental":
            self._validate_args(_hash_file=hash_file)
            print_status(f"Attacking {hash_file}  in {attack_mode} mode.")
            cmd = f"{self.mainexec} --incremental {hash_file}"
            cmd = shlex.split(cmd)
            
        return cmd

    def _update_all_process(self):
        for crack_process in self.process.values():
            crack_process.update_status()
    
    
    def show_process(self):
        self._update_all_process()
        title = f"{'pid':>5} | {'status':>8} | {'Start time':>13} | {'cmd'}"
        print(title)
        print(f"{'-'*len(title):>5}")
        for pid, crack_process in self.process.items():
            join_cmd = shlex.join(crack_process.cmd)
            print(f"{pid:>3} | {crack_process.status.value:>8} | {crack_process.init_time} |{join_cmd}")
        
            
    
    def _validate_args(self, *, 
                        _attack_mode=None, 
                        _hash_type=None, 
                        _hash_file, 
                        _wordlist=None,
                        _mask_file=None, 
                        _mask=None):
        if _wordlist and _mask_file: 
            _validate_read_file(_hash_file, _wordlist, _mask_file)
        else:
            _validate_read_file(_hash_file)
        
        if _hash_type:
            self._validate_hash_type(_hash_type)
        if _attack_mode:
            self._validate_attack_mode(_attack_mode)
        if _mask:
            self._validate_mask(_mask)
            
    def _validate_attack_mode(self, attack_mode):
        
        if isinstance(attack_mode, int):
            if attack_mode not  in self.attack_mode:
                raise Exception(f"Invalid Attack Mode: {attack_mode}.")
            attack_mode = self.attack_mode[attack_mode] # convert index of attack mode to ("single" or "wordlist" or "incremental")
        elif isinstance(attack_mode, str):
            if attack_mode not in self.attack_mode.values():
                raise Exception(f"Invalid Attack Mode: {attack_mode}.")

    def _validate_mask(self, mask):
        mask_iter = _genitermask(mask)
        while mask_symbol := next(mask_iter, ""):
            if mask_symbol not in self.masks:
                raise Exception("Invalid mask {mask}.")
    
    def _validate_hash_type(self, hash_type):
        if not hash_type in self.hash_formats:
            raise Exception("Invalid Hash Type.")

    def unshadow(self, *, password_file=None, shadow_file=None, unshadow_file='unshadow.txt'):
        _validate_read_file(password_file, shadow_file)
        shell.cmd(f"unshadow {password_file} {shadow_file} > {unshadow_file}")
        print_successful(f"Generated {unshadow_file}.")
    
    
    
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


def _genitermask(mask):
    iter_str_mask = iter(mask)
    mask_symbol = next(iter_str_mask, "") + next(iter_str_mask, "")
    while mask_symbol:
        yield mask_symbol
        mask_symbol = next(iter_str_mask, "") + next(iter_str_mask, "")

def _validate_read_file(*read_files):
    for read_file in read_files:
        if os.path.isfile(read_file) and os.access(read_file, os.R_OK):
            pass
        elif os.path.isfile(read_file):
            raise Exception(f"Permission denied to read {read_file}.")
        else:
            raise Exception(f"The file {read_file} ")

def _validate_write_file(*write_files):
    for write_file in write_files:
        if os.path.isfile(write_file):
            raise Exception(f"File {write_file} already exist.")



class JTRAttacks:

    @staticmethod
    def single(*, attackMode=0, hashType, hashFile, wordlist):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile,
                             _wordlist=wordlist)
        hc = Hashcat()
        print_status(f"Attacking {hashFile} with {wordlist} in straigth mode.")
        wordlistAttack =   f"{hc.mainexec} -a {attackMode} -m {hashType} {hashFile} {wordlist}"
        Bash.exec(wordlistAttack)

    @staticmethod
    def wordlist(*, attackMode=1, hashType, hashFile, wordlist):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile,
                             _wordlist=wordlist)
        jtr = John()
        print_status(f"Attacking {hashFile} with {wordlist} wordlist in straigth mode.")
        Bash.exec(f"{jtr.mainexec} --format={hashType} -w={wordlist} {hashFile}")


    @staticmethod
    def incremental(*, attackMode=2, hashType, hashFile):
        John.checkAttackArgs(_hashType=hashType,
                             _hashFile=hashFile)
        jtr = John()
        print_status(f"Attacking {hashFile} with {wordlist} in incremental mode.")
        incrementalAttack =   f"{jtr.mainexec} --format={hashType} {hashFile}"
        Bash.exec(incrementalAttack)


    @staticmethod
    def maskAttack(*, attackMode=3, hashType, hashFile, maskFile):
        PasswordCracker.checkAttackArgs(_hashType=hashType,
                                        _hashFile=hashFile,
                                        _maskFile=maskFile)
        jtr = John()
        maskFilePath = FilePath(maskFile)
        hashFilePath = FilePath(hashFile)

        print_status(f"Attacking {hashFile} with {maskFile} in mask attack mode.")
        with open(maskFilePath, 'r') as masks:
            while mask := masks.readline().rstrip():
                if not PasswordCracker.statusHashFile(hashFilePath):
                    maskAttack =   f"{jtr.mainexec} --mask={mask} --format={hashType} {hashFile}"
                    print_status(f"Running: {maskAttack}")
                    Bash.exec(maskAttack)

    # @staticmethod
    # def combination(*, attackMode=1, hashType, hashFile, wordlists=[]):
    #     self._validate_args(_hash_type=hash_type,
    #                         _hash_file=hash_file,
    #                         _wordlist=wordlist)

    #     if type(wordlist) is list:
    #         wordlists = shlex.join(wordlist)
    #     else:
    #         wordlists = wordlist

    #     print_status(f"Attacking {hash_file} with {wordlists} in combinator mode.")
    #     cmd = f"{self.mainexec} -a {attack_mode} -m {hash_type} {hash_file} {wordlists}"
    #     cmd = shlex.split(cmd)



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
