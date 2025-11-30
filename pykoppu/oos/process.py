"""
Process module.
"""

from typing import Any

class Process:
    """
    Represents a process in the OOS.

    Attributes:
        pid (int): The process ID.
        status (str): The status of the process.
        code (Any): The code associated with the process.
        hardware (Any): The hardware resources allocated to the process.
    """

    def __init__(self, pid: int, code: Any, hardware: Any):
        """
        Initializes the Process.

        Args:
            pid (int): The process ID.
            code (Any): The code associated with the process.
            hardware (Any): The hardware resources allocated to the process.
        """
        self.pid = pid
        self.status = "created"
        self.code = code
        self.hardware = hardware

    def start(self):
        """
        Starts the process.
        """
        self.status = "running"
        if self.hardware and self.code:
            return self.hardware.execute_program(self.code)
        return None
