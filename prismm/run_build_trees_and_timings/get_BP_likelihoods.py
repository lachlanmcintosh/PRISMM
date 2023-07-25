import logging
import numpy as np
from typing import Dict, Any, List
import re
import math








# LIKELIHOOD STUFF:

def timing_struct_to_BP_likelihood_per_chrom(
    data: Any, 
    structures: List[Dict[str, Any]], 
    p_up: int, 
    p_down: int
) -> List[Dict[str, Any]]:
    """
    Calculate the likelihood per chromosome given the timing structure and parameters.

    Parameters:
    data: The data used for calculations.
    structures: A list of structures each containing paths, CNs, epochs_created, and will include BP_individual_log_likelihoods and BP_loglikelihood.
    p_up: A parameter used in likelihood calculation.
    p_down: A parameter used in likelihood calculation.

    Returns:
    A list of structures with calculated likelihoods added.
    """
    # Validate inputs
    assert isinstance(structures, list), "Structures should be a list of dictionaries."
    assert isinstance(p_up, (int, float)), "p_up should be a numeric value."
    assert isinstance(p_down, (int, float)), "p_down should be a numeric value."

    for structure in structures: 
        assert None not in structure["epochs_created"], "Epochs_created should not contain None."

        # Calculate likelihoods
        likelihoods = calculate_likelihoods_from_paths(paths=structure["paths"], CNs=structure["CNs"], data=data, p_up=p_up, p_down=p_down)
        
        # Log debug messages
        logging.debug(f"structures\n{structures}")
        logging.debug(f"paths\n{structure['paths']}")
        logging.debug(f"likelihoods\n{likelihoods}")

        # Calculate log likelihoods
        ll = np.log(likelihoods)
        logging.debug(f"log likelihoods\n{ll}")

        # Store individual log likelihoods in structure
        structure["BP_individual_log_likelihoods"] = ll

        # Calculate and store BP likelihoods in structure
        BP_likelihood = np.sum(ll[:, 1:], axis=1)
        logging.debug(f"sum them to get BP likelihoods\n{BP_likelihood}")
        structure["BP_loglikelihood"] = BP_likelihood

    return structures

def is_GD_round(code):
    """
    Checks if the last character of the given code is 'G' or '0' versus a non-zero integer.

    Parameters:
        code (str): Code represented as a string.

    Returns:
        bool: True if the last character of the code is 'G' or '0', False if it's a non-zero integer.
    """

    while code and code[-1] == '0':
        code = code[:-1]
        if len(code) == 0: 
            return True

    if code and code[-1] == 'G':
        return True
    else:
        return False

def shorten_by_one(path):
    """
    Shortens the given path by one. If the last character is '0', it is removed along with the preceding 'G'. 
    If the path is '0', a ValueError is raised.
    """
    if path == '0':
        raise ValueError("Cannot shorten '0'")
    
    if path.endswith('G0'):
        return path[:-2]
    elif path[-1].isdigit() and int(path[-1]) > 0:
        return path[:-1] + str(int(path[-1]) - 1)
    else:
        raise ValueError(f"Invalid path: {path}")


def calculate_likelihoods_from_paths(paths, CNs, data, p_up, p_down):
    likelihoods = np.zeros(paths.shape, dtype=float, order="C")
    # TODO, make sure these are floats the entire time
    assert isinstance(p_up, int) and 0 <= p_up <= 100, f"p_up should be an integer from 0 to 100: {p_up}"
    assert isinstance(p_down, int) and 0 <= p_down <= 100, f"p_down should be an integer from 0 to 100: {p_down}"
    p_up = p_up/100.0
    p_down = p_down/100.0

    assert 0 <= p_up <= 1 and 0 <= p_down <= 1, f"p_up: {p_up}, p_down: {p_down}, p_up and p_down should be between 0 and 1"

    for row in range(paths.shape[0]):
        for col in range(paths.shape[1]):
            path = paths[row][col]
            if is_GD_round(path) or CNs[col] < 2:
                likelihood = data[path][1][min(2,CNs[col])] # the overall prob of going from CN 1 to ...min(2,CNs[col])
                # the reason for the min(2,*) is that if it is a copy number zero node then find the prob it is zero, if it is 1 then likewise, if 2 or more then it is just the prob of a bifuctation\
            else:
                # for the sake of the SNV likelihood we need the doubling up to be at the last second:
                if len(path) > 1:
                    likelihood = data[shorten_by_one(path)][1][1] * p_up
                    n = data[shorten_by_one(path)].shape[1]  # assuming 'data' is a numpy array

                    for j in range(2, n):
                        likelihood += data[shorten_by_one(path)][1][j] * p_up * (p_down ** (j-1)) * j

                else:
                    assert(len(path) == 1)
                    likelihood = data[path][1][2]



            if math.isnan(likelihood):
                logging.getLogger().setLevel(logging.DEBUG)
                logging.debug("Last element in path: %s", path[-1])
                logging.debug("Value of CNs[col]: %s", CNs[col])
                logging.debug("Value of p_up: %s", p_up)
                logging.debug("Value of p_down: %s", p_down)
                logging.debug("Calculated likelihood: %s", likelihood)
                logging.debug("Exiting the program.")
                logging.debug("Likelihood contains 'nan'. Exiting the program.")
                sys.exit()

            likelihoods[row][col] = likelihood


    if np.isnan(likelihoods).any():
        print("The likelihoods array contains NaN values. Exiting the program.")
        sys.exit()

    return likelihoods

