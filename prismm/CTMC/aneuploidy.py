import numpy as np
from scipy.linalg import expm

def aneuploidy(n, lam, mu, s):
    Q = np.zeros((n, n))
    for i in range(n):
        if i != 0:
            Q[i, i-1] = lam * i
        if i != n-1:
            Q[i, i+1] = mu * i
        Q[i, i] = -np.sum(Q[i])
    return expm(s * Q)
