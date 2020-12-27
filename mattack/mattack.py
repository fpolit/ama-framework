#!/usr/bin/env python3


PWD = os.path.abspath(__file__)
# john_hashes = []
# with Reader.openWithName("test.csv") as file:
#     for line in file:
#         print(line)
#!/usr/bin/env python3

john_hashes=[
"descrypt",             "bsdicrypt",            "md5crypt",         "md5crypt-long",      "bcrypt",             "scrypt",
"tripcode",             "AndroidBackup",        "adxcrypt",         "agilekeychain",      "aix-ssha1",          "aix-ssha256",
"aix-ssha512",          "andOTP",               "ansible",          "argon2",             "as400-des",          "as400-ssha1",
"AxCrypt",              "AzureAD",              "BestCrypt",        "bfegg",              "Bitcoin",            "BitLocker",
"LM",                   "AFS",                  "asa-md5",          "bitshares",          "Bitwarden",          "BKS",
"Blackberry-ES10",      "WoWSRP",               "Blockchain",       "chap",               "Clipperz",           "cloudkeychain",
"dynamic_n",            "CRC32",                "sha1crypt",        "sha256crypt",        "sha512crypt",        "Citrix_NS10",
"dahua",                "dashlane",             "diskcryptor",      "Django",             "django-scrypt",      "dmd5",
"dmg",                  "dominosec",            "dominosec8",       "DPAPImk",            "dragonfly3-32",      "dragonfly3-64",
"dragonfly4-32",        "dragonfly4-64",        "Drupal7",          "eCryptfs",           "eigrp",              "electrum",
"EncFS",                "enpass",               "EPI",              "EPiServer",          "ethereum",           "fde",
"Fortigate256",         "Fortigate",            "FormSpring",       "FVDE",               "geli",               "gost",
"gpg",                  "HAVAL-128-4",          "HAVAL-256-3",      "hdaa",               "hMailServer",        "hsrp",
"IKE",                  "ipb2",                 "itunes-backup",    "iwork",              "KeePass",            "keychain",
"keyring",              "keystore",             "known_hosts",      "krb4",               "krb5",               "krb5asrep",
"krb5pa-sha1",          "krb5tgs",              "krb5-17",          "krb5-18",            "krb5-3",             "kwallet",
"lp",                   "lpcli",                "leet",             "lotus5",             "lotus85",            "LUKS",
"MD2",                  "mdc2",                 "MediaWiki",        "monero",             "money",              "MongoDB",
"scram",                "Mozilla",              "mscash",           "mscash2",            "MSCHAPv2",           "mschapv2-naive",
"krb5pa-md5",           "mssql",                "mssql05",          "mssql12",            "multibit",           "mysqlna",
"mysql-sha1",           "mysql",                "net-ah",           "nethalflm",          "netlm",              "netlmv2",
"net-md5",              "netntlmv2",            "netntlm",          "netntlm-naive",      "net-sha1",           "nk",
"notes",                "md5ns",                "nsec3",            "NT",                 "o10glogon",          "o3logon",
"o5logon",              "ODF",                  "Office",           "oldoffice",          "OpenBSD-SoftRAID",   "openssl-enc",
"oracle",               "oracle11",             "Oracle12C",        "osc",                "ospf",               "Padlock",
"Palshop",              "Panama",               "PBKDF2-HMAC-MD4",  "PBKDF2-HMAC-MD5",    "PBKDF2-HMAC-SHA1",   "PBKDF2-HMAC-SHA256",
"PBKDF2-HMAC-SHA512",   "PDF",                  "PEM",              "pfx",                "pgpdisk",            "pgpsda",
"pgpwde",               "phpass",               "PHPS",             "PHPS2",              "pix-md5",            "PKZIP",
"po",                   "postgres",             "PST",              "PuTTY",              "pwsafe",             "qnx",
"RACF",                 "RACF-KDFAES",          "radius",           "RAdmin",             "RAKP",               "rar",
"RAR5",                 "Raw-SHA512",           "Raw-Blake2",       "Raw-Keccak",         "Raw-Keccak-256",     "Raw-MD4",
"Raw-MD5",              "Raw-MD5u",             "Raw-SHA1",         "Raw-SHA1-AxCrypt",   "Raw-SHA1-Linkedin",  "Raw-SHA224",
"Raw-SHA256",           "Raw-SHA3",             "Raw-SHA384",       "ripemd-128",         "ripemd-160",         "rsvp",
"Siemens-S7",           "Salted-SHA1",          "SSHA512",          "sapb",               "sapg",               "saph",
"sappse",               "securezip",            "7z",               "Signal",             "SIP",                "skein-256",
"skein-512",            "skey",                 "SL3",              "Snefru-128",         "Snefru-256",         "LastPass",
"SNMP",                 "solarwinds",           "SSH",              "sspr",               "Stribog-256",        "Stribog-512",
"STRIP",                "SunMD5",               "SybaseASE",        "Sybase-PROP",        "tacacs-plus",        "tcp-md5",
"telegram",             "tezos",                "Tiger",            "tc_aes_xts",         "tc_ripemd160",       "tc_ripemd160boot",
"tc_sha512",            "tc_whirlpool",         "vdi",              "OpenVMS",            "vmx",                "VNC",
"vtp",                  "wbb3",                 "whirlpool",        "whirlpool0",         "whirlpool1",         "wpapsk",
"wpapsk-pmk",           "xmpp-scram",           "xsha",             "xsha512",            "ZIP",                "ZipMonster",
"plaintext",            "has-160",              "HMAC-MD5",         "HMAC-SHA1",          "HMAC-SHA224",        "HMAC-SHA256",
"HMAC-SHA384",          "HMAC-SHA512",          "dummy",            "crypt",              "cq"
]

