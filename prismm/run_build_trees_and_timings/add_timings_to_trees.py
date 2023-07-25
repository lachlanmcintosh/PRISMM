#DONE
import logging
import copy
import numpy as np
from typing import Dict, Tuple, List

from prismm.run_build_trees_and_timings.check_timing_array import ensure_consistent_rows
from prismm.run_build_trees_and_timings.label_tree import label_tree


def initialize_epochs_created(num_labels, zero_epoch_nodes):
    """
    Initialize a 2D numpy array with shape (1, num_labels) containing None values. The value of the root_label-th element
    in the first row is set to 0 and all other values are set to None.

    :param num_labels: The number of labels in the tree.
    :param root_label: The label of the root node.
    :return: A 2D numpy array of None values with shape (1, num_labels).
    """
    assert isinstance(num_labels, int) and num_labels > 0, "Num labels should be a positive integer."
    assert len(zero_epoch_nodes) == 2
    assert max(zero_epoch_nodes) < num_labels
    assert min(zero_epoch_nodes) == 1

    # create a 2D numpy array with the shape (1, num_labels) and fill with the value None.
    epochs_created = np.full((1, num_labels), None)
    epochs_created[0, 0] = 0

    for label in zero_epoch_nodes:
        epochs_created[0, label] = 1

    assert epochs_created.shape[0] == 1

    return epochs_created


def find_sibling(parents: dict, query_key: int) -> list:
    """
    Given a dictionary of 'parents' containing key-value pairs where the key is a child node and 
    the value is its parent node, this function takes a 'query_key' and returns a list of sibling keys.
    If the 'query_key' does not exist in the dictionary or there are no siblings, an empty list is returned.

    :param parents: A dictionary where keys are child nodes and values are parent nodes.
    :param query_key: The key for which we are searching sibling keys.
    :return: A list of sibling keys.
    """

    # Get the parent value for the query_key.
    query_parent = parents.get(query_key)

    if query_parent is None:
        return []

    # Find sibling keys by iterating through the parents dictionary.
    sibling_keys = [
        key for key, parent in parents.items() if parent == query_parent and key != query_key
    ]
    assert(len(sibling_keys) == 1)

    return sibling_keys[0]


def create_epochs_temp(epochs_created_row: np.ndarray, 
                       label: int, 
                       parents_time: int, 
                       total_epochs_est: int,
                       copy_number: int) -> np.ndarray:
    """Helper function to create a temporary epochs array with updated values for a specific label."""

    # Check if the parent's time is less than or equal to the total estimated epochs and if label_to_copy_number is 1,
    # or if the parent's time is strictly less than the total estimated epochs
    # TODO, change this back
    if (parents_time <= total_epochs_est and copy_number == 1) or parents_time < total_epochs_est:
    #if parents_time < total_epochs_est:
        # Determine the start of the sequence based on whether the parent is the root
        sequence_start = parents_time +1 if copy_number != 1 else parents_time

        # Create a temporary array by repeating the current row (total_epochs_est - sequence_start + 1) times
        epochs_created_temp = np.tile(epochs_created_row, (total_epochs_est - sequence_start + 1, 1))

        # Set the label column in the temporary array to a sequence from sequence_start to total_epochs_est
        epochs_created_temp[:, label] = list(range(sequence_start, total_epochs_est + 1))
        logging.debug(f'epochs_created_temp:{epochs_created_temp}')
        return epochs_created_temp

    return None


def handle_other_nodes(epochs_created: np.ndarray, 
                       label_to_copy: Dict[int, int], 
                       label: int, 
                       parent: int, 
                       total_epochs_est: int) -> np.ndarray:
    """
    Handle the creation of new epochs for nodes in a graph-like structure.

    Args:
        epochs_created: 2D array representing the epochs created for each node.
        label_to_copy: Dictionary mapping labels to copy numbers.
        label: The label of the node to handle.
        parent: The label of the parent node.
        total_epochs_est: The total estimated epochs.

    Returns:
        The updated epochs_created array after handling the specified node.

    Raises:
        ValueError: If any of the input arguments do not meet their expected conditions.
    """
    if epochs_created.ndim != 2:
        raise ValueError("Timings should be a 2-dimensional array.")

    if not(0 <= label < epochs_created.shape[1]):
        raise ValueError("Label should be within the range of timings.")

    if not isinstance(total_epochs_est, (int, np.integer)) or total_epochs_est < 0:
        raise ValueError("Epochs should be a positive integer or a non-negative numpy integer.")

    if epochs_created.shape[0] <= 0:
        raise ValueError("The epochs_created array must have at least one row.")
    
    if not isinstance(label_to_copy, dict):
        raise ValueError("label_to_copy should be a dictionary or similar mapping type.")

    new_epochs_created = epochs_created
    for row in range(len(epochs_created)):
        parents_time = epochs_created[row][parent]
        if parents_time is None:
            raise ValueError("Parent's time cannot be None.")

        logging.debug(f'row:{row}')
        logging.debug(f'total_epochs_est:{total_epochs_est}')
        logging.debug(f'parent:{parent}')
        logging.debug(f'parents_time:{parents_time}')
        logging.debug(f'copynumber:{label_to_copy[label]}')

        epochs_created_temp = create_epochs_temp(epochs_created_row = epochs_created[row], 
                                                    label = label, 
                                                    parents_time = parents_time, 
                                                    total_epochs_est = total_epochs_est,
                                                    copy_number = label_to_copy[label])
        if epochs_created_temp is None:
            continue
        #    return None
        logging.debug(f'epochs_created_temp:{epochs_created_temp}')

        if row == 0:
            new_epochs_created = epochs_created_temp
            logging.debug(f':new_epochs_created{new_epochs_created}')
        else:
            new_epochs_created = np.vstack([new_epochs_created,epochs_created_temp])

    return new_epochs_created


