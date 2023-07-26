#DONE 
import logging 
import copy
from prismm.utils.path_codes import pre_mid_post_to_path_length

##### STEP 4; now we have SNV counts, make all possible trees that could explain those SNV counts for the given epoch structure “(pre,mid, post)”

##### To save redundancy and speed up computational time-complexity of discovering and sorting through all evolutionary 
##### trees that explain the SNV data we do not insert copy number 1’s when finding all tree structures too iterate over.
##### They can be considered implicit and inserted everywhere at the very end. 
##### Non unitary copy numbers are not necessarily 
##### The reason for this is that there is a bijection between tree structures that include copy number 1’s and 
##### have paired timeline arrays where it every copy number must have existed for non zero time except for copy number 1
##### and the tree structures that do not include copy number 1 as every leaf of every tree and force all nodes to have 
##### a non zero evolutionary history where SNVs were allowed to accumulate. The latter is easier to computationally discover.
##### The tree structures can be simply constructed in a tuple of tuples format like tree = (value, left subtree, right subtree). 

### some basic tree functions:
from typing import Optional, Tuple, Union, List, Set


def sort_tree(tree: Optional[Tuple]) -> Optional[Tuple]:
    """
    Sorts a tree in ascending order according to the first element of each subtree.

    Args:
        tree (Optional[Tuple]): The tree to be sorted. Each node is a tuple with the first element being the value,
                                the second element being the left subtree, and the third element being the right subtree.

    Returns:
        Optional[Tuple]: The sorted tree.

    """
    # Input validation: tree must be either None or a tuple
    assert isinstance(tree, (type(None), Tuple)), "Input must be a tuple or None."

    if tree is None:
        return None

    if len(tree) == 1:
        return tree

    if len(tree) == 2:
        value, subtree = tree
        return (value, sort_tree(subtree))

    if len(tree) == 3:
        value, left_subtree, right_subtree = tree
        sorted_left = sort_tree(left_subtree)
        sorted_right = sort_tree(right_subtree)

        if sorted_left[0] > sorted_right[0]:
            return (value, sorted_left, sorted_right)
        else:
            return (value, sorted_right, sorted_left)



# OLD ONE
def compare_trees(tree1, tree2):
    tree1 = sort_tree(tree1)
    tree2 = sort_tree(tree2)
    len_tree1 = len(tree1)
    len_tree2 = len(tree2)

    if tree1 is None and tree2 is None:
        return True
    if tree1 is None or tree2 is None:
        return False

    # If the lengths of the trees are different, they are not equal
    if len_tree1 != len_tree2:
        return False

    # If the lengths of the trees are both 1, compare their values
    if len_tree1 == 1 and len_tree2 == 1:
        return tree1[0] == tree2[0]

    # If the lengths of the trees are both 2, compare their values
    if len_tree1 == 2 and len_tree2 == 2:
        if tree1[0] != tree2[0]:
            return False
        return compare_trees(tree1[1], tree2[1])

    # If the lengths of the trees are both 3, compare their values
    if len_tree1 == 3 and len_tree2 == 3:
        if tree1[0] != tree2[0]:
            return False
        return compare_trees(tree1[1], tree2[1]) and compare_trees(tree1[2], tree2[2])

    # If the code reaches this point, the trees are not equal
    return False

#OLD ONE
def forests_are_equal(trees1, trees2):
    if len(trees1) != len(trees2):
        return False
    for tree1 in trees1:
        found_match = False
        for tree2 in trees2:
            if compare_trees(tree1, tree2):
                found_match = True
                break
        if not found_match:
            return False
    return True


def compare_trees(tree1: Optional[Tuple], tree2: Optional[Tuple]) -> bool:
    """
    Compare two binary trees for equality.
    
    Parameters:
    tree1 (Tuple): First binary tree
    tree2 (Tuple): Second binary tree
    
    Returns:
    bool: True if trees are equal, False otherwise
    """
    sorted_tree1 = sort_tree(tree1)
    sorted_tree2 = sort_tree(tree2)
    
    return sorted_tree1 == sorted_tree2


def forests_are_equal(forest1: List[Tuple], forest2: List[Tuple]) -> bool:
    """
    Compare two forests for equality. Forests are equal if they contain the same trees.
    
    Parameters:
    forest1 (List[Tuple]): First forest as a list of trees
    forest2 (List[Tuple]): Second forest as a list of trees
    
    Returns:
    bool: True if forests are equal, False otherwise
    """
    sorted_forest1 = sorted(sort_tree(tree) for tree in forest1)
    sorted_forest2 = sorted(sort_tree(tree) for tree in forest2)
    
    return sorted_forest1 == sorted_forest2


