import logging
import copy
import numpy as np

from prismm.run_build_trees_and_timings.parse_arguments import parse_arguments
from prismm.run_build_trees_and_timings.IO_operations import load_results_from_file, save_dict_to_file
from prismm.run_simulation.simulation_priors.random_number_generator import sample_p_up_and_p_down_from_dirichelet_distribution
from prismm.script_args import print_args
from prismm.utils.set_logging_settings import set_logging_settings
from prismm.run_build_trees_and_timings.get_SNV_multiplicities import count_SNV_multiplicities
from prismm.utils.path_codes import generate_path, path_code_to_pre_mid_post, pre_mid_post_to_path_length
from prismm.run_build_trees_and_timings.get_all_trees import get_all_trees
from prismm.run_build_trees_and_timings.add_timings_to_trees import add_timings_to_trees
from prismm.run_build_trees_and_timings.get_annotated_trees_and_timings import get_annotated_trees_and_timings
from prismm.run_build_trees_and_timings.get_joint_SNV_CN_likelihoods import find_BP_and_SNV_loglik

from prismm.utils.LENGTHS import LENGTHS

def sum_SNV_counts(observed_SNV_multiplicities):
    d = observed_SNV_multiplicities
    total = 0
    for key1 in d:
        for key2 in d[key1]:
            total += d[key1][key2]
    return total


def sum_chrom_multiplicities(observed_CN_multiplicities):
    return sum(observed_CN_multiplicities.values())

def sum_observed_copy_numbers(dictionary):
    total_sum = 0
    for value_list in dictionary.values():
        total_sum += sum(value_list)
    return total_sum



def print_results(res, path, p_up, p_down, pre, mid, post):
    logging.info("############################\n" * 10)
    logging.info(res)
    logging.info("path: " + str(path))
    logging.info("p_up: " + str(p_up))
    logging.info("p_down: " + str(p_down))
    logging.info("pre: " + str(pre))
    logging.info("mid: " + str(mid))
    logging.info("post: " + str(post))


def print_all_trees_and_timings(trees_and_timings):
    logging.debug("Print all trees and timings info")
    for chrom in trees_and_timings:
        logging.debug(chrom)
        logging.debug(trees_and_timings[chrom])

def initial_rate_estimate(pre, mid, post, SS):
    logging.info("Initial rate estimate")
    total_SNV_time = pre + mid + post + 2 + 1
    total_SNVs = sum_SNV_counts(SS["SNV_solutions"]["observed_SNV_multiplicities"])
    logging.info("total SNVs")
    logging.info(total_SNVs)
    logging.info("observed_SNV_multiplicities")
    logging.info(SS["SNV_solutions"]["observed_SNV_multiplicities"])

    logging.info("observed_copy_numbers")
    logging.info(SS["simulation"]["observed_copy_numbers"])

    total_chromosomes = sum_observed_copy_numbers(SS["simulation"]["observed_copy_numbers"])
    plambda_start = float(total_SNVs) / float(total_SNV_time) / float(total_chromosomes) * 23
    logging.info("plambda_start: " + str(plambda_start))

    return plambda_start, total_SNVs

def get_tree_and_rate_parameters(res, SEARCH_DEPTH, SS):
    if res == SEARCH_DEPTH:
        p_up = int(SS["simulation"]["p_up"] * 100)
        p_down = int(SS["simulation"]["p_down"] * 100)
        pre = SS["simulation"]["pre"]
        mid = SS["simulation"]["mid"]
        post = SS["simulation"]["post"]
        path = generate_path(pre, mid, post)
    else:
        path = SS["CN_solutions"]["searchable_likelihoods"]["path"].iloc[res]
        p_up = int(SS["CN_solutions"]["searchable_likelihoods"]['p_up'].iloc[res])
        p_down = int(SS["CN_solutions"]["searchable_likelihoods"]['p_down'].iloc[res])
        pre, mid, post = path_code_to_pre_mid_post(path)

    for x in [pre, mid, post, p_up, p_down]:
        assert isinstance(x, (int, np.integer)), f"Expected integer, but got {x} of type {type(x)}."

    for x in [p_up,p_down]:
        assert(x >= 0 and x <= 100)

    return path, p_up, p_down, pre, mid, post

import math

def poisson_zero_probability(lam,rounds):
    """
    Calculate the probability that a Poisson random variable is zero for a given parameter.

    :param lam: The Poisson parameter (average rate).
    :return: The probability that a Poisson random variable is zero.
    """
    num_SNVs = 0
    probability = (math.exp(-lam) * (lam ** num_SNVs)) / math.factorial(num_SNVs)
    probability = (probability**23)**rounds
    return probability

from scipy.stats import dirichlet

