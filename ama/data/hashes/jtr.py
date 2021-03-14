#!/usr/bin/env python3
"""
Jhon the Ripper hashes
"""

jtrHashes=[
    "descrypt",             "bsdicrypt",            "md5crypt",         "md5crypt-long",      "bcrypt",             "scrypt",
    "tripcode",             "androidbackup",        "adxcrypt",         "agilekeychain",      "aix-ssha1",          "aix-ssha256",
    "aix-ssha512",          "andotp",               "ansible",          "argon2",             "as400-des",          "as400-ssha1",
    "axcrypt",              "azuread",              "bestcrypt",        "bfegg",              "bitcoin",            "bitlocker",
    "lm",                   "afs",                  "asa-md5",          "bitshares",          "bitwarden",          "bks",
    "blackberry-es10",      "wowsrp",               "blockchain",       "chap",               "clipperz",           "cloudkeychain",
    "dynamic_n",            "crc32",                "sha1crypt",        "sha256crypt",        "sha512crypt",        "citrix_ns10",
    "dahua",                "dashlane",             "diskcryptor",      "django",             "django-scrypt",      "dmd5",
    "dmg",                  "dominosec",            "dominosec8",       "dpapimk",            "dragonfly3-32",      "dragonfly3-64",
    "dragonfly4-32",        "dragonfly4-64",        "drupal7",          "ecryptfs",           "eigrp",              "electrum",
    "encfs",                "enpass",               "epi",              "episerver",          "ethereum",           "fde",
    "fortigate256",         "fortigate",            "formspring",       "fvde",               "geli",               "gost",
    "gpg",                  "haval-128-4",          "haval-256-3",      "hdaa",               "hmailserver",        "hsrp",
    "ike",                  "ipb2",                 "itunes-backup",    "iwork",              "keepass",            "keychain",
    "keyring",              "keystore",             "known_hosts",      "krb4",               "krb5",               "krb5asrep",
    "krb5pa-sha1",          "krb5tgs",              "krb5-17",          "krb5-18",            "krb5-3",             "kwallet",
    "lp",                   "lpcli",                "leet",             "lotus5",             "lotus85",            "luks",
    "md2",                  "mdc2",                 "mediawiki",        "monero",             "money",              "mongodb",
    "scram",                "mozilla",              "mscash",           "mscash2",            "mschapv2",           "mschapv2-naive",
    "krb5pa-md5",           "mssql",                "mssql05",          "mssql12",            "multibit",           "mysqlna",
    "mysql-sha1",           "mysql",                "net-ah",           "nethalflm",          "netlm",              "netlmv2",
    "net-md5",              "netntlmv2",            "netntlm",          "netntlm-naive",      "net-sha1",           "nk",
    "notes",                "md5ns",                "nsec3",            "nt",                 "o10glogon",          "o3logon",
    "o5logon",              "odf",                  "office",           "oldoffice",          "openbsd-softraid",   "openssl-enc",
    "oracle",               "oracle11",             "oracle12c",        "osc",                "ospf",               "padlock",
    "palshop",              "panama",               "pbkdf2-hmac-md4",  "pbkdf2-hmac-md5",    "pbkdf2-hmac-sha1",   "pbkdf2-hmac-sha256",
    "pbkdf2-hmac-sha512",   "pdf",                  "pem",              "pfx",                "pgpdisk",            "pgpsda",
    "pgpwde",               "phpass",               "phps",             "phps2",              "pix-md5",            "pkzip",
    "po",                   "postgres",             "pst",              "putty",              "pwsafe",             "qnx",
    "racf",                 "racf-kdfaes",          "radius",           "radmin",             "rakp",               "rar",
    "rar5",                 "raw-sha512",           "raw-blake2",       "raw-keccak",         "raw-keccak-256",     "raw-md4",
    "raw-md5",              "raw-md5u",             "raw-sha1",         "raw-sha1-axcrypt",   "raw-sha1-linkedin",  "raw-sha224",
    "raw-sha256",           "raw-sha3",             "raw-sha384",       "ripemd-128",         "ripemd-160",         "rsvp",
    "siemens-s7",           "salted-sha1",          "ssha512",          "sapb",               "sapg",               "saph",
    "sappse",               "securezip",            "7z",               "signal",             "sip",                "skein-256",
    "skein-512",            "skey",                 "sl3",              "snefru-128",         "snefru-256",         "lastpass",
    "snmp",                 "solarwinds",           "ssh",              "sspr",               "stribog-256",        "stribog-512",
    "strip",                "sunmd5",               "sybasease",        "sybase-prop",        "tacacs-plus",        "tcp-md5",
    "telegram",             "tezos",                "tiger",            "tc_aes_xts",         "tc_ripemd160",       "tc_ripemd160boot",
    "tc_sha512",            "tc_whirlpool",         "vdi",              "openvms",            "vmx",                "vnc",
    "vtp",                  "wbb3",                 "whirlpool",        "whirlpool0",         "whirlpool1",         "wpapsk",
    "wpapsk-pmk",           "xmpp-scram",           "xsha",             "xsha512",            "zip",                "zipmonster",
    "plaintext",            "has-160",              "hmac-md5",         "hmac-sha1",          "hmac-sha224",        "hmac-sha256",
    "hmac-sha384",          "hmac-sha512",          "dummy",            "crypt",              "cq"
]

