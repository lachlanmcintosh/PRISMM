"""
This module is part of the PRISMM project and is the entry point to simulate a cancer genome.
"""

import pickle
import copy
import logging
from typing import Dict, List, Any, Tuple
from pathlib import Path

from prismm.run_simulation.simulate_cancer_genome.simulate_cancer_genome import simulate_cancer_genome
from prismm.run_simulation.simulated_tree_analysis.count_multiplicities import count_copy_numbers_and_multiplicities
from prismm.run_simulation.create_simulated_tree.create_simulated_tree import create_phylogenetic_trees_from_simulation
from prismm.run_simulation.create_simulated_tree.extract_copy_number_trees_from_phylogenetic_trees import extract_copy_number_trees_from_phylogenetic_trees
from prismm.run_simulation.simulated_tree_analysis.print import print_simulated_genome_data
from prismm.run_simulation.simulation_priors.simulate_prior import simulate_parameters_not_given_as_arguments
from prismm.run_simulation.parse_arguments import parse_arguments
from prismm.script_args import print_args
from prismm.utils.set_logging_settings import set_logging_settings
from prismm.utils.path_codes import pre_mid_post_to_path_length
from prismm.utils.FILES import SIMULATIONS_FILE_FOLDER
from prismm.utils.IO_operations import save_simulation_to_file

def simulate_genome_and_summarise_observable_variables(args) -> Tuple[Dict, List, List, Dict, Dict]:
    """
    This function simulates a cancer genome and records it's phylogenetic tree based on the provided arguments. It also extracts the observable variables to perform inference on.
    """
    # Simulate the genome
    simulated_chromosomes = simulate_cancer_genome(
        p_up=args.p_up,
        p_down=args.p_down,
        pre=args.pre,
        mid=args.mid,
        post=args.post,
        rate=args.rate
    )

    # Perform basic analysis of the simulated genome
    phylogenetic_trees = create_phylogenetic_trees_from_simulation(
        simulated_chromosomes=simulated_chromosomes,
        total_epochs=pre_mid_post_to_path_length(args.pre, args.mid, args.post)
    )

    copy_number_trees = extract_copy_number_trees_from_phylogenetic_trees(phylogenetic_trees=phylogenetic_trees) 

    observed_copy_numbers, observed_copy_number_multiplicities = count_copy_numbers_and_multiplicities(simulated_chromosomes=simulated_chromosomes)

    for chrom_type in copy_number_trees:
        assert sorted([copy_number_trees[chrom_type][1][0],copy_number_trees[chrom_type][2][0]]) == sorted(observed_copy_numbers[chrom_type])

    return simulated_chromosomes, phylogenetic_trees, copy_number_trees, observed_copy_numbers, observed_copy_number_multiplicities
    
save_results_to_file  = save_simulation_to_file


def main(args) -> None:
    """
    Main function to run the simulation, analyze the results, and save them.

    The function performs the following steps:
    1. Simulate parameters that are not provided as arguments.
    2. Simulate a genome and perform basic analysis.
    3. Print the simulated genome data.
    4. Save the results to a file.
    """
    
    logging.info("GENERATING A SIMULATION")
    logging.info("\n\nArguments given as input:")
    print_args(args)

    args = simulate_parameters_not_given_as_arguments(args)
    logging.info("\n\nAll arguments given as input or simulated:")
    print_args(args)

    simulated_chromosomes, phylogenetic_trees, copy_number_trees, observed_copy_numbers, observed_copy_number_multiplicities = simulate_genome_and_summarise_observable_variables(args)

    # TODO: move the observed_copy_numbers and multiplicities to the summed module. Don't need them here, they are in the wrong place. We use these values when doing the initial search in the summed module. Actually leave them here. It is a good check to make sure that all chromosomes were properly inserted into the tree. 

    print_simulated_genome_data(
        simulated_chromosomes=simulated_chromosomes,
        phylogenetic_trees=phylogenetic_trees,
        copy_number_trees=copy_number_trees,
        observed_copy_numbers=observed_copy_numbers,
        observed_copy_number_multiplicities=observed_copy_number_multiplicities
    )
    
    logging.info("\n\nAll arguments given as input or simulated:")
    print_args(args)

    # Save the results
    save_simulation_to_file(
        args=args,
        simulated_chromosomes=simulated_chromosomes,
        phylogenetic_trees=phylogenetic_trees,
        copy_number_trees=copy_number_trees,
        observed_copy_numbers=observed_copy_numbers,
        observed_copy_number_multiplicities=observed_copy_number_multiplicities,
    )


if __name__ == "__main__":
    args = parse_arguments()
    set_logging_settings(args)
    main(args)

