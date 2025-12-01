"""
TSP Problem Module.

Implements the Traveling Salesperson Problem (TSP) and its conversion to Hamiltonian.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Any, Dict, List
from ..base import PUBOProblem

class TSP(PUBOProblem):
    """
    Traveling Salesperson Problem (TSP).
    
    Finds the shortest route visiting each city exactly once and returning to the origin.
    """
    
    def __init__(self, distance_matrix: np.ndarray, penalty: float = 10.0):
        """
        Initialize TSP problem.
        
        Args:
            distance_matrix (np.ndarray): NxN matrix of distances between cities.
            penalty (float): Penalty strength for constraints.
        """
        super().__init__()
        self.distance_matrix = np.array(distance_matrix)
        self.n_cities = self.distance_matrix.shape[0]
        self.penalty = penalty
        self.to_hamiltonian()
        
    def to_hamiltonian(self):
        """
        Convert TSP to Hamiltonian.
        
        Variables: x_{i,t} = 1 if city i is visited at step t.
        Total variables: N^2.
        
        Constraints:
        1. Each city visited exactly once: sum_t x_{i,t} = 1 for all i.
        2. Each step has exactly one city: sum_i x_{i,t} = 1 for all t.
        
        Objective:
        Minimize distance: sum_{i,j} sum_t d_{ij} x_{i,t} x_{j,t+1}
        
        Hamiltonian:
        H = A * sum_i (sum_t x_{i,t} - 1)^2  (Row constraints)
          + A * sum_t (sum_i x_{i,t} - 1)^2  (Column constraints)
          + sum_{i,j} sum_t d_{ij} x_{i,t} x_{j,t+1} (Distance)
        """
        N = self.n_cities
        A = self.penalty
        
        # Total variables = N * N
        n_vars = N * N
        self.J = np.zeros((n_vars, n_vars))
        self.h = np.zeros(n_vars)
        
        # Helper to get index of x_{i,t}
        def idx(i, t):
            return i * N + t
            
        # 1. Constraint: Each city visited once (Row sum = 1)
        # H_row = A * sum_i (sum_t x_{i,t} - 1)^2
        #       = A * sum_i [ (sum_t x_{i,t})^2 - 2 sum_t x_{i,t} + 1 ]
        #       = A * sum_i [ sum_t x_{i,t}^2 + sum_{t!=t'} x_{i,t} x_{i,t'} - 2 sum_t x_{i,t} + 1 ]
        # Since x^2 = x for binary variables:
        #       = A * sum_i [ sum_t x_{i,t} + sum_{t!=t'} x_{i,t} x_{i,t'} - 2 sum_t x_{i,t} ]
        #       = A * sum_i [ sum_{t!=t'} x_{i,t} x_{i,t'} - sum_t x_{i,t} ]
        
        for i in range(N):
            for t in range(N):
                # Linear term: -A
                u = idx(i, t)
                self.h[u] += -A
                
                # Quadratic term: A for all pairs (t, t') with t != t'
                for t_prime in range(N):
                    if t != t_prime:
                        v = idx(i, t_prime)
                        self.J[u, v] += A
                        
        # 2. Constraint: Each step has one city (Column sum = 1)
        # H_col = A * sum_t (sum_i x_{i,t} - 1)^2
        # Similar derivation:
        #       = A * sum_t [ sum_{i!=j} x_{i,t} x_{j,t} - sum_i x_{i,t} ]
        
        for t in range(N):
            for i in range(N):
                # Linear term: -A
                u = idx(i, t)
                self.h[u] += -A
                
                # Quadratic term: A for all pairs (i, j) with i != j
                for j in range(N):
                    if i != j:
                        v = idx(j, t)
                        self.J[u, v] += A
                        
        # 3. Objective: Minimize Distance
        # H_dist = sum_{i,j} d_{ij} sum_t x_{i,t} x_{j,t+1}
        # Note: t+1 is modulo N (closed loop)
        
        for i in range(N):
            for j in range(N):
                if i == j: continue
                dist = self.distance_matrix[i, j]
                
                for t in range(N):
                    u = idx(i, t)
                    v = idx(j, (t + 1) % N)
                    
                    # Add distance to coupling
                    # Note: J is symmetric in our storage, but here we add directed term.
                    # Since x_u x_v = x_v x_u, we add to J[u,v] and J[v,u] carefully.
                    # Usually we just add to J[u,v] and let the symmetry handle it or add half.
                    # Let's add full value to J[u,v] and assume J is treated as sum J_uv x_u x_v
                    # If J is symmetric matrix in energy calculation 0.5 xJx, then we need to add to both?
                    # My previous logic (MaxCut) used J[i,j] = val; J[j,i] = val.
                    # Here u != v always (different time steps).
                    
                    self.J[u, v] += dist
                    # self.J[v, u] += dist # Don't double count if we iterate all pairs?
                    # Wait, the loop iterates all i,j. So it will encounter (j,i) later.
                    # But (j,i) term is x_{j,t} x_{i,t+1}. This is DIFFERENT from x_{i,t} x_{j,t+1}.
                    # So these are distinct terms in the Hamiltonian sum.
                    # So we just add to J[u,v].
                    # However, if the solver expects a symmetric J, we should ensure J[u,v] == J[v,u].
                    # But x_u x_v is the same as x_v x_u.
                    # So term d_{ij} x_{i,t} x_{j,t+1} contributes to interaction between u and v.
                    # We should add d_{ij} to the interaction strength.
                    # If we enforce symmetry, we can add d_{ij} to J[u,v] and J[v,u] ?
                    # Or just J[u,v] += d_{ij} and rely on solver to symmetrize?
                    # Let's add to J[u,v] and J[v,u] to be safe and explicit about the undirected interaction between variables.
                    # But wait, d_{ij} might not be equal to d_{ji} (asymmetric TSP).
                    # But x_{i,t} x_{j,t+1} connects u=(i,t) and v=(j,t+1).
                    # The reverse interaction is v=(j,t+1) and u=(i,t).
                    # This is the SAME pair of variables.
                    # So the coefficient for x_u x_v is d_{ij}.
                    # If we want symmetric J, we set J[u,v] = J[v,u] = d_{ij}.
                    # Wait, if we do that, the energy term 0.5 * (J[u,v]x_u x_v + J[v,u]x_v x_u) = d_{ij} x_u x_v.
                    # Correct.
                    
                    self.J[v, u] += dist

    def plot(self, result: Any, threshold: float = 0.5) -> None:
        """
        Visualize TSP solution.
        """
        N = self.n_cities
        x = (result.solution >= threshold).astype(int)
        
        # Decode solution
        # Find city at each step
        tour = []
        for t in range(N):
            # Find i such that x_{i,t} == 1
            cities_at_t = []
            for i in range(N):
                if x[i * N + t] == 1:
                    cities_at_t.append(i)
            
            if len(cities_at_t) == 1:
                tour.append(cities_at_t[0])
            else:
                # Invalid tour step (0 or >1 cities)
                tour.append(None)
                
        # Plot
        plt.figure(figsize=(8, 8))
        
        # Generate random positions if not provided (assuming distance matrix implies geometry)
        # For visualization, we can use MDS to project distances to 2D, or just circle if unknown.
        # Let's assume cities are on a circle for generic visualization if no coords.
        # But wait, usually TSP comes with coordinates.
        # Here we only have distance matrix.
        # Let's use simple circular layout.
        coords = np.zeros((N, 2))
        for i in range(N):
            angle = 2 * np.pi * i / N
            coords[i] = [np.cos(angle), np.sin(angle)]
            
        # Draw all cities
        plt.scatter(coords[:, 0], coords[:, 1], s=100, c='blue')
        for i in range(N):
            plt.text(coords[i, 0] * 1.1, coords[i, 1] * 1.1, str(i), fontsize=12)
            
        # Draw tour
        valid_tour = True
        if None in tour:
            valid_tour = False
            plt.title(f"Invalid Tour: {tour}")
        else:
            # Check if all cities visited
            if len(set(tour)) == N:
                plt.title(f"Valid Tour: {tour}")
                # Draw edges
                for t in range(N):
                    i = tour[t]
                    j = tour[(t + 1) % N]
                    p1 = coords[i]
                    p2 = coords[j]
                    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-')
            else:
                valid_tour = False
                plt.title(f"Incomplete Tour: {tour}")
                
        plt.axis('equal')
        plt.show()
