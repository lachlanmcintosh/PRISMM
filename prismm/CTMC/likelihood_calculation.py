
from scipy.optimize import minimize
from aneuploidy import aneuploidy
from genome_doubling import genome_doubling
import numpy as np

def neg_log_likelihood(params, observations, n, model=0):
    lam, mu = params[:2]
    G = genome_doubling(n)
    
    # 2GD Model
    if model == 2:
        s, t, u = params[2:5]
        A_s = aneuploidy(n, lam, mu, s)
        A_t = aneuploidy(n, lam, mu, t)
        A_u = aneuploidy(n, lam, mu, u)
        
        # Matrix multiplication: A_s * G * A_t * G * A_u
        T1 = np.dot(A_s, G)
        T2 = np.dot(T1, A_t)
        T3 = np.dot(T2, G)
        T = np.dot(T3, A_u)
    
    # 1GD Model
    elif model == 1:
        s, t = params[2:4]
        A_s = aneuploidy(n, lam, mu, s)
        A_t = aneuploidy(n, lam, mu, t)
        
        # Matrix multiplication: A_s * G * A_t
        T1 = np.dot(A_s, G)
        T = np.dot(T1, A_t)
        
    # No GD Model
    else:
        s, = params[2:3]
        T = aneuploidy(n, lam, mu, s)
    
    likelihood = np.prod([T[1, i]**observations[i] for i in range(len(observations))])
    
    if likelihood == 0:
        return -float('inf')
    else:
        return -np.log(likelihood)



def compute_best_likelihoods(observations, dimension):

    initial_guess_2GD = [1, 1, 1, 1, 1]
    initial_guess_1GD = [1, 1, 1, 1]
    initial_guess_no_GD = [1, 1, 1]
    
    bounds_2GD = [(0, None) for _ in range(5)]
    bounds_1GD = [(0, None) for _ in range(4)]
    bounds_no_GD = [(0, None) for _ in range(3)]

    result_2GD = minimize(neg_log_likelihood, initial_guess_2GD, args=(observations, dimension, 2), bounds=bounds_2GD, method='L-BFGS-B')
    result_1GD = minimize(neg_log_likelihood, initial_guess_1GD, args=(observations, dimension, 1), bounds=bounds_1GD, method='L-BFGS-B')
    result_no_GD = minimize(neg_log_likelihood, initial_guess_no_GD, args=(observations, dimension, 0), bounds=bounds_no_GD, method='L-BFGS-B')

    return {
        "2GD_likelihood": -result_2GD.fun,
        "2GD_params": {
            "lam": result_2GD.x[0],
            "mu": result_2GD.x[1],
            "s": result_2GD.x[2],
            "t": result_2GD.x[3],
            "u": result_2GD.x[4]
        },
        "1GD_likelihood": -result_1GD.fun,
        "1GD_params": {
            "lam": result_1GD.x[0],
            "mu": result_1GD.x[1],
            "s": result_1GD.x[2],
            "t": result_1GD.x[3]
        },
        "no_GD_likelihood": -result_no_GD.fun,
        "no_GD_params": {
            "lam": result_no_GD.x[0],
            "mu": result_no_GD.x[1],
            "s": result_no_GD.x[2]
        }
    }