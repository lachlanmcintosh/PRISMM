import numpy as np

def genome_doubling(n):
    G = np.zeros((n, n))
    for i in range(n):
        if 2 * i < n:
            G[i, 2 * i] = 1
        else:
            G[i, i] = 1
    return G
