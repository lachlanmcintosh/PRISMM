import random
import math
import numpy as np
import logging

def sample_SNV_rate_on_uniform_log_scale(min_value: int, max_value: int) -> int:
    """
    Generate a random integer between min_value and max_value on a logarithmic scale.
    
    Parameters:
    min_value (int): The lower limit for the generated random integer.
    max_value (int): The upper limit for the generated random integer.

    Returns:
    int: A random integer between min_value and max_value on a logarithmic scale.
    """
    if min_value <= 0 or max_value <= 0:
        raise ValueError("Both min_value and max_value should be positive")

    log_min = math.log(min_value)
    log_max = math.log(max_value)
    random_log = random.uniform(log_min, log_max)

    # this needn't be an integer, but it simplifies reading the logs of the simulation at no cost
    return int(round(math.exp(random_log)))


def sample_p_up_and_p_down_from_dirichelet_distribution(alpha: list) -> np.ndarray:
    """
    Generate probabilities based on the Dirichlet distribution.
    
    Parameters:
    alpha (list): Parameters of the Dirichlet distribution.

    Returns:
    np.ndarray: An array of probabilities.
    """
    if len(alpha) != 3:
        raise ValueError("alpha should have exactly 3 elements")

    probabilities = np.random.dirichlet(alpha)

    # Round probabilities to 2 decimal places
    probabilities = np.round(probabilities, 2)
    probabilities = probabilities[:2]

    for prob in probabilities:
        assert prob == round(prob, 2)
        assert 0 <= prob <= 1, "p_up must be between 0 and 1 inclusive"
    
    return probabilities


def sample_num_anueploidy_epochs_before_GD_from_trimmed_poisson_distribution(max_value: int, lam: float, max_attempts: int = 10000) -> int:
    """
    Generate a random number from a Poisson distribution, 
    where the number is within the range defined by min_value and max_value.
    
    Parameters:
    max_value (int): The maximum value that can be generated.
    lam (float): The lambda parameter for the Poisson distribution.
    max_attempts (int, optional): The maximum number of attempts to generate the number. Defaults to 10000.

    Returns:
    int: A random number generated from a Poisson trimmed distribution.
    """
    if max_value < 0 or lam < 0 or max_attempts <= 0:
        raise ValueError("max_value, lam should be non-negative and max_attempts should be positive")

    for _ in range(max_attempts):
        value = np.random.poisson(lam)
        if 0 <= value <= max_value:
            return value

    logging.error(f"Could not generate a suitable random number within {max_attempts} attempts.")
    raise ValueError(f"Could not generate a suitable random number within {max_attempts} attempts.")
