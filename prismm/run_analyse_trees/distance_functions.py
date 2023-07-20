from abc import ABC, abstractmethod
import pytest
from typing import Dict, List, Tuple, Union, Type


def sum_tree_distance(tree1, tree2, diff_struct_is_inf=False):
    """
    Calculate the sum of absolute differences between the epoch_created values of each node for the nodes
    that have identical copy_number values in two given trees.

    Args:
        tree1 (dict): The first tree represented as a dictionary.
        tree2 (dict): The second tree represented as a dictionary.
        diff_struct_is_inf (bool, optional): If True, returns infinity if there is a structural difference
                                             between the trees. Default is False.

    Returns:
        float: The sum of absolute differences between the epoch_created values of nodes with identical
               copy_number values.
    """
    total = 0

    if (tree1 is not None and tree2 is not None and
            tree1['copy_number'] == tree2['copy_number'] and
            tree1["epoch_index"] is not None and
            tree2["epoch_index"] is not None):
        total += abs(tree1['epoch_index'] - tree2['epoch_index'])

    if tree1.get('child') is not None and tree2.get('child') is not None:
        total += sum_tree_distance(tree1['child'], tree2['child'], diff_struct_is_inf)
    elif diff_struct_is_inf:
        return float('inf')

    if tree1.get('complement') is not None and tree2.get('complement') is not None:
        total += sum_tree_distance(tree1['complement'], tree2['complement'], diff_struct_is_inf)
    elif diff_struct_is_inf:
        return float('inf')

    return total



def count_nodes_with_same_attributes(tree1, tree2, attributes):
    """
    This function uses recursion to iterate through both trees and count the number of nodes that have
    the same value for the specified attributes. It first checks if the current nodes in both trees have
    the attribute key, and if they do and their values are equal, it increments the count by 1.

    :param tree1: A dictionary representing the first tree
    :param tree2: A dictionary representing the second tree
    :param attributes: A list of strings representing the attributes to be compared
    :return: The count of nodes with the same attribute value in both trees
    """
    count = 0
    for attribute in attributes:
        if attribute in tree1 and attribute in tree2 and tree1[attribute] == tree2[attribute]:
            count += 1
    for child_key in ['child', 'complement']:
        if child_key in tree1 and child_key in tree2 and tree1[child_key] is not None and tree2[child_key] is not None:
            count += count_nodes_with_same_attributes(tree1[child_key], tree2[child_key], attributes)
    return count


# define two special functions
count_nodes_with_same_copy_number = lambda tree1, tree2: count_nodes_with_same_attributes(tree1, tree2, ['copy_number'])
count_nodes_with_same_properties = lambda tree1, tree2: count_nodes_with_same_attributes(tree1, tree2, ['epoch_index', 'copy_number'])


def are_trees_identical_by_epoch_and_copy_number(tree1: dict, tree2: dict) -> bool:
    """
    This function takes two trees as input, each represented as a dictionary, and returns a Boolean indicating whether they
    are topologically identical and have the same epoch_created value and copy_number value at each node.

    Args:
        tree1: A dictionary representing a tree.
        tree2: A dictionary representing a tree.

    Returns:
        A boolean indicating whether the two trees are topologically identical and have the same epoch_created value and
        copy_number value at each node.
    """

    if tree1['epoch_index'] != tree2['epoch_index'] or tree1['copy_number'] != tree2['copy_number']:
        return False

    tree1_child = tree1.get('child')
    tree2_child = tree2.get('child')
    tree1_complement = tree1.get('complement')
    tree2_complement = tree2.get('complement')

    if not tree1_child and not tree2_child and not tree1_complement and not tree2_complement:
        return True

    if bool(tree1_child) != bool(tree2_child) or bool(tree1_complement) != bool(tree2_complement):
        return False

    if tree1_child and not are_trees_identical_by_epoch_and_copy_number(tree1_child, tree2_child):
        return False

    if tree1_complement and not are_trees_identical_by_epoch_and_copy_number(tree1_complement, tree2_complement):
        return False

    return True


class DistanceFunction(ABC):
    """
    Abstract base class for distance functions. 
    Defines an interface for a function that takes an integer difference 
    and returns a float.
    """
    
    @abstractmethod
    def __call__(self, difference: int) -> float:
        """
        Abstract method that will be implemented in the derived classes.

        :param difference: An integer to be used in the distance function.
        :return: A float as a result of the distance function.
        """
        pass


