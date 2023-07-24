#DONE
from prismm.run_build_trees_and_timings.get_all_trees import sort_tree, compare_trees, forests_are_equal, insert_node, complete_trees, generate_trees, max_tree_depth, get_all_trees

def test_sort_tree():
    # Test case 1: Empty tree
    tree = None
    result = sort_tree(tree)
    assert result is None, f'Expected None, but got {result}'

    # Test case 2: Tree with a single value
    tree = (5,)
    result = sort_tree(tree)
    assert result == (5,), f'Expected (5,), but got {result}'

    # Test case 3: Tree with two values
    tree = (4, (2,))
    result = sort_tree(tree)
    assert result == (4, (2,)), f'Expected (4, (2,)), but got {result}'

    # Test case 4: Tree with three values
    tree = (3, (5,), (2,))
    result = sort_tree(tree)
    assert result == (3, (5,), (2,)), f'Expected (3, (5,), (2,)), but got {result}'

    # Test case 5: Tree with nested values
    tree = (7, (4, (8,), (6,)), (9,))
    result = sort_tree(tree)
    assert result == (7, (9,), (4, (8,), (6,))), f'Expected (7, (9,), (4, (8,), (6,))), but got {result}'

    # Test case 6: Input is not a tuple
    tree = "not a tuple"
    try:
        sort_tree(tree)
    except AssertionError:
        pass
    else:
        assert False, 'Expected AssertionError, but no error was raised'

    # Test case 7: Input is not None or a tuple
    tree = 123
    try:
        sort_tree(tree)
    except AssertionError:
        pass
    else:
        assert False, 'Expected AssertionError, but no error was raised'


def test_compare_trees():
    test_cases = [
        ((5, (3,), (2, (1,), (1,))), (5, (3,), (2, (1,), (1,))), True),
        ((5, (3,), (2, (1,), (1,))), (5, (2, (1,), (1,)), (3,)), True),
        ((5, (4,), (1, (1,), (0,))), (5, (1, (1,), (0,)), (4,)), True),
        ((1,), (1,), True),  # single element trees
        ((), (), True),  # empty trees
        (None, None, True),  # both trees are None
        ((5, (3,), (2,)), (5, (2,), (3,)), True),  # same values, different structure
        ((5, (3,), (2,)), (4, (3,), (2,)), False),  # different values, same structure
        ((5, (3,), (2,)), (4, (3,)), False),  # different values, different structure
        ((5,) * 1000, (5,) * 1000, True),  # large trees
        ((5, (3,), (2,)), (6, (3,), (2,)), False),  # same structure, different values
        ((5, (3,), (2,)), None, False),  # tree and None
        ((5, (3,), (2,)), (4,), False),  # different structures, different number of values
    ]

    for i, (tree1, tree2, expected_result) in enumerate(test_cases):
        result = compare_trees(tree1, tree2)
        assert result == expected_result, f'Test case {i+1} failed. Input: {tree1} vs {tree2}. Expected {expected_result}, but got {result}'



def test_forests_are_equal():
    test_cases = [
        ([(5, (3,), (2, (1,), (1,))), (5, (2, (1,), (1,)), (3,))], [(5, (3,), (2, (1,), (1,))), (5, (2, (1,), (1,)), (3,))], True),
        ([(5, (3,), (2, (1,), (1,))), (5, (4,), (1, (1,), (0,)))], [(5, (3,), (2, (1,), (1,))), (5, (1, (1,), (0,)), (4,))], True),
        ([(5, (3,), (2, (1,), (1,))), (5, (3,), (2, (1,), (1,))), (5, (2, (1,), (1,)), (3,)), (5, (4,), (1, (1,), (0,)))], 
         [(5, (2, (1,), (1,)), (3,)), (5, (3,), (2, (1,), (1,))), (5, (1, (1,), (0,)), (4,)), (5, (3,), (2, (1,), (1,)))], True),
        ([(1,)], [(1,)], True),  # forests with one tree
        ([], [], True),  # empty forests
    ]

    for i, (forest1, forest2, expected_result) in enumerate(test_cases):
        result = forests_are_equal(forest1, forest2)
        assert result == expected_result, f'Test case {i+1} failed. Input: {forest1} vs {forest2}. Expected forests to be equal: {expected_result}, but got {result}'


