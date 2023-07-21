from typing import Callable, Dict, List, Tuple, Any
import random
import logging

# Define the logger
logger = logging.getLogger(__name__)

def select_chromosomes(chromosomes: List[Dict[str, Any]], num: int) -> List[int]:
    """
    Select a random set of chromosomes.

    :param chromosomes: A list of chromosomes represented as dictionaries.
    :param num: Number of chromosomes to select.
    :return: List of selected chromosome indices.
    """
    return random.choices(range(len(chromosomes)), k=num)

def simulate_agnostic_chromosome_loss(chromosomes: List[Dict[str, Any]], chrom_count: int) -> int:
    """
    Simulate the loss of a random number of chromosomes.

    :param chromosomes: A list of chromosomes represented as dictionaries.
    :param chrom_count: The current chromosome count.
    :return: The updated chromosome count after the loss.
    :raises ValueError: If chromosomes are not a list or chrom_count is not an int.
    :raises KeyError: If a chromosome dictionary is missing the "dead" key.
    """
    if not isinstance(chromosomes, list):
        logger.error(f"Expected list, got {type(chromosomes)}")
        raise ValueError(f"Expected list, got {type(chromosomes)}")
    if not isinstance(chrom_count, int):
        logger.error(f"Expected int, got {type(chrom_count)}")
        raise ValueError(f"Expected int, got {type(chrom_count)}")

    for which in select_chromosomes(chromosomes, random.randint(0, len(chromosomes))):
        try:
            chromosomes[which]["dead"] = True
            chrom_count -= 1
        except KeyError:
            logger.error("Chromosome dictionary missing 'dead' key.")
            raise

    return chrom_count

def simulate_agnostic_chromosome_gain(
    chromosomes: List[Dict[str, Any]],
    epoch: int,
    chrom_count: int,
    create_new_chromosome: Callable[[Dict[str, Any], int, int], Dict[str, Any]]
) -> int:
    """
    Simulate the gain of a random number of chromosomes.

    :param chromosomes: A list of chromosomes represented as dictionaries.
    :param epoch: The current epoch.
    :param chrom_count: The current chromosome count.
    :param create_new_chromosome: Function to create a new chromosome.
    :return: The updated chromosome count after the gain.
    :raises ValueError: If chromosomes are not a list, epoch or chrom_count is not an int.
    :raises KeyError: If a chromosome dictionary is missing the "dead" key.
    """
    if not isinstance(chromosomes, list):
        logger.error(f"Expected list, got {type(chromosomes)}")
        raise ValueError(f"Expected list, got {type(chromosomes)}")
    if not isinstance(epoch, int):
        logger.error(f"Expected int, got {type(epoch)}")
        raise ValueError(f"Expected int, got {type(epoch)}")
    if not isinstance(chrom_count, int):
        logger.error(f"Expected int, got {type(chrom_count)}")
        raise ValueError(f"Expected int, got {type(chrom_count)}")

    for which in select_chromosomes(chromosomes, random.randint(0, len(chromosomes))):
        try:
            if not chromosomes[which]["dead"]:
                new_chrom = create_new_chromosome(chromosomes[which], chrom_count, epoch)
                chromosomes.append(new_chrom)
                chrom_count += 1
        except KeyError:
            logger.error("Chromosome dictionary missing 'dead' key.")
            raise

    return chrom_count

def simulate_anueploidy_agnostic(
    simulated_chromosomes: Dict[str, List[Dict[str, Any]]],
    epoch: int,
    chrom_count: int,
    create_new_chromosome: Callable[[Dict[str, Any], int, int], Dict[str, Any]]
) -> Tuple[int, Dict[str, List[Dict[str, Any]]]]:
    """
    Simulate Anueploidy on a given set of chromosomes, agnostic of chromosome details.

    Randomly select chromosomes to lose and gain, updating their status accordingly.

    :param simulated_chromosomes: A dictionary with chromosome types as keys and a list of chromosomes as values.
                                  Each chromosome is represented as a dictionary.
    :param epoch: The current epoch.
    :param chrom_count: The current chromosome count.
    :param create_new_chromosome: Function to create a new chromosome.
    :return: The updated chromosome count and the updated chromosomes after simulation.
    :raises ValueError: If simulated_chromosomes is not a dict, epoch or chrom_count is not an int.
    """
    if not isinstance(simulated_chromosomes, dict):
        logger.error(f"Expected dict, got {type(simulated_chromosomes)}")
        raise ValueError(f"Expected dict, got {type(simulated_chromosomes)}")
    if not isinstance(epoch, int):
        logger.error(f"Expected int, got {type(epoch)}")
        raise ValueError(f"Expected int, got {type(epoch)}")
    if not isinstance(chrom_count, int):
        logger.error(f"Expected int, got {type(chrom_count)}")
        raise ValueError(f"Expected int, got {type(chrom_count)}")

    for chrom_type, chromosomes in simulated_chromosomes.items():
        chrom_count = simulate_agnostic_chromosome_loss(chromosomes, chrom_count)
        chrom_count = simulate_agnostic_chromosome_gain(chromosomes, epoch, chrom_count, create_new_chromosome)

    return chrom_count, simulated_chromosomes
