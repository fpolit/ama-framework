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
        self.cracker = cracker.getName()
        self.hashType = hashType
        self.warningMsg = f"Invalid {self.cracker} hash type: {self.hashType}"
        super().__init__(self.warningMsg)


class NotSupportedCracker(Exception):
    def __init__(self, cracker):
        self.cracker = cracker
        self.warningMsg = f"Not supported {self.cracker} cracker"
        super().__init__(self.warningMsg)


class InvalidCracker(Exception):
    def __init__(self, invalidCracker):
        self.invalidCracker = invalidCracker
        self.warningMsg = f"Invalid cracker selected: {self.invalidCracker}"
        super().__init__(self.warningMsg)


class InvalidHashType(Exception):
    def __init__(self, cracker, hash_type):
        cracker_name = cracker.mainName
        self.warning = f"Invalid {cracker_name} hash Type: {hash_type}"
        super().__init__(self.warning)


# exceptions for john cracker (subclass of PaswordCracker class)
class InvalidParallelJob(Exception):
    def __init__(self, parallel_job):
        self.warning = f"Invalid parallel job: {parallel_job}"
        super().__init__(self.warning)


# exceptions for hashcat cracker (subclass of PaswordCracker class)
class InvalidWordlistsNumber(Exception):
    def __init__(self, wordlists):
        self.warning = (
            f"""
            Only 2 wordlists needed to perform combination attack using hashcat.
            Supplied wordlists: {wordlists}
            """
        )
        super().__init__(self.warning)


# exceptions for hydra cracker (subclass of PaswordCracker class)
class InvalidServiceError(Exception):
    def __init__(self, service):
        self.warning = f"Invalid service: {service}"
        super().__init__(self.warning)