# sensitive letters
# jtrHashes=[
# "descrypt",             "bsdicrypt",            "md5crypt",         "md5crypt-long",      "bcrypt",             "scrypt",
# "tripcode",             "AndroidBackup",        "adxcrypt",         "agilekeychain",      "aix-ssha1",          "aix-ssha256",
# "aix-ssha512",          "andOTP",               "ansible",          "argon2",             "as400-des",          "as400-ssha1",
# "AxCrypt",              "AzureAD",              "BestCrypt",        "bfegg",              "Bitcoin",            "BitLocker",
# "LM",                   "AFS",                  "asa-md5",          "bitshares",          "Bitwarden",          "BKS",
# "Blackberry-ES10",      "WoWSRP",               "Blockchain",       "chap",               "Clipperz",           "cloudkeychain",
# "dynamic_n",            "CRC32",                "sha1crypt",        "sha256crypt",        "sha512crypt",        "Citrix_NS10",
# "dahua",                "dashlane",             "diskcryptor",      "Django",             "django-scrypt",      "dmd5",
# "dmg",                  "dominosec",            "dominosec8",       "DPAPImk",            "dragonfly3-32",      "dragonfly3-64",
# "dragonfly4-32",        "dragonfly4-64",        "Drupal7",          "eCryptfs",           "eigrp",              "electrum",
# "EncFS",                "enpass",               "EPI",              "EPiServer",          "ethereum",           "fde",
# "Fortigate256",         "Fortigate",            "FormSpring",       "FVDE",               "geli",               "gost",
# "gpg",                  "HAVAL-128-4",          "HAVAL-256-3",      "hdaa",               "hMailServer",        "hsrp",
# "IKE",                  "ipb2",                 "itunes-backup",    "iwork",              "KeePass",            "keychain",
# "keyring",              "keystore",             "known_hosts",      "krb4",               "krb5",               "krb5asrep",
# "krb5pa-sha1",          "krb5tgs",              "krb5-17",          "krb5-18",            "krb5-3",             "kwallet",
# "lp",                   "lpcli",                "leet",             "lotus5",             "lotus85",            "LUKS",
# "MD2",                  "mdc2",                 "MediaWiki",        "monero",             "money",              "MongoDB",
# "scram",                "Mozilla",              "mscash",           "mscash2",            "MSCHAPv2",           "mschapv2-naive",
# "krb5pa-md5",           "mssql",                "mssql05",          "mssql12",            "multibit",           "mysqlna",
# "mysql-sha1",           "mysql",                "net-ah",           "nethalflm",          "netlm",              "netlmv2",
# "net-md5",              "netntlmv2",            "netntlm",          "netntlm-naive",      "net-sha1",           "nk",
# "notes",                "md5ns",                "nsec3",            "NT",                 "o10glogon",          "o3logon",
# "o5logon",              "ODF",                  "Office",           "oldoffice",          "OpenBSD-SoftRAID",   "openssl-enc",
# "oracle",               "oracle11",             "Oracle12C",        "osc",                "ospf",               "Padlock",
# "Palshop",              "Panama",               "PBKDF2-HMAC-MD4",  "PBKDF2-HMAC-MD5",    "PBKDF2-HMAC-SHA1",   "PBKDF2-HMAC-SHA256",
# "PBKDF2-HMAC-SHA512",   "PDF",                  "PEM",              "pfx",                "pgpdisk",            "pgpsda",
# "pgpwde",               "phpass",               "PHPS",             "PHPS2",              "pix-md5",            "PKZIP",
# "po",                   "postgres",             "PST",              "PuTTY",              "pwsafe",             "qnx",
# "RACF",                 "RACF-KDFAES",          "radius",           "RAdmin",             "RAKP",               "rar",
# "RAR5",                 "Raw-SHA512",           "Raw-Blake2",       "Raw-Keccak",         "Raw-Keccak-256",     "Raw-MD4",
# "Raw-MD5",              "Raw-MD5u",             "Raw-SHA1",         "Raw-SHA1-AxCrypt",   "Raw-SHA1-Linkedin",  "Raw-SHA224",
# "Raw-SHA256",           "Raw-SHA3",             "Raw-SHA384",       "ripemd-128",         "ripemd-160",         "rsvp",
# "Siemens-S7",           "Salted-SHA1",          "SSHA512",          "sapb",               "sapg",               "saph",
# "sappse",               "securezip",            "7z",               "Signal",             "SIP",                "skein-256",
# "skein-512",            "skey",                 "SL3",              "Snefru-128",         "Snefru-256",         "LastPass",
# "SNMP",                 "solarwinds",           "SSH",              "sspr",               "Stribog-256",        "Stribog-512",
# "STRIP",                "SunMD5",               "SybaseASE",        "Sybase-PROP",        "tacacs-plus",        "tcp-md5",
# "telegram",             "tezos",                "Tiger",            "tc_aes_xts",         "tc_ripemd160",       "tc_ripemd160boot",
# "tc_sha512",            "tc_whirlpool",         "vdi",              "OpenVMS",            "vmx",                "VNC",
# "vtp",                  "wbb3",                 "whirlpool",        "whirlpool0",         "whirlpool1",         "wpapsk",
# "wpapsk-pmk",           "xmpp-scram",           "xsha",             "xsha512",            "ZIP",                "ZipMonster",
# "plaintext",            "has-160",              "HMAC-MD5",         "HMAC-SHA1",          "HMAC-SHA224",        "HMAC-SHA256",
# "HMAC-SHA384",          "HMAC-SHA512",          "dummy",            "crypt",              "cq"
# ]
