import logging
from typing import Dict, List, Any

def print_simulated_genome_data(
    simulated_chromosomes: Dict[str, List[Any]], 
    phylogenetic_trees: Dict[str, List[Any]], 
    copy_number_trees: Dict[str, List[Any]], 
    observed_copy_numbers: Dict[str, List[Any]], 
    observed_copy_number_multiplicities: Dict[str, List[Any]]
) -> None:
    """
    Logs some information about simulated chromosomes and trees.

    Args:
        simulated_chromosomes: A dictionary containing lists of simulated chromosomes.
        truth_trees: A dictionary containing lists of truth trees.
        CN_trees: A dictionary containing lists of CN trees.
        observed_CNs: A dictionary containing lists of observed CNs.
        observed_CN_multiplicities: A dictionary containing lists of observed CN multiplicities.
    """
    logging.info("Simulated genome was:")
    for chrom in simulated_chromosomes:
        logging.debug("chrom: %s, value: %s", str(chrom), simulated_chromosomes[chrom])

    logging.debug("The phylogenetic dict trees are:")
    for chrom_type in phylogenetic_trees:
        logging.debug("chrom_type: %s, value: %s", chrom_type, phylogenetic_trees[chrom_type])

    logging.info("The copy number dict simplified trees are:")
    for chrom_type in copy_number_trees:
        logging.info("chrom_type: %s, value: %s", chrom_type, copy_number_trees[chrom_type])

    logging.info("Observed chromosomal copy numbers:")
    for chrom_type in observed_copy_numbers:
        logging.info("chrom_type: %s, value: %s", chrom_type, observed_copy_numbers[chrom_type])

    logging.info("Observed chromosomal copy number multiplicities")
    for value in observed_copy_number_multiplicities:
        logging.info("value: %s, multiplicity: %s", value, observed_copy_number_multiplicities[value])