class ZeroDistance(DistanceFunction):
    """
    Zero distance function class. Always returns zero regardless of the input.
    """
    
    def __call__(self, difference: int) -> float:
        assert isinstance(difference, int), f"Invalid input type. Expected int but got {type(difference)}"
        return 0.0

class AbsoluteDifference(DistanceFunction):
    """
    Euclidean distance function class.
    """
    def __call__(self, difference: int) -> float:
        assert isinstance(difference, int), f"Invalid input type. Expected int but got {type(difference)}"
        return abs(float(difference))


class SquaredDistance(DistanceFunction):
    """
    Squared distance function class.
    """
    def __call__(self, difference: int) -> float:
        assert isinstance(difference, int), f"Invalid input type. Expected int but got {type(difference)}"
        return float(difference ** 2)


class InfiniteDistance(DistanceFunction):
    """
    Infinite distance function class.
    """
    def __call__(self, difference: int) -> float:
        assert isinstance(difference, int), f"Invalid input type. Expected int but got {type(difference)}"
        if difference != 0:
            return float('inf')
        else:
            return 0



def calculate_difference(tree1, tree2, distance_function):
    return distance_function(abs(tree1 - tree2))

def compute_similarity(
    tree1: Union[Dict, None], 
    tree2: Union[Dict, None], 
    copy_number_distance: DistanceFunction, 
    epoch_index_distance: DistanceFunction, 
    similarity_divisor: int
) -> float:
    # Handling None cases for tree1 and tree2
    if tree1 is None and tree2 is None:
        return 0.0

    elif tree1 is None or tree2 is None:
        if tree1 is None:
            tree1 = {'copy_number': 0, 'epoch_index': 0}
        else:
            assert(tree2 is None)
            tree2 = {'copy_number': 0, 'epoch_index': 0}

        return calculate_difference(
            tree1['copy_number'], 
            tree2['copy_number'], 
            copy_number_distance
        )
    
    else:
        epoch_index_difference = calculate_difference(
            tree1['epoch_index'], 
            tree2['epoch_index'], 
            epoch_index_distance
        )

        left_similarity = compute_similarity(
            tree1.get('complement', None), 
            tree2.get('complement', None), 
            copy_number_distance, 
            epoch_index_distance, 
            similarity_divisor
        )

        right_similarity = compute_similarity(
            tree1.get('child', None), 
            tree2.get('child', None), 
            copy_number_distance, 
            epoch_index_distance, 
            similarity_divisor
        )

        #print("*****",tree1,tree2,epoch_index_difference, left_similarity, right_similarity)

        total_similarity = (
            epoch_index_difference 
            + left_similarity 
            + right_similarity
        ) / similarity_divisor

        return total_similarity

def compute_solution_similarity(
    solutions: Dict,
    node_distance_functions: List[Type[DistanceFunction]]
) -> None:
    """
    Compute similarity for solutions with various distance and similarity functions.

    Args:
        solutions: Solutions dictionary containing trees to compare.
        node_distance_functions: List of distance function classes for node comparisons.

    Returns: None. The function modifies the solutions dictionary in-place.
    """
    # Create distance function pairs
    pairs = [(x, y) for y in node_distance_functions for x in node_distance_functions]

    # Iterate over solutions
    for solution in solutions["solutions"]:
        for node_distance_function_pair in pairs:
            for normalising_constant in [1,4]:

                # Create instances of distance function classes
                copy_number_distance = node_distance_function_pair[0]()
                epoch_created_distance = node_distance_function_pair[1]()

                # Initialize total similarity
                total_similarity = 0

                for chrom in range(23):
                    # Compute similarity
                    similarity = compute_similarity(
                        solution[chrom]["dict_tree"],
                        solutions["simplified_truth_trees"][chrom],
                        copy_number_distance,
                        epoch_created_distance,
                        normalising_constant
                    )

                    # Add to total similarity
                    total_similarity += similarity

                # Save result
                key = f"{copy_number_distance.__class__.__name__}_{epoch_created_distance.__class__.__name__}_{normalising_constant}"
                solution[key] = total_similarity

