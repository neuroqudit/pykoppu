"""
Base problem module.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple

class PUBOProblem(ABC):
    """
    Abstract base class for PUBO (Polynomial Unconstrained Binary Optimization) problems.

    Attributes:
        n_variables (int): The number of variables in the problem.
        terms (List[Tuple[List[int], float]]): The terms of the objective function.
    """

    def __init__(self, n_variables: int):
        self.n_variables = n_variables
        self.terms = []

    def add_term(self, indices: List[int], value: float):
        """
        Adds a term to the objective function.

        Args:
            indices (List[int]): The indices of the variables in the term.
            value (float): The coefficient of the term.
        """
        self.terms.append((indices, value))
