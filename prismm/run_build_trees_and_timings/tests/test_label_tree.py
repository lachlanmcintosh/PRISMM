from prismm.run_build_trees_and_timings.label_tree import label_tree

def test_label_tree():
    # Test case 1
    result = label_tree((5, (3,), (2, (1,), (1,))))
    print(result)
    assert result == (
        [0, [1], [2, [3], [4]]], 
        4, 
        {1: 0, 3: 2, 4: 2, 2: 0}, 
        {0: 5, 1: 3, 2: 2, 3: 1, 4: 1}
        )

    # Test case 2
    result = label_tree((8, (2,), (6, (4,), (2,))))
    print(result)
    assert result == (
        [0, [1], [2, [3], [4]]], 
        4, 
        {1: 0, 3: 2, 4: 2, 2: 0}, 
        {0: 8, 1: 2, 2: 6, 3: 4, 4: 2}
        )
    

if __name__ == "__main__":
    test_label_tree()