def test_insert_node():
    def sort_expected_output(trees):
        return [sort_tree(tree) for tree in trees]

    # Test Case 1: Inserting a node into an empty tree
    trees = [()]
    copy_number = 5
    result = insert_node(trees, copy_number)
    expected_output = [(5,)]
    assert result == sort_expected_output(expected_output), f"Expected {expected_output}, but got {result}"

    # Test Case 2: Inserting a node into a tree with only one node
    trees = [(10,)]
    copy_number = 3
    result = insert_node(trees, copy_number)
    expected_output = [(10, (7,), (3,))]
    assert result == sort_expected_output(expected_output), f"Expected {expected_output}, but got {result}"

    # Test Case 3: Inserting a node into a tree with multiple nodes
    trees = [(12, (5,), (7,))]
    copy_number = 2
    result = insert_node(trees, copy_number)
    expected_output = [
                        (12, (5, (3,), (2,)), (7,)),
                        (12, (5,), (7, (5,), (2,))),
                        (12, (5, (3,), (2,)), (7, (5,), (2,)))
                      ]
    assert result == sort_expected_output(expected_output), f"Expected {expected_output}, but got {result}"

    # Test Case 4: Inserting a node with a copy number greater than the root's copy number
    trees = [(7,)]
    copy_number = 10
    result = insert_node(trees, copy_number)
    expected_output = []
    assert result == sort_expected_output(expected_output), f"Expected {expected_output}, but got {result}"

    # Test Case 5: Inserting a node with a copy number that's equal to the root node
    trees = [(5,)]
    copy_number = 5
    result = insert_node(trees, copy_number)
    expected_output = []
    assert result == sort_expected_output(expected_output), f"Expected {expected_output}, but got {result}"

    # Test Case 6: Inserting a node into a tree with several nodes
    trees = [(15, (10,), (5,))]
    copy_number = 3
    result = insert_node(trees, copy_number)
    expected_output = [
                        (15, (10, (7,), (3,)), (5,)),
                        (15, (10,), (5, (2,), (3,))),
                        (15, (10, (7,), (3,)), (5, (2,), (3,)))
                      ]
    assert result == sort_expected_output(expected_output), f"Expected {expected_output}, but got {result}"

    # Test Case 7: Inserting a node into multiple trees
    trees = [(15, (10,), (5,)), (10, (5,), (3,))]
    copy_number = 2
    result = insert_node(trees, copy_number)
    expected_output = [
                        (15, (10, (8,), (2,)), (5,)),
                        (15, (10,), (5, (3,), (2,))),
                        (15, (10, (8,), (2,)), (5, (3,), (2,))),
                        (10, (5, (3,), (2,)), (3,)),
                        (10, (5,), (3, (1,), (2,))),
                        (10, (5, (3,), (2,)), (3, (1,), (2,)))
                      ]
    assert result == sort_expected_output(expected_output), f"Expected {expected_output}, but got {result}"

def test_complete_trees():
    trees = [
        (2, (1,), (1,)),
        (3, (1,), (2,)),
        (4, (2,), (2,))
    ]

    completed_trees_result = complete_trees(trees)
    # Convert each tree in the result set to a list for easier comparison
    completed_trees_result = sorted([list(tree) for tree in completed_trees_result])
    expected_result = [
        [2, (1,), (1,)],
        [3, (2, (1,), (1,)), (1,)],
        [4, (2, (1,), (1,)), (2, (1,), (1,))]
    ]

    assert completed_trees_result == expected_result, f"Unexpected tree: {completed_trees_result}"

    trees = [
        (6, (4,), (2,)),
        (2, (2,), (0,))
    ]

    completed_trees_result = complete_trees(trees)
    # Convert each tree in the result set to a list for easier comparison
    completed_trees_result = sorted([list(tree) for tree in completed_trees_result])
    expected_result = [
        [2, (2, (1,), (1,)), (0,)], 
        [6, (4, (2, (1,), (1,)), (2, (1,), (1,))), (2, (1,), (1,))], 
        [6, (4, (3, (2, (1,), (1,)), (1,)), (1,)), (2, (1,), (1,))]
    ]

    assert completed_trees_result == expected_result, f"Unexpected tree: {completed_trees_result}"