def get_timings_per_tree(tree: Tuple, total_epochs_est: int) -> Tuple[str, str, int, np.array, Dict[str, int]]:
    """
    Get timings per tree.
    
    Args:
        tree (str): Input tree.
        total_epochs_est (int): Total epochs estimate.

    Returns:
        tuple: A tuple containing tree, labelled_tree, label_count, epochs_created, and parents.
    """

    logging.debug("get_timings_per_tree")

    labelled_tree, label_count, parents, label_to_copy = label_tree(tree)
    logging.debug("labelled_tree, label_count, parents, label_to_copy")
    logging.debug((labelled_tree, label_count, parents, label_to_copy))

    zero_epoch_nodes = [key for key, value in parents.items() if value == 0]

    epochs_created = initialize_epochs_created(
        num_labels=label_count + 1, 
        zero_epoch_nodes = zero_epoch_nodes) 

    if label_count == 2:
        return (tree, labelled_tree, label_count, epochs_created, parents)

    for label in range(1, label_count + 1):
        if label in zero_epoch_nodes:
            continue

        sibling = find_sibling(parents,label)

        if sibling < label:
            logging.debug("insertion by copying sibling")
            epochs_created[:,label] = epochs_created[:,sibling]
        else:
            logging.debug("insertion by finding all possible epochs")
            epochs_created = handle_other_nodes(
                epochs_created=epochs_created,
                label_to_copy=label_to_copy,
                label=label,
                parent=parents[label],
                total_epochs_est=total_epochs_est
            )

        if epochs_created is None or np.any(epochs_created[:,label] == None):
            return (None, None, None, None, None)

    ensure_consistent_rows(
        epochs_created=epochs_created, 
        parents=parents
    )
    logging.debug("epochs_created")
    logging.debug(epochs_created)


    return (tree, labelled_tree, label_count, epochs_created, parents)

import sys
def get_timings_per_chrom(all_trees: List[Tuple], total_epochs_est: int) -> List[Tuple[str, str, int, np.array, Dict[str, int]]]:
    """
    Get timings per chromosome for all trees.
    
    Args:
        all_trees (list): List of all trees.
        total_epochs_est (int): Total epochs estimate.

    Returns:
        list: A list of tuples containing tree, labelled_tree, label_count, epochs_created, and parents for each tree.
    """

    chrom_trees_and_timings = [
        get_timings_per_tree(tree=x, total_epochs_est=total_epochs_est) 
        for x in all_trees
    ]

    # Filter out trees with invalid epochs_created data
    print(chrom_trees_and_timings)
    #chrom_trees_and_timings = [
    #    x for x in chrom_trees_and_timings 
    #    if x[3] is not None and not None in x[3]
    #]

    return chrom_trees_and_timings

def add_timings_to_trees(trees: Dict[str, List], total_epochs_est: int) -> Dict[str, List[Tuple[str, str, int, np.array, Dict[str, int]]]]:
    """
    Get timings for all trees.
    
    Args:
        trees (dict): A dictionary of trees with their identifiers as keys.
        total_epochs_est (int): Total epochs estimate.

    Returns:
        dict: A dictionary with tree identifiers as keys and their timings as values.
    """

    timings = {}

    for chrom, tree in trees.items():
        assert isinstance(tree, list)
        timings[chrom] = get_timings_per_chrom(
            all_trees = tree, 
            total_epochs_est = total_epochs_est
        )
        
        logging.debug(f"Estimated total epochs for chromosome {chrom}: {total_epochs_est}")
        logging.debug(f"Trees and timings for chromosome {chrom}: {timings[chrom]}")

    return timings