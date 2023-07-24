import logging
import copy
from prismm.run_build_trees_and_timings.get_all_trees import forests_are_equal 
import numpy as np

from typing import Dict, Tuple


def recursively_label_tree(tree: Tuple, label_count: int, parents: Dict[int, int], 
               label_to_copy: Dict[int, int]) -> Tuple[tuple, int, Dict[int, int], Dict[int, int]]:
    """
    Recursively labels a given tree with unique identifiers, replacing the original labels.
    Also, maintains a dictionary of old labels to new labels (label_to_copy) 
    and a dictionary of child labels to parent labels (parents). 

    Args:
        tree (Tuple): The tree to be labeled.
        label_count (int): The current count of unique labels.
        parents (Dict[int, int]): A dictionary mapping child labels to their parent labels.
        label_to_copy (Dict[int, int]): A dictionary mapping new labels to copy number.

    Returns:
        Tuple[Tuple, int, Dict[int, int], Dict[int, int]]: The labeled tree and the updated 
        label_count, parents, and label_to_copy.
    """

    # modify the tree in place, to do that recursively convert to a list
    tree=list(tree)

    # Validate inputs
    if label_to_copy == {} or label_count == 0:
        assert parents == {}, f"Unexpected value for parents: {parents}"
        assert label_to_copy == {}, f"Unexpected value for label_to_copy: {label_to_copy}"
        assert label_count == 0, f"Unexpected value for label_count: {label_count}"

    # Create a unique label and update mappings
    unique_label = label_count
    label_to_copy[unique_label] = tree[0]
    tree[0] = unique_label
    new_parent = unique_label

    # Recursively label the children if they exist
    for i in range(1, len(tree)):
        tree[i], label_count, parents, label_to_copy = recursively_label_tree(tree[i], label_count+1, parents, label_to_copy)
        parents[tree[i][0]] = new_parent

    return tree, label_count, parents, label_to_copy

def label_tree(tree):
    return recursively_label_tree(
        tree=copy.deepcopy(tree),
        label_count=0,
        parents={},
        label_to_copy={}
    )

import sys

def initialize_epochs_created(num_labels, zero_epoch_nodes):
    """
    Initialize a 2D numpy array with shape (1, num_labels) containing None values. The value of the root_label-th element
    in the first row is set to 0 and all other values are set to None.

    :param num_labels: The number of labels in the tree.
    :param root_label: The label of the root node.
    :return: A 2D numpy array of None values with shape (1, num_labels).
    """
    assert isinstance(num_labels, int) and num_labels > 0, "Num labels should be a positive integer."

    # create a 2D numpy array with the shape (1, num_labels) and fill with the value None.
    epochs_created = np.full((1, num_labels), None)
    epochs_created[0, 0] = -1

    for label in zero_epoch_nodes:
        epochs_created[0, label] = 0

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


'''
def handle_other_nodes(epochs_created, label_to_copy, label, parent, total_epochs_est):
    assert epochs_created.ndim == 2, "Timings should be a 2-dimensional array."
    assert 0 <= label < epochs_created.shape[1], "Label should be within the range of timings."
    #assert isinstance(total_epochs_est, int) and total_epochs_est >= 0, "Epochs should be a positive integer."
    assert isinstance(total_epochs_est, (int, np.integer)) and total_epochs_est >= 0, "Epochs should be a positive integer or a non-negative numpy integer."
    assert epochs_created.shape[0] > 0, "The epochs_created array must have at least one row."

    new_epochs_created = epochs_created
    for row in range(len(epochs_created)):
        parents_time = epochs_created[row][parent]
        assert(parents_time is not None)
        logging.debug(f'row:{row}')
        logging.debug(f'total_epochs_est:{total_epochs_est}')
        logging.debug(f'parent:{parent}')
        logging.debug(f'parents_time:{parents_time}')
        logging.debug(f'copynumber:{label_to_copy[label]}')

        # first handle the two nodes under the root:
        if parent == 0:
            epochs_created_temp = np.tile(epochs_created[row], (1, 1))
            epochs_created_temp[:, label] = 0
        else:    
            if parents_time <= total_epochs_est and label_to_copy[label] == 1:
                if parents_time != -1:
                    epochs_created_temp = np.tile(epochs_created[row], (total_epochs_est - parents_time + 1, 1))
                    epochs_created_temp[:, label] = list(range(parents_time, total_epochs_est + 1))
                else:
                    epochs_created_temp = np.tile(epochs_created[row], (total_epochs_est - parents_time, 1))
                    epochs_created_temp[:, label] = list(range(parents_time + 1, total_epochs_est + 1))
                logging.debug(f'epochs_created_temp:{epochs_created_temp}')

            elif parents_time < total_epochs_est:
                epochs_created_temp = np.tile(epochs_created[row], (total_epochs_est - parents_time, 1))
                epochs_created_temp[:, label] = list(range(parents_time + 1, total_epochs_est + 1))
                logging.debug(f'epochs_created_temp:{epochs_created_temp}')

            else:
                continue

        if row == 0:
            new_epochs_created = epochs_created_temp
            logging.debug(f':new_epochs_created{new_epochs_created}')
        else:
            new_epochs_created = np.vstack([new_epochs_created,epochs_created_temp])

    return new_epochs_created'''


import logging
import numpy as np
from typing import Dict, Union, Any, Tuple

