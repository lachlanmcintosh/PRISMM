from typing import List

from prismm.run_simulation.simulate_cancer_genome.initialize_simulated_chromosomes import initialize_simulated_chromosomes
from prismm.run_simulation.simulate_cancer_genome.simulate_SNVs import simulate_snvs
from prismm.run_simulation.simulate_cancer_genome.simulation_checks import check_all_chrs_are_unique, check_simulated_chromosomes
from prismm.run_simulation.simulate_cancer_genome.simulate_GD import simulate_gd
from prismm.run_simulation.simulate_cancer_genome.simulate_anueploidy_agnostic import simulate_anueploidy_agnostic
from prismm.run_simulation.simulate_cancer_genome.simulate_anueploidy_model import simulate_anueploidy
from prismm.utils.LENGTHS import LENGTHS
from prismm.utils.get_ev_string import get_ev_string
from prismm.utils.path_codes import pre_mid_post_to_path_length

def simulate_cancer_genome(p_up: float, p_down: float, pre: int, mid: int, post: int, rate: float, agnostic: bool=False) -> List:
    """
    Simulate a genome based on given parameters.

    :param p_up: Probability of upward mutation.
    :param p_down: Probability of downward mutation.
    :param pre: Pre-mutation period.
    :param mid: Mid-mutation period.
    :param post: Post-mutation period.
    :param rate: Mutation rate.
    :param agnostic: Indicates if the simulation is agnostic or not.
    :return: Simulated chromosomes.
    """
    # Initialize unique SNVs count
    snv_count = 0

    # Initialize chromosomes
    simulated_chromosomes = initialize_simulated_chromosomes()

    # Initialize unique chromosomes count (46 for a human cell)
    chrom_count = 46

    # Get epochs sequence based on pre, mid, and post mutation periods
    ev_sequence = get_ev_string(pre, mid, post)

    if not ev_sequence:
        return simulated_chromosomes

    for epoch, epoch_type in enumerate(ev_sequence):
        # Simulate SNVs
        snv_count, simulated_chromosomes = simulate_snvs(simulated_chromosomes, LENGTHS, rate, epoch, snv_count)

        # Ensure all chromosomes are unique
        check_all_chrs_are_unique(simulated_chromosomes)

        if (mid != -1 and epoch == pre) or (post != -1 and epoch == pre + 1 + mid):
            if epoch_type != "G":
                raise ValueError(f"Expected 'G' at epoch {epoch}, got {epoch_type}")
            chrom_count, simulated_chromosomes = simulate_gd(simulated_chromosomes, epoch+1, chrom_count)
        else:
            if epoch_type != "A":
                raise ValueError(f"Expected 'A' at epoch {epoch}, got {epoch_type}")
            if agnostic:
                chrom_count, simulated_chromosomes = simulate_anueploidy_agnostic(simulated_chromosomes, epoch+1, chrom_count)
            else:
                chrom_count, simulated_chromosomes = simulate_anueploidy(simulated_chromosomes, epoch+1, chrom_count, p_up, p_down)

        # Ensure all chromosomes are unique after mutations
        check_all_chrs_are_unique(simulated_chromosomes)

    if pre_mid_post_to_path_length(pre,mid,post) != len(ev_sequence):
        raise ValueError("Mismatch between mutation periods and length of epochs sequence")

    check_simulated_chromosomes(simulated_chromosomes, pre, mid, post, ev_sequence)

    return simulated_chromosomes
