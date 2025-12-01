"""
Portfolio Optimization Module.

Implements Portfolio Optimization as a QUBO.
"""

import numpy as np
from ..base import PUBOProblem

class PortfolioOptimization(PUBOProblem):
    """
    Portfolio Optimization Problem.
    
    Minimize risk and maximize return.
    H = q * sum sigma_ij x_i x_j - sum mu_i x_i
    """
    
    def __init__(self, expected_returns: list, covariance_matrix: np.ndarray, risk_aversion: float):
        """
        Initialize Portfolio Optimization.
        
        Args:
            expected_returns (list): List of expected returns (mu).
            covariance_matrix (np.ndarray): Covariance matrix (sigma).
            risk_aversion (float): Risk aversion coefficient (q).
        """
        super().__init__()
        self.mu = np.array(expected_returns)
        self.sigma = np.array(covariance_matrix)
        self.q = risk_aversion
        self.to_hamiltonian()
        
    def to_hamiltonian(self):
        """
        Convert to Hamiltonian.
        
        H = q * x^T Sigma x - mu^T x
        
        Map to E = -0.5 x^T J x - h^T x
        
        -0.5 J = q * Sigma  => J = -2 * q * Sigma
        -h = -mu            => h = mu
        """
        self.J = -2 * self.q * self.sigma
        self.h = self.mu
