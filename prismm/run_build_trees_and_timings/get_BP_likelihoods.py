import logging
import numpy as np
from typing import Dict
import re
import math

def find_non_parent_children(parents):
    """
    Find children that are not parents in the given parent-child relationship dictionary.

    Args:
        parents (dict): A dictionary with keys as child indices and values as their parent indices.

    Returns:
        set: A set of child indices that are not parents.
    """
    all_children = set(parents.keys())
    all_parents = set(parents.values())
    non_parent_children = all_children.difference(all_parents)
    return non_parent_children

def test_find_non_parent_children():
    parents = {1: 0, 2: 0, 4: 3, 5: 3}
    expected_non_parent_children = {1, 2, 4, 5}
    non_parent_children = find_non_parent_children(parents)
    assert non_parent_children == expected_non_parent_children, f"Expected {expected_non_parent_children}, but got {non_parent_children}"

# Run the test function
test_find_non_parent_children()


def calculate_child_parent_diff(epochs_created: np.ndarray, parents: Dict, max_epoch: int):
    """
    Calculate the difference between child and parent epochs.

    Args:
        epochs_created (np.ndarray): A 2D numpy array containing the epochs when elements were created.
        parents (Dict): A dictionary with keys as child indices and values as their parent indices.
        epochs (int): The total number of epochs.

    Returns:
        np.ndarray: A 2D numpy array containing the difference between child and parent epochs.
    """
    assert isinstance(epochs_created, np.ndarray) and epochs_created.ndim == 2, f"epochs_created must be a 2D numpy array, but was {type(epochs_created)} with dimensions {epochs_created.ndim}. epochs_created: {str(epochs_created)}"

    assert isinstance(parents, dict), f"parents must be a dictionary, but was {type(parents)}"
    
    branch_lengths = np.copy(epochs_created)
    for child in parents: 
        branch_lengths[:, parents[child]] = epochs_created[:, child] - epochs_created[:, parents[child]]

    non_parent_children = find_non_parent_children(parents)
    for column in non_parent_children:
        branch_lengths[:, column] = max_epoch - epochs_created[:, column]
        
    return branch_lengths

def test_calculate_child_parent_diff():
    # First test case
    epochs_created = np.array([[-1, 0, 1, 1, 1, 1, 0],
                               [-1, 0, 1, 2, 2, 1, 0],
                               [-1, 0, 2, 2, 2, 2, 0],
                               [-1, 1, 2, 2, 2, 2, 1]], dtype=object)
    parents = {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0}
    max_epoch = 2
    result = calculate_child_parent_diff(epochs_created, parents, max_epoch)
    expected = np.array([[1, 1, 0, 1, 1, 1, 2],
                         [1, 1, 1, 0, 0, 1, 2],
                         [1, 2, 0, 0, 0, 0, 2],
                         [2, 1, 0, 0, 0, 0, 1]], dtype=object)
    assert np.array_equal(result, expected), f"calculate_child_parent_diff returned incorrect values.\nExpected: {expected}\nGot: {result}"

    # Second test case
    epochs_created = np.array([[-1, 0, 1, 1, 1, 1, 1, 1, 0],
                               [-1, 0, 1, 1, 1, 1, 2, 2, 0],
                               [-1, 0, 1, 2, 2, 1, 1, 1, 0],
                               [-1, 0, 1, 2, 2, 1, 2, 2, 0],
                               [-1, 0, 2, 2, 2, 2, 2, 2, 0],
                               [-1, 1, 2, 2, 2, 2, 2, 2, 1]], dtype=object)
    parents = {3: 2, 4: 2, 2: 1, 6: 5, 7: 5, 5: 1, 1: 0, 8: 0}
    max_epoch = 2
    result = calculate_child_parent_diff(epochs_created, parents, max_epoch)
    expected = np.array([[1, 1, 0, 1, 1, 0, 1, 1, 2],
                         [1, 1, 0, 1, 1, 1, 0, 0, 2],
                         [1, 1, 1, 0, 0, 0, 1, 1, 2],
                         [1, 1, 1, 0, 0, 1, 0, 0, 2],
                         [1, 2, 0, 0, 0, 0, 0, 0, 2],
                         [2, 1, 0, 0, 0, 0, 0, 0, 1]], dtype=object)
    assert np.array_equal(result, expected), f"calculate_child_parent_diff returned incorrect values.\nExpected: {expected}\nGot: {result}"


test_calculate_child_parent_diff()

def extract_copy_numbers(tree):
    CNs = [x for x in re.split("\(|\)|,|'", str(tree)) if x.isdigit()]
    CNs = [int(x) for x in CNs]
    return CNs


