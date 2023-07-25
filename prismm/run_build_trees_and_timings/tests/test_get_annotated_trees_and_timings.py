from prismm.run_build_trees_and_timings.get_annotated_trees_and_timings import (
    calculate_branch_lengths,
    extract_copy_numbers,
    find_indices,
    stack_same_CN_branch_lengths,
    get_branch_lengths
)
import numpy as np

def test_calculate_branch_lengths():
    # Define inputs
    epochs_created = np.array([
        [1, 2, 3, 4], 
        [2, 3, 4, 5]
        ])
    parents = {1: 0, 2: 1, 3: 2}
    max_epoch = 5

    # Define expected output
    expected_output = np.array([
        [1, 1, 1, 1], 
        [1, 1, 1, 0]
        ])

    # Call the function with the inputs
    output = calculate_branch_lengths(epochs_created, parents, max_epoch)

    # Assert that the function output matches the expected output
    assert np.array_equal(output, expected_output), f"For inputs {epochs_created}, {parents}, {max_epoch}, expected output was {expected_output} but got {output}"


    # Test with a larger epochs_created array
    epochs_created = np.array([
        [1, 2, 3, 4, 5, 6, 7],
        [2, 3, 4, 5, 6, 7, 8]
    ])
    parents = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}
    max_epoch = 8
    expected_output = np.array([
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0]
    ])
    output = calculate_branch_lengths(epochs_created, parents, max_epoch)
    assert np.array_equal(output, expected_output), f"For inputs {epochs_created}, {parents}, {max_epoch}, expected output was {expected_output} but got {output}"

    # Test with a 3D epochs_created array
    epochs_created = np.array([
        [1, 2, 3], 
        [4, 5, 6],
        [2, 3, 4], 
        [5, 6, 7]
        ])
    parents = {1: 0, 2: 1}
    max_epoch = 7
    expected_output = np.array([
        [1, 1, 4],
        [1, 1, 1],
        [1, 1, 3],
        [1, 1, 0]
        ])
    output = calculate_branch_lengths(epochs_created, parents, max_epoch)
    assert np.array_equal(output, expected_output), f"For inputs {epochs_created}, {parents}, {max_epoch}, expected output was {expected_output} but got {output}"


def test_extract_copy_numbers():
    # Testing with a simple tree structure
    tree = '(1, (2, 3))'
    assert extract_copy_numbers(tree) == [1, 2, 3]

    # Testing with a more complex tree structure
    tree = '(1, (2, (3, 4)), 5)'
    assert extract_copy_numbers(tree) == [1, 2, 3, 4, 5]

    # Testing with non-integer values in the tree
    tree = '(a, (b, c))'
    assert extract_copy_numbers(tree) == []

    # Testing with an empty tree
    tree = ''
    assert extract_copy_numbers(tree) == []


def test_find_indices():
    # Testing with an integer list
    assert find_indices([1, 2, 3, 2, 4, 2], 2) == [1, 3, 5]

    # Testing with a string list
    assert find_indices(['a', 'b', 'c', 'b', 'd', 'b'], 'b') == [1, 3, 5]


def test_stack_same_CN_branch_lengths():
    # Testing with valid copy_numbers and branch_lengths
    copy_numbers = [1, 2, 3, 2, 1]
    branch_lengths = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
    result = stack_same_CN_branch_lengths(copy_numbers, branch_lengths)
    assert np.array_equal(result[0], np.array([[3, 6, 5], [8, 16, 10]])), f"Expected different branch lengths, got {result[0]}"
    assert result[1] == [3, 2, 1], f"Expected different copy numbers, got {result[1]}"

    # Testing with all copy numbers the same
    copy_numbers = [1, 1, 1, 1, 1]
    branch_lengths = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
    result = stack_same_CN_branch_lengths(copy_numbers, branch_lengths)
    assert np.array_equal(result[0], np.array([[14], [34]])), f"Expected different branch lengths, got {result[0]}"
    assert result[1] == [1], f"Expected different copy numbers, got {result[1]}"

    # Testing with all branch lengths the same
    copy_numbers = [1, 2, 3, 2, 1]
    branch_lengths = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]])
    result = stack_same_CN_branch_lengths(copy_numbers, branch_lengths)
    assert np.array_equal(result[0], np.array([[1, 2, 1], [1, 2, 1]])), f"Expected different branch lengths, got {result[0]}"
    assert result[1] == [3, 2, 1], f"Expected different copy numbers, got {result[1]}"

