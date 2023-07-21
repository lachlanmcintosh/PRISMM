from typing import Dict, List

def initialize_simulated_chromosomes() -> Dict[int, List[Dict[str, str]]]:
    """
    Initialize a dictionary of simulated chromosomes with default values.

    Each chromosome is represented as a dictionary with keys:
    - 'unique_identifier': a unique identifier for the chromosome
    - 'parent': parent of the chromosome (-1 denotes the root)
    - 'epoch_created': time of creation of the chromosome (0 for all chromosomes here)
    - 'paternal': True if the chromosome is paternal, False otherwise
    - 'SNVs': list of single nucleotide variants (empty initially)
    - 'dead': whether the chromosome is dead (False for all chromosomes initially)

    Returns:
        A dictionary where each key is a chromosome type (0 to 22) and each value is a list of two 
        initialized chromosomes of that type.
    """
    simulated_chromosomes = {}

    for chrom_type in range(23):
        # Initialize two chromosomes for each type
        simulated_chromosomes[chrom_type] = [
            {
                "unique_identifier": chrom_type + x,
                "parent": -1,
                "epoch_created": 0,
                "paternal": x == 0,  # First chromosome is paternal, second is not
                "sibling": None,
                "SNVs": [],
                "dead": False,
            }
            for x in (0,23)  # maternal and paternal chromosomes for each type
        ]

    return simulated_chromosomes
