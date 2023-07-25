
def test_get_BP_likelihoods():
    trees_and_timings = {
        "chrom1": [
            (
                None,
                None,
                None,
                np.array([[2, 3], [3, 2]]),
                None,
            ),
            (
                None,
                None,
                None,
                np.array([[0, 2], [2, 1]]),
                None,
            ),
        ]
    }
    pre, mid, post = 2, 1, 1
    p_up, p_down = 65, 10
    data = {
        "3G": [None, [0.2, 0.6, 0.2]],
        "1G1": [None, [0.9, 0.1, 0]],
        "2G0": [None, [1, 0, 0]],
    }

    expected_BP_likelihoods = {
        "chrom1": [
            np.array([-0.916290731874155, -0.916290731874155]),
            np.array([-0.40546510810816444, -0.40546510810816444]),
        ]
    }

    BP_likelihoods = get_BP_likelihoods(trees_and_timings, pre, mid, post, p_up, p_down, data)

    for chrom in BP_likelihoods.keys():
        for i in range(len(BP_likelihoods[chrom])):
            assert np.allclose(BP_likelihoods[chrom][i], expected_BP_likelihoods[chrom][i], rtol=1e-9, atol=1e-9)



def test_calculate_paths_and_likelihoods():
    data = {
        "3G": [None, [0.2, 0.6, 0.2]],
        "1G1": [None, [0.9, 0.1, 0]],
        "2G0": [None, [1, 0, 0]],
    }
    branch_lengths = np.array([[2, 1], [1, 1]])
    CNs = ["1", "0"]
    starts = np.array([[0, 2], [2, 1]])
    ends = np.array([[2, 3], [3, 2]])
    path = ["A", "A", "GD", "A"]

    expected_paths = np.array([["3G", "1G1"], ["1G1", "1G1"]], dtype=object)
    expected_likelihoods = np.array([[0.6, 0.9], [0.9, 0.9]])

    paths, likelihoods = calculate_paths_and_likelihoods(
        branch_lengths, CNs, data, starts, ends, path
    )

    assert np.array_equal(paths, expected_paths)
    assert np.array_equal(likelihoods, expected_likelihoods)


def test_shorten_by_one():
    """
    Tests the `shorten_by_one` function with various path values.
    """
    test_cases = [
        ('1G2', '1G1'),
        ('1G1', '1G0'),
        ('1G0', '1'),
        ('3G4G0', '3G4'),
        ('3G4', '3G3'),
        ('3G3', '3G2'),
        ('3G2', '3G1'),
        ('3G1', '3G0'),
        ('3G0', '3'),
        ('3', '2'),
        ('2', '1'),
        ('1', '0'),
        # Testing error cases
        ('0', ValueError),
    ]

    for i, (path, expected) in enumerate(test_cases):
        try:
            result = shorten_by_one(path)
            assert result == expected, f"Test case {i+1} failed: ({path}) => {result}, expected {expected}"
        except ValueError as e:
            assert isinstance(expected, type) and issubclass(expected, Exception), f"Test case {i+1} failed: Exception was not expected for path {path}"
        except Exception as e:
            print(f"Test case {i+1} failed with an unexpected exception: {type(e).__name__} - {e}")


def test_check_last_character():
    """
    Test the check_last_character function with various test cases.
    """
    test_cases = {
        '0': True,
        '1': False,
        '0G0': True,
        '0G1': False,
        '1G0': True,
        '0G': True,
        '1G': True,
        'G': True,
        'G1': False,
        '10': False, 
        '01': False,
        '00': True
    }

    for code, expected in test_cases.items():
        result = check_last_character(code)
        assert result == expected, f"For code '{code}', expected {expected} but got {result}"

def test_create_path():
    assert create_path(3, 2, 1) == ["A", "A", "A", "GD", "A", "A", "GD", "A"]
    assert create_path(0, 0, 0) == ["GD", "GD"]
    assert create_path(2, 0, 2) == ["A", "A", "GD", "GD", "A", "A"]
    assert create_path(1, 1, -1) == ["A", "GD", "A"]

