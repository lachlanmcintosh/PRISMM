from prismm.utils.FILES import SIMULATIONS_FILE_FOLDER
import pickle
import os

def load_results_from_file(test_case, simulation_name):
    file_name = f'{SIMULATIONS_FILE_FOLDER}/{simulation_name}_{test_case}.pickle'
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
    return data["simulation"]


def save_likelihoods(likelihoods, marginal_likelihoods, top_likelihoods, searchable_likelihoods, args):
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