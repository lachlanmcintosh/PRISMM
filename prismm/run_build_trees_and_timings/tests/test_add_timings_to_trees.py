#DONE
from prismm.run_build_trees_and_timings.add_timings_to_trees import (
    get_timings_per_tree,
    initialize_epochs_created,
    find_sibling,
    create_epochs_temp,
    get_timings_per_chrom,
    handle_other_nodes,
    get_all_timings
)
import numpy as np
import logging

#logging.basicConfig(level=logging.DEBUG)

def test_initialize_epochs_created():
    logging.info("running test_initialize_epochs_created")

    # Normal case
    epochs_created = initialize_epochs_created(num_labels=4, zero_epoch_nodes=[1, 3])
    assert epochs_created.shape == (1, 4)
    assert epochs_created[0, 0] == 0
    assert epochs_created[0, 1] == 1
    assert epochs_created[0, 2] == None
    assert epochs_created[0, 3] == 1

    # Error cases
    try:
        initialize_epochs_created(num_labels=0, zero_epoch_nodes=[0, 1])
    except AssertionError:
        pass
    else:
        assert False, "Expected AssertionError"

    try:
        initialize_epochs_created(num_labels=-1, zero_epoch_nodes=[0, 1])
    except AssertionError:
        pass
    else:
        assert False, "Expected AssertionError"


def test_get_timings_per_tree():
    logging.info("running test_get_timings_per_tree")

    # TEST 1
    tree = (6, (4, (2, (1,), (1,)), (2, (1,), (1,))), (2, (1,), (1,)))
    
    # Define the expected results
    expected_tree = (6, (4, (2, (1,), (1,)), (2, (1,), (1,))), (2, (1,), (1,)))
    expected_labelled_tree = [0, [1, [2, [3], [4]], [5, [6], [7]]], [8, [9], [10]]]
    expected_label_count = 10
    expected_epochs_created = np.array([[0, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1],
                                        [0, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2]], dtype=object)
    expected_parents = {3: 2, 4: 2, 2: 1, 6: 5, 7: 5, 5: 1, 1: 0, 9: 8, 10: 8, 8: 0}
    TOTAL_EPOCHS_EST = 2

    # Call the function and get the result
    result = get_timings_per_tree(tree=tree, total_epochs_est=TOTAL_EPOCHS_EST)
    result_tree, result_labelled_tree, result_label_count, result_epochs_created, result_parents = result

    # Compare each element of the result with the expected result
    assert result_tree == expected_tree, f'For tree, expected {expected_tree} but got {result_tree}'
    assert result_labelled_tree == expected_labelled_tree, f'For labelled_tree, expected {expected_labelled_tree} but got {result_labelled_tree}'
    assert result_label_count == expected_label_count, f'For label_count, expected {expected_label_count} but got {result_label_count}'
    assert np.array_equal(result_epochs_created, expected_epochs_created), f'For epochs_created, expected {expected_epochs_created} but got {result_epochs_created}'
    assert result_parents == expected_parents, f'For parents, expected {expected_parents} but got {result_parents}'


    # TEST 2
    TOTAL_EPOCHS_EST = 3
    result = get_timings_per_tree(tree=tree, total_epochs_est=TOTAL_EPOCHS_EST)
    result_tree, result_labelled_tree, result_label_count, result_epochs_created, result_parents = result

    expected_epochs_created = np.array([[0, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1],
        [0, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2],
        [0, 1, 2, 2, 2, 2, 2, 2, 1, 3, 3],
        [0, 1, 2, 2, 2, 2, 3, 3, 1, 1, 1],
        [0, 1, 2, 2, 2, 2, 3, 3, 1, 2, 2],
        [0, 1, 2, 2, 2, 2, 3, 3, 1, 3, 3],
        [0, 1, 2, 3, 3, 2, 2, 2, 1, 1, 1],
        [0, 1, 2, 3, 3, 2, 2, 2, 1, 2, 2],
        [0, 1, 2, 3, 3, 2, 2, 2, 1, 3, 3],
        [0, 1, 2, 3, 3, 2, 3, 3, 1, 1, 1],
        [0, 1, 2, 3, 3, 2, 3, 3, 1, 2, 2],
        [0, 1, 2, 3, 3, 2, 3, 3, 1, 3, 3],
        [0, 1, 3, 3, 3, 3, 3, 3, 1, 1, 1],
        [0, 1, 3, 3, 3, 3, 3, 3, 1, 2, 2],
        [0, 1, 3, 3, 3, 3, 3, 3, 1, 3, 3]]
        )

    assert result_tree == expected_tree, f'For tree, expected {expected_tree} but got {result_tree}'
    assert result_labelled_tree == expected_labelled_tree, f'For labelled_tree, expected {expected_labelled_tree} but got {result_labelled_tree}'
    assert result_label_count == expected_label_count, f'For label_count, expected {expected_label_count} but got {result_label_count}'
    assert np.array_equal(result_epochs_created, expected_epochs_created), f'For epochs_created, expected {expected_epochs_created} but got {result_epochs_created}'
    assert result_parents == expected_parents, f'For parents, expected {expected_parents} but got {result_parents}'