def create_epochs_temp(epochs_created_row: np.ndarray, 
                       label: int, 
                       parents_time: int, 
                       total_epochs_est: int,
                       copy_number: int) -> np.ndarray:
    """Helper function to create a temporary epochs array with updated values for a specific label."""

    # Check if the parent's time is less than or equal to the total estimated epochs and if label_to_copy_number is 1,
    # or if the parent's time is strictly less than the total estimated epochs
    if (parents_time <= total_epochs_est and copy_number == 1) or parents_time < total_epochs_est:
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
            return None
        logging.debug(f'epochs_created_temp:{epochs_created_temp}')

        if row == 0:
            new_epochs_created = epochs_created_temp
            logging.debug(f':new_epochs_created{new_epochs_created}')
        else:
            new_epochs_created = np.vstack([new_epochs_created,epochs_created_temp])

    return new_epochs_created


def get_timings_per_tree(tree, total_epochs_est): 
    logging.debug("get_timings_per_tree")

    labelled_tree, label_count, parents, label_to_copy = label_tree(tree)
    zero_epoch_nodes = [key for key, value in parents.items() if value == 0] 

    epochs_created = initialize_epochs_created(num_labels=label_count + 1, zero_epoch_nodes = zero_epoch_nodes) # plus one because counting starts at 0.
    if label_count == 2:
        return epochs_created

    for label in range(1, label_count + 1):
        if label in zero_epoch_nodes:
            continue

        sibling = find_sibling(parents,label)
        print(sibling)
        print(label)
        if sibling < label:
            logging.debug("insertion by copying sibling")
            epochs_created[:,label] = epochs_created[:,sibling]
        else:
            logging.debug("insertion by finding all possible epochs")
            epochs_created = handle_other_nodes(epochs_created=epochs_created,
                                                label_to_copy=label_to_copy,
                                                label=label,
                                                parent=parents[label],
                                                total_epochs_est=total_epochs_est
                                                )
        logging.debug("epochs_created")
        logging.debug(epochs_created)
        if epochs_created is None or np.any(epochs_created[:,label] == None):
            return (None, None, None, None, None)

    logging.debug("epochs_created")
    logging.debug(epochs_created)

    logging.debug("epochs_created after filter_rows")
    epochs_created = filter_rows_based_on_parents(epochs_created=epochs_created, parents=parents)
    logging.debug(epochs_created)

    return (tree, labelled_tree, label_count, epochs_created, parents)








def get_all_timings(trees, total_epochs_est):
    trees_and_timings = {}
    for chrom in trees:
        trees_and_timings[chrom] = get_trees_and_timings_per_chrom(
            all_trees = trees[chrom], 
            total_epochs_est=total_epochs_est
            )
        
        logging.debug("In 'get_all_timings'")
        logging.debug(f"Estimated total epochs for chromosome {chrom}: {total_epochs_est}")
        logging.debug(f"Trees and timings for chromosome {chrom}: {trees_and_timings[chrom]}")

    return trees_and_timings

def get_trees_and_timings_per_chrom(all_trees, total_epochs_est):
    logging.debug("all trees")
    logging.debug(all_trees)

    chrom_trees_and_timings = [get_timings_per_tree(tree=x, total_epochs_est=total_epochs_est) for x in all_trees]

    logging.debug("chrom_trees_and_timings")
    logging.debug(chrom_trees_and_timings)

    # TODO, check this and make it clearer:
    chrom_trees_and_timings = [x for x in chrom_trees_and_timings if x[3] is not None and not None in x[3]]

    logging.debug("chrom_trees_and_timings")
    logging.debug(chrom_trees_and_timings)

    return chrom_trees_and_timings








# don't know about these three funcitons now:
def group_columns_by_parent(parents):
    """
    Group columns by parent.

    Args:
        parents (dict): A dictionary with keys as child indices and values as their parent indices.

    Returns:
        dict: A dictionary with keys as parent indices and values as lists of their child indices.
    """
    grouped_columns = {}
    for child, parent in parents.items():
        if parent in grouped_columns:
            grouped_columns[parent].append(child)
        else:
            grouped_columns[parent] = [child]
    return grouped_columns



def is_valid_row(row, grouped_columns):
    """
    Check if a row is valid based on the constraints of grouped_columns.

    Args:
        row (np.array): A NumPy array representing a row of data.
        grouped_columns (dict): A dictionary with keys as parent indices and values as lists of their child indices.

    Returns:
        bool: True if the row is valid, False otherwise.
    """
    for parent, children in grouped_columns.items():
        child_columns = [row[child] for child in children]
        if len(set(child_columns)) > 1:
            return False
    return True

# this function may be redundant now...
def filter_rows_based_on_parents(epochs_created, parents):
    """
    Filter rows in the timings array based on constraints from the parents dictionary.

    Args:
        timings (np.array): A 2D NumPy array representing the input data.
        parents (dict): A dictionary with keys as child indices and values as their parent indices.

    Returns:
        np.array: A filtered 2D NumPy array containing only the valid rows based on the constraints.
    """
    grouped_columns = group_columns_by_parent(parents)
    filtered_rows = [row for row in epochs_created if is_valid_row(row, grouped_columns)]
    filtered_timings = np.array(filtered_rows, dtype=object)
    return filtered_timings