def test_extract_copy_numbers():
    tree = "(3,(1,1))"
    CNs = extract_copy_numbers(tree)
    assert CNs == [3, 1, 1], "extract_copy_numbers returned incorrect CNs"


test_extract_copy_numbers()


def stack_same_CN_branch_lengths(unique_CNs, CNs, branch_lengths):
    for i, CN in enumerate(unique_CNs):
        indices = find_indices(CNs, CN)
        new_stacked_branch_lengths = branch_lengths[:, indices].sum(axis=1)

        if i == 0:
            stacked_branch_lengths = new_stacked_branch_lengths
        else:
            stacked_branch_lengths = np.vstack((stacked_branch_lengths, new_stacked_branch_lengths))

    return np.transpose(stacked_branch_lengths)

def stack_same_CN_branch_lengths(CNs, branch_lengths):
    """
    Stacks branch lengths of the same copy number state.

    Arguments:
    unique_CNs -- a list of unique copy number states.
    CNs -- a list of copy number states, matching the second dimension of branch_lengths.
    branch_lengths -- a 2D array where the second dimension matches CNs.

    Returns:
    A 2D numpy array where branch lengths of the same copy number state have been stacked.
    """
    # Remove the first column
    CNs = CNs[1:]
    branch_lengths = branch_lengths[:, 1:]
    unique_CNs = sorted(list(set(CNs)), reverse = True)

    for i, CN in enumerate(unique_CNs):
        indices = find_indices(CNs, CN)
        new_stacked_branch_lengths = branch_lengths[:, indices].sum(axis=1)

        if i == 0:
            stacked_branch_lengths = new_stacked_branch_lengths
        else:
            stacked_branch_lengths = np.vstack((stacked_branch_lengths, new_stacked_branch_lengths))

    return np.transpose(stacked_branch_lengths), unique_CNs

def find_indices(list_to_check, item_to_find):
    indices = [i for i, x in enumerate(list_to_check) if x == item_to_find]
    return indices

def test_find_indices():
    test_list = [1, 2, 3, 2, 4, 2, 5]
    item = 2
    indices = find_indices(test_list, item)
    assert indices == [1, 3, 5], "find_indices returned incorrect indices"


def stack_same_CN_branch_lengths(CNs, branch_lengths):
    """
    Stacks branch lengths of the same copy number state.

    Arguments:
    CNs -- a list of copy number states, matching the second dimension of branch_lengths.
    branch_lengths -- a 2D array where the second dimension matches CNs.

    Returns:
    A 2D numpy array where branch lengths of the same copy number state have been stacked.
    """
    # Remove the first column
    CNs = CNs[1:]
    branch_lengths = branch_lengths[:, 1:]
    unique_CNs = sorted(list(set(CNs)), reverse=True)

    stacked_branch_lengths = []  # Initialize an empty list

    for CN in unique_CNs:
        indices = find_indices(CNs, CN)
        new_stacked_branch_lengths = branch_lengths[:, indices].sum(axis=1)
        stacked_branch_lengths.append(new_stacked_branch_lengths)

    stacked_branch_lengths = np.vstack(stacked_branch_lengths).T

    return stacked_branch_lengths, unique_CNs