def test_find_sibling():
    logging.info("running test_find_sibling")

    # Define a test parents dictionary
    parents = {
        2: 1,
        3: 1,
        4: 5,
        6: 5
    }

    # Test case 1: normal case
    sibling = find_sibling(parents=parents, query_key=2)
    assert sibling == 3, f"Expected 3, but got {sibling}"

    # Test case 2: normal case
    sibling = find_sibling(parents=parents, query_key=4)
    assert sibling == 6, f"Expected 6, but got {sibling}"

    # Test case 3: query_key does not exist in parents
    sibling = find_sibling(parents=parents, query_key=7)
    assert sibling == [], f"Expected [], but got {sibling}"

    # Test case 4: no sibling for query_key
    sibling = find_sibling(parents=parents, query_key=1)
    assert sibling == [], f"Expected [], but got {sibling}"

def test_create_epochs_temp():
    logging.info("running test_create_epochs_temp")

    # Test case 1: when parents_time is less than total_epochs_est and copy_number is 1
    epochs_created_row = np.array([0, None, None])
    temp = create_epochs_temp(epochs_created_row=epochs_created_row, label=1, parents_time=2, total_epochs_est=5, copy_number=1)
    expected = np.array([[0, 2, None], [0, 3, None], [0, 4, None], [0, 5, None]])
    assert np.array_equal(temp, expected), f"Expected {expected}, but got {temp}"

    # Test case 2: when parents_time is less than total_epochs_est
    epochs_created_row = np.array([0, None, None])
    temp = create_epochs_temp(epochs_created_row=epochs_created_row, label=1, parents_time=1, total_epochs_est=5, copy_number=2)
    expected = np.array([[0, 2, None], [0, 3, None], [0, 4, None], [0, 5, None]])
    assert np.array_equal(temp, expected), f"Expected {expected}, but got {temp}"

    # Test case 3: when parents_time is equal to total_epochs_est and copy_number is 1
    epochs_created_row = np.array([0, None, None])
    temp = create_epochs_temp(epochs_created_row=epochs_created_row, label=1, parents_time=5, total_epochs_est=5, copy_number=1)
    expected = np.array([[0, 5, None]])
    assert np.array_equal(temp, expected), f"Expected {expected}, but got {temp}"

    # Test case 4: when parents_time is greater than total_epochs_est
    epochs_created_row = np.array([0, None, None])
    temp = create_epochs_temp(epochs_created_row=epochs_created_row, label=1, parents_time=6, total_epochs_est=5, copy_number=2)
    assert temp is None, f"Expected None, but got {temp}"

def test_handle_other_nodes():
    # Import necessary modules
    import numpy as np
    from typing import Dict

    logging.info("running test_handle_other_nodes")

    # Test case 1: normal case
    epochs_created = np.array([[0, 1, None, None], [0, 2, None, None]])
    label_to_copy = {2: 1, 3: 2}
    label = 2
    parent = 1
    total_epochs_est = 5

    result = handle_other_nodes(epochs_created=epochs_created, label_to_copy=label_to_copy, label=label, parent=parent, total_epochs_est=total_epochs_est)
    expected = np.array([
        [0, 1, 1, None],
        [0, 1, 2, None],
        [0, 1, 3, None],
        [0, 1, 4, None],
        [0, 1, 5, None],
        [0, 2, 2, None],
        [0, 2, 3, None],
        [0, 2, 4, None],
        [0, 2, 5, None]])
    assert np.array_equal(result, expected), f"Expected {expected}, but got {result}"

    logging.info("test_handle_other_nodes passed.")

def test_get_timings_per_chrom():

    # Define input
    all_trees = [
        (6, (4, (2, (1,), (1,)), (2, (1,), (1,))), (2, (1,), (1,))),
        (5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,)))
    ]
    total_epochs_est = 2


    # Define expected result
    expected_result = [
        (
            (6, (4, (2, (1,), (1,)), (2, (1,), (1,))), (2, (1,), (1,))), 
            [0, [1, [2, [3], [4]], [5, [6], [7]]], [8, [9], [10]]], 
            10, 
            np.array([[0, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1],
                      [0, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2]], dtype=object), 
            {3: 2, 4: 2, 2: 1, 6: 5, 7: 5, 5: 1, 1: 0, 9: 8, 10: 8, 8: 0}
        ),
        (
            (5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,))), 
            [0, [1, [2, [3], [4]], [5]], [6, [7], [8]]], 
            8, 
            np.array([[0, 1, 2, 2, 2, 2, 1, 1, 1],
                      [0, 1, 2, 2, 2, 2, 1, 2, 2]], dtype=object), 
            {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 7: 6, 8: 6, 6: 0}
        )
    ]

    # Call the function
    result = get_timings_per_chrom(all_trees=all_trees, total_epochs_est=total_epochs_est)

    # Check that the result matches the expected result
    for (res_tree, res_labelled_tree, res_label_count, res_epochs_created, res_parents), \
        (exp_tree, exp_labelled_tree, exp_label_count, exp_epochs_created, exp_parents) \
        in zip(result, expected_result):

        assert res_tree == exp_tree, f"For tree, expected {exp_tree}, but got {res_tree}"
        assert res_labelled_tree == exp_labelled_tree, f"For labelled_tree, expected {exp_labelled_tree}, but got {res_labelled_tree}"
        assert res_label_count == exp_label_count, f"For label_count, expected {exp_label_count}, but got {res_label_count}"
        assert np.array_equal(res_epochs_created, exp_epochs_created), f"For epochs_created, expected {exp_epochs_created}, but got {res_epochs_created}"
        assert res_parents == exp_parents, f"For parents, expected {exp_parents}, but got {res_parents}"
    
    # Check that the result is a list
    assert isinstance(result, list), f"Expected result to be a list, but got {type(result)}"

    # Check that each item in the list is a tuple of length 5
    for item in result:
        assert isinstance(item, tuple) and len(item) == 5, f"Expected each item to be a tuple of length 5, but got {item}"

    # Check that the third item of each tuple is an integer
    for item in result:
        assert isinstance(item[2], int), f"Expected third item of each tuple to be an integer, but got {item[2]}"

    # Check that the fourth item of each tuple is an np.ndarray
    for item in result:
        assert isinstance(item[3], np.ndarray), f"Expected fourth item of each tuple to be an np.ndarray, but got {item[3]}"

    # Check that the fifth item of each tuple is a dict
    for item in result:
        assert isinstance(item[4], dict), f"Expected fifth item of each tuple to be a dict, but got {item[4]}"

    logging.info("test_get_timings_per_chrom passed.")



