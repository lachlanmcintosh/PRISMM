from prismm.utils.FILES import SIMULATIONS_FILE_FOLDER
import pickle
import os
from typing import Dict, List
import logging


def load_results_from_file(args):
    file_name = f'{SIMULATIONS_FILE_FOLDER}/{args.simulation_filename}_{args.test_case}.pickle'
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
    return data["simulation"]

def save_simulation_to_file(args, simulated_chromosomes: Dict,
                         phylogenetic_trees: List, copy_number_trees: List, observed_copy_numbers: Dict,
                         observed_copy_number_multiplicities: Dict) -> None:
    """
    Function to save the simulation results to a pickle file.
    """

    file_name = SIMULATIONS_FILE_FOLDER + f'/{args.simulation_filename}_{args.test_case}.pickle'
    with open(file_name, 'wb') as f:
        pickle.dump({
            "simulation": {
                'simulated_chromosomes': simulated_chromosomes,
                'phylogenetic_trees': phylogenetic_trees,
                'copy_number_trees': copy_number_trees,
                'observed_copy_numbers': observed_copy_numbers,
                'observed_copy_number_multiplicities': observed_copy_number_multiplicities,
                'args': args
            }
        }, f)
    logging.info(f"Simulation saved to file {file_name}")

def save_likelihoods_to_file(likelihoods, marginal_likelihoods, top_likelihoods, searchable_likelihoods, args):
    print(args)
    file_name = f'{SIMULATIONS_FILE_FOLDER}/{args.simulation_filename}_{args.test_case}.pickle'
    
    data_to_dump = {"CN_solutions":
                    {
                        'likelihoods': likelihoods,
                        'marginal_likelihoods': marginal_likelihoods,
                        'top_likelihoods': top_likelihoods,
                        'searchable_likelihoods': searchable_likelihoods,
                        'args': args
                        }
    }
    
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            old_data = pickle.load(f)
        old_data.update(data_to_dump)
        data_to_dump = old_data
    
    with open(file_name, 'wb') as f:
        pickle.dump(data_to_dump, f)