hashesjson = os.path.join(dirname(PWD), 'hhash.json')
with open(hashesjson, 'r') as hash_hashcat:
    hashcat_hashes = json.load(hash_hashcat)


class MaskAttack:
    """
        This class perform a mask attack
    """
    hashFormat = john_hashes

    def __init__(self, masksFile, hashType, hashFile):
        self.masksFile = masksFile
        self.hashType = hashType
        self.hashFile = hashFile

    @staticmethod
    def searchHash(search=None, *, sensitive=False):
        if search:
            if not sensitive:
                hashPattern = re.compile(rf"\w*{search}\w*", re.IGNORECASE)
            else:
                hashPattern = re.compile(rf"\w*{search}\w*")

            print_status(f"Posible hashes(*{search}*):")
            for hashFormat in MaskAttack.hashFormat:
                if hashPattern.search(hashFormat):
                    print_successful(hashFormat)

        else:
            print_failure("No pattern given.")

    @staticmethod
    def checkStatus(hash):
        """
            Check status of the hash (it is cracked or no)
            It hash is cracked when it is in the ~/.john/john.pot file
            otherwise it isn't cracked
        """
        import pdb; pdb.set_trace()
        crackedPattern = re.compile(rf"(\w|\W|\s)*{hash}(\w|\W|\s)*")
        homeUser = os.path.expanduser("~")
        johnPotPath = os.path.join(homeUser, ".john/john.pot")
        with open(johnPotPath, 'r') as johnPotFile:
            while   crackedHash := johnPotFile.readline().rstrip():
                if(crackedPattern.fullmatch(crackedHash)):
                    return True
        return False


    def run(self, nodes=None, ntasks=None, partition=None, cpusPerTask=1, memPerCpu=None,
        jobName="mattack", output=None, error=None, slurmScript="mattack.sh", time=None):
        """
            Submit a slurm task
        """
        try:

            #import pdb; pdb.set_trace()
            if not partition:   #No partition variable is supplied(we cann't submmit this task with slurm)
                #run simply in the actual node
                if cpusPerTask>1 and ntasks>1: #no hybrid taks supported by john
                    raise Exception("No hybrid execution supported")
                elif cpusPerTask>1 and ntasks==1: #omp work
                    Bash.exec(f"export OMP_NUM_THREADS={cpusPerTask}")
                    with open(self.masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            attack_cmd = f"john --mask={mask} --format={self.hashType} {self.hashFile}"
                            print()
                            Bash.exec(attack_cmd)
                            print_status(f"Running {attack_cmd}")
                elif ntasks>1 and not cpusPerTask==1:  #mpi work
                    with open(self.masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            attack_cmd = f"mpirun -n {ntasks} john --mask={mask} --format={self.hashType} {self.hashFile}"
                            print()
                            Bash.exec(attack_cmd)
                            print_status(f"Running {attack_cmd}")
                else:   # serial work(canceled because parallel support is enable)
                    print_failure("You will run john parallelly(ntasks>1)")
                    sys.exit(1)
            else:   # we can summit this work with slurm
                if cpusPerTask>1 and ntasks>1: #no hybrid taks supported by john
                    raise Exception("No hybrid execution supported")
                elif cpusPerTask>1 and ntasks==1 and nodes==1: #omp work in only 1 node(OpenMP isn't scalable)
                    # writing slurm script (sscript)
                    sscript =   "#!/bin/bash" +\
                                f"#\nSBATCH --job-name={jobName}" +\
                                f"#\nSBATCH --nodes={nodes}"  +\
                                f"#\nSBATCH --ntasks={ntasks}"    +\
                                f"#\nSBATCH --cpus-per-task={cpusPerTask}"

                    if time:
                        sscript += f"\n#SBATCH --time={time}\n"

                    sscript += "\n\n#Performing a parallel mask attack"
                    with open(self.masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            sscript += f"\nsrun john --mask={mask} --format={self.hashType} {self.hashFile}"

                    with open(slurmScript, 'w') as submmitScript:   # writing generated slurm submmit script
                        submmitScript.write(sscript)

                    infoAttack =    f"Performing a mask attack against of {self.hashType} hash in {self.hashFile}" +\
                                    f"\n\tmaskFile: {self.masksFile}"

                    parallelAttackinfo =    f"Parallel attack desciption:" +\
                                            f"\n\tnodes: {nodes}" +\
                                            f"\n\tntasks: {ntasks}" +\
                                            f"\n\tpartition: {partition}\n"
                                            # ADD MORE DETAILS
                    print_status(infoAttack)
                    print_status(parallelAttackinfo)
                    #Bash.exec(f"sbatch {slurmScript}")

                elif cpusPerTask==1 and ntasks>1 and nodes>=1: #mpi work(parallel scalable task)
                    # writing slurm script (sscript)
                    sscript =   "#!/bin/bash" +\
                                f"\n#SBATCH --job-name={jobName}" +\
                                f"\n#SBATCH --nodes={nodes}"  +\
                                f"\n#SBATCH --ntasks={ntasks}"    +\
                                f"\n#SBATCH --cpus-per-task={cpusPerTask}"

                    if memPerCpu:
                        sscript += f"\n#SBATCH --mem-per-cpu={memPerCpu}\n"

                    if time:
                        sscript += f"\n#SBATCH --time={time}\n"

                    if error:
                        sscript += f"\n#SBATCH --error={error}\n"
                    if output:
                        sscript += f"\n#SBATCH --output={output}\n"

                    sscript += "\n\n#Performing several parallel mask attacks"
                    with open(self.masksFile, 'r') as masks:
                        while mask := masks.readline():
                            mask = mask.rstrip()
                            sscript += f"\nsrun mpirun john --mask={mask} --format={self.hashType} {self.hashFile}"

                    with open(slurmScript, 'w') as submmitScript:   # writing generated slurm submmit script
                        submmitScript.write(sscript)



                    infoAttack =    f"Performing a mask attack against of {self.hashType} hash in {self.hashFile}" +\
                                    f"\n\tmaskFile: {self.masksFile}"

                    parallelAttackinfo =    f"Parallel attack desciption:" +\
                                            f"\n\tnodes: {nodes}" +\
                                            f"\n\tntasks: {ntasks}" +\
                                            f"\n\tpartition: {partition}\n"
                                            # ADD MORE DETAILS
                    print_status(infoAttack)
                    print_status(parallelAttackinfo)
                    Bash.exec(f"sbatch {slurmScript}")

                else:
                    raise Exception("Invalid arguments.")

        except Exception as error:
            print_failure(error)
            sys.exit(1)