def test_get_all_timings():

    # Define input
    trees = {
        'chrom1': [(6, (4, (2, (1,), (1,)), (2, (1,), (1,))), (2, (1,), (1,)))],
        'chrom2': [(5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,)))]
    }
    total_epochs_est = 2

    # Define expected result
    expected_result = {
        'chrom1': [
            (
                (6, (4, (2, (1,), (1,)), (2, (1,), (1,))), (2, (1,), (1,))),
                [0, [1, [2, [3], [4]], [5, [6], [7]]], [8, [9], [10]]],
                10, 
                np.array([[0, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1],
                          [0, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2]], dtype=object), 
                {3: 2, 4: 2, 2: 1, 6: 5, 7: 5, 5: 1, 1: 0, 9: 8, 10: 8, 8: 0}
            )
        ],
        'chrom2': [
            (
                (5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,))),
                [0, [1, [2, [3], [4]], [5]], [6, [7], [8]]],
                8, 
                np.array([[0, 1, 2, 2, 2, 2, 1, 1, 1],
                          [0, 1, 2, 2, 2, 2, 1, 2, 2]], dtype=object), 
                {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 7: 6, 8: 6, 6: 0}
            )
        ]
    }

    # Call the function
    result = get_all_timings(trees=trees, total_epochs_est=total_epochs_est)

    # Check that the result matches the expected result
    assert set(result.keys()) == set(expected_result.keys()), f"For keys, expected {set(expected_result.keys())}, but got {set(result.keys())}"
    
    for chrom in result.keys():
        for (res_tree, res_labelled_tree, res_label_count, res_epochs_created, res_parents), \
            (exp_tree, exp_labelled_tree, exp_label_count, exp_epochs_created, exp_parents) \
            in zip(result[chrom], expected_result[chrom]):

            assert res_tree == exp_tree, f"For tree, expected {exp_tree}, but got {res_tree}"
            assert res_labelled_tree == exp_labelled_tree, f"For labelled_tree, expected {exp_labelled_tree}, but got {res_labelled_tree}"
            assert res_label_count == exp_label_count, f"For label_count, expected {exp_label_count}, but got {res_label_count}"
            assert np.array_equal(res_epochs_created, exp_epochs_created), f"For epochs_created, expected {exp_epochs_created}, but got {res_epochs_created}"
            assert res_parents == exp_parents, f"For parents, expected {exp_parents}, but got {res_parents}"
    
    logging.info("test_get_all_timings passed.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logging.info("Starting tests...")
    test_get_timings_per_tree()
    test_find_sibling()
    test_initialize_epochs_created()
    test_create_epochs_temp()
    test_handle_other_nodes()
    test_get_timings_per_chrom()
    test_get_all_timings()
    logging.info("All tests passed.")




# BELOW ARE OLDER TEST FUNCTIONS
# BELOW ARE OLDER TEST FUNCTIONS
# BELOW ARE OLDER TEST FUNCTIONS
# BELOW ARE OLDER TEST FUNCTIONS
# BELOW ARE OLDER TEST FUNCTIONS
# BELOW ARE OLDER TEST FUNCTIONS
# BELOW ARE OLDER TEST FUNCTIONS


# Call the test function
#test_get_timings_per_tree()


def test_get_chrom_trees_and_timings():
    test_cases = [
        {
            'input': {'tree': (6, (4, (2, (1,), (1,)), (2, (1,), (1,))), (2, (1,), (1,))), 'total_epochs_est': 2},
            'output': ((6, (4, (2, (1,), (1,)), (2, (1,), (1,))), (2, (1,), (1,))), [0, [1, [2, [3], [4]], [5, [6], [7]]], [8, [9], [10]]], 10, np.array([[-1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
       [-1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
       [-1, 0, 1, 1, 1, 1, 1, 1, 0, 2, 2],
       [-1, 0, 1, 1, 1, 1, 2, 2, 0, 0, 0],
       [-1, 0, 1, 1, 1, 1, 2, 2, 0, 1, 1],
       [-1, 0, 1, 1, 1, 1, 2, 2, 0, 2, 2],
       [-1, 0, 1, 2, 2, 1, 1, 1, 0, 0, 0],
       [-1, 0, 1, 2, 2, 1, 1, 1, 0, 1, 1],
       [-1, 0, 1, 2, 2, 1, 1, 1, 0, 2, 2],
       [-1, 0, 1, 2, 2, 1, 2, 2, 0, 0, 0],
       [-1, 0, 1, 2, 2, 1, 2, 2, 0, 1, 1],
       [-1, 0, 1, 2, 2, 1, 2, 2, 0, 2, 2],
       [-1, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0],
       [-1, 0, 2, 2, 2, 2, 2, 2, 0, 1, 1],
       [-1, 0, 2, 2, 2, 2, 2, 2, 0, 2, 2],
       [-1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1],
       [-1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2]], dtype=object), {3: 2, 4: 2, 2: 1, 6: 5, 7: 5, 5: 1, 1: 0, 9: 8, 10: 8, 8: 0})
        },
        {
            'input': {'tree': (3, (3, (2, (1,), (1,)), (1,)), (0,)), 'total_epochs_est': 2},
            'output': ((3, (3, (2, (1,), (1,)), (1,)), (0,)), [0, [1, [2, [3], [4]], [5]], [6]], 6, np.array([[-1, 0, 1, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 0],
       [-1, 0, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0})
        },
        {
            'input': {'tree': (5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,))), 'total_epochs_est': 2},
            'output': ((5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,))), [0, [1, [2, [3], [4]], [5]], [6, [7], [8]]], 8, np.array([[-1, 0, 1, 1, 1, 1, 0, 0, 0],
       [-1, 0, 1, 1, 1, 1, 0, 1, 1],
       [-1, 0, 1, 1, 1, 1, 0, 2, 2],
       [-1, 0, 1, 2, 2, 1, 0, 0, 0],
       [-1, 0, 1, 2, 2, 1, 0, 1, 1],
       [-1, 0, 1, 2, 2, 1, 0, 2, 2],
       [-1, 0, 2, 2, 2, 2, 0, 0, 0],
       [-1, 0, 2, 2, 2, 2, 0, 1, 1],
       [-1, 0, 2, 2, 2, 2, 0, 2, 2],
       [-1, 1, 2, 2, 2, 2, 1, 1, 1],
       [-1, 1, 2, 2, 2, 2, 1, 2, 2]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 7: 6, 8: 6, 6: 0})
        },
        {
            'input': {'tree': (3, (3, (2, (1,), (1,)), (1,)), (0,)), 'total_epochs_est': 2},
            'output': ((3, (3, (2, (1,), (1,)), (1,)), (0,)), [0, [1, [2, [3], [4]], [5]], [6]], 6, np.array([[-1, 0, 1, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 0],
       [-1, 0, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0})
        }
    ]

    for test_case in test_cases:
        input_data = test_case['input']
        expected_output = test_case['output']
        result = get_chrom_trees_and_timings(**input_data)
        assert result == expected_output, f'For {input_data}, expected {expected_output} but got {result}'



# Test cases for get_all_trees_and_timings function
def test_get_all_trees_and_timings():
    observed_SNV_multiplicities = {"chr1": {1: 1, 2: 1}}
    observed_CNs = {"chr1": [1, 2]}
    pre, mid, post = 1, 1, 1
    total_epochs_est = calculate_epochs(pre,mid,post) 
    trees_and_timings = get_all_trees_and_timings(observed_SNV_multiplicities, observed_CNs, pre, mid, post,total_epochs_est)

    assert "chr1" in trees_and_timings, "Chromosome key is missing in the result"
    assert len(trees_and_timings["chr1"]) > 0, "No trees and timings found for the chromosome"





def test_initialize_epochs_created():
    test_cases = [
        {"num_labels": 3, "root_label": 0, "expected": [[-1, None, None]]},
        {"num_labels": 7, "root_label": 0, "expected": [[-1, None, None, None, None, None, None]]},
        {"num_labels": 9, "root_label": 0, "expected": [[-1, None, None, None, None, None, None, None, None]]},
        {"num_labels": 11, "root_label": 0, "expected": [[-1, None, None, None, None, None, None, None, None, None, None]]}
    ]

    for test_case in test_cases:
        num_labels = test_case["num_labels"]
        root_label = test_case["root_label"]
        expected = test_case["expected"]
        
        timings = initialize_epochs_created(num_labels, root_label)
        assert timings.shape == (1, num_labels), f"Expected (1, {num_labels}), but got {timings.shape}"
        assert np.all(timings == expected), f"Expected {expected}, but got {timings}"



def test_find_sibling():
    parents = {1: 0, 2: 0, 4: 3, 5: 3}
    key = 1
    siblings = find_sibling(parents, key)
    expected_output = 2
    assert siblings == expected_output, f"Expected {expected_output}, but got {siblings}"

    key = 4
    siblings = find_sibling(parents, key)
    expected_output = 5
    assert siblings == expected_output, f"Expected {expected_output}, but got {siblings}"


def test_handle_other_nodes():
    test_cases = [
        {
            "input": {
                "epochs_created": np.array([[-1, 0, None, None, None, None, None, None, None],
                                            [-1, 1, None, None, None, None, None, None, None],
                                            [-1, 2, None, None, None, None, None, None, None]], dtype=object),
                "label_to_copy": {0: 4, 1: 4, 2: 2, 3: 1, 4: 1, 5: 2, 6: 1, 7: 1, 8: 0},
                "label": 2,
                "parent": 1,
                "total_epochs_est": 2
            },
            "expected": np.array([[-1, 0, 1, None, None, None, None, None, None],
                                  [-1, 0, 2, None, None, None, None, None, None],
                                  [-1, 1, 2, None, None, None, None, None, None]], dtype=object)
        },
        {
            "input": {
                "epochs_created": np.array([[-1, 0, 1, None, None, None, None, None, None],
                                            [-1, 0, 2, None, None, None, None, None, None],
                                            [-1, 1, 2, None, None, None, None, None, None]], dtype=object),
                "label_to_copy": {0: 4, 1: 4, 2: 2, 3: 1, 4: 1, 5: 2, 6: 1, 7: 1, 8: 0},
                "label": 3,
                "parent": 2,
                "total_epochs_est": 2
            },
            "expected": np.array([[-1, 0, 1, 1, None, None, None, None, None],
                                  [-1, 0, 1, 2, None, None, None, None, None],
                                  [-1, 0, 2, 2, None, None, None, None, None],
                                  [-1, 1, 2, 2, None, None, None, None, None]], dtype=object)
        },
        {
            "input": {
                "epochs_created": np.array([[-1, 0, 1, 1, 1, 1, None, None, None],
                                            [-1, 0, 1, 2, 2, 1, None, None, None],
                                            [-1, 0, 2, 2, 2, 2, None, None, None],
                                            [-1, 1, 2, 2, 2, 2, None, None, None]], dtype=object),
                "label_to_copy": {0: 4, 1: 4, 2: 2, 3: 1, 4: 1, 5: 2, 6: 1, 7: 1, 8: 0},
                "label": 6,
                "parent": 5,
                "total_epochs_est": 2
            },
            "expected": np.array([[-1, 0, 1, 1, 1, 1, 1, None, None],
                                  [-1, 0, 1, 1, 1, 1, 2, None, None],
                                  [-1, 0, 1, 2, 2, 1, 1, None, None],
                                  [-1, 0, 1, 2, 2, 1, 2, None, None],
                                  [-1, 0, 2, 2, 2, 2, 2, None, None],
                                  [-1, 1, 2, 2, 2, 2, 2, None, None]], dtype=object)
            }
        ]

    for i, test_case in enumerate(test_cases):
        result = handle_other_nodes(test_case["input"]["epochs_created"],
                                    test_case["input"]["label_to_copy"],
                                    test_case["input"]["label"],
                                    test_case["input"]["parent"],
                                    test_case["input"]["total_epochs_est"])

        assert np.array_equal(result, test_case["expected"]), f"Test case {i+1} failed: expected {test_case['expected']}, but got {result}"


def test_group_columns_by_parent():
    test_cases = [
        {
            "input": {'parents': {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0}},
            "expected": {2: [3, 4], 1: [2, 5], 0: [1, 6]}
        },
        {
            "input": {'parents': {2: 1, 3: 1, 1: 0, 5: 4, 6: 4, 4: 0}},
            "expected": {1: [2, 3], 0: [1, 4], 4: [5, 6]}
        },
        {
            "input": {'parents': {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0}},
            "expected": {2: [3, 4], 1: [2, 5], 0: [1, 6]}
        },
        {
            "input": {'parents': {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 7: 6, 8: 6, 6: 0}},
            "expected": {2: [3, 4], 1: [2, 5], 0: [1, 6], 6: [7, 8]}
        },
        {
            "input": {'parents': {4: 3, 5: 3, 3: 2, 6: 2, 2: 1, 7: 1, 1: 0, 8: 0}},
            "expected": {3: [4, 5], 2: [3, 6], 1: [2, 7], 0: [1, 8]}
        }
    ]

    for i, test_case in enumerate(test_cases):
        result = group_columns_by_parent(test_case["input"]["parents"])

        assert result == test_case["expected"], f"Test case {i+1} failed: expected {test_case['expected']}, but got {result}"


def test_filter_rows_based_on_parents():
    epochs_created = np.array([[-1, 0, 0],
                        [-1, 0, 1],
                        [-1, 1, 0],
                        [-1, 1, 1]], dtype=object)

    parents = {1: 0, 2: 0}

    expected_filtered_epochs_created = np.array([[-1, 0, 0],
                                          [-1, 1, 1]], dtype=object)

    filtered_epochs_created = filter_rows_based_on_parents(epochs_created = epochs_created, parents = parents)
    assert np.array_equal(filtered_epochs_created, expected_filtered_epochs_created), f"Expected {expected_filtered_epochs_created}, but got {filtered_epochs_created}"


def test_get_all_trees_and_timings():
    # Fill in your input data here
    input_data = {
        'observed_SNV_multiplicities': {
            0: {3: 62, 1: 27, 2: 22},
            1: {5: 24, 3: 28, 1: 208, 2: 85},
            2: {5: 45, 2: 65, 1: 192, 3: 21},
            3: {3: 42, 2: 83, 1: 74},
            4: {2: 36, 1: 34},
            5: {4: 27, 2: 55, 1: 88, 3: 37},
            6: {2: 39, 1: 35},
            7: {1: 57, 3: 41, 2: 23},
            8: {4: 39, 2: 62, 1: 37},
            9: {1: 82},
            10: {3: 29, 1: 23, 2: 18},
            11: {2: 65, 1: 80},
            12: {3: 20, 1: 42, 2: 16},
            13: {3: 22, 1: 38, 2: 30},
            14: {4: 13, 3: 14, 1: 38, 2: 17},
            15: {1: 28},
            16: {3: 11, 2: 9, 1: 11},
            17: {4: 6, 2: 19, 1: 62},
            18: {5: 7, 3: 7, 2: 13, 1: 16},
            19: {2: 10, 1: 13},
            20: {2: 16, 1: 10, 3: 9},
            21: {3: 4, 2: 4, 1: 20},
            22: {4: 21, 2: 42, 1: 72}
        },
        'observed_CNs': {
            0: [3, 0],
            1: [5, 2],
            2: [5, 1],
            3: [3, 2],
            4: [2, 0],
            5: [4, 3],
            6: [2, 0],
            7: [3, 1],
            8: [4, 2],
            9: [1, 1],
            10: [3, 0],
            11: [2, 2],
            12: [3, 1],
            13: [3, 2],
            14: [4, 0],
            15: [1, 0],
            16: [3, 0],
            17: [4, 1],
            18: [5, 0],
            19: [2, 0],
            20: [3, 2],
            21: [3, 0],
            22: [4, 0]
        },
        'pre': 1,
        'mid': 1,
        'post': -1,
        'total_epochs_est': 2
    }
 

    # Call the function with the input data
    result = get_all_trees_and_timings(**input_data)

    # Fill in your expected output here
    expected_output = {0: [((3, (3, (2, (1,), (1,)), (1,)), (0,)), [0, [1, [2, [3], [4]], [5]], [6]], 6, array([[-1, 0, 1, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 0],
       [-1, 0, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0})], 1: [((7, (5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,))), (2, (1,), (1,))), [0, [1, [2, [3, [4], [5]], [6]], [7, [8], [9]]], [10, [11], [12]]], 12, array([[-1, 0, 1, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0],
       [-1, 0, 1, 2, 2, 2, 2, 1, 1, 1, 0, 1, 1],
       [-1, 0, 1, 2, 2, 2, 2, 1, 1, 1, 0, 2, 2],
       [-1, 0, 1, 2, 2, 2, 2, 1, 2, 2, 0, 0, 0],
       [-1, 0, 1, 2, 2, 2, 2, 1, 2, 2, 0, 1, 1],
       [-1, 0, 1, 2, 2, 2, 2, 1, 2, 2, 0, 2, 2]], dtype=object), {4: 3, 5: 3, 3: 2, 6: 2, 2: 1, 8: 7, 9: 7, 7: 1, 1: 0, 11: 10, 12: 10, 10: 0})], 2: [((6, (5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,))), (1,)), [0, [1, [2, [3, [4], [5]], [6]], [7, [8], [9]]], [10]], 10, array([[-1, 0, 1, 2, 2, 2, 2, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 2, 2, 1, 2, 2, 0]], dtype=object), {4: 3, 5: 3, 3: 2, 6: 2, 2: 1, 8: 7, 9: 7, 7: 1, 1: 0, 10: 0})], 3: [((5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,))), [0, [1, [2, [3], [4]], [5]], [6, [7], [8]]], 8, array([[-1, 0, 1, 1, 1, 1, 0, 0, 0],
       [-1, 0, 1, 1, 1, 1, 0, 1, 1],
       [-1, 0, 1, 1, 1, 1, 0, 2, 2],
       [-1, 0, 1, 2, 2, 1, 0, 0, 0],
       [-1, 0, 1, 2, 2, 1, 0, 1, 1],
       [-1, 0, 1, 2, 2, 1, 0, 2, 2],
       [-1, 0, 2, 2, 2, 2, 0, 0, 0],
       [-1, 0, 2, 2, 2, 2, 0, 1, 1],
       [-1, 0, 2, 2, 2, 2, 0, 2, 2],
       [-1, 1, 2, 2, 2, 2, 1, 1, 1],
       [-1, 1, 2, 2, 2, 2, 1, 2, 2]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 7: 6, 8: 6, 6: 0})], 4: [((2, (2, (1,), (1,)), (0,)), [0, [1, [2], [3]], [4]], 4, array([[-1, 0, 0, 0, 0],
       [-1, 0, 1, 1, 0],
       [-1, 0, 2, 2, 0],
       [-1, 1, 1, 1, 1],
       [-1, 1, 2, 2, 1],
       [-1, 2, 2, 2, 2]], dtype=object), {2: 1, 3: 1, 1: 0, 4: 0})], 5: [((7, (4, (2, (1,), (1,)), (2, (1,), (1,))), (3, (2, (1,), (1,)), (1,))), [0, [1, [2, [3], [4]], [5, [6], [7]]], [8, [9, [10], [11]], [12]]], 12, array([[-1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
       [-1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 2, 1],
       [-1, 0, 1, 1, 1, 1, 1, 1, 0, 2, 2, 2, 2],
       [-1, 0, 1, 1, 1, 1, 2, 2, 0, 1, 1, 1, 1],
       [-1, 0, 1, 1, 1, 1, 2, 2, 0, 1, 2, 2, 1],
       [-1, 0, 1, 1, 1, 1, 2, 2, 0, 2, 2, 2, 2],
       [-1, 0, 1, 2, 2, 1, 1, 1, 0, 1, 1, 1, 1],
       [-1, 0, 1, 2, 2, 1, 1, 1, 0, 1, 2, 2, 1],
       [-1, 0, 1, 2, 2, 1, 1, 1, 0, 2, 2, 2, 2],
       [-1, 0, 1, 2, 2, 1, 2, 2, 0, 1, 1, 1, 1],
       [-1, 0, 1, 2, 2, 1, 2, 2, 0, 1, 2, 2, 1],
       [-1, 0, 1, 2, 2, 1, 2, 2, 0, 2, 2, 2, 2],
       [-1, 0, 2, 2, 2, 2, 2, 2, 0, 1, 1, 1, 1],
       [-1, 0, 2, 2, 2, 2, 2, 2, 0, 1, 2, 2, 1],
       [-1, 0, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2],
       [-1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2]], dtype=object), {3: 2, 4: 2, 2: 1, 6: 5, 7: 5, 5: 1, 1: 0, 10: 9, 11: 9, 9: 8, 12: 8, 8: 0}), ((7, (4, (3, (2, (1,), (1,)), (1,)), (1,)), (3, (2, (1,), (1,)), (1,))), [0, [1, [2, [3, [4], [5]], [6]], [7]], [8, [9, [10], [11]], [12]]], 12, array([[-1, 0, 1, 2, 2, 2, 2, 1, 0, 1, 1, 1, 1],
       [-1, 0, 1, 2, 2, 2, 2, 1, 0, 1, 2, 2, 1],
       [-1, 0, 1, 2, 2, 2, 2, 1, 0, 2, 2, 2, 2]], dtype=object), {4: 3, 5: 3, 3: 2, 6: 2, 2: 1, 7: 1, 1: 0, 10: 9, 11: 9, 9: 8, 12: 8, 8: 0})], 6: [((2, (2, (1,), (1,)), (0,)), [0, [1, [2], [3]], [4]], 4, array([[-1, 0, 0, 0, 0],
       [-1, 0, 1, 1, 0],
       [-1, 0, 2, 2, 0],
       [-1, 1, 1, 1, 1],
       [-1, 1, 2, 2, 1],
       [-1, 2, 2, 2, 2]], dtype=object), {2: 1, 3: 1, 1: 0, 4: 0})], 7: [((4, (3, (2, (1,), (1,)), (1,)), (1,)), [0, [1, [2, [3], [4]], [5]], [6]], 6, array([[-1, 0, 1, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 0],
       [-1, 0, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0})], 8: [((6, (4, (3, (2, (1,), (1,)), (1,)), (1,)), (2, (1,), (1,))), [0, [1, [2, [3, [4], [5]], [6]], [7]], [8, [9], [10]]], 10, array([[-1, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0],
       [-1, 0, 1, 2, 2, 2, 2, 1, 0, 1, 1],
       [-1, 0, 1, 2, 2, 2, 2, 1, 0, 2, 2]], dtype=object), {4: 3, 5: 3, 3: 2, 6: 2, 2: 1, 7: 1, 1: 0, 9: 8, 10: 8, 8: 0}), ((6, (4, (2, (1,), (1,)), (2, (1,), (1,))), (2, (1,), (1,))), [0, [1, [2, [3], [4]], [5, [6], [7]]], [8, [9], [10]]], 10, array([[-1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
       [-1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
       [-1, 0, 1, 1, 1, 1, 1, 1, 0, 2, 2],
       [-1, 0, 1, 1, 1, 1, 2, 2, 0, 0, 0],
       [-1, 0, 1, 1, 1, 1, 2, 2, 0, 1, 1],
       [-1, 0, 1, 1, 1, 1, 2, 2, 0, 2, 2],
       [-1, 0, 1, 2, 2, 1, 1, 1, 0, 0, 0],
       [-1, 0, 1, 2, 2, 1, 1, 1, 0, 1, 1],
       [-1, 0, 1, 2, 2, 1, 1, 1, 0, 2, 2],
       [-1, 0, 1, 2, 2, 1, 2, 2, 0, 0, 0],
       [-1, 0, 1, 2, 2, 1, 2, 2, 0, 1, 1],
       [-1, 0, 1, 2, 2, 1, 2, 2, 0, 2, 2],
       [-1, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0],
       [-1, 0, 2, 2, 2, 2, 2, 2, 0, 1, 1],
       [-1, 0, 2, 2, 2, 2, 2, 2, 0, 2, 2],
       [-1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1],
       [-1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2]], dtype=object), {3: 2, 4: 2, 2: 1, 6: 5, 7: 5, 5: 1, 1: 0, 9: 8, 10: 8, 8: 0})], 9: [((2, (1,), (1,)), [0, [1], [2]], 2, array([[-1, 0, 0],
       [-1, 1, 1],
       [-1, 2, 2]], dtype=object), {1: 0, 2: 0})], 10: [((3, (3, (2, (1,), (1,)), (1,)), (0,)), [0, [1, [2, [3], [4]], [5]], [6]], 6, array([[-1, 0, 1, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 0],
       [-1, 0, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0})], 11: [((4, (2, (1,), (1,)), (2, (1,), (1,))), [0, [1, [2], [3]], [4, [5], [6]]], 6, array([[-1, 0, 0, 0, 0, 0, 0],
       [-1, 0, 0, 0, 0, 1, 1],
       [-1, 0, 0, 0, 0, 2, 2],
       [-1, 0, 1, 1, 0, 0, 0],
       [-1, 0, 1, 1, 0, 1, 1],
       [-1, 0, 1, 1, 0, 2, 2],
       [-1, 0, 2, 2, 0, 0, 0],
       [-1, 0, 2, 2, 0, 1, 1],
       [-1, 0, 2, 2, 0, 2, 2],
       [-1, 1, 1, 1, 1, 1, 1],
       [-1, 1, 1, 1, 1, 2, 2],
       [-1, 1, 2, 2, 1, 1, 1],
       [-1, 1, 2, 2, 1, 2, 2],
       [-1, 2, 2, 2, 2, 2, 2]], dtype=object), {2: 1, 3: 1, 1: 0, 5: 4, 6: 4, 4: 0})], 12: [((4, (3, (2, (1,), (1,)), (1,)), (1,)), [0, [1, [2, [3], [4]], [5]], [6]], 6, array([[-1, 0, 1, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 0],
       [-1, 0, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0})], 13: [((5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,))), [0, [1, [2, [3], [4]], [5]], [6, [7], [8]]], 8, array([[-1, 0, 1, 1, 1, 1, 0, 0, 0],
       [-1, 0, 1, 1, 1, 1, 0, 1, 1],
       [-1, 0, 1, 1, 1, 1, 0, 2, 2],
       [-1, 0, 1, 2, 2, 1, 0, 0, 0],
       [-1, 0, 1, 2, 2, 1, 0, 1, 1],
       [-1, 0, 1, 2, 2, 1, 0, 2, 2],
       [-1, 0, 2, 2, 2, 2, 0, 0, 0],
       [-1, 0, 2, 2, 2, 2, 0, 1, 1],
       [-1, 0, 2, 2, 2, 2, 0, 2, 2],
       [-1, 1, 2, 2, 2, 2, 1, 1, 1],
       [-1, 1, 2, 2, 2, 2, 1, 2, 2]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 7: 6, 8: 6, 6: 0})], 14: [((4, (4, (3, (2, (1,), (1,)), (1,)), (1,)), (0,)), [0, [1, [2, [3, [4], [5]], [6]], [7]], [8]], 8, array([[-1, 0, 1, 2, 2, 2, 2, 1, 0]], dtype=object), {4: 3, 5: 3, 3: 2, 6: 2, 2: 1, 7: 1, 1: 0, 8: 0})], 15: [((1, (1,), (0,)), [0, [1], [2]], 2, array([[-1, 0, 0],
       [-1, 1, 1],
       [-1, 2, 2]], dtype=object), {1: 0, 2: 0})], 16: [((3, (3, (2, (1,), (1,)), (1,)), (0,)), [0, [1, [2, [3], [4]], [5]], [6]], 6, array([[-1, 0, 1, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 0],
       [-1, 0, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0})], 17: [((5, (4, (2, (1,), (1,)), (2, (1,), (1,))), (1,)), [0, [1, [2, [3], [4]], [5, [6], [7]]], [8]], 8, array([[-1, 0, 1, 1, 1, 1, 1, 1, 0],
       [-1, 0, 1, 1, 1, 1, 2, 2, 0],
       [-1, 0, 1, 2, 2, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 2, 2, 0],
       [-1, 0, 2, 2, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 6: 5, 7: 5, 5: 1, 1: 0, 8: 0})], 18: [((5, (5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,))), (0,)), [0, [1, [2, [3, [4], [5]], [6]], [7, [8], [9]]], [10]], 10, array([[-1, 0, 1, 2, 2, 2, 2, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 2, 2, 1, 2, 2, 0]], dtype=object), {4: 3, 5: 3, 3: 2, 6: 2, 2: 1, 8: 7, 9: 7, 7: 1, 1: 0, 10: 0})], 19: [((2, (2, (1,), (1,)), (0,)), [0, [1, [2], [3]], [4]], 4, array([[-1, 0, 0, 0, 0],
       [-1, 0, 1, 1, 0],
       [-1, 0, 2, 2, 0],
       [-1, 1, 1, 1, 1],
       [-1, 1, 2, 2, 1],
       [-1, 2, 2, 2, 2]], dtype=object), {2: 1, 3: 1, 1: 0, 4: 0})], 20: [((5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,))), [0, [1, [2, [3], [4]], [5]], [6, [7], [8]]], 8, array([[-1, 0, 1, 1, 1, 1, 0, 0, 0],
       [-1, 0, 1, 1, 1, 1, 0, 1, 1],
       [-1, 0, 1, 1, 1, 1, 0, 2, 2],
       [-1, 0, 1, 2, 2, 1, 0, 0, 0],
       [-1, 0, 1, 2, 2, 1, 0, 1, 1],
       [-1, 0, 1, 2, 2, 1, 0, 2, 2],
       [-1, 0, 2, 2, 2, 2, 0, 0, 0],
       [-1, 0, 2, 2, 2, 2, 0, 1, 1],
       [-1, 0, 2, 2, 2, 2, 0, 2, 2],
       [-1, 1, 2, 2, 2, 2, 1, 1, 1],
       [-1, 1, 2, 2, 2, 2, 1, 2, 2]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 7: 6, 8: 6, 6: 0})], 21: [((3, (3, (2, (1,), (1,)), (1,)), (0,)), [0, [1, [2, [3], [4]], [5]], [6]], 6, array([[-1, 0, 1, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 0],
       [-1, 0, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0})], 22: [((4, (4, (2, (1,), (1,)), (2, (1,), (1,))), (0,)), [0, [1, [2, [3], [4]], [5, [6], [7]]], [8]], 8, array([[-1, 0, 1, 1, 1, 1, 1, 1, 0],
       [-1, 0, 1, 1, 1, 1, 2, 2, 0],
       [-1, 0, 1, 2, 2, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 2, 2, 0],
       [-1, 0, 2, 2, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 6: 5, 7: 5, 5: 1, 1: 0, 8: 0})]} 

    # Assert that the function output matches the expected output
    assert result == expected_output