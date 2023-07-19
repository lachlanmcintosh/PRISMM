import logging
import copy
from prismm.run_build_trees_and_timings.get_all_trees import forests_are_equal 
import numpy as np


def get_all_timings(trees, observed_SNV_multiplicities, total_epochs, pre, mid, post):
    trees_and_timings = {}
    for chrom in observed_SNV_multiplicities:
        logging.debug(f"(pre,mid,post) + {(pre,mid,post)}")
        trees_and_timings[chrom] = get_chrom_trees_and_timings(all_trees = trees[chrom], total_epochs=total_epochs)
        logging.debug(trees_and_timings[chrom])

    return trees_and_timings



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
        'max_epoch': 2
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

def test_get_timings_per_tree():
    test_cases = [
        {
            'input': {'tree': (6, (4, (2, (1,), (1,)), (2, (1,), (1,))), (2, (1,), (1,))), 'max_epoch': 2},
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
            'input': {'tree': (3, (3, (2, (1,), (1,)), (1,)), (0,)), 'max_epoch': 2},
            'output': ((3, (3, (2, (1,), (1,)), (1,)), (0,)), [0, [1, [2, [3], [4]], [5]], [6]], 6, np.array([[-1, 0, 1, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 0],
       [-1, 0, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0})
        },
        {
            'input': {'tree': (5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,))), 'max_epoch': 2},
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
            'input': {'tree': (3, (3, (2, (1,), (1,)), (1,)), (0,)), 'max_epoch': 2},
            'output': ((3, (3, (2, (1,), (1,)), (1,)), (0,)), [0, [1, [2, [3], [4]], [5]], [6]], 6, np.array([[-1, 0, 1, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 0],
       [-1, 0, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0})
        }
    ]

    for test_case in test_cases:
        input_data = test_case['input']
        expected_output = test_case['output']
        result = get_timings_per_tree(**input_data)
        assert result == expected_output, f'For {input_data}, expected {expected_output} but got {result}'

# Call the test function
#test_get_timings_per_tree()



def get_chrom_trees_and_timings(all_trees,total_epochs):
    logging.debug("all trees")
    logging.debug(all_trees)

    #chrom_trees_and_timings = [get_timings_per_tree(tree=x, total_epochs=total_epochs) for x in all_trees]
    #chrom_trees_and_timings = [time_limited_get_timings_per_tree(tree=x, total_epochs=total_epochs) for x in all_trees]
    #get_timings_per_tree, tree, total_epochs

    chrom_trees_and_timings = [get_timings_per_tree(tree=x, total_epochs=total_epochs) for x in all_trees]

    logging.debug("chrom_trees_and_timings")
    logging.debug(chrom_trees_and_timings)

    chrom_trees_and_timings = [x for x in chrom_trees_and_timings if x[3] is not None and not None in x[3]]

    logging.debug("chrom_trees_and_timings")
    logging.debug(chrom_trees_and_timings)

    #assert(len(chrom_trees_and_timings) != 0)

    return chrom_trees_and_timings

def test_get_chrom_trees_and_timings():
    test_cases = [
        {
            'input': {'tree': (6, (4, (2, (1,), (1,)), (2, (1,), (1,))), (2, (1,), (1,))), 'max_epoch': 2},
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
            'input': {'tree': (3, (3, (2, (1,), (1,)), (1,)), (0,)), 'max_epoch': 2},
            'output': ((3, (3, (2, (1,), (1,)), (1,)), (0,)), [0, [1, [2, [3], [4]], [5]], [6]], 6, np.array([[-1, 0, 1, 1, 1, 1, 0],
       [-1, 0, 1, 2, 2, 1, 0],
       [-1, 0, 2, 2, 2, 2, 0],
       [-1, 1, 2, 2, 2, 2, 1]], dtype=object), {3: 2, 4: 2, 2: 1, 5: 1, 1: 0, 6: 0})
        },
        {
            'input': {'tree': (5, (3, (2, (1,), (1,)), (1,)), (2, (1,), (1,))), 'max_epoch': 2},
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
            'input': {'tree': (3, (3, (2, (1,), (1,)), (1,)), (0,)), 'max_epoch': 2},
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

# Call the test function
#test_get_chrom_trees_and_timings()


# Test cases for get_all_trees_and_timings function
def test_get_all_trees_and_timings():
    observed_SNV_multiplicities = {"chr1": {1: 1, 2: 1}}
    observed_CNs = {"chr1": [1, 2]}
    pre, mid, post = 1, 1, 1
    max_epoch = calculate_epochs(pre,mid,post) 
    trees_and_timings = get_all_trees_and_timings(observed_SNV_multiplicities, observed_CNs, pre, mid, post,max_epoch)

    assert "chr1" in trees_and_timings, "Chromosome key is missing in the result"
    assert len(trees_and_timings["chr1"]) > 0, "No trees and timings found for the chromosome"



def get_timings_per_tree(tree, total_epochs): 
    logging.debug("get_timings_per_tree")

    labelled_tree, label_count, parents, label_to_copy = label_tree(
        tree=copy.deepcopy(tree),
        label_count=0,
        parents={},
        label_to_copy={}
    )

    if total_epochs == -1:
        epochs_created = initialize_epochs_created(num_labels=label_count + 1, root_label=label)
        epochs_created = -1
        return (tree, labelled_tree, label_count, epochs_created, parents)

    for label in range(label_count + 1):
        if label == 0:
            epochs_created = initialize_epochs_created(num_labels=label_count + 1, root_label=label)
            assert epochs_created.shape[0] > 0, "The epochs_created array must have at least one row."
        else:
            logging.debug("labelled_tree")
            logging.debug(labelled_tree)
            logging.debug("copy numbers")
            logging.debug([label_to_copy[x] for x in range(label_count+1)])
            logging.debug("label")
            logging.debug(label)
            logging.debug("epochs_created")
            logging.debug(epochs_created)
            assert epochs_created.shape[0] > 0, "The epochs_created array must have at least one row."
            sibling = find_sibling(parents,label)
            if sibling < label:
                logging.debug("insertion by copying sibling")
                epochs_created[:,label] = epochs_created[:,sibling]
            else:
                logging.debug("insertion by finding all possible epochs")
                epochs_created = handle_other_nodes(epochs_created=epochs_created,
                                                    label_to_copy=label_to_copy,
                                                    label=label,
                                                    parent=parents[label],
                                                    total_epochs=total_epochs
                                                    )
            logging.debug("epochs_created")
            logging.debug(epochs_created)

            if None in epochs_created[:,label]:
                return (None, None, None, None, None)

    logging.debug("epochs_created")
    logging.debug(epochs_created)
    logging.debug("epochs_created after filter_rows")
    epochs_created = filter_rows_based_on_parents(epochs_created=epochs_created, parents=parents)
    logging.debug(epochs_created)

    return (tree, labelled_tree, label_count, epochs_created, parents)

def time_limited_get_timings_per_tree(tree, total_epochs, max_time=1.0):
    # Create a process pool executor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Run get_timings_per_tree with the specified timeout
        future = executor.submit(get_timings_per_tree, tree, total_epochs)
        try:
            result = future.result(timeout=max_time)
        except concurrent.futures.TimeoutError:
            result = (None, None, None, None, None)
    return result




def label_tree(tree, label_count, parents, label_to_copy):
    if label_to_copy == {} or label_count == 0:
        assert parents == {}, f"Unexpected value for parents: {parents}"
        assert label_to_copy == {}, f"Unexpected value for label_to_copy: {label_to_copy}"
        assert label_count == 0, f"Unexpected value for label_count: {label_count}"

    tree = list(tree)

    unique_label = label_count
    label_to_copy[unique_label] = tree[0]
    tree[0] = unique_label

    new_parent = unique_label

    if len(tree) >= 2:
        tree[1], label_count, parents, label_to_copy = label_tree(tree[1], label_count+1, parents, label_to_copy)
        parents[tree[1][0]] = new_parent

        if len(tree) == 3:
            tree[2], label_count, parents, label_to_copy = label_tree(tree[2], label_count+1, parents, label_to_copy)
            parents[tree[2][0]] = new_parent

    return (tree, label_count, parents, label_to_copy)


def test_label_tree():
    tree_1 = (5, (3,), (2, (1,), (1,)))
    expected_tree_1 = (0, (1,), (2, (3,), (4,)))
    parents_1 = {1: 0, 2: 0, 3: 2, 4: 2}
    label_to_copy_1 = {0: 5, 1: 3, 2: 2, 3: 1, 4: 1}

    result_tree_1, _, result_parents_1, result_label_to_copy_1 = label_tree(tree_1, 0, {}, {})

    assert forests_are_equal([result_tree_1], [expected_tree_1]), f"Expected {expected_tree_1}, but got {result_tree_1}"
    assert result_parents_1 == parents_1, f"Expected {parents_1}, but got {result_parents_1}"
    assert result_label_to_copy_1 == label_to_copy_1, f"Expected {label_to_copy_1}, but got {result_label_to_copy_1}"

    tree_2 = (6, (3,), (3, (2,), (1,)))
    expected_tree_2 = (0, (1,), (2, (3,), (4,)))
    parents_2 = {1: 0, 2: 0, 3: 2, 4: 2}
    label_to_copy_2 = {0: 6, 1: 3, 2: 3, 3: 2, 4: 1}

    result_tree_2, _, result_parents_2, result_label_to_copy_2 = label_tree(tree_2, 0, {}, {})

    assert forests_are_equal([result_tree_2], [expected_tree_2]), f"Expected {expected_tree_2}, but got {result_tree_2}"
    assert result_parents_2 == parents_2, f"Expected {parents_2}, but got {result_parents_2}"
    assert result_label_to_copy_2 == label_to_copy_2, f"Expected {label_to_copy_2}, but got {result_label_to_copy_2}"



test_label_tree()



def initialize_epochs_created(num_labels, root_label):
    """
    Initialize a 2D numpy array with shape (1, num_labels) containing None values. The value of the root_label-th element
    in the first row is set to 0 and all other values are set to None.

    :param num_labels: The number of labels in the tree.
    :param root_label: The label of the root node.
    :return: A 2D numpy array of None values with shape (1, num_labels).
    """
    assert isinstance(num_labels, int) and num_labels > 0, "Num labels should be a positive integer."
    assert isinstance(root_label, int) and 0 <= root_label < num_labels, "Root label should be within the range of labels."
    epochs_created = np.full((1, num_labels), None)
    epochs_created[0, root_label] = -1

    assert epochs_created.shape[0] > 0, "The resulting array must have at least one row."

    return epochs_created

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

test_initialize_epochs_created()




def find_sibling(parents: dict, query_key: int) -> list:
    """
    Given a dictionary of 'parents' containing key-value pairs where the key is a child node and 
    the value is its parent node, this function takes a 'query_key' and returns a list of sibling keys.
    If the 'query_key' does not exist in the dictionary or there are no siblings, an empty list is returned.

    :param parents: A dictionary where keys are child nodes and values are parent nodes.
    :param query_key: The key for which we are searching sibling keys.
    :return: A list of sibling keys.
    """

    # Get the parent value for the query_key.
    query_parent = parents.get(query_key)

    if query_parent is None:
        return []

    # Find sibling keys by iterating through the parents dictionary.
    sibling_keys = [
        key for key, parent in parents.items() if parent == query_parent and key != query_key
    ]
    assert(len(sibling_keys) == 1)
    return sibling_keys[0]


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

test_find_sibling()


def handle_other_nodes(epochs_created, label_to_copy, label, parent, total_epochs):
    assert epochs_created.ndim == 2, "Timings should be a 2-dimensional array."
    assert 0 <= label < epochs_created.shape[1], "Label should be within the range of timings."
    #assert isinstance(total_epochs, int) and total_epochs >= 0, "Epochs should be a positive integer."
    assert isinstance(total_epochs, (int, np.integer)) and total_epochs >= 0, "Epochs should be a positive integer or a non-negative numpy integer."
    assert epochs_created.shape[0] > 0, "The epochs_created array must have at least one row."

    new_epochs_created = epochs_created
    for row in range(len(epochs_created)):
        parents_time = epochs_created[row][parent]
        assert(parents_time is not None)
        logging.debug(f'row:{row}')
        logging.debug(f'total_epochs:{total_epochs}')
        logging.debug(f'parent:{parent}')
        logging.debug(f'parents_time:{parents_time}')
        logging.debug(f'total_epochs:{total_epochs}')
        logging.debug(f'copynumber:{label_to_copy[label]}')

        # first handle the two nodes under the root:
        if parent == 0:
            epochs_created_temp = np.tile(epochs_created[row], (1, 1))
            epochs_created_temp[:, label] = 0
        else:    
            if parents_time <= total_epochs and label_to_copy[label] == 1:
                if parents_time != -1:
                    epochs_created_temp = np.tile(epochs_created[row], (total_epochs - parents_time + 1, 1))
                    epochs_created_temp[:, label] = list(range(parents_time, total_epochs + 1))
                else:
                    epochs_created_temp = np.tile(epochs_created[row], (total_epochs - parents_time, 1))
                    epochs_created_temp[:, label] = list(range(parents_time + 1, total_epochs + 1))
                logging.debug(f'epochs_created_temp:{epochs_created_temp}')

            elif parents_time < total_epochs:
                epochs_created_temp = np.tile(epochs_created[row], (total_epochs - parents_time, 1))
                epochs_created_temp[:, label] = list(range(parents_time + 1, total_epochs + 1))
                logging.debug(f'epochs_created_temp:{epochs_created_temp}')

            else:
                continue

        if row == 0:
            new_epochs_created = epochs_created_temp
            logging.debug(f':new_epochs_created{new_epochs_created}')
        else:
            new_epochs_created = np.vstack([new_epochs_created,epochs_created_temp])

    return new_epochs_created


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
                "max_epoch": 2
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
                "max_epoch": 2
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
                "max_epoch": 2
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
                                    test_case["input"]["max_epoch"])

        assert np.array_equal(result, test_case["expected"]), f"Test case {i+1} failed: expected {test_case['expected']}, but got {result}"

test_handle_other_nodes()


def group_columns_by_parent(parents):
    """
    Group columns by parent.

    Args:
        parents (dict): A dictionary with keys as child indices and values as their parent indices.

    Returns:
        dict: A dictionary with keys as parent indices and values as lists of their child indices.
    """
    grouped_columns = {}
    for child, parent in parents.items():
        if parent in grouped_columns:
            grouped_columns[parent].append(child)
        else:
            grouped_columns[parent] = [child]
    return grouped_columns


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


test_group_columns_by_parent()


def is_valid_row(row, grouped_columns):
    """
    Check if a row is valid based on the constraints of grouped_columns.

    Args:
        row (np.array): A NumPy array representing a row of data.
        grouped_columns (dict): A dictionary with keys as parent indices and values as lists of their child indices.

    Returns:
        bool: True if the row is valid, False otherwise.
    """
    for parent, children in grouped_columns.items():
        child_columns = [row[child] for child in children]
        if len(set(child_columns)) > 1:
            return False
    return True

# this function may be redundant now...
def filter_rows_based_on_parents(epochs_created, parents):
    """
    Filter rows in the timings array based on constraints from the parents dictionary.

    Args:
        timings (np.array): A 2D NumPy array representing the input data.
        parents (dict): A dictionary with keys as child indices and values as their parent indices.

    Returns:
        np.array: A filtered 2D NumPy array containing only the valid rows based on the constraints.
    """
    grouped_columns = group_columns_by_parent(parents)
    filtered_rows = [row for row in epochs_created if is_valid_row(row, grouped_columns)]
    filtered_timings = np.array(filtered_rows, dtype=object)
    return filtered_timings

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

# Run the test function
test_filter_rows_based_on_parents()



