from prismm.utils.path_codes import pre_mid_post_to_path_length
from prismm.run_build_trees_and_timings.get_all_trees import get_all_trees
from prismm.run_build_trees_and_timings.add_timings_to_trees import add_timings_to_trees
import logging
import numpy as np
from typing import Dict

def add_branch_lengths_to_timings_and_trees_per_chrom(trees_and_timings, pre_est, mid_est, post_est, total_epochs_est):
    logging.debug("trees_and_timings")
    logging.debug(trees_and_timings)
    all_structures = [] 
    for index, these_tts in enumerate(trees_and_timings):  # these tts are a 2d array
        if None in these_tts[3]:
            continue
            #BP_likelihoods = -1
        else:
            # trace back to here, asdfasdf
            CNs, unique_CNs, branch_lengths, stacked_branch_lengths = get_branch_lengths(trees_and_timings=these_tts, max_epoch=total_epochs_est)

            logging.debug("CNs, unique_CNs, branch_lengths, stacked_branch_lengths")
            logging.debug(f"{CNs}, {unique_CNs}, {branch_lengths}, {stacked_branch_lengths}")
            logging.debug("starts and ends")

            path_est = create_path(pre_est, mid_est, post_est)

            logging.debug(path_est)

            starts = these_tts[3] #+1
            ends = these_tts[3] + branch_lengths #+1

            logging.debug("starts")
            logging.debug(starts)
            logging.debug("ends")
            logging.debug(ends)

            paths = calculate_BP_paths(branch_lengths, starts, ends, path_est)

        tree, labelled_tree, count, epochs_created, parents = these_tts

        all_structures += [{
            "pre_est": pre_est,
            "mid_est": mid_est,
            "post_est": post_est,
            "path_est": path_est,
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

def add_branch_lengths_to_timings_and_trees(trees_and_timings, pre_est, mid_est, post_est, total_epochs_est):
    all_structures = {}
    
    for chrom in trees_and_timings:
        all_structures[chrom] = add_branch_lengths_to_timings_and_trees_per_chrom(trees_and_timings = trees_and_timings[chrom], 
                                                                        pre_est = pre_est, 
                                                                        mid_est = mid_est, 
                                                                        post_est = post_est, 
                                                                        total_epochs_est = total_epochs_est
                                                                        )

    return all_structures

import sys

def get_annotated_trees_and_timings(SS, pre_est, mid_est, post_est, tree_flexibility):

    total_epochs_est = pre_mid_post_to_path_length(pre_est, mid_est, post_est)

    #start_time_trees_and_timings = time.time()
    trees = get_all_trees(
        observed_SNV_multiplicities=SS["observed_SNV_multiplicities"],
        observed_copy_numbers=SS["observed_copy_numbers"],
        total_epochs_est=total_epochs_est,
        tree_flexibility=tree_flexibility
    )
    logging.debug("got all the trees")
    for chrom in trees:
        logging.debug(trees[chrom])

    trees_and_timings = add_timings_to_trees( 
        trees=trees,
        total_epochs_est=total_epochs_est
    )

    logging.debug("got all the timings too")
    for chrom in trees_and_timings:
        logging.debug(trees_and_timings[chrom])
        
    sys.exit()
    #end_time_trees_and_timings = time.time()

    #aggregated_execution_times["get_all_trees_and_timings"] += round(end_time_trees_and_timings - start_time_trees_and_timings, 2)

    #if trees_and_timings is None:
    #    continue

    #start_time_all_structures = time.time()
    annotated_trees_and_timings = add_branch_lengths_to_timings_and_trees(
        trees_and_timings=trees_and_timings,
        pre_est=pre_est,
        mid_est=mid_est,
        post_est=post_est,
        total_epochs_est=total_epochs_est
    )
    #end_time_all_structures = time.time()

    #aggregated_execution_times["timing_struct_to_all_structures"] += round(end_time_all_structures - start_time_all_structures, 2)

    return annotated_trees_and_timings


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

def extract_copy_numbers(tree):
    CNs = [x for x in re.split("\(|\)|,|'", str(tree)) if x.isdigit()]
    CNs = [int(x) for x in CNs]
    return CNs


def find_indices(list_to_check, item_to_find):
    indices = [i for i, x in enumerate(list_to_check) if x == item_to_find]
    return indices

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


