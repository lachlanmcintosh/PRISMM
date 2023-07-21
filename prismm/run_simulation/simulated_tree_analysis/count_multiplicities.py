from typing import Dict, List, Tuple
from collections import Counter

def count_copy_numbers(simulated_chromosomes: Dict[str, List[Dict]]) -> Dict[str, List[int]]:
    """
    Count the number of each parental specific copy number found in the genome.
    """
    observed_copy_numbers = {}
    for chrom_type in simulated_chromosomes:
        observed_copy_numbers[chrom_type] = [
            len([x for x in simulated_chromosomes[chrom_type] if paternal == x["paternal"] and not x["dead"]])
            for paternal in [True, False]
        ]
    return observed_copy_numbers

def count_copy_number_multiplicities(observed_copy_numbers: Dict[str, List[int]]) -> Dict[int, int]:
    """
    Count the multiplicities of each observed copy number in the genome.

    Args:
        observed_CNs: The input observed copy numbers.

    Returns:
        A dictionary mapping each observed copy number to its multiplicity.
    """
    # Create an empty Counter object
    multiplicities = Counter()

    # Update the Counter with the observed copy numbers
    for copy_number in observed_copy_numbers.values():
        multiplicities.update(copy_number)

    # Sort the multiplicities dictionary by its keys in ascending order and return it
    multiplicities = dict(sorted(multiplicities.items()))

    return multiplicities


def count_copy_numbers_and_multiplicities(simulated_chromosomes: Dict[str, List[Dict]]) -> Tuple[Dict[str, List[int]], Dict[int, int]]:
    
    observed_copy_numbers = count_copy_numbers(simulated_chromosomes=simulated_chromosomes)
    observed_copy_number_multiplicities = count_copy_number_multiplicities(observed_copy_numbers=observed_copy_numbers)

    return observed_copy_numbers, observed_copy_number_multiplicities