def test_generate_trees():
    # Test case 1
    observed_CNs_1 = [3, 2]
    SNV_CNs_1 = [3, 2]
    expected_trees_1 = [(5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,)))]
    expected_trees_1 = [sort_tree(tree) for tree in expected_trees_1]
    result_trees_1 = generate_trees(observed_CNs_1, SNV_CNs_1)
    assert forests_are_equal(result_trees_1, expected_trees_1), f"Expected {expected_trees_1}, but got {result_trees_1}"

    # Test case 2
    observed_CNs_2 = [4, 1]
    SNV_CNs_2 = [2]
    expected_trees_2 = [(5, (4, (2, (1,), (1,)), (2, (1,), (1,))), (1,))]
    expected_trees_2 = [sort_tree(tree) for tree in expected_trees_2]
    result_trees_2 = generate_trees(observed_CNs_2, SNV_CNs_2)
    assert forests_are_equal(result_trees_2, expected_trees_2), f"Expected {expected_trees_2}, but got {result_trees_2}"

    observed_CNs_3 = [3, 0]
    SNV_CNs_3 = [3, 2, 1]
    result_trees_3 = generate_trees(observed_CNs_3, SNV_CNs_3)
    expected_trees_3 = [(3, (3, (2, (1,), (1,)), (1,)), (0,))]
    expected_trees_3 = [sort_tree(tree) for tree in expected_trees_3]
    assert forests_are_equal(result_trees_3, expected_trees_3), f"Expected {expected_trees_3}, but got {result_trees_3}"


def test_max_tree_depth():
    tree1 = (6, (3,), (3, (2,), (1,)))
    tree2 = (1, (2, (3,)), (4, (5, (6,))))
    tree3 = (1,)
    tree4 = ()
    tree5 = (1, (2, (3, (4, (5, (6,))))))
    tree6 = (4, (2, (1,), (1,)), (2, (1,), (1,)))

    assert max_tree_depth(tree1) == 3, f"Failed for tree1: {tree1}"
    assert max_tree_depth(tree2) == 4, f"Failed for tree2: {tree2}"
    assert max_tree_depth(tree3) == 1, f"Failed for tree3: {tree3}"
    assert max_tree_depth(tree4) == 0, f"Failed for tree4: {tree4}"
    assert max_tree_depth(tree5) == 6, f"Failed for tree5: {tree5}"
    assert max_tree_depth(tree6) == 3, f"Failed for tree5: {tree5}"

def test_get_all_trees():
    # Test case 1: every chromosome has the same multiplicity and copy number
    observed_SNV_multiplicities_1 = {"chrom1": {3: 1, 2: 1, 1: 1}, "chrom2": {2: 1}, "chrom3": {1: 1}}
    observed_copy_numbers_1 = {"chrom1": [4, 1], "chrom2": [3, 0], "chrom3": [2, 2]}
    total_epochs_1 = 3
    tree_flexibility_1 = 3
    result_trees_1 = get_all_trees(observed_SNV_multiplicities_1, observed_copy_numbers_1, total_epochs_1, tree_flexibility_1)
    expected_trees_1 = {
        'chrom1': [(5, (4, (3, (2, (1,), (1,)), (1,)), (1,)), (1,))], 
        'chrom2': [(3, (3, (2, (1,), (1,)), (1,)), (0,))], 
        'chrom3': [(4, (2, (1,), (1,)), (2, (1,), (1,)))]
    }  
    assert result_trees_1 == expected_trees_1, f"Expected {expected_trees_1}, but got {result_trees_1}"

    # Test case 2: have too few epochs
    total_epochs_2 = 2
    result_trees_2 = get_all_trees(observed_SNV_multiplicities_1, observed_copy_numbers_1, total_epochs_2, tree_flexibility_1)
    expected_trees_2 = None  # Needs to be replaced with actual expected result
    assert result_trees_2 == expected_trees_2, f"Expected {expected_trees_2}, but got {result_trees_2}"

    # Test case 3: reduce tree_flexibility too far
    total_epochs_3 = 3
    tree_flexibility_3 = 1
    result_trees_3 = get_all_trees(observed_SNV_multiplicities_1, observed_copy_numbers_1, total_epochs_3, tree_flexibility_3)
    expected_trees_3 = None  # Needs to be replaced with actual expected result
    assert result_trees_3 == expected_trees_3, f"Expected {expected_trees_3}, but got {result_trees_3}"


if __name__ == "__main__":
    test_sort_tree()
    test_compare_trees()
    test_forests_are_equal()
    test_insert_node()
    test_complete_trees()
    test_generate_trees()
    test_max_tree_depth()
    test_get_all_trees()