#!/usr/bin/env python3


# exceptions for general PaswordCracker class
class CrackerExecNotFound(Exception):
    def __init__(self, passwordCracker):
        if isinstance(passwordCracker, list):
            self.passwordCracker = passwordCracker[0]
        else:
            self.passwordCracker = passwordCracker

        self.warningMsg = f"{self.passwordCracker} executable didn't found"
        super().__init__(self.warningMsg)

class CrackerDisableError(Exception):
    def __init__(self, crackerName):
        self.cracker = crackerName
        self.warningMsg = f"{self.cracker} is disable"
        super().__init__(self.warningMsg)


class AttackModeError(Exception):
    def __init__(self, attackMode):
        self.attackMode = attackMode
        self.warningMsg = f"Invalid attack mode: {attackMode}"
        super().__init__(self.warningMsg)


class CrackerHashError(Exception):
    def __init__(self, cracker, hashType):
        self.cracker = cracker.name
        self.hashType = hashType
        self.warningMsg = f"Invalid {self.cracker} hash type: {self.hashType}"
        super().__init__(self.warningMsg)

# exceptions for Hashcat subclass of PaswordCracker class
