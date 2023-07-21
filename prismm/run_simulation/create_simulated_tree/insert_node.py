import copy
from typing import Dict, List, Tuple, Optional


def deep_copy_node(node: Dict, epoch_created: Optional[int] = None) -> Dict:
    """
    Create a deep copy of a node and reset its 'child' and 'complement' fields.

    :param node: The node to be copied.
    :param epoch_created: The 'epoch_created' value for the copied node. If None, the copied node's 'epoch_created' is used.
    :return: The copied node.
    """
    copied_node = copy.deepcopy(node)
    copied_node["child"] = None
    copied_node["complement"] = None
    if epoch_created is not None:
        copied_node["epoch_created"] = epoch_created
    return copied_node


def validate_leaf_node(tree: Dict) -> None:
    """
    Validate that a given tree is a leaf node.

    :param tree: The tree to validate.
    :raises ValueError: If the tree is not a leaf node.
    """
    if tree["child"] is not None:
        raise ValueError(f"Expected tree['child'] to be None, but got {tree['child']}")
    if tree["complement"] is not None:
        raise ValueError(f"Expected tree['complement'] to be None, but got {tree['complement']}")


def insert_node_immediately_under_here(tree: Dict, node: Dict) -> None:
    """
    Inserts a node into a leaf of a given tree.

    :param tree: The tree where the node is to be inserted.
    :param node: The node to be inserted into the tree.
    :raises ValueError: If the tree is not a leaf node.
    """

    validate_leaf_node(tree)

    # Create a deep copy of the tree as the complement
    tree["complement"] = deep_copy_node(tree, epoch_created=node["epoch_created"])

    # Insert the node as a child
    tree["child"] = deep_copy_node(node)


def validate_complement_node(tree: Dict) -> None:
    """
    Validate that a given tree has a complement node.

    :param tree: The tree to validate.
    :raises ValueError: If the tree does not have a complement node.
    """
    if tree["complement"] is None:
        raise ValueError(f"Expected tree['complement'] to not be None, but it was.")


def validate_original_chromosome(node: Dict) -> None:
    """
    Validate that a given node is an original chromosome.

    :param node: The node to validate.
    :raises ValueError: If the node is not an original chromosome.
    """
    expected_keys = {"unique_identifier", "epoch_created", "parent", "SNVs", "paternal", "dead", "sibling"}
    if set(node.keys()) != expected_keys:
        raise ValueError(f"Unexpected keys: {node.keys()} - Expected keys: {expected_keys}")
    if node["unique_identifier"] >= 46:
        raise ValueError(f"Expected node['unique_identifier'] to be less than 46, but got {node['unique_identifier']}")


def insert_node_under_this_branch(tree: Dict, node: Dict) -> None:
    """
    Inserts a node under the complement of a given tree.

    :param tree: The tree where the node is to be inserted.
    :param node: The node to be inserted under the complement of the tree.
    :raises ValueError: If the tree does not have a complement node.
    """

    validate_complement_node(tree)

    if node["parent"] == -1:
        validate_original_chromosome(node)
        tree["complement"] = deep_copy_node(node)
    else:
        tree["complement"] = insert_node_into_tree(tree["complement"], node)

def insert_node_into_either_subtree(child_tree: Optional[Dict], complement_tree: Optional[Dict], node: Optional[Dict]) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Insert a node into the child and complement trees if they are not None.

    :param child_tree: The child tree where the node is to be inserted.
    :param complement_tree: The complement tree where the node is to be inserted.
    :param node: The node to be inserted into the trees.
    :return: The modified child and complement trees.
    """
    if child_tree is not None:
        child_tree = insert_node_into_tree(child_tree, node)
    if complement_tree is not None:
        complement_tree = insert_node_into_tree(complement_tree, node)

    return child_tree, complement_tree

def insert_node_into_tree(tree: Optional[Dict], node: Optional[Dict]) -> Optional[Dict]:
    """
    Inserts a node into a tree structure according to the unique identifier and parent-child relationships.

    :param tree: The tree where the node is to be inserted.
    :param node: The node to be inserted into the tree.
    :return: The modified tree.
    """
    if node is None or tree is None:
        return tree

    if node["unique_identifier"] != tree["unique_identifier"]:
        if node["parent"] == tree["unique_identifier"]:
            if tree["child"] is None:
                insert_node_immediately_under_here(tree, node)
            else:
                insert_node_under_this_branch(tree, node)
        else:
            tree["child"], tree["complement"] = insert_node_into_either_subtree(child_tree=tree["child"], complement_tree=tree["complement"], node=node)

    return tree


def insert_nodes_into_tree(tree: Dict, sorted_list: List[Dict]) -> Dict:
    """
    Insert all nodes and add metadata to tree and simplify.

    :param tree: The tree into which nodes are to be inserted.
    :param sorted_list: The sorted list of nodes to be inserted.
    :return: The tree with nodes inserted.
    """
    for _, new_node in sorted_list:
        tree = insert_node_into_tree(tree, new_node)
    return tree