def test_timing_struct_to_BP_likelihood_per_chrom():
    data = {
        "3G": [None, [0.2, 0.6, 0.2]],
        "1G1": [None, [0.9, 0.1, 0]],
        "2G0": [None, [1, 0, 0]],
    }
    trees_and_timings = [
        (
            None,
            None,
            None,
            np.array([[2, 3], [3, 2]]),
            None,
        ),
        (
            None,
            None,
            None,
            np.array([[0, 2], [2, 1]]),
            None,
        ),
    ]
    pre, mid, post = 2, 1, 1

    expected_all_BP_likelihoods = [
        np.array([-0.916290731874155, -0.916290731874155]),
        np.array([-0.40546510810816444, -0.40546510810816444]),
    ]

    all_BP_likelihoods = timing_struct_to_BP_likelihood_per_chrom(data, trees_and_timings, pre, mid, post)

    for i in range(len(all_BP_likelihoods)):
        assert np.allclose(all_BP_likelihoods[i], expected_all_BP_likelihoods[i], rtol=1e-9, atol=1e-9)


def test_calculate_BP_paths():
    # Test case 1
    branch_lengths = np.array([[1, 2, 2], [2, 1, 1], [3, 0, 0]], dtype=object)
    starts = np.array([[-1, 0, 0], [-1, 1, 1], [-1, 2, 2]], dtype=object)
    ends = np.array([[0, 2, 2], [1, 2, 2], [2, 2, 2]], dtype=object)
    path = ['A', 'GD', 'A']
    result = calculate_BP_paths(branch_lengths, starts, ends, path)
    expected = np.array([['0', '1G0', '1G0'], ['0', '0G0', '0G0'], ['0', '0', '0']], dtype=object)
    assert np.array_equal(result, expected), f"calculate_BP_paths returned incorrect result: {result}"

    # Test case 2
    # Test case 2
    branch_lengths = np.array([[1, 1, 0, 1, 1, 1, 2],
                               [1, 1, 1, 0, 0, 1, 2],
                               [1, 2, 0, 0, 0, 0, 2],
                               [2, 1, 0, 0, 0, 0, 1]], dtype=object)
    starts = np.array([[-1, 0, 1, 1, 1, 1, 0],
                       [-1, 0, 1, 2, 2, 1, 0],
                       [-1, 0, 2, 2, 2, 2, 0],
                       [-1, 1, 2, 2, 2, 2, 1]], dtype=object)
    ends = np.array([[0, 1, 1, 2, 2, 2, 2],
                     [0, 1, 2, 2, 2, 2, 2],
                     [0, 2, 2, 2, 2, 2, 2],
                     [1, 2, 2, 2, 2, 2, 2]], dtype=object)
    path = ['A', 'GD', 'A']
    result = calculate_BP_paths(branch_lengths, starts, ends, path)
    expected = np.array([['0', '1', '0', '0G0', '0G0', '0G0', '1G0'],
                         ['0', '1', '0G0', '0', '0', '0G0', '1G0'],
                         ['0', '1G0', '0', '0', '0', '0', '1G0'],
                         ['0', '0G0', '0', '0', '0', '0', '0G0']], dtype=object)
    assert np.array_equal(result, expected), f"calculate_BP_paths returned incorrect result: {result}"

    # Test case 3
    branch_lengths = np.array([[1, 1, 0, 1, 1, 0, 1, 1, 2],
                               [1, 1, 0, 1, 1, 1, 0, 0, 2],
                               [1, 1, 1, 0, 0, 0, 1, 1, 2],
                               [1, 1, 1, 0, 0, 1, 0, 0, 2],
                               [1, 2, 0, 0, 0, 0, 0, 0, 2],
                               [2, 1, 0, 0, 0, 0, 0, 0, 1]], dtype=object)
    starts = np.array([[-1, 0, 1, 1, 1, 1, 1, 1, 0],
                       [-1, 0, 1, 1, 1, 1, 2, 2, 0],
                       [-1, 0, 1, 2, 2, 1, 1, 1, 0],
                       [-1, 0, 1, 2, 2, 1, 2, 2, 0],
                       [-1, 0, 2, 2, 2, 2, 2, 2, 0],
                       [-1, 1, 2, 2, 2, 2, 2, 2, 1]], dtype=object)
    ends = np.array([[0, 1, 1, 2, 2, 1, 2, 2, 2],
                     [0, 1, 1, 2, 2, 2, 2, 2, 2],
                     [0, 1, 2, 2, 2, 1, 2, 2, 2],
                     [0, 1, 2, 2, 2, 2, 2, 2, 2],
                     [0, 2, 2, 2, 2, 2, 2, 2, 2],
                     [1, 2, 2, 2, 2, 2, 2, 2, 2]], dtype=object)
    path = ['A', 'GD', 'A']
    result = calculate_BP_paths(branch_lengths, starts, ends, path)
    expected = np.array([['0', '1', '0', '0G0', '0G0', '0', '0G0', '0G0', '1G0'],
                         ['0', '1', '0', '0G0', '0G0', '0G0', '0', '0', '1G0'],
                         ['0', '1', '0G0', '0', '0', '0', '0G0', '0G0', '1G0'],
                         ['0', '1', '0G0', '0', '0', '0G0', '0', '0', '1G0'],
                         ['0', '1G0', '0', '0', '0', '0', '0', '0', '1G0'],
                         ['0', '0G0', '0', '0', '0', '0', '0', '0', '0G0']], dtype=object)
    assert np.array_equal(result, expected), f"calculate_BP_paths returned incorrect result: {result}"



