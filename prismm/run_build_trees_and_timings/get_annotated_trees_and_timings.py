from prismm.utils.path_codes import pre_mid_post_to_path_length
from prismm.run_build_trees_and_timings.get_all_trees import get_all_trees
from prismm.run_build_trees_and_timings.add_timings_to_trees import add_timings_to_trees
from prismm.utils.path_codes import create_path
import logging
import numpy as np
from typing import Dict, List, Tuple, Any
import re

def calculate_branch_lengths(epochs_created: np.ndarray, parents: Dict[int, int], total_epochs_est: int) -> np.ndarray:
    """
    Calculate the difference between child and parent epochs.

    Args:
        epochs_created (np.ndarray): A 2D numpy array containing the epochs when elements were created.
        parents (Dict[int, int]): A dictionary with keys as child indices and values as their parent indices.
        total_epochs_est (int): The total number of epochs.

    Returns:
        np.ndarray: A 2D numpy array containing the difference between child and parent epochs.
    """

    # Input validation
    if not isinstance(epochs_created, np.ndarray) or epochs_created.ndim != 2:
        logging.error(f"epochs_created must be a 2D numpy array, but was {type(epochs_created)} with dimensions {epochs_created.ndim}. epochs_created: {str(epochs_created)}")
        return None

    if not isinstance(parents, dict):
        logging.error(f"parents must be a dictionary, but was {type(parents)}")
        return None

    # Find leaf nodes
    all_children = set(parents.keys())
    all_parents = set(parents.values())
    leaf_nodes = all_children.difference(all_parents)

    branch_lengths = np.copy(epochs_created)
    for child in parents: 
        branch_lengths[:, parents[child]] = epochs_created[:, child] - epochs_created[:, parents[child]]

    for leaf in leaf_nodes:
        branch_lengths[:, leaf] = total_epochs_est - epochs_created[:, leaf]
        
    return branch_lengths


def extract_copy_numbers(tree: Tuple) -> List[int]:
    """
    Extract copy numbers from the given tree.

    Arguments:
    tree -- an object representing a tree.

    Returns:
    A list of copy numbers extracted from the tree.
    """
    # Adjusted regex to also split on spaces
    tree_elements = re.split("\(|\)|,|'|\s", str(tree))

    # Filter out non-digit elements and convert to integers
    copy_numbers = [int(element) for element in tree_elements if element.isdigit()]

    return copy_numbers


def find_indices(list_to_check: List[Any], item_to_find: Any) -> List[int]:
    """
    Find indices of a specific item in a list.

    Arguments:
    list_to_check -- the list in which to find the item.
    item_to_find -- the item to find in the list.

    Returns:
    A list of indices where the item is found.
    """
    # Check if the list is empty
    assert list_to_check, "Input list is empty."

    indices = [index for index, element in enumerate(list_to_check) if element == item_to_find]

    return indices


def stack_same_CN_branch_lengths(copy_numbers: List[int], branch_lengths: np.ndarray) -> Tuple[np.ndarray, List[int]]:
    """
    Stack branch lengths of the same copy number state.

    Arguments:
    copy_numbers -- a list of copy number states, matching the second dimension of branch_lengths.
    branch_lengths -- a 2D array where the second dimension matches copy_numbers.

    Returns:
    A tuple containing a 2D numpy array where branch lengths of the same copy number state have been stacked, 
    and a list of unique copy number states.
    """
    # Check if the copy_numbers list and second dimension of branch_lengths have the same size
    assert len(copy_numbers) == branch_lengths.shape[1], "Copy numbers and branch lengths dimension mismatch."
    assert len(copy_numbers) >= 2

    # Remove the root node
    copy_numbers = copy_numbers[1:]
    branch_lengths = branch_lengths[:, 1:]

    # Get unique copy numbers in descending order
    unique_copy_numbers = sorted(set(copy_numbers), reverse=True)

    stacked_branch_lengths = []

    for copy_number in unique_copy_numbers:
        indices = find_indices(copy_numbers, copy_number)

        # Sum the branch lengths along the specified axis (column-wise sum)
        new_stacked_branch_lengths = branch_lengths[:, indices].sum(axis=1)

        stacked_branch_lengths.append(new_stacked_branch_lengths)

    # Stack arrays in sequence vertically (row-wise)
    stacked_branch_lengths = np.vstack(stacked_branch_lengths).T

    return stacked_branch_lengths, unique_copy_numbers

