"""
This module precomputes matrices related to aneuploidy pathways based on user-provided parameters.
The precomputed matrices are then used to calculate the likelihood of different pathways.

Usage:
    python generate_path_likelihoods.py [p_up] [p_down] [max_CN] [path_length] [path_description]

Arguments:
    p_up: The probability of an upward mutation.
    p_down: The probability of a downward mutation.
    max_CN: The maximum copy number.
    path_length: The length of the path.
    path_description: The description of the path.
"""

import os
import argparse
import pickle
import numpy as np
from numpy import linalg as LA
import logging
import csv


# Constants
MATRIX_DIRECTORY = "MATRICES"
LOGGING_FORMAT = "%(levelname)s: %(message)s"

# Configure logging
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)

def generate_transition_matrix(path_length, u, d):
    """
    Generate a matrix based on the given path_length, u, and d.

    Parameters:
    - path_length: Integer, depth of the path.
    - u: Float, probability value for u.
    - d: Float, probability value for d.

    Returns:
    - m: numpy array, the resulting matrix.
    """

    # m[i,j] tells you the probability of going from copy number i to copy number j in 1 generation
    # m[i,j]^k tells you the probability of going from copy number i to copy number j in k generations

    dimension = 1 + 2 ** path_length
    m = np.zeros((dimension, dimension))

    # base case
    m[0, 0] = 1
    m[1, 0] = d
    m[1, 1] = 1 - u - d
    m[1, 2] = u

    # other cases
    for i in range(2, 2 ** (path_length) + 1):
        for j in range(dimension):  # This ensures you won't go out of bounds
            u_term = m[i-1, j-2] * u if j-2 >= 0 else 0
            neutral_term = m[i-1, j-1] * (1 - u - d) if j-1 >= 0 else 0
            d_term = m[i-1, j] * d
            m[i, j] = u_term + neutral_term + d_term

    return m

def load_or_create_matrices(p_up, p_down, max_CN, path_length, path_description):
    # base_filename = f"{MATRIX_DIRECTORY}/{path_description}/subbed_mat_u{p_up}_d{p_down}.pickle"
    base_filename = f"{MATRIX_DIRECTORY}/{path_description}/subbed_mat_u{p_up:.2f}_d{p_down:.2f}.pickle"
    powers_filename = base_filename.replace(".pickle", ".powers.pickle")
    precomputed_paths_filename = base_filename.replace(".pickle", ".precomputed_paths.pickle")

    genome_doubling_filename = f"{MATRIX_DIRECTORY}/{path_description}/GD.sobj"
    print(genome_doubling_filename)
    genome_doubling_matrix = load_base_matrix(genome_doubling_filename)

    if not os.path.isfile(precomputed_paths_filename):
        if not os.path.isfile(base_filename):
            anueploidy_matrix = generate_transition_matrix(path_length, p_up, p_down)
            print("generated the anueploidy matrix")
            with open(base_filename, 'wb') as m_output:
                pickle.dump(anueploidy_matrix, m_output)
                print("saved the anueploidy matrix")
        else:
            print("anueploidy matrix already exists so loading it")
            with open(base_filename, 'rb') as m_input:
                anueploidy_matrix = pickle.load(m_input)

        print("checking size")
        anueploidy_matrix, genome_doubling_matrix = ensure_correct_matrix_size(anueploidy_matrix, genome_doubling_matrix, max_CN)
        print("normalising rows")
        normalize_rows_in_anueploidy_matrix(anueploidy_matrix, max_CN)

        print("loading path combinations")
        all_paths = load_all_path_combinations(path_length,path_description)
        print("loading all single paths")
        single_paths = separate_single_paths_from_all_paths(all_paths)
        
        print("calculating all powers")
        powers = calculate_powers_of_anueploidy_matrix_for_each_single_path(anueploidy_matrix, single_paths, powers_filename)
        print("calculating all paths")
        path_dict = precompute_paths(powers, genome_doubling_matrix, all_paths, precomputed_paths_filename)


def load_base_matrix(filename):
    return load(filename)

def ensure_correct_matrix_size(anueploidy_matrix, genome_doubling_matrix, max_CN):
    max_CN_plus_two = max_CN + 2
    anueploidy_matrix = anueploidy_matrix[:max_CN_plus_two,:max_CN_plus_two]
    genome_doubling_matrix = genome_doubling_matrix[:max_CN_plus_two,:max_CN_plus_two]
    return anueploidy_matrix, genome_doubling_matrix

def normalize_rows_in_anueploidy_matrix(anueploidy_matrix, max_CN):
    for row in range(max_CN + 1):
        total = np.sum(anueploidy_matrix[row,:])
        if total != 0:
            anueploidy_matrix[row,:] /= total


def load_all_path_combinations(path_length,path_description):
    return load(f"MATRICES/{path_description}/all_path_combinations.sobj")


def separate_single_paths_from_all_paths(all_paths):
    return [x for x in all_paths if "G" not in x]