def insert_node(trees, CN):
    """
    Insert a node with the given copy number (CN) into every possible location in the input trees.

    :param trees: A list of binary trees.
    :param CN: The copy number to be inserted into the trees.
    :return: A list of new trees with the CN inserted once into each input tree.
    """

    # base case
    if trees == [] or trees == [()]:
        return [(CN,)]
    new_trees = []

    # otherwise
    for tree in trees:
        if len(tree) == 1 and CN < tree[0]:
            new_CNs = (CN, tree[0] - CN)
            new_trees.append(sort_tree((tree[0], (max(new_CNs),), (min(new_CNs),))))
        elif len(tree) == 3:
            for subtree in insert_node([tree[1]], CN):
                new_trees.append(sort_tree((tree[0], subtree, tree[2])))

            for subtree in insert_node([tree[2]], CN):
                new_trees.append(sort_tree((tree[0], tree[1], subtree)))

    return new_trees

from typing import List, Tuple

def insert_node(trees: List[Tuple], copy_number: int) -> List[Tuple]:
    """
    Insert a node with the given copy number (CN) into every possible location in the input trees.

    :param trees: A list of binary trees.
    :param copy_number: The copy number to be inserted into the trees.
    :return: A list of new trees with the CN inserted once into each input tree.
    """

    # base case
    if not trees or trees == [()]:
        return [(copy_number,)]
    
    new_trees = []

    # insert node into trees
    for tree in trees:

        # If the tree has only one node and the copy_number is less than the node value
        if isinstance(tree, tuple) and len(tree) == 1 and copy_number < tree[0]:
            new_copy_numbers = (copy_number, tree[0] - copy_number)
            new_trees.append(sort_tree((tree[0], (max(new_copy_numbers),), (min(new_copy_numbers),))))
        
        # If the tree has multiple nodes, insert the copy number into each subtree
        elif isinstance(tree, tuple) and len(tree) == 3:
            
            # Generate new trees by inserting the copy_number into the left subtree
            left_subtrees = insert_node([tree[1]], copy_number)
            for left_subtree in left_subtrees:
                new_trees.append(sort_tree((tree[0], left_subtree, tree[2])))
            
            # Generate new trees by inserting the copy_number into the right subtree
            right_subtrees = insert_node([tree[2]], copy_number)
            for right_subtree in right_subtrees:
                new_trees.append(sort_tree((tree[0], tree[1], right_subtree)))
            
            # Generate new trees by inserting the copy_number into both subtrees
            for left_subtree in left_subtrees:
                for right_subtree in right_subtrees:
                    new_trees.append(sort_tree((tree[0], left_subtree, right_subtree)))

    return new_trees


def complete_tree(tree: Union[Tuple[int], Tuple[int, Tuple[int]], Tuple[int, Tuple[int], Tuple[int]]]) -> Set[Tuple[int, Tuple[int], Tuple[int]]]:
    """
    Given a tree structure as tuple, completes the tree by adding nodes and
    making it left-heavy. Returns a set of completed tree structures.

    :param tree: A tuple representing a tree structure with 1 to 3 elements.
    :return: A set of completed tree structures.
    :raises ValueError: If the input tree tuple has a length other than 1, 2, or 3.
    """
    assert isinstance(tree, tuple), f"Expected 'tree' to be a tuple, but got {type(tree).__name__} with value {tree}"
    assert 1 <= len(tree) <= 3, "Tree must have 1 to 3 elements"

    def _complete_three_elements(tree: Tuple[int, Tuple[int], Tuple[int]]) -> Set[Tuple[int, Tuple[int], Tuple[int]]]:
        """
        Helper function for handling trees with three elements.

        :param tree: A tuple representing a tree structure with 3 elements.
        :return: A set of completed tree structures.
        """
        left_trees = complete_tree(tree[1])
        right_trees = complete_tree(tree[2])

        completed_trees = set()
        for left_tree in left_trees:
            for right_tree in right_trees:
                completed_trees.add(sort_tree((tree[0], left_tree, right_tree)))
        return completed_trees

    def _complete_two_elements(tree: Tuple[int, Tuple[int]]) -> Set[Tuple[int, Tuple[int], Tuple[int]]]:
        """
        Helper function for handling trees with two elements.

        :param tree: A tuple representing a tree structure with 2 elements.
        :return: A set of completed tree structures.
        """
        left_trees = complete_tree(tree[1])
        completed_trees = set()

        for left_tree in left_trees:
            for i in range(1, tree[0] - left_tree[0]):
                right_trees = complete_tree((tree[0] - left_tree[0] - i,))
                for right_tree in right_trees:
                    completed_trees.add(sort_tree((tree[0], left_tree, right_tree)))
        return completed_trees

    def _complete_one_element(tree: Tuple[int]) -> Set[Tuple[int, Tuple[int], Tuple[int]]]:
        """
        Helper function for handling trees with one element.

        :param tree: A tuple representing a tree structure with 1 element.
        :return: A set of completed tree structures.
        """
        if tree[0] == 0 or tree[0] == 1:
            return {tree}

        completed_trees = set()
        for i in range(1, tree[0]):
            left_trees = complete_tree((i,))
            right_trees = complete_tree((tree[0] - i,))

            for left_tree in left_trees:
                for right_tree in right_trees:
                    completed_trees.add(sort_tree((tree[0], left_tree, right_tree)))
        return completed_trees

    if len(tree) == 3:
        return _complete_three_elements(tree)
    elif len(tree) == 2:
        return _complete_two_elements(tree)
    elif len(tree) == 1:
        return _complete_one_element(tree)
    else:
        raise ValueError("Invalid tree structure. Expected tuple length between 1 and 3.")


