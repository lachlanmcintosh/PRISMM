
def test_sum_tree_distance():
    def assert_with_message(value1, value2, message):
        assert value1 == value2, f"{message}: expected {value2}, but got {value1}"

    tree1 = {
        "copy_number": 1,
        "epoch_index": 1,
        "child": {
            "copy_number": 2,
            "epoch_index": 2,
        },
        "complement": {
            "copy_number": 3,
            "epoch_index": 3,
        }
    }

    tree2 = {
        "copy_number": 1,
        "epoch_index": 4,
        "child": {
            "copy_number": 2,
            "epoch_index": 5,
        },
        "complement": {
            "copy_number": 3,
            "epoch_index": 6,
        }
    }

    assert_with_message(sum_tree_distance(tree1, tree2), 9, "Test case 1 failed")
    assert_with_message(sum_tree_distance(tree1, tree2, diff_struct_is_inf=True), float('inf'), "Test case 2 failed")
    
    tree2["complement"] = None
    assert_with_message(sum_tree_distance(tree1, tree2, diff_struct_is_inf=True), float('inf'), "Test case 3 failed")
    assert_with_message(sum_tree_distance(tree1, tree2), 6, "Test case 4 failed")
    
    tree2["child"] = None
    assert_with_message(sum_tree_distance(tree1, tree2, diff_struct_is_inf=True), float('inf'), "Test case 5 failed")
    assert_with_message(sum_tree_distance(tree1, tree2), 3, "Test case 6 failed")


test_sum_tree_distance()


def test_count_nodes_with_same_attributes():
    tree1 = {'copy_number': 1, 'epoch_index': 2, 'child': {'copy_number': 2, 'epoch_index': 3}}
    tree2 = {'copy_number': 1, 'epoch_index': 2, 'child': {'copy_number': 2, 'epoch_index': 4}}

    result = count_nodes_with_same_attributes(tree1, tree2, ['copy_number', 'epoch_index'])
    expected = 3
    assert result == expected, f"Expected {expected}, but got {result}"

    tree1['complement'] = {'copy_number': 3, 'epoch_index': 5}
    tree2['complement'] = {'copy_number': 3, 'epoch_index': 6}

    result = count_nodes_with_same_attributes(tree1, tree2, ['copy_number', 'epoch_index'])
    expected = 4
    assert result == expected, f"Expected {expected}, but got {result}"

test_count_nodes_with_same_attributes()



def test_are_trees_identical_by_epoch_and_copy_number():
    # Identical trees
    tree1 = {'epoch_index': 1, 'copy_number': 2, 'child': {'epoch_index': 3, 'copy_number': 4}}
    tree2 = {'epoch_index': 1, 'copy_number': 2, 'child': {'epoch_index': 3, 'copy_number': 4}}
    assert are_trees_identical_by_epoch_and_copy_number(tree1, tree2)

    # Different epoch_index
    tree1 = {'epoch_index': 1, 'copy_number': 2, 'child': {'epoch_index': 3, 'copy_number': 4}}
    tree2 = {'epoch_index': 2, 'copy_number': 2, 'child': {'epoch_index': 3, 'copy_number': 4}}
    assert not are_trees_identical_by_epoch_and_copy_number(tree1, tree2)

    # Different copy_number
    tree1 = {'epoch_index': 1, 'copy_number': 2, 'child': {'epoch_index': 3, 'copy_number': 4}}
    tree2 = {'epoch_index': 1, 'copy_number': 3, 'child': {'epoch_index': 3, 'copy_number': 4}}
    assert not are_trees_identical_by_epoch_and_copy_number(tree1, tree2)


def test_distance_function(distance_function: DistanceFunction, difference: int, expected_output: float):
    """
    Test function for the DistanceFunction class and its subclasses.

    :param distance_function: An instance of a DistanceFunction subclass.
    :param difference: An integer to be used in the distance function.
    :param expected_output: The expected output of the distance function.
    """
    assert isinstance(difference, int), f"Invalid input type. Expected int but got {type(difference)}"
    assert isinstance(expected_output, float), f"Invalid expected output type. Expected float but got {type(expected_output)}"
    
    result = distance_function(difference)
    assert result == pytest.approx(expected_output), f"Expected {expected_output}, but got {result}"

def run_tests():
    # Testing ZeroDistance class
    zero_distance = ZeroDistance()
    test_distance_function(zero_distance, 5, 0.0)
    test_distance_function(zero_distance, 0, 0.0)

    # Testing AbsoluteDifference class
    euclidean_distance = AbsoluteDifference()
    test_distance_function(euclidean_distance, 5, 5.0)
    test_distance_function(euclidean_distance, 0, 0.0)

    # Testing SquaredDistance class
    squared_distance = SquaredDistance()
    test_distance_function(squared_distance, 2, 4.0)
    test_distance_function(squared_distance, 0, 0.0)



run_tests()



def test_calculate_difference():
    calc = NodeSimilarityCalculator()
    tree1 = {"copy_number": 5, "epoch_index": 10}
    tree2 = {"copy_number": 3, "epoch_index": 8}

    copy_number_distance = lambda x: x
    epoch_index_distance = lambda x: x
    assert calc._calculate_difference(tree1, tree2, copy_number_distance, epoch_index_distance) == (2, 2)

def test_compute_similarity():
    calc = NodeSimilarityCalculator()
    tree1 = {"copy_number": 5, "epoch_index": 10}
    tree2 = {"copy_number": 3, "epoch_index": 8}

    copy_number_distance = lambda x: x
    epoch_index_distance = lambda x: x
    assert calc.compute_similarity(tree1, tree2, copy_number_distance, epoch_index_distance) == (0.5, 1.0)