def calculate_powers_of_anueploidy_matrix_for_each_single_path(anueploidy_matrix, single_paths, powers_filename):
    if os.path.isfile(powers_filename):
        with open(powers_filename,'rb') as infile:
            powers = pickle.load(infile)
    else:
        powers = calculate_and_store_powers(anueploidy_matrix, single_paths, powers_filename)
    return powers


def calculate_and_store_powers(anueploidy_matrix, single_paths, powers_filename):
    powers = {}
    for path in single_paths:
        if int(path) not in powers:
            path_likelihood_mat = LA.matrix_power(anueploidy_matrix,int(path))
            powers[int(path)] = path_likelihood_mat
    with open(powers_filename,'wb') as infile:
        pickle.dump(powers,infile)
    return powers


def precompute_paths(powers, genome_doubling_matrix, all_paths, precomputed_paths_filename):
    if os.path.isfile(precomputed_paths_filename):
        try:
            with open(precomputed_paths_filename,'rb') as precomputed_data:
                path_dict = pickle.load(precomputed_data)
        except Exception as e:
            logging.error(f"Failed to load precomputed paths due to: {str(e)}")
            os.remove(precomputed_paths_filename)
            path_dict = {}
        path_dict = precompute_paths_for_all_paths(powers, genome_doubling_matrix, all_paths, path_dict, precomputed_paths_filename)
    else:
        path_dict = precompute_paths_for_all_paths(powers, genome_doubling_matrix, all_paths, {}, precomputed_paths_filename)
    return path_dict


def precompute_paths_for_all_paths(powers, genome_doubling_matrix, all_paths, path_dict, precomputed_paths_filename):
    count = 0
    for path in all_paths:
        if path in path_dict:
            continue
        path_dict[path] = precompute_path(powers, genome_doubling_matrix, path)
        count += 1
    with open(precomputed_paths_filename,'wb') as precomputed_data:
        pickle.dump(path_dict, precomputed_data)
    return path_dict


def precompute_path(powers, genome_doubling_matrix, path):
    splits = path.split("G")
    G1 = 0
    G2 = 0
    if len(splits) == 1:
        pre = int(path)
        mid = 0
        post = 0
    if len(splits) == 2:
        pre = int(splits[0])
        mid = 0
        post = int(splits[1])
        G1 = 1
    if len(splits) == 3:
        pre = int(splits[0])
        mid = int(splits[1])
        post = int(splits[2])
        G1 = 1
        G2 = 1

    # Compute the probabilities for this path
    path_likelihood_mat = powers[pre]

    if G1 > 0:
        path_likelihood_mat = np.matmul(path_likelihood_mat, genome_doubling_matrix)

    path_likelihood_mat = np.matmul(path_likelihood_mat, powers[mid])

    if G2 > 0:
        path_likelihood_mat = np.matmul(path_likelihood_mat, genome_doubling_matrix)

    path_likelihood_mat = np.matmul(path_likelihood_mat, powers[post])
    return path_likelihood_mat


def load(filename):
    if filename.endswith('.sobj'):
        return sage.all.load(filename)
    else:
        with open(filename, 'rb') as file:
            return pickle.load(file)


def load_precomputed_paths(p_up, p_down, path_description):
    base_filename = f"{MATRIX_DIRECTORY}/{path_description}/subbed_mat_u{p_up:.2f}_d{p_down:.2f}.precomputed_paths.pickle"
    with open(base_filename, 'rb') as infile:
        return pickle.load(infile)

def generate_table(p_up, p_down, path_description):
    all_paths_filename = f"{MATRIX_DIRECTORY}/{path_description}/all_path_combinations.sobj"
    all_paths = load(all_paths_filename)

    precomputed_paths = load_precomputed_paths(p_up, p_down, path_description)
    table_filename = f"{MATRIX_DIRECTORY}/{path_description}/table_u{p_up:.2f}_d{p_down:.2f}.csv"

    with open(table_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
 
        # Write the header
        num_columns = precomputed_paths[list(precomputed_paths.keys())[0]].shape[1]
        header = ["path", "p_up", "p_down"] + [f"CN_{i}" for i in range(num_columns)]
        csvwriter.writerow(header)

        for path in all_paths:
            if path in precomputed_paths:
                row_data = [path, p_up, p_down] + list(precomputed_paths[path][1, :])
                csvwriter.writerow(row_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate path likelihood matrices based on user-provided parameters.")
    parser.add_argument('p_up', type=float, help="The probability of an upward mutation.")
    parser.add_argument('p_down', type=float, help="The probability of a downward mutation.")
    parser.add_argument('max_CN', type=int, help="The maximum copy number.")
    parser.add_argument('path_length', type=int, help="The length of the path.")
    parser.add_argument('path_description', type=str, help="The description of the path.")
    
    args = parser.parse_args()

    load_or_create_matrices(args.p_up, args.p_down, args.max_CN, args.path_length, args.path_description)
    generate_table(args.p_up, args.p_down, args.path_description)