def complete_trees(trees):
    """
    Given a list of trees, returns a new list with each tree completed.
    
    Args:
    trees (list): A list of trees, where each tree is a tuple.
    
    Returns:
    list: A list of completed trees.
    """
    result = set()

    for tree in trees:
        result = result.union(complete_tree(tree))

    return list(result)



def generate_trees(observed_copy_numbers, SNV_CNs):
    """
    Generate all possible trees of every copy number from the multiplicity counts of the chromosomes and the SNVs.

    :param observed_copy_numbers: A list of observed copy numbers.
    :param SNV_CNs: A list of copy numbers for SNVs.
    :return: A list of unique trees.
    """

    SNV_CNs.sort(reverse=True)
    observed_copy_numbers.sort(reverse=True)

    for SNV_CN in SNV_CNs:
        assert isinstance(SNV_CN, int)
        assert SNV_CN >= 0

    for CN in observed_copy_numbers:
        assert isinstance(CN, int)
        assert(CN >= 0)

    # Initialize trees with the following tree for each chromosome
    trees = [(sum(observed_copy_numbers), (max(observed_copy_numbers),), (min(observed_copy_numbers),))]

    for SNV_CN in SNV_CNs:
        if SNV_CN == 1:
            continue

        trees_with_new_node = insert_node(trees, SNV_CN)

        if not trees_with_new_node:
            assert SNV_CN in observed_copy_numbers
            continue

        if SNV_CN in observed_copy_numbers:
            trees += trees_with_new_node # (we don't want to force it being inserted so we append it)
        else:
            trees = trees_with_new_node

        while True:
            # don't know how many time to reinsert the node:
            trees_with_node_inserted_again = insert_node(trees_with_new_node, SNV_CN)
            if not trees_with_node_inserted_again:
                break

            trees += trees_with_node_inserted_again
            trees_with_new_node = trees_with_node_inserted_again

    # Insert the "leaf nodes" into the tree - all of which are of CN 1
    trees = complete_trees(trees)

    trees = sorted([sort_tree(tree) for tree in trees])
    return trees

def generate_and_filter_trees(chrom, trees):
    this_chroms_trees = generate_trees(
        observed_copy_numbers=trees["data"][chrom]["observed_SNV_multiplicities"],
        SNV_CNs=list(trees["data"][chrom]["observed_copy_numbers"].keys())
    )

    return [
        tree for tree in this_chroms_trees
        if tree_in_bounds(tree=tree,
                          total_epochs_est=trees["metadata"]["total_epoch_est"],
                          tree_flexibility=trees["metadata"]["tree_flexibility"])
    ]

def get_all_trees(observed_SNV_multiplicities, observed_copy_numbers, pre_est, mid_est, post_est, tree_flexibility):
    tts = {}
    
    total_epochs_est = pre_mid_post_to_path_length(pre=pre_est, mid=mid_est, post=post_est)

    tts["metadata"] = {
        "pre_est": pre_est, 
        "mid_est": mid_est, 
        "post_est": post_est, 
        "total_epochs_est": total_epochs_est, 
        "tree_flexibility": tree_flexibility
        }
    
    tts["results"] = {int(x):{} for x in range(23)}

    for chrom in observed_SNV_multiplicities:
        tts["results"][chrom]["observed_SNV_multiplicities"] = observed_SNV_multiplicities
        tts["results"][chrom]["observed_copy_numbers"] = observed_copy_numbers
        tts["results"][chrom]["trees"] = generate_and_filter_trees(chrom, tts)

    return tts


def max_tree_depth(tree):
    """
    Calculate the maximum depth of a given tree.

    The tree is represented as a tuple of nested tuples, where each inner tuple
    represents a subtree. The depth of the tree is the length of the longest
    path from the root to a leaf node.

    Args:
        tree (tuple): The tree to calculate the depth of.

    Returns:
        int: The maximum depth of the tree.
    """
    if not tree:
        return 0

    if not isinstance(tree, tuple):
        raise ValueError("Invalid input. Tree must be a tuple of nested tuples.")

    max_depth = 0
    for subtree in tree[1:]:
        depth = max_tree_depth(subtree)
        max_depth = max(max_depth, depth)

    return max_depth + 1

def tree_in_bounds(tree, total_epochs_est, tree_flexibility):
    depth = max_tree_depth(tree)
    # it is plus 2 here because the root node is a ficitonal node and the leaves don't HAVE to count
    return depth >= total_epochs_est + 2 - tree_flexibility and depth <= total_epochs_est + 2


