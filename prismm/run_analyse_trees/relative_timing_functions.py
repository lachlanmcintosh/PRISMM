"""
Module: Timing Comparison

This module provides functionalities for extracting, aligning, and comparing timing values from tree-like data structures. It is used to compare "truth" tree structures against "solution" tree structures using different comparison operators. These functionalities are encapsulated in four main functions:

1. extract_timing_values: Recursive function to extract timing values from a tree structure.
2. align_timing_values: Aligns the timing value lists by padding the shorter one with the last element of the longer list.
3. compare_relative_timing: Compares relative timing of nodes across multiple chromosomes using a specified operator.
4. add_relative_timing_comparison: Applies the compare_relative_timing function to each solution in a provided structure and stores the results in new keys.

Each function's specific functionality, parameters, and return values are documented within the respective function's docstring.
"""


from typing import Dict, List, Tuple, Optional


def extract_timing_values(node: Dict, epochs: List[Tuple[int]], is_root: bool = True) -> None:
    """
    Recursive function to extract timing values from a tree structure.

    :param node: The current node in the tree.
    :param epochs: The list of timing values collected so far.
    :param is_root: A flag to indicate if the node is the root node.
    """
    assert isinstance(node, dict), "Expected 'node' to be a dictionary"
    assert isinstance(epochs, list), "Expected 'epochs' to be a list"
    assert isinstance(is_root, bool), "Expected 'is_root' to be a boolean"

    if not is_root:  # Only append if it's not the root
        epochs.append((node['epoch_index'],))
        
    if 'complement' in node:
        extract_timing_values(node['complement'], epochs, is_root=False)
    if 'child' in node:
        extract_timing_values(node['child'], epochs, is_root=False)


def align_timing_values(truth_epochs: List[Tuple[int]], solution_epochs: List[Tuple[int]]) -> Tuple[List[Tuple[int]], List[Tuple[int]]]:
    """
    Aligns the timing value lists by padding the shorter one with the last element of the longer list.

    :param truth_epochs: List of truth timing values.
    :param solution_epochs: List of solution timing values.
    :return: The aligned lists of truth and solution timing values.
    """
    assert isinstance(truth_epochs, list), "Expected 'truth_epochs' to be a list"
    assert isinstance(solution_epochs, list), "Expected 'solution_epochs' to be a list"
    
    difference = len(solution_epochs) - len(truth_epochs)
    if difference > 0:
        truth_epochs += [truth_epochs[-1]] * difference
    elif difference < 0:
        solution_epochs += [solution_epochs[-1]] * -difference
    return truth_epochs, solution_epochs


def compare_relative_timing(SS: Dict, solution: Dict, operator: str, is_root: bool = True) -> Tuple[int, int, int]:
    """
    Compares relative timing of nodes across multiple chromosomes using a specified operator.

    :param SS: The truth tree structure.
    :param solution: The solution tree structure.
    :param operator: The operator to use for comparison ("<" or "<=").
    :param is_root: A flag to indicate if the root node should be included in the comparison.
    :return: The count of correct, incorrect and missing comparisons.
    """
    assert operator in ["<", "<="], "Expected 'operator' to be '<' or '<='"
    
    count_true = 0
    count_false = 0
    count_missing = 0

    for chromosome in SS["simplified_truth_trees"]:
        truth_epochs = []
        solution_epochs = []

        extract_timing_values(SS["simplified_truth_trees"][chromosome], truth_epochs, is_root)
        extract_timing_values(solution[chromosome]["dict_tree"], solution_epochs, is_root)

        truth_epochs, solution_epochs = align_timing_values(truth_epochs, solution_epochs)

        for i, _ in enumerate(truth_epochs):
            for j in range(i + 1, len(truth_epochs)):
                truth = truth_epochs[i] < truth_epochs[j] if operator == "<" else truth_epochs[i] <= truth_epochs[j]
                solution = solution_epochs[i] < solution_epochs[j] if operator == "<" else solution_epochs[i] <= solution_epochs[j]

                if truth and solution:
                    count_true += 1
                elif truth and not solution:
                    count_false += 1

                if solution_epochs[i] is None or solution_epochs[j] is None:
                    count_missing += 1

    return count_true, count_false, count_missing


def add_relative_timing_comparison(SS: Dict, is_root: bool = True) -> Dict:
    """
    Applies the compare_relative_timing function to each solution in SS["solutions"] and stores the results in new keys.

    :param SS: The original structure of solutions and truth.
    :param is_root: A flag to indicate if the root node should be included in the comparison.
    :return: The updated structure with added comparison results.
    """
    assert "solutions" in SS, "Expected 'solutions' key in SS"
    
    for solution in SS["solutions"]:
        for operator in ["<", "<="]:
            count_true, count_false, count_missing = compare_relative_timing(SS, solution, operator, is_root)
            solution["counts_" + operator] = {
                "count_true": count_true,
                "count_false": count_false,
                "count_missing": count_missing
            }
    return SS
