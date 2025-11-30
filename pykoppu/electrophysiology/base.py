"""
Base driver module.
"""
from abc import ABC, abstractmethod

class BaseDriver(ABC):
    """
    Abstract base class for electrophysiology drivers.
    """

    def __init__(self, opu):
        self.opu = opu

    @abstractmethod
    def execute_program(self, bioasm):
        """
        Executes a bio-assembly program.

        Args:
            bioasm: The bio-assembly program to execute.
        """
        pass