def test_stack_same_CN_branch_lengths():
    # First test case
    unique_CNs = [5, 3, 2, 1]
    CNs = [5, 3, 2, 1, 1, 1, 2, 1, 1]
    branch_lengths = np.array([[1, 1, 0, 1, 1, 1, 0, 2, 2],
                               [1, 1, 0, 1, 1, 1, 1, 1, 1],
                               [1, 1, 0, 1, 1, 1, 2, 0, 0],
                               [1, 1, 1, 0, 0, 1, 0, 2, 2],
                               [1, 1, 1, 0, 0, 1, 1, 1, 1],
                               [1, 1, 1, 0, 0, 1, 2, 0, 0],
                               [1, 2, 0, 0, 0, 0, 0, 2, 2],
                               [1, 2, 0, 0, 0, 0, 1, 1, 1],
                               [1, 2, 0, 0, 0, 0, 2, 0, 0],
                               [2, 1, 0, 0, 0, 0, 0, 1, 1],
                               [2, 1, 0, 0, 0, 0, 1, 0, 0]], dtype=object)
    result = stack_same_CN_branch_lengths(CNs, branch_lengths)
    expected = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
                         [1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1],
                         [0, 1, 2, 1, 2, 3, 0, 1, 2, 0, 1],
                         [7, 5, 3, 5, 3, 1, 4, 2, 0, 2, 0]], dtype=object).T
    assert np.array_equal(result, expected), f"stack_same_CN_branch_lengths returned incorrect values.\nExpected: {expected}\nGot: {result}"

    # Second test case
    unique_CNs = [3, 2, 1, 0]
    CNs = [3, 3, 2, 1, 1, 1, 0]
    branch_lengths = np.array([[1, 1, 0, 1, 1, 1, 2],
                               [1, 1, 1, 0, 0, 1, 2],
                               [1, 2, 0, 0, 0, 0, 2],
                               [2, 1, 0, 0, 0, 0, 1]], dtype=object)
    result = stack_same_CN_branch_lengths(CNs, branch_lengths)
   
    expected = np.array([[2, 2, 3, 3],
                         [0, 1, 0, 0],
                         [3, 1, 0, 0],
                         [2, 2, 2, 1]], dtype=object).T
    assert np.array_equal(result, expected), f"stack_same_CN_branch_lengths returned incorrect values.\nExpected: {expected}\nGot: {result}"

    # Third test case
    unique_CNs = [4, 2, 1, 0]
    CNs = [4, 4, 2, 1, 1, 2, 1, 1, 0]
    branch_lengths = np.array([[1, 1, 0, 1, 1, 0, 1, 1, 2],
                               [1, 1, 0, 1, 1, 1, 0, 0, 2],
                               [1, 1, 1, 0, 0, 0, 1, 1, 2],
                               [1, 1, 1, 0, 0, 1, 0, 0, 2],
                               [1, 2, 0, 0, 0, 0, 0, 0, 2],
                               [2, 1, 0, 0, 0, 0, 0, 0, 1]], dtype=object)
    result = stack_same_CN_branch_lengths(CNs, branch_lengths)
    expected = np.array([[2, 2, 2, 2, 3, 3],
                         [0, 1, 1, 2, 0, 0],
                         [4, 2, 2, 0, 0, 0],
                         [2, 2, 2, 2, 2, 1]], dtype=object).T
    assert np.array_equal(result, expected), f"stack_same_CN_branch_lengths returned incorrect values.\nExpected: {expected}\nGot: {result}"


#test_stack_same_CN_branch_lengths()



def get_branch_lengths(trees_and_timings, max_epoch):
    tree, labelled_tree, count, epochs_created, parents = trees_and_timings
    branch_lengths = calculate_child_parent_diff(
        epochs_created = epochs_created, 
        parents = parents,
        max_epoch = max_epoch
    )
    CNs = extract_copy_numbers(tree)
    stacked_branch_lengths,unique_CNs = stack_same_CN_branch_lengths(CNs, branch_lengths)
   
    logging.debug("trees_and_timings")
    logging.debug(str(trees_and_timings))
    logging.debug("max_epoch")
    logging.debug(max_epoch)
    logging.debug("branch_lengths")
    logging.debug(branch_lengths)
    logging.debug("stacked_branch_lengths")
    logging.debug(stacked_branch_lengths)

    return CNs, unique_CNs, branch_lengths, stacked_branch_lengths


def get_path_code(code_list):
    output = ""
    count = 0

    for code in code_list:
        if code == "A":
            count += 1
        elif code == "GD":
            output += str(count)
            count = 0
            output += "G"

    output += str(count)
    return output

# Configure logging settings (you only need to do this once in your script or module)
# this would be a good idea to use throughout the script

def timing_struct_to_all_structures(trees_and_timings, pre, mid, post, max_epoch):
    all_structures = {}
    
    for chrom in trees_and_timings:
        all_structures[chrom] = timing_structs_to_all_structs_per_chrom(trees_and_timings[chrom], pre, mid, post, max_epoch)

    

    return all_structures


def timing_structs_to_all_structs_per_chrom(trees_and_timings, pre, mid, post, max_epoch):
    logging.debug("trees_and_timings")
    logging.debug(trees_and_timings)
    all_structures = [] 
    for index, these_tts in enumerate(trees_and_timings):  # these tts are a 2d array
        if None in these_tts[3]:
            continue
            #BP_likelihoods = -1
        else:
            # trace back to here, asdfasdf
            CNs, unique_CNs, branch_lengths, stacked_branch_lengths = get_branch_lengths(trees_and_timings=these_tts, max_epoch=max_epoch)

            logging.debug("CNs, unique_CNs, branch_lengths, stacked_branch_lengths")
            logging.debug(f"{CNs}, {unique_CNs}, {branch_lengths}, {stacked_branch_lengths}")
            logging.debug("starts and ends")

            path = create_path(pre, mid, post)

            logging.debug(path)

            starts = these_tts[3] #+1
            ends = these_tts[3] + branch_lengths #+1

            logging.debug("starts")
            logging.debug(starts)
            logging.debug("ends")
            logging.debug(ends)

            paths = calculate_BP_paths(branch_lengths, starts, ends, path)

        tree, labelled_tree, count, epochs_created, parents = these_tts

        all_structures += [{
            "pre": pre,
            "mid": mid,
            "post": post,
            "path": path,
            "tree": tree,
            "parents": parents,
            "labelled_tree": labelled_tree,
            "count": count,
            "epochs_created": epochs_created,
            "CNs": CNs,
            "branch_lengths": branch_lengths,
            "unique_CNs": unique_CNs,
            "stacked_branch_lengths": stacked_branch_lengths,
            "starts":starts,
            "ends":ends,
            "paths":paths
        }]

    return all_structures