def get_branch_lengths(tts: Dict[str, Any], total_epochs_est: int) -> Dict[str, Any]:
    """
    Calculate branch lengths, extract copy numbers, stack branch lengths of the same copy number state, and find unique copy numbers.
    
    Args:
        tts (Dict[str, Any]): A dictionary containing 'epochs_created', 'parents', and 'tree' as keys.
        total_epochs_est (int): The total number of epochs.

    Returns:
        Dict[str, Any]: The updated dictionary with added 'branch_lengths', 'CNs', 'stacked_branch_lengths', and 'unique_CNs'.
    """
    # Input validation
    if not isinstance(tts, dict):
        logging.error(f"tts must be a dictionary, but was {type(tts)}")
        return None

    if not isinstance(total_epochs_est, int) or total_epochs_est < 0:
        logging.error(f"total_epochs_est must be a non-negative integer, but was {type(total_epochs_est)} with value {total_epochs_est}")
        return None

    tts["branch_lengths"] = calculate_branch_lengths(
        epochs_created=tts.get("epochs_created"), 
        parents=tts.get("parents"),
        total_epochs_est=total_epochs_est
    )
    
    if tts["branch_lengths"] is None:
        return None

    tts["CNs"] = extract_copy_numbers(tts.get("tree"))
    
    stacked_branch_lengths, unique_CNs = stack_same_CN_branch_lengths(tts["CNs"], tts["branch_lengths"])
    
    if stacked_branch_lengths is None or unique_CNs is None:
        return None

    tts["stacked_branch_lengths"] = stacked_branch_lengths
    tts["unique_CNs"] = unique_CNs


def generate_path_code(path: List[str]) -> str:
    """
    This function takes a list of codes and generates a path code string.
    It treats "A" as an increment to a count, and "GD" as a delimiter to separate
    chunks of counts with "G".

    Args:
    path: A list of string codes. 

    Returns:
    A string representing the path code.
    """
    path_code = ""
    count = 0

    for code in path:
        if code == "A":
            count += 1
        elif code == "GD":
            path_code += str(count)
            count = 0
            path_code += "G"

    path_code += str(count)
    return path_code


def calculate_branch_process_paths(branch_lengths: np.ndarray, starts: np.ndarray, ends: np.ndarray, path: List[str]) -> np.ndarray:
    """
    This function calculates the paths in a branching process.

    Args:
    branch_lengths: A 2D numpy array representing the lengths of the branches.
    starts: A 2D numpy array representing the start points for each path.
    ends: A 2D numpy array representing the end points for each path.
    path: A list of string codes that represent the path.

    Returns:
    A 2D numpy array with the same shape as branch_lengths, filled with path codes.
    """
    assert branch_lengths.shape == starts.shape == ends.shape, "The input arrays must have the same shape."
    assert len(path) >= np.max(ends), "The path list should be at least as long as the maximum value in the ends array."

    paths = np.zeros(branch_lengths.shape, dtype=object, order="C")

    for row in range(branch_lengths.shape[0]):
        for col in range(branch_lengths.shape[1]):
            these_paths = path[starts[row][col] : ends[row][col]]
            path_code = generate_path_code(these_paths)
            paths[row][col] = path_code

    return paths


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


import sys
def add_branch_lengths_to_timings_and_trees_per_chrom(trees_and_timings, pre_est, mid_est, post_est, total_epochs_est):
    logging.debug("trees_and_timings")
    logging.debug(trees_and_timings)
    all_structures = [] 
    for these_tts in trees_and_timings: 

        # trace back to here, asdfasdf
        get_branch_lengths(tts=these_tts, total_epochs_est=total_epochs_est)
        print(these_tts.keys())


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

def get_annotated_trees_and_timings(observed_SNV_multiplicities, observed_copy_numbers, pre_est, mid_est, post_est, tree_flexibility):

    logging.debug(f"pre_est, mid_est, post_est: {(pre_est, mid_est, post_est)}")

    #start_time_trees_and_timings = time.time()
    trees = get_all_trees(
        observed_SNV_multiplicities=observed_SNV_multiplicities,
        observed_copy_numbers=observed_copy_numbers,
        pre_est=pre_est, 
        mid_est=mid_est, 
        post_est=post_est,
        tree_flexibility=tree_flexibility
    )
    
    logging.debug("got all the trees")
    for chrom in trees:
        logging.debug(f"chrom:{chrom}, trees:{trees[chrom]}")

    trees_and_timings = add_timings_to_trees( 
        trees=trees
    )

    logging.debug("got all the timings too")
    for chrom in trees_and_timings:
        logging.debug(f"chrom:{chrom}, trees:{trees_and_timings[chrom]}")

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




