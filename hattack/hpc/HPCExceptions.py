#!/usr/bin/env python3

class HybridWorkError(Exception):
    """
    Exceptions to catch: hybrid word not supported
    """

    def __init__(self, **parameters):
        self.warningMsg = f"Hybrid work not supported: {parameters}"
        super().__init__(self.warningMsg)


class ParallelWorkError(Exception):
    """
    Exception to catch: no supported parallel work of a specific type
    """

    def __init__(self, parallelJobType):
        self.warningMsg = f"No supported {parallelJobType} parallel jobs.")
        super().__init__(self.warningMsg)


class SlurmParametersError(Exception):
    """
    Exceptions to catch: a group of invalid slurm parameters
    """

    def __init__(self, **invalidParameters):
        self.warningMsg = f"Invalid parameters: {invalidParameters}"
        super().__init__(self.warningMsg)
