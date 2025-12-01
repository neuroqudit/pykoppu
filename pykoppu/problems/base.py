"""
Problem Base Module.

Defines the interface for problems solvable by KOPPU.
"""

from abc import ABC, abstractmethod
import numpy as np

class PUBOProblem(ABC):
    """
    Polynomial Unconstrained Binary Optimization (PUBO) Problem.
    """
    
    def __init__(self):
        self.J: np.ndarray = np.array([])
        self.h: np.ndarray = np.array([])
        
    @abstractmethod
    def to_hamiltonian(self):
        """Convert the problem to Hamiltonian form (J, h)."""
        pass
