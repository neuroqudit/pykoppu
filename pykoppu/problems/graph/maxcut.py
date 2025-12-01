"""
MaxCut Problem Module.

Implements the MaxCut problem and its conversion to Hamiltonian.
"""

import networkx as nx
import numpy as np
from ..base import PUBOProblem

class MaxCut(PUBOProblem):
    """
    MaxCut Problem.
    
    Finds a cut that maximizes the sum of weights of edges crossing the cut.
    """
    
    def __init__(self, graph: nx.Graph):
        """
        Initialize MaxCut problem.
        
        Args:
            graph (nx.Graph): The input graph.
        """
        super().__init__()
        self.graph = graph
        self.to_hamiltonian()
        
    def to_hamiltonian(self):
        """
        Convert MaxCut to Ising Hamiltonian.
        
        MaxCut Hamiltonian: H = sum_{i,j} w_{ij} s_i s_j
        where s_i in {-1, 1}.
        
        We want to minimize E = -0.5 * s^T J s - h^T s
        
        For MaxCut, we want to maximize sum w_ij (1 - s_i s_j) / 2
        Equivalent to minimizing sum w_ij s_i s_j
        
        So J_ij = -w_ij (because E has -0.5 factor? No, let's be careful)
        
        Standard Ising: E = - sum J_ij s_i s_j
        We want to minimize sum w_ij s_i s_j.
        So -J_ij = w_ij => J_ij = -w_ij.
        
        However, we need to normalize weights to the dynamic range of the neuron.
        Target range: +/- 1.5 nA.
        """
        n = len(self.graph.nodes)
        adj = nx.to_numpy_array(self.graph)
        
        # J_ij = -w_ij
        J = -adj
        
        # Normalize to +/- 1.5e-9
        max_weight = np.max(np.abs(J))
        if max_weight > 0:
            scale_factor = 1.5e-9 / max_weight
            J = J * scale_factor
            
        self.J = J
        self.h = np.zeros(n) # MaxCut has no local field