def test_get_branch_lengths():
    # Define mock data
    tts = {
        "epochs_created": np.array([
            [1, 2, 3], 
            [2, 3, 4]
        ]),
        "parents": {1: 0, 2: 1},
        "tree": (3, (2, 1))
    }
    max_epoch = 5

    # Call the function with the mock data
    output = get_branch_lengths(tts, max_epoch)

    # Define expected output
    expected_output = {
        'epochs_created': np.array([
            [1, 2, 3], 
            [2, 3, 4]
        ]),
        'parents': {1: 0, 2: 1},
        'tree': (3, (2, 1)),
        'branch_lengths': np.array([
            [1, 1, 2], 
            [1, 1, 1]
        ]),
        'CNs': [3, 2, 1],
        'stacked_branch_lengths': np.array([
            [1, 2], 
            [1, 1]
        ]),
        'unique_CNs': [2, 1]
    }

    # Assert that the function output matches the expected output
    assert np.array_equal(output['epochs_created'], expected_output['epochs_created']), \
        "Mismatch in 'epochs_created'"
    assert output['parents'] == expected_output['parents'], "Mismatch in 'parents'"
    assert output['tree'] == expected_output['tree'], "Mismatch in 'tree'"
    assert np.array_equal(output['branch_lengths'], expected_output['branch_lengths']), \
        "Mismatch in 'branch_lengths'"
    assert output['CNs'] == expected_output['CNs'], "Mismatch in 'CNs'"
    assert np.array_equal(output['stacked_branch_lengths'], expected_output['stacked_branch_lengths']), \
        "Mismatch in 'stacked_branch_lengths'"
    assert output['unique_CNs'] == expected_output['unique_CNs'], "Mismatch in 'unique_CNs'"

    # Test with invalid max_epoch
    tts = {
        "epochs_created": np.array([
            [0, 0, 1, 1], 
            [0, 0, 2, 2]
        ]),
        "parents": {1: 0, 2: 1, 3: 2},
        "tree": (4, (2, (1,1)))
    }
    max_epoch = 2
    output = get_branch_lengths(tts, max_epoch)

    # Define expected output for invalid max_epoch
    expected_output = {
        'epochs_created': np.array([
            [0, 0, 1, 1], 
            [0, 0, 2, 2]
        ]),
        'parents': {1: 0, 2: 1, 3: 2},
        'tree': (4, (2, (1, 1))),
        'branch_lengths': np.array([
            [0, 1, 0, 1], 
            [0, 2, 0, 0]
        ]),
        'CNs': [4, 2, 1, 1],
        'stacked_branch_lengths': np.array([
            [1, 1], 
            [2, 0]
        ]),
        'unique_CNs': [2, 1]
    }

    assert np.array_equal(output['epochs_created'], expected_output['epochs_created']), \
        "Mismatch in 'epochs_created'"
    assert output['parents'] == expected_output['parents'], "Mismatch in 'parents'"
    assert output['tree'] == expected_output['tree'], "Mismatch in 'tree'"
    assert np.array_equal(output['branch_lengths'], expected_output['branch_lengths']), \
        "Mismatch in 'branch_lengths'"
    assert output['CNs'] == expected_output['CNs'], "Mismatch in 'CNs'"
    assert np.array_equal(output['stacked_branch_lengths'], expected_output['stacked_branch_lengths']), \
        "Mismatch in 'stacked_branch_lengths'"
    assert output['unique_CNs'] == expected_output['unique_CNs'], "Mismatch in 'unique_CNs'"



# Run the test function
if __name__ == "__main__":
    test_calculate_branch_lengths()
    test_extract_copy_numbers()
    test_find_indices()
    test_stack_same_CN_branch_lengths()
    test_get_branch_lengths()
