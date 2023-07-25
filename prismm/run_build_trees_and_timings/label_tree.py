import copy
from typing import Tuple, Dict

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