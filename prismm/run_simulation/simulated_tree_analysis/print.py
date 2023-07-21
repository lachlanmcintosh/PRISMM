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
    Logs some information about simulated chromosomes and trees
    """
    logging.info("\n\nSimulated genome was:")
    for chrom in simulated_chromosomes:
        logging.info("chrom: %s, value: %s", str(chrom), str(simulated_chromosomes[chrom]))

    logging.info("\n\nThe phylogenetic dict trees are:")
    for chrom_type in phylogenetic_trees:
        logging.info("chrom_type: %s, value: %s", chrom_type, phylogenetic_trees[chrom_type])

    logging.info("\n\nThe copy number dict simplified trees are:")
    for chrom_type in copy_number_trees:
        logging.info("chrom_type: %s, value: %s", chrom_type, copy_number_trees[chrom_type])

    logging.info("\n\nObserved parental specific copy numbers:")
    for chrom_type in observed_copy_numbers:
        logging.info("chrom_type: %s, value: %s", chrom_type, observed_copy_numbers[chrom_type])

    logging.info("\n\nObserved parental specific copy number multiplicities")
    for value in observed_copy_number_multiplicities:
        logging.info("value: %s, multiplicity: %s", value, observed_copy_number_multiplicities[value])

