#!/usr/bin/env python3
#
# Hydra Cracker - Feb 14 2021
#
# Maintainer: Gustavo Lozano <glozanoa@uni.pe>

# cracker modules import
from .passwordCracker import PasswordCracker


class Hydra(PasswordCracker):
    SERVICES = ("adam6500", "asterisk", "afp", "cisco", "cisco-enable", "cvs", "firebird", "ftp", "ftps",
                "http-head", "http-get", "http-post", "https-head", "https-get", "https-post",
                "http-get-form", "http-post-form", "https-get-form", "https-post-form", "http-proxy",
                "http-proxy-urlenum", "icq", "imap", "imaps", "irc", "ldap2", "ldap2s",
                "ldap3[-{cram|digest}md5][s]","memcached", "mongodb", "mssql", "mysql", "nntp",
                "oracle-listener", "oracle-sid", "pcanywhere", "pcnfs", "pop3", "pop3s", "postgres",
                "radmin2", "rdp", "redis", "rexec", "rlogin", "rpcap", "rsh", "rtsp",
                "s7-300", "sip", "smb", "smtp", "smtps", "smtp-enum", "snmp", "socks5", "ssh",
                "sshkey", "svn", "teamspeak", "telnet", "telnets", "vmauthd", "vnc", "xmpp")

    def __init__(self):
        super().__init__(name=["hydra"])

    @staticmethod
    def attack(*,
               target=None, service=None, port=None,
               user=None, usersFile=None,
               password=None, wordlist=None,
               userPassFile=None,
               ssl=None, oldssl=None,
               targetsFile=None
               ):
        pass