def calculate_log_likelihood(alpha, probabilities):
    """
    Calculate the log-likelihood of given probabilities based on the Dirichlet distribution.

    Args:
        alpha: list or np.array
            Parameters of the Dirichlet distribution.
        probabilities: np.array
            Probabilities to calculate the log-likelihood for. 

    Returns:
        float: The log-likelihood of the probabilities based on the Dirichlet distribution.
    """
    # Reverse the scaling and rounding transformation
    probabilities = [float(x)/100 for x in probabilities]
    print(probabilities)

    return dirichlet.logpdf(probabilities, alpha)

def test_calculate_log_likelihood():
    alpha = [20, 20, 100]
    probabilities = sample_p_up_and_p_down_from_dirichelet_distribution(alpha)*100
    log_likelihood = calculate_log_likelihood(alpha, probabilities)

    assert isinstance(log_likelihood, np.float64), f"Output is not a float: {type(log_likelihood)}"

test_calculate_log_likelihood()


def handle_results(result_dict):
    for key, value in result_dict.items():
        logging.info(f'{key}: {value}')
        if isinstance(key,int):
            handle_chroms(result_dict, key)

def handle_chroms(result_dict, chrom):
    for x in ["observed_SNV_multiplicities","tree","CNs","starts","ends","branch_lengths","paths","BP_individual_log_likelihoods","BP_loglikelihood","unique_CNs","stacked_branch_lengths","counts"]:
        logging.info(f'{x}: {result_dict[chrom][x]}')
    temp = [count / LENGTHS[chrom] for count in result_dict[chrom]["counts"]]
    #print(temp)
    #print(result_dict[chrom]["stacked_branch_lengths"])
    #print(result_dict[chrom])
    normalize_counts(result_dict, chrom, temp)
    handle_likelihoods(result_dict, chrom)

def normalize_counts(result_dict, chrom, temp):
    for x in range(len(temp)):
        if result_dict[chrom]["stacked_branch_lengths"][x] != 0:
            temp[x] = temp[x]/result_dict[chrom]["stacked_branch_lengths"][x]
    logging.info(f'normalised_counts: {temp}')

def handle_likelihoods(result_dict, chrom):
    for x in ["SNV_log_likelihoods","SNV_log_likelihood","SNV_BP_log_likelihood"]:
        logging.info(f'{x}: {result_dict[chrom][x]}')

def check_failure(all_structures):
    SNV_failure = False
    for chrom in all_structures:
        for structure in all_structures[chrom]:
            if np.isinf(structure["SNV_log_likelihood"]).all():
                print("chrom",chrom)
                print(all_structures[chrom])
                print("failed because of SNV likelihood")
                SNV_failure=True
    return SNV_failure

import time



def handle_errors(all_structures):
    print("failed and don't know why")
    SNV_failure = check_failure(all_structures)
    if SNV_failure:
        print("isn't a SNV failure")
        return True

    for i in range(20):
        print("SEEMINGLY EXCLUSIVELY A SNV OR A BP FAILURE")
    for chrom in all_structures:
        print("chrom", chrom)
        for structure in all_structures[chrom]:
            for key in structure:
                print(f"\tKEY:{key}, {structure[key]}")
    for i in range(20):
        print("***************************************")

    impossible = False
    for chrom in all_structures:
        this_chrom_possible = False
        for structure in all_structures[chrom]:
            if any(str(x) != '-inf' for x in structure["SNV_BP_log_likelihood"]):
                this_chrom_possible = True

        if not this_chrom_possible:
            impossible = True

    return impossible



