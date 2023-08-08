import json
import logging
from prismm.utils.pretty_print import pretty_print
from prismm.utils.path_codes import generate_path
from prismm.run_summed_BP_search.count_higher_likelihood_paths import count_higher_likelihood_paths


def print_path_likelihoods(likelihoods, searchable_likelihoods, marginal_likelihoods, top_likelihoods, default_paths, simulation):
    def print_dataframe_rows(df, label, path):
        path_in_df = any(df['path'] == path)
        if path_in_df:
            path_rows = df.loc[df['path'] == path]
            logging.info(f"{label} for path {path}:\n{path_rows}")
        else:
            logging.info(f"Path {path} not found in {label}")
            
    # Create the path using the data dictionary values for pre, mid, and post
    print(simulation.keys())
    path = generate_path(simulation['args'].pre, simulation['args'].mid, simulation['args'].post)
    
    # Print the pre, mid, and post values and the generated path
    logging.info(f"pre: {simulation['args'].pre}, mid: {simulation['args'].mid}, post: {simulation['args'].post} => path: {path}")
    
    # Print the likelihood row for that path
    path_in_likelihoods = any(likelihoods['path'] == path)
    if path_in_likelihoods:
        print_dataframe_rows(likelihoods, "Likelihood", path)
    else:
        raise ValueError(f"Path {path} not found in likelihoods")
        
    # Print the rows for the given path in other dataframes
    print_dataframe_rows(marginal_likelihoods, "Marginal likelihood", path)
    print_dataframe_rows(top_likelihoods, "Top likelihood", path)
    print_dataframe_rows(searchable_likelihoods, "Searchable likelihood", path)
    
    # Check if the path is in default_paths and print a message accordingly
    logging.info(f"Default paths searched through are {default_paths}")
    if path in default_paths:
        logging.info(f"Path {path} is a default path")
    else:
        logging.info(f"Path {path} not found in default paths")

    # Calculate the marginal likelihood for the path
    path_likelihood_rows = likelihoods.loc[likelihoods['path'] == path]
    marginal_likelihood = path_likelihood_rows['likelihood'].sum()
    logging.info(f"Marginal likelihood for path {path}: {marginal_likelihood}")

    # Calculate the number of unique paths with a higher likelihood and get the paths
    count_higher_likelihood_paths(likelihoods=marginal_likelihoods, path=path, name="marginal likelihoods")

    # same for top likelihoods
    count_higher_likelihood_paths(likelihoods=top_likelihoods, path=path, name="top likelihoods")




def pretty_print_simulation(simulation):
    for key, value in simulation.items():
        pretty_print(key)
        pretty_print(value)

def print_dataframes(dataframes: dict):
    for name, df in dataframes.items():
        logging.info(f"{name}:\n{df}\n")

def pretty_print_tree(tree):
    """
    Pretty-prints a nested dictionary representing a tree.

    Args:
        tree (dict): The tree dictionary to be pretty-printed.
    """
    print(json.dumps(tree, indent=4, sort_keys=True))

def print_summary(total_nodes, num_chrom_with_correct_CN, num_chrom_with_correct_CN_and_epoch_created, average_distance_from_truth_of_epoch_created):
    print(f"Total nodes: {total_nodes}")
    print(f"Number of chromosomes with correct copy numbers: {num_chrom_with_correct_CN}")
    print(f"Number of chromosomes with correct copy numbers and epochs created: {num_chrom_with_correct_CN_and_epoch_created}")
    print(f"Average distance from truth of epoch created: {average_distance_from_truth_of_epoch_created}")
    
