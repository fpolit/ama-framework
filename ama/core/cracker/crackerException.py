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


class InvalidHashTypeError(Exception):
    def __init__(self, cracker, hashType):
        crackerName = cracker.mainName
        self.warning = f"Invalid {crackerName} hash Type: {hashType}"
        super().__init__(self.warning)


# exceptions for john cracker (subclass of PaswordCracker class)
class InvalidParallelJobError(Exception):
    def __init__(self, parallelJob):
        self.warning = f"Invalid parallel job: {parallelJob}"
        super().__init__(self.warning)


# exceptions for hashcat cracker (subclass of PaswordCracker class)


# exceptions for hydra cracker (subclass of PaswordCracker class)
class InvalidSeviceError(Exception):
    def __init__(self, service):
        self.warning = f"Invalid service: {service}"
        super().__init__(self.warning)
