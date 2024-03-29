import logging
from prismm.run_summed_BP_search.parse_arguments import parse_arguments
from prismm.utils.IO_operations import load_results_from_file, save_likelihoods_to_file
from prismm.run_summed_BP_search.print_things import pretty_print_simulation, print_dataframes, print_path_likelihoods
from prismm.run_summed_BP_search.multiplicities_to_likelihoods import CN_multiplicities_to_likelihoods, CN_multiplicities_to_likelihoods_cts
from prismm.run_summed_BP_search.compute_likelihoods import compute_likelihoods
from prismm.utils.set_logging_settings import set_logging_settings
from prismm.script_args import print_args


def generate_default_paths(max_default_path_length):
    default_paths = [str(x) for x in range(max_default_path_length)]
    default_paths += [str(x) + "G" + str(y)
                      for x in range(max_default_path_length)
                      for y in range(max_default_path_length)
                      if x + y <= max_default_path_length]

    return default_paths

def load_simulation_and_compute_likelihoods(args, default_paths):
    simulation = load_results_from_file(args=args)
    pretty_print_simulation(simulation=simulation)
    likelihoods = CN_multiplicities_to_likelihoods(args=args,
                                                   observed_copy_number_multiplicities=simulation['observed_copy_number_multiplicities'])
    continuous_likelihoods = CN_multiplicities_to_likelihoods_cts(args=args, observed_copy_number_multiplicities=simulation['observed_copy_number_multiplicities'])
    computed_likelihoods = compute_likelihoods(
        likelihoods=likelihoods,
        max_number_of_solutions=args.max_number_of_solutions,
        default_paths=default_paths,
        prob_dist_filter=args.prob_dist_filter,
        path_length_diff=args.path_length_diff
    )

    return simulation, likelihoods, computed_likelihoods

def save_and_print_dataframes(args, simulation, likelihoods, computed_likelihoods, default_paths):
    marginal_likelihoods, top_likelihoods, searchable_likelihoods = computed_likelihoods
    dataframes = {
        "Marginal Likelihoods" : marginal_likelihoods,
        "Top Likelihoods" : top_likelihoods,
        "Likelihoods" : likelihoods,
        "Searchable Likelihoods" : searchable_likelihoods
    }
    print_dataframes(dataframes)
    logging.info("finished_print_dataframes")

    save_likelihoods_to_file(
        args=args,
        likelihoods=likelihoods,
        marginal_likelihoods=marginal_likelihoods,
        top_likelihoods=top_likelihoods,
        searchable_likelihoods=searchable_likelihoods
    )

    print_path_likelihoods(
        likelihoods=likelihoods,
        searchable_likelihoods=searchable_likelihoods,
        marginal_likelihoods=marginal_likelihoods,
        top_likelihoods=top_likelihoods,
        default_paths=default_paths,
        simulation=simulation
    )

def main(args):
    print("doing the summed BP search")
    print_args(args)
    set_logging_settings(args)

    default_paths = generate_default_paths(max_default_path_length=args.max_default_path_length)
    simulation, likelihoods, computed_likelihoods = load_simulation_and_compute_likelihoods(args, default_paths)
    save_and_print_dataframes(args=args, simulation=simulation, likelihoods=likelihoods, computed_likelihoods=computed_likelihoods, default_paths=default_paths)

if __name__ == '__main__':
    args = parse_arguments()
    main(args)