def timing_struct_to_BP_likelihood_per_chrom(data, structures, p_up, p_down):
    #logging.getLogger().setLevel(logging.DEBUG)

    all_BP_likelihoods = []

    for structure in structures: 
        assert(None not in structure["epochs_created"])
        logging.debug("structures")
        logging.debug(structures)

        likelihoods = calculate_likelihoods_from_paths(paths=structure["paths"], CNs=structure["CNs"], data=data, p_up=p_up, p_down=p_down)

        logging.debug("paths")
        logging.debug(structure["paths"])

        logging.debug("likelihoods")
        logging.debug(likelihoods)

        ll = np.log(likelihoods)
        
        logging.debug("log likelihoods")
        logging.debug(ll)
        structure["BP_individual_log_likelihoods"] = ll

        BP_likelihood = np.sum(ll[:, 1:], axis=1)

        logging.debug("sum them to get BP likelihoods")
        logging.debug(BP_likelihood)

        structure["BP_loglikelihood"] = BP_likelihood

    #logging.getLogger().setLevel(logging.INFO)




def create_path(pre, mid, post):
    path = []
    if pre > 0:
        path += ["A"] * pre
    if mid > -1:
        path += ["GD"]
    if mid > 0:
        path += ["A"] * mid
    if post > -1:
        path += ["GD"]
    if post > 0:
        path += ["A"] * post

    return path


def calculate_BP_paths(branch_lengths, starts, ends, path):
    paths = np.zeros(ends.shape, dtype=object, order="C")

    for row in range(branch_lengths.shape[0]):
        for col in range(branch_lengths.shape[1]):

            these_paths = path[starts[row][col] : ends[row][col]]  # MODIFIED THIS, BUT NOT ENTIRELY SURE, CHECK, ERROR
            path_code = get_path_code(these_paths)

            paths[row][col] = path_code

    # this needs to be updated for paths with length longer than 1. 
    # suppose a path was like GG1. The branching process can take this and calculate a probability, however when the SNV likelihood doe sthe same thing it gives an incompatible probability. 
    # the SNV likelihood needs to know how long SNV can accumulate on a branch. for SNVs to accurately take iunto consideration of how lon g they can accumulate, the BP lieklihood needs to recognise this. 

    # therefore GG1 really needs to look like p(GG1) = p(GD, GD) * p(D)^3 * 4 * p(L)
    # this is not straightforward to program. How do we do it?
    # furthermroe, how do we recognise it?
    #

    # first we recoginise this phenomenum as occuring to paths greater than length 1. all other paths naturally work.
    # P(GG1 1 to 2 true) = P(GG1 1 to 1) * UA/(1-U-D)
    # this works because there si always one chromosome where nothing happens to it. in the 1 to 1 caseA

    # does this also work fro paths of length 1?
    # yes if it is a non genome doubling one. 
    # actually it always works unless the last epoch is a gd one. then it is just the usual. /calculate_BP_paths

    return paths


def check_last_character(code):
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

    if code and code[-1] in {'G', '0'}:
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

    assert isinstance(p_up, int) and 0 <= p_up <= 100, f"p_up should be an integer from 0 to 100: {p_up}"
    assert isinstance(p_down, int) and 0 <= p_down <= 100, f"p_down should be an integer from 0 to 100: {p_down}"
    p_up = p_up/100.0
    p_down = p_down/100.0

    assert 0 <= p_up <= 1 and 0 <= p_down <= 1, f"p_up: {p_up}, p_down: {p_down}, p_up and p_down should be between 0 and 1"


    for row in range(paths.shape[0]):
        for col in range(paths.shape[1]):
            path = paths[row][col]
            if check_last_character(path) or CNs[col] < 2:
                likelihood = data[path][1][min(2,CNs[col])] # the prob of going from CN 1 to ...
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

