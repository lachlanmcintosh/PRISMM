import logging
import copy
from prismm.run_build_trees_and_timings.get_all_trees import forests_are_equal 
import numpy as np

def get_all_timings(trees, total_epochs_est):
    trees_and_timings = {}
    for chrom in trees:
        trees_and_timings[chrom] = get_trees_and_timings_per_chrom(all_trees=trees[chrom], total_epochs_est=total_epochs_est)
        
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

def get_timings_per_tree(tree, total_epochs_est): 
    logging.debug("get_timings_per_tree")

    labelled_tree, label_count, parents, label_to_copy = label_tree(
        tree=copy.deepcopy(tree),
        label_count=0,
        parents={},
        label_to_copy={}
    )

    # TODO: WTF IS THIS, total_epochs_est will never be -1
    if total_epochs_est == -1:
        epochs_created = initialize_epochs_created(num_labels=label_count + 1, root_label=label)
        epochs_created = -1
        return (tree, labelled_tree, label_count, epochs_created, parents)

    for label in range(label_count + 1):
        if label == 0:
            epochs_created = initialize_epochs_created(num_labels=label_count + 1, root_label=label)
            assert epochs_created.shape[0] > 0, "The epochs_created array must have at least one row."
        else:
            logging.debug("labelled_tree")
            logging.debug(labelled_tree)
            logging.debug("copy numbers")
            logging.debug([label_to_copy[x] for x in range(label_count+1)])
            logging.debug("label")
            logging.debug(label)
            logging.debug("epochs_created")
            logging.debug(epochs_created)
            assert epochs_created.shape[0] > 0, "The epochs_created array must have at least one row."
            sibling = find_sibling(parents,label)
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

            if None in epochs_created[:,label]:
                return (None, None, None, None, None)

    logging.debug("epochs_created")
    logging.debug(epochs_created)
    logging.debug("epochs_created after filter_rows")
    epochs_created = filter_rows_based_on_parents(epochs_created=epochs_created, parents=parents)
    logging.debug(epochs_created)

    return (tree, labelled_tree, label_count, epochs_created, parents)


def label_tree(tree, label_count, parents, label_to_copy):
    if label_to_copy == {} or label_count == 0:
        assert parents == {}, f"Unexpected value for parents: {parents}"
        assert label_to_copy == {}, f"Unexpected value for label_to_copy: {label_to_copy}"
        assert label_count == 0, f"Unexpected value for label_count: {label_count}"

    tree = list(tree)

    unique_label = label_count
    label_to_copy[unique_label] = tree[0]
    tree[0] = unique_label

    new_parent = unique_label

    if len(tree) >= 2:
        tree[1], label_count, parents, label_to_copy = label_tree(tree[1], label_count+1, parents, label_to_copy)
        parents[tree[1][0]] = new_parent

        if len(tree) == 3:
            tree[2], label_count, parents, label_to_copy = label_tree(tree[2], label_count+1, parents, label_to_copy)
            parents[tree[2][0]] = new_parent

    return (tree, label_count, parents, label_to_copy)


def initialize_epochs_created(num_labels, root_label):
    """
    Initialize a 2D numpy array with shape (1, num_labels) containing None values. The value of the root_label-th element
    in the first row is set to 0 and all other values are set to None.

    :param num_labels: The number of labels in the tree.
    :param root_label: The label of the root node.
    :return: A 2D numpy array of None values with shape (1, num_labels).
    """
    assert isinstance(num_labels, int) and num_labels > 0, "Num labels should be a positive integer."
    assert isinstance(root_label, int) and 0 <= root_label < num_labels, "Root label should be within the range of labels."
    epochs_created = np.full((1, num_labels), None)
    epochs_created[0, root_label] = -1

    assert epochs_created.shape[0] > 0, "The resulting array must have at least one row."

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

    return new_epochs_created


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