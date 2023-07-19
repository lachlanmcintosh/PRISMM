from typing import List

from prismm.run_simulation.parse_arguments import parse_arguments
from prismm.run_analyse_trees.analyse_trees import compute_solution_similarity, add_relative_timing_comparison, \
    print_similarity_results, process_further, print_solution_results, sort_simulation_results_by_likelihood, \
    get_all_trees_ready_for_comparison, save_simulation_data, load_simulation_data, print_dicts_memory
from prismm.run_analyse_trees.node_distance_functions import ZeroDistance, AbsoluteDifference, SquaredDistance, \
    InfiniteDistance
from prismm.utils.set_logging import set_logging


def main() -> None:
    """
    The main function that processes a simulation test case and analyzes estimated trees.

    Args:
        test_case (str): A string specifying which test case to process.
        simulation_filename (str): The filename containing the simulation data.

    """

    # Parse the arguments
    args = parse_arguments()
    test_case = args.test_case
    simulation_filename = args.simulation_filename

    # Configure logging settings based on --debug argument
    set_logging(args)

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

if __name__ == "__main__":

    main()