def test_get_path_code():
    # Test case 1
    code_list = ["A", "A", "GD", "A", "A", "A", "GD", "A"]
    result = get_path_code(code_list)
    expected = "2G3G1"
    assert result == expected, f"get_path_code returned incorrect result: {result}"

    # Test case 2
    code_list = []
    result = get_path_code(code_list)
    expected = "0"
    assert result == expected, f"get_path_code returned incorrect result: {result}"

    # Test case 3
    code_list = ['A', 'GD']
    result = get_path_code(code_list)
    expected = '1G0'
    assert result == expected, f"get_path_code returned incorrect result: {result}"

test_get_path_code()



def test_stack_same_CN_branch_lengths():
    # First test case
    unique_CNs = [5, 3, 2, 1]
    CNs = [5, 3, 2, 1, 1, 1, 2, 1, 1]
    branch_lengths = np.array([[1, 1, 0, 1, 1, 1, 0, 2, 2],
                               [1, 1, 0, 1, 1, 1, 1, 1, 1],
                               [1, 1, 0, 1, 1, 1, 2, 0, 0],
                               [1, 1, 1, 0, 0, 1, 0, 2, 2],
                               [1, 1, 1, 0, 0, 1, 1, 1, 1],
                               [1, 1, 1, 0, 0, 1, 2, 0, 0],
                               [1, 2, 0, 0, 0, 0, 0, 2, 2],
                               [1, 2, 0, 0, 0, 0, 1, 1, 1],
                               [1, 2, 0, 0, 0, 0, 2, 0, 0],
                               [2, 1, 0, 0, 0, 0, 0, 1, 1],
                               [2, 1, 0, 0, 0, 0, 1, 0, 0]], dtype=object)
    result = stack_same_CN_branch_lengths(CNs, branch_lengths)
    expected = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
                         [1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1],
                         [0, 1, 2, 1, 2, 3, 0, 1, 2, 0, 1],
                         [7, 5, 3, 5, 3, 1, 4, 2, 0, 2, 0]], dtype=object).T
    assert np.array_equal(result, expected), f"stack_same_CN_branch_lengths returned incorrect values.\nExpected: {expected}\nGot: {result}"

    # Second test case
    unique_CNs = [3, 2, 1, 0]
    CNs = [3, 3, 2, 1, 1, 1, 0]
    branch_lengths = np.array([[1, 1, 0, 1, 1, 1, 2],
                               [1, 1, 1, 0, 0, 1, 2],
                               [1, 2, 0, 0, 0, 0, 2],
                               [2, 1, 0, 0, 0, 0, 1]], dtype=object)
    result = stack_same_CN_branch_lengths(CNs, branch_lengths)
   
    expected = np.array([[2, 2, 3, 3],
                         [0, 1, 0, 0],
                         [3, 1, 0, 0],
                         [2, 2, 2, 1]], dtype=object).T
    assert np.array_equal(result, expected), f"stack_same_CN_branch_lengths returned incorrect values.\nExpected: {expected}\nGot: {result}"

    # Third test case
    unique_CNs = [4, 2, 1, 0]
    CNs = [4, 4, 2, 1, 1, 2, 1, 1, 0]
    branch_lengths = np.array([[1, 1, 0, 1, 1, 0, 1, 1, 2],
                               [1, 1, 0, 1, 1, 1, 0, 0, 2],
                               [1, 1, 1, 0, 0, 0, 1, 1, 2],
                               [1, 1, 1, 0, 0, 1, 0, 0, 2],
                               [1, 2, 0, 0, 0, 0, 0, 0, 2],
                               [2, 1, 0, 0, 0, 0, 0, 0, 1]], dtype=object)
    result = stack_same_CN_branch_lengths(CNs, branch_lengths)
    expected = np.array([[2, 2, 2, 2, 3, 3],
                         [0, 1, 1, 2, 0, 0],
                         [4, 2, 2, 0, 0, 0],
                         [2, 2, 2, 2, 2, 1]], dtype=object).T
    assert np.array_equal(result, expected), f"stack_same_CN_branch_lengths returned incorrect values.\nExpected: {expected}\nGot: {result}"


