import numpy as np
from numpy.random import multinomial
from aneuploidy import aneuploidy
from genome_doubling import genome_doubling



# Function to generate simulated observations given a transition matrix and starting state
def generate_observations(transition_matrix, start_state, num_observations):
    observations = np.random.multinomial(num_observations, transition_matrix[start_state, :])
    return observations


# Given parameters and model, compute the transition matrix
def compute_transition_matrix(params, n, model=0):
    lam, mu = params[:2]
    G = genome_doubling(n)

    if model == 2:  # 2GD
        s, t, u = params[2:5]
        A_s = aneuploidy(n, lam, mu, s)
        A_t = aneuploidy(n, lam, mu, t)
        A_u = aneuploidy(n, lam, mu, u)
        
        T1 = np.dot(A_s, G)
        T2 = np.dot(T1, A_t)
        T3 = np.dot(T2, G)
        T = np.dot(T3, A_u)
    
    elif model == 1:  # 1GD
        s, t = params[2:4]
        A_s = aneuploidy(n, lam, mu, s)
        A_t = aneuploidy(n, lam, mu, t)
        
        T1 = np.dot(A_s, G)
        T = np.dot(T1, A_t)
        
    else:  # no GD
        s, = params[2:3]
        T = aneuploidy(n, lam, mu, s)

    return T