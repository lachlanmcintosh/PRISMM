from typing import List

from prismm.utils.set_logging_settings import set_logging_settings
from prismm.script_args import print_args
from prismm.run_analyse_trees.parse_arguments import parse_arguments

from prismm.run_analyse_trees.IO_operations import load_simulation_data, save_simulation_data
from prismm.run_analyse_trees.process_results import sort_simulation_results_by_likelihood, get_all_trees_ready_for_comparison
from prismm.run_analyse_trees.tree_things import filter_tree
from prismm.run_analyse_trees.printing_things import print_solution_results, print_similarity_results, print_dicts_memory
from prismm.run_analyse_trees.distance_functions import ZeroDistance, AbsoluteDifference, SquaredDistance, InfiniteDistance, compute_solution_similarity
from prismm.run_analyse_trees.process_results import process_further
from prismm.run_analyse_trees.relative_timing_functions import add_relative_timing_comparison
from prismm.utils.set_logging_settings import set_logging_settings


def main(args) -> None:
    """
    The main function that processes a simulation test case and analyzes estimated trees.

    Args:
        test_case (str): A string specifying which test case to process.
        simulation_filename (str): The filename containing the simulation data.

    """

    # Parse the arguments
    print("analysing the trees generated by the inference")
    print_args(args)

    test_case = args.test_case
    simulation_filename = args.simulation_filename

    # Configure logging settings based on --debug argument
    set_logging_settings(args)

    SS = load_simulation_data(test_case, simulation_filename)
    SS["solutions"] = sort_simulation_results_by_likelihood(SS["solutions"])
    get_all_trees_ready_for_comparison(SS)
    print_solution_results(SS)

    # List of node distance functions
    node_distance_functions = [ZeroDistance, AbsoluteDifference, SquaredDistance, InfiniteDistance]

    # Call the function
    compute_solution_similarity(SS, node_distance_functions)
    add_relative_timing_comparison(SS)
    print_similarity_results(SS)

    process_further(SS)

    save_simulation_data(test_case, simulation_filename, SS)

    
    print_dicts_memory(SS)

if __name__ == '__main__':
    args = parse_arguments()
    main(args)