import sys
def find_solutions(SS, p_window, plambda_window, tree_flexibility, alpha):
    print(SS.keys())
    SS["SNV_solutions"] = {}
    SS["SNV_solutions"]["observed_SNV_multiplicities"] = count_SNV_multiplicities(SS["simulation"]['simulated_chromosomes'])
    SEARCH_DEPTH = len(SS["CN_solutions"]['searchable_likelihoods'])
    results = []

    aggregated_execution_times = {
        "total_time": 0,
        "get_all_trees_and_timings": 0,
        "timing_struct_to_all_structures": 0,
        "find_BP_and_SNV_loglik": 0
    }

    for res in range(SEARCH_DEPTH + 1):
        start_time_res = time.time()
        print("RES", res)
        path_est, p_up_start, p_down_start, pre_est, mid_est, post_est = get_tree_and_rate_parameters(res, SEARCH_DEPTH, SS)
        print_results(res, path_est, p_up_start, p_down_start, pre_est, mid_est, post_est)

        annotated_trees_and_timings = get_annotated_trees_and_timings(observed_SNV_multiplicities=SS["SNV_solutions"]["observed_SNV_multiplicities"],
                                                                      observed_copy_numbers=SS["simulation"]["observed_copy_numbers"],
                                                                      pre_est=pre_est, 
                                                                      mid_est=mid_est, 
                                                                      post_est=post_est, 
                                                                      tree_flexibility=tree_flexibility)

        plambda_start, total_SNVs = initial_rate_estimate(pre_est, mid_est, post_est, SS)

        start_time_BP_SNV_loglik = time.time()
        BP_SNV_loglik = find_BP_and_SNV_loglik(
            plambda_start=plambda_start,
            p_up_start=p_up_start,
            p_down_start=p_down_start,
            p_window=p_window,
            plambda_window=plambda_window,
            all_structures=annotated_trees_and_timings,
            observed_SNV_multiplicities=SS["SNV_solutions"]["observed_SNV_multiplicities"],
            total_SNVs=total_SNVs,
            tree_flexibility=tree_flexibility
        )
        end_time_BP_SNV_loglik = time.time()


        aggregated_execution_times["find_BP_and_SNV_loglik"] += round(end_time_BP_SNV_loglik - start_time_BP_SNV_loglik, 2)

        if BP_SNV_loglik is not None:
            best_neg_loglik, best_p_up, best_p_down, best_plambda, best_structure = BP_SNV_loglik
            logging.info("BP_SNV_output")

            probabilities = [best_p_up, best_p_down, 100-best_p_up-best_p_down]
            log_likelihood = calculate_log_likelihood(alpha, probabilities)

            result_dict = copy.deepcopy(best_structure)
            result_dict["neg_loglik_est"] = best_neg_loglik-log_likelihood
            result_dict["p_up_est"] = best_p_up
            result_dict["p_down_est"] = best_p_down
            result_dict["plambda_est"] = best_plambda
            # TODO: CHANGE THIS TO RATE OR SOMETHING LESS CONFUSING
            result_dict["correct_path"] = res == SEARCH_DEPTH
            result_dict["pre_est"] = pre_est
            result_dict["mid_est"] = mid_est
            result_dict["post_est"] = post_est
            
        else:
            result_dict = None

        if result_dict is not None:
            handle_results(result_dict)
        else:
            impossible = handle_errors(annotated_trees_and_timings)
            if impossible:
                continue

        result_dict["execution_times"] = copy.deepcopy(aggregated_execution_times)
        results.append(copy.deepcopy(result_dict))


    return results



def init(args):
    test_case = args.test_case
    SS = load_results_from_file(test_case=test_case, simulation_filename=args.simulation_filename)
    return SS



def main(args):
    print("building trees and timing arrays from likely paths")
    print_args(args)
    set_logging_settings(args)

    if args.debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    logging.info("load and start finding results")

    SS = init(args)

    SS["solutions"] = find_solutions(SS=SS, p_window=args.p_window, plambda_window=args.plambda_window, tree_flexibility=args.tree_flexibility, alpha=args.alpha)

    # Sort the dictionary based on 'best_neg_loglik' in descending order
    sorted_solutions = sorted(SS['solutions'], key=lambda x: x['neg_loglik_est'], reverse=True)

    print(f"the truth is:")
    print(
        f"pre: {SS['pre']},\n"
        f"mid: {SS['mid']},\n"
        f"post: {SS['post']},\n"
        f"p_up: {SS['p_up']},\n"
        f"p_down: {SS['p_down']},\n"
        f"rate: {SS['rate']}"
    )
    for solution in sorted_solutions:
        print(
            f"best_neg_loglik: {solution['neg_loglik_est']}, "
            f"best_p_up: {solution['p_up_est']}, "
            f"best_p_down: {solution['p_down_est']}, "
            f"best_plambda: {solution['plambda_est']}, "
            f"best_pre: {solution[0]['pre_est']}, "
            f"best_mid: {solution[0]['mid_est']}, "
            f"best_post: {solution[0]['post_est']}, "
            f"correct_path: {solution['correct_path']}, \n"
            f"total_time: {solution['execution_times']['total_time']}, "
            f"time_get_all_trees_and_timings: {solution['execution_times']['get_all_trees_and_timings']}, "
            f"time_timing_struct_to_all_structures: {solution['execution_times']['timing_struct_to_all_structures']}, "
            f"time_find_BP_and_SNV_loglik: {solution['execution_times']['timing_struct_to_all_structures']} \n\n"
        )

   
    for chrom in SS["copy_number_trees"]:
        print(chrom, SS["copy_number_trees"][chrom])
    print(SS.keys())

    # Save some solutions to file here
    save_dict_to_file(dictionary=SS, test_case=args.test_case, simulation_filename=args.simulation_filename)


if __name__ == '__main__':
    args = parse_arguments()
    main(args)

