import random
from typing import Tuple, Union

from prismm.run_simulation.simulation_priors.random_number_generator import (
    sample_SNV_rate_on_uniform_log_scale,
    sample_p_up_and_p_down_from_dirichelet_distribution,
    sample_num_anueploidy_epochs_before_GD_from_trimmed_poisson_distribution
)
from prismm.utils.path_codes import pre_mid_post_to_path_length

def sample_pre_mid_post(gd_probabilities: Tuple[float, float, float], max_epochs: int, lam: float) -> Tuple[int, int, int]:
    """
    Assign specific values to 'pre', 'mid' and 'post' parameters based on provided probabilities.

    This function is used to generate 'pre', 'mid' and 'post' parameters for simulation. 

    Args:
        p1 (float): The probability of no GD.
        p2 (float): The probability of one round of GD.
        p3 (float): The probability of two rounds of GD.
        max_epochs (int): The maximum epochs.
        lam (float): The rate parameter for the Poisson distribution.

    Returns:
        tuple of int: A tuple containing the generated values for 'pre', 'mid' and 'post'.
    """

    num_rounds_GD = random.choices([0, 1, 2], weights=gd_probabilities, k=1)[0]

    max_value = (max_epochs - 2) // (num_rounds_GD + 1)

    if num_rounds_GD == 0:
        return (sample_num_anueploidy_epochs_before_GD_from_trimmed_poisson_distribution(max_value=max_value, lam=lam), 
                -1, 
                -1)

    elif num_rounds_GD == 1:
        return (sample_num_anueploidy_epochs_before_GD_from_trimmed_poisson_distribution(max_value=max_value, lam=lam), 
                sample_num_anueploidy_epochs_before_GD_from_trimmed_poisson_distribution(max_value=max_value, lam=lam), 
                -1)
    
    else:
        return (sample_num_anueploidy_epochs_before_GD_from_trimmed_poisson_distribution(max_value=max_value, lam=lam),
                sample_num_anueploidy_epochs_before_GD_from_trimmed_poisson_distribution(max_value=max_value, lam=lam),
                sample_num_anueploidy_epochs_before_GD_from_trimmed_poisson_distribution(max_value=max_value, lam=lam))


def simulate_parameters_not_given_as_arguments(args) -> None:
    """
    Simulates parameters that are not given as arguments and sets default values if needed, based on certain rules.
    """

    if args.pre is None or args.mid is None or args.post is None:
        assert(args.pre is None and args.mid is None and args.post is None)
        args.pre, args.mid, args.post = sample_pre_mid_post(
            gd_probabilities=args.gd_probabilities, 
            max_epochs=args.max_epochs, 
            lam=args.lam
            )

    args.total_epochs = pre_mid_post_to_path_length(args.pre, args.mid, args.post)

    if args.p_up is None or args.p_down is None:
        assert(args.p_up is None and args.p_down is None)

        args.p_up, args.p_down = sample_p_up_and_p_down_from_dirichelet_distribution(args.alpha)

    if args.rate is None:
        args.rate = sample_SNV_rate_on_uniform_log_scale(100, 1000000)

    return(args)