#test_stack_same_CN_branch_lengths()

def test_find_non_parent_children():
    parents = {1: 0, 2: 0, 4: 3, 5: 3}
    expected_non_parent_children = {1, 2, 4, 5}
    non_parent_children = find_non_parent_children(parents)
    assert non_parent_children == expected_non_parent_children, f"Expected {expected_non_parent_children}, but got {non_parent_children}"

# Run the test function
test_find_non_parent_children()


def test_calculate_child_parent_diff():
    # First test case
    epochs_created = np.array([[-1, 0, 1, 1, 1, 1, 0],
                               [-1, 0, 1, 2, 2, 1, 0],
                               [-1, 0, 2, 2, 2, 2, 0],
                               [-1, 1, 2, 2, 2, 2, 1]], dtype=object)
    parents = {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0}
    max_epoch = 2
    result = calculate_child_parent_diff(epochs_created, parents, max_epoch)
    expected = np.array([[1, 1, 0, 1, 1, 1, 2],
                         [1, 1, 1, 0, 0, 1, 2],
                         [1, 2, 0, 0, 0, 0, 2],
                         [2, 1, 0, 0, 0, 0, 1]], dtype=object)
    assert np.array_equal(result, expected), f"calculate_child_parent_diff returned incorrect values.\nExpected: {expected}\nGot: {result}"

    # Second test case
    epochs_created = np.array([[-1, 0, 1, 1, 1, 1, 1, 1, 0],
                               [-1, 0, 1, 1, 1, 1, 2, 2, 0],
                               [-1, 0, 1, 2, 2, 1, 1, 1, 0],
                               [-1, 0, 1, 2, 2, 1, 2, 2, 0],
                               [-1, 0, 2, 2, 2, 2, 2, 2, 0],
                               [-1, 1, 2, 2, 2, 2, 2, 2, 1]], dtype=object)
    parents = {3: 2, 4: 2, 2: 1, 6: 5, 7: 5, 5: 1, 1: 0, 8: 0}
    max_epoch = 2
    result = calculate_child_parent_diff(epochs_created, parents, max_epoch)
    expected = np.array([[1, 1, 0, 1, 1, 0, 1, 1, 2],
                         [1, 1, 0, 1, 1, 1, 0, 0, 2],
                         [1, 1, 1, 0, 0, 0, 1, 1, 2],
                         [1, 1, 1, 0, 0, 1, 0, 0, 2],
                         [1, 2, 0, 0, 0, 0, 0, 0, 2],
                         [2, 1, 0, 0, 0, 0, 0, 0, 1]], dtype=object)
    assert np.array_equal(result, expected), f"calculate_child_parent_diff returned incorrect values.\nExpected: {expected}\nGot: {result}"


test_calculate_child_parent_diff()


def test_find_indices():
    test_list = [1, 2, 3, 2, 4, 2, 5]
    item = 2
    indices = find_indices(test_list, item)
    assert indices == [1, 3, 5], "find_indices returned incorrect indices"




def test_extract_copy_numbers():
    tree = "(3,(1,1))"
    CNs = extract_copy_numbers(tree)
    assert CNs == [3, 1, 1], "extract_copy_numbers returned incorrect CNs"


test_extract_copy_numbers()