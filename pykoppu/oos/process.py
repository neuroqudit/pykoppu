"""
OOS Process Module.

This module defines the Process class which manages the execution lifecycle.
"""

from typing import Any, Optional
from ..biocompiler.compiler import BioCompiler
from ..electrophysiology import connect

class Process:
    """
    Represents a computing process on the OPU.
    """
    
    def __init__(self, problem: Any, backend: str = "brian2"):
        """
        Initialize a process.
        
        Args:
            problem: The problem instance to solve.
            backend (str): The backend driver to use.
        """
        self.problem = problem
        self.backend = backend
        self.compiler = BioCompiler()
        self.driver = connect(backend)
        
    def run(self) -> Any:
        """
        Run the process.
        
        Returns:
            Any: The result of the computation.
        """
        # 1. Compile
        instructions = self.compiler.compile(self.problem)
        
        # 2. Execute
        try:
            result = self.driver.execute(instructions)
        finally:
            self.driver.disconnect()
            
        return result
