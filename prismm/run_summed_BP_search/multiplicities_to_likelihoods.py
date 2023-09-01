import numpy as np
import pandas as pd
import re
from typing import Dict
from prismm.utils.FILES import PRECOMPUTED_FILE_FOLDER

def calculate_likelihoods(all_data, observed_copy_number_multiplicities):
    
    # Convert observed_copy_number_multiplicities keys to string
    observed_copy_number_multiplicities_str = {
        str(key): value for key, value in observed_copy_number_multiplicities.items()
    }

    # For debugging: print the columns in all_data and the keys in observed_copy_number_multiplicities_str
    #print("Columns in all_data:", all_data.columns)
    #print("Keys in observed_copy_number_multiplicities_str:", observed_copy_number_multiplicities_str.keys())

    # Create a list comprehension using the adjusted column names
    lls = np.sum(
        [all_data[f"CN_{copy}"] * multiplicity for copy, multiplicity in observed_copy_number_multiplicities_str.items()],
        axis=0
    )
    
    assert np.shape(lls) == np.shape(all_data["CN_0"]), "Mismatch in shapes of lls and all_data['CN_0']"
    
    likelihoods = np.exp(lls)
    
    if "0" in observed_copy_number_multiplicities:
        zero_column_name = "CN_0"
        likelihoods = likelihoods / (1 - np.exp(all_data[zero_column_name]))**observed_copy_number_multiplicities["0"]
    
    return likelihoods



def test_calculate_likelihoods():
    # Test Case 1
    all_data = {
        "0": np.array([0.0, 0.0, 0.0]),
        "1": np.array([0.5, 0.5, 0.5]),
        "2": np.array([1.0, 1.0, 1.0]),
        "3": np.array([1.5, 1.5, 1.5])
    }
    observed_copy_number_multiplicities = {
        0: 2,
        1: 1,
        2: 3
    }
    
    expected_likelihoods = np.array([0.01831564, 0.01831564, 0.01831564])
    
    result = calculate_likelihoods(all_data, observed_copy_number_multiplicities)
    assert np.allclose(result, expected_likelihoods), f"Expected {expected_likelihoods}, but got {result}"

    # Test Case 2
    all_data = {
        "0": np.array([0.1, 0.2, 0.3]),
        "1": np.array([0.4, 0.5, 0.6]),
        "2": np.array([0.7, 0.8, 0.9]),
        "3": np.array([1.0, 1.1, 1.2])
    }
    observed_copy_number_multiplicities = {
        1: 2,
        2: 1
    }
    
    expected_likelihoods = np.array([1.778271, 2.178106, 2.576879])
    
    result = calculate_likelihoods(all_data, observed_copy_number_multiplicities)
    assert np.allclose(result, expected_likelihoods, rtol=1e-5), f"Expected {expected_likelihoods}, but got {result}"

    # Test Case 3
    all_data = {
        "0": np.array([0.2, 0.3, 0.4]),
        "1": np.array([0.5, 0.6, 0.7]),
        "2": np.array([0.8, 0.9, 1.0]),
        "3": np.array([1.1, 1.2, 1.3])
    }
    observed_copy_number_multiplicities = {
        0: 1,
        1: 1,
        2: 1,
        3: 1
    }
    
    expected_likelihoods = np.array([1.513225, 1.878165, 2.218444])
    
    result = calculate_likelihoods(all_data, observed_copy_number_multiplicities)
    assert np.allclose(result, expected_likelihoods, rtol=1e-5), f"Expected {expected_likelihoods}, but got {result}"


def CN_multiplicities_to_likelihoods(args, observed_copy_number_multiplicities: Dict[int, int]):
    file_name = f"{PRECOMPUTED_FILE_FOLDER}p{args.path_length}_v{args.precomputed_version}/concatenated_table_logged.csv"
    all_data = pd.read_csv(file_name)
    likelihoods = calculate_likelihoods(all_data, observed_copy_number_multiplicities)
    named_likelihoods = all_data[["p_up", "p_down", "path"]].copy()
    named_likelihoods.insert(3, "likelihood", likelihoods, True)
    named_likelihoods.replace([np.inf, -np.inf], np.nan, inplace=True)
    named_likelihoods.dropna(axis=0, inplace=True)
    named_likelihoods.sort_values(by=['likelihood'], inplace=True, ascending=False)
    total = np.nansum(named_likelihoods["likelihood"])
    named_likelihoods["likelihood"] /= total
    return named_likelihoods

def test_CN_multiplicities_to_likelihoods():
    def read_pickle_with_custom_columns(file_name):
        # Dummy implementation
        return pd.DataFrame({
            "0": [0, 1, 2],
            "1": [0, 1, 2],
            "2": [0, 1, 2],
            "3": [0, 1, 2],
            "p_up": [0.1, 0.2, 0.3],
            "p_down": [0.3, 0.2, 0.1],
            "path": ["path1", "path2", "path3"],
        })

    observed_copy_number_multiplicities = {
        0: 2,
        1: 1,
        2: 3
    }

    expected_named_likelihoods = pd.DataFrame({
        "p_up": [0.1, 0.2, 0.3],
        "p_down": [0.3, 0.2, 0.1],
        "path": ["path1", "path2", "path3"],
        "likelihood": [0.31830989, 0.31830989, 0.36338023]
    })

    result = CN_multiplicities_to_likelihoods(observed_copy_number_multiplicities)
    pd.testing.assert_frame_equal(result, expected_named_likelihoods, check_exact=False, rtol=1e-5)

    # Additional test cases can be added here with different observed_copy_number_multiplicities values and read_pickle_with_custom_columns function

#test_CN_multiplicities_to_likelihoods()


def CN_multiplicities_to_likelihoods_cts(args, observed_copy_number_multiplicities: Dict[int, int]):
    # want the three likelihoods here, want the best 2GD one, the best 1GD one, and the best no GD one
    
    
