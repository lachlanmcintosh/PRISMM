# DONE
import numpy as np
from typing import Dict, List

# NOW SOME CHECKS:
def group_children_by_parent(parents: Dict[int, int]) -> Dict[int, List[int]]:
    """
    Transforms a dictionary of child-parent pairs into a dictionary of parent-children groups.

    Args:
        parents (Dict[int, int]): A dictionary mapping child indices (keys) to their respective parent indices (values).

    Returns:
        Dict[int, List[int]]: A dictionary mapping parent indices (keys) to lists of their respective child indices (values).
    """
    assert isinstance(parents, dict), "Input 'parents' must be a dictionary."

    parent_to_children = {}
    for child_index, parent_index in parents.items():
        assert isinstance(child_index, int), "Child index must be an integer."
        assert isinstance(parent_index, int), "Parent index must be an integer."

        parent_to_children.setdefault(parent_index, []).append(child_index)

    return parent_to_children


def is_row_parent_consistent(row: np.array, parent_to_children: Dict[int, List[int]]) -> bool:
    """
    Verifies if a row is consistent based on the rule that all children of the same parent should have the same value.

    Args:
        row (np.array): A NumPy array representing a row of data.
        parent_to_children (Dict[int, List[int]]): A dictionary mapping parent indices (keys) to lists of their respective child indices (values).

    Returns:
        bool: True if the row is consistent (i.e., all children of the same parent have the same value), False otherwise.
    """
    assert isinstance(row, np.ndarray), "Input 'row' must be a numpy array."
    assert isinstance(parent_to_children, dict), "Input 'parent_to_children' must be a dictionary."

    for parent, children_indices in parent_to_children.items():
        assert isinstance(parent, int), "Parent index must be an integer."
        assert isinstance(children_indices, list), "Children indices must be a list."

        child_values = [row[child_index] for child_index in children_indices]
        if len(set(child_values)) > 1:
            return False
    return True


def ensure_consistent_rows(epochs_created: np.array, parents: Dict[int, int]) -> None:
    """
    Ensures that all rows in the epochs_created array satisfy the consistency rule, based on the parent-child relationship in 'parents'.
    Raises an error if there are inconsistent rows.

    Args:
        epochs_created (np.array): A 2D NumPy array representing the epochs created.
        parents (Dict[int, int]): A dictionary mapping child indices (keys) to their respective parent indices (values).

    Returns:
        None
    """
    assert isinstance(epochs_created, np.ndarray), "Input 'epochs_created' must be a numpy array."
    assert len(epochs_created.shape) == 2, "Input 'epochs_created' must be a 2D numpy array."
    assert isinstance(parents, dict), "Input 'parents' must be a dictionary."

    parent_to_children = group_children_by_parent(parents)

    for row in epochs_created:
        if not is_row_parent_consistent(row, parent_to_children):
            raise ValueError("Inconsistent row found. All children of the same parent must have the same value.")

