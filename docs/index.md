# Welcome to KOPPU

**K-dimensional Organoid Probabilistic Processing Unit**

KOPPU is a project designed to interface with organoid processing units. This repository contains the `pykoppu` SDK.

## Getting Started

### Installation

```bash
pip install pykoppu
```

### Basic Usage

```python
import networkx as nx
from pykoppu import Process, MaxCut

# 1. Define a problem
G = nx.erdos_renyi_graph(10, 0.5)
problem = MaxCut(G)

# 2. Create a process
process = Process(problem, backend="brian2")

# 3. Run
result = process.run()
print(result)
```
