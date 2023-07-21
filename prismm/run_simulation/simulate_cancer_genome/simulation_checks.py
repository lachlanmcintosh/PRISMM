import logging
from typing import Dict, List, Any, Union

# Set up logging
logging.basicConfig(level=logging.DEBUG)


def count_paternity(chromosomes: List[Dict[str, Any]], paternal: Union[str, bool]) -> int:
    """
    Count the number of chromosomes of a particular chromosome type with a specific paternal type that are not marked as dead.

    Parameters:
        chromosomes: A list of dictionaries representing chromosomes.
        paternal: A string or boolean value representing the paternal type.

    Returns:
        The count of chromosomes with the specified paternal type that are not marked as dead.
    """
    for chrom in chromosomes:
        if "paternal" not in chrom:
            raise ValueError("Chromosome is missing 'paternal' key")
        if "dead" not in chrom:
            raise ValueError("Chromosome is missing 'dead' key")

    return sum(1 for chrom in chromosomes if chrom["paternal"] == paternal and not chrom["dead"])


def check_all_chrs_are_unique(simulated_chromosomes: Dict[str, List[Dict[str, str]]]) -> bool:
    """
    Check if all chromosomes in the simulated_chromosomes dictionary have unique identifiers.

    Parameters:
        simulated_chromosomes: A dictionary where the values are lists of dictionaries representing chromosomes.

    Returns:
        True if all chromosomes have unique identifiers, raises ValueError otherwise.
    """
    ids = []
    for chrom_type in simulated_chromosomes.values():
        for chrom in chrom_type:
            if "unique_identifier" not in chrom:
                raise KeyError(f"The key 'unique_identifier' does not exist in {chrom}")
            ids.append(chrom["unique_identifier"])

    unique_ids = set(ids)
    if len(ids) != len(unique_ids):
        failed_ids = [id_ for id_ in ids if ids.count(id_) > 1]
        raise ValueError(f"Non-unique identifiers found: {failed_ids}")

    return True


def check_expected_keys_in_simulated_chromosomes_present(simulated_chromosomes: Dict[str, List[Dict[str, str]]]) -> bool:
    """
    Check if all keys that are expected to be present in simulated chromosomes are actually present.

    Parameters:
        simulated_chromosomes: A dictionary where the values are lists of dictionaries representing chromosomes.

    Returns:
        True if all expected keys are present in each chromosome, False otherwise.
    """
    expected_keys = {"SNVs", "paternal", "epoch_created", "parent", "unique_identifier", "dead", "sibling"}

    for chrom_type in simulated_chromosomes.values():
        for chrom in chrom_type:
            if not expected_keys.issubset(chrom.keys()):
                return False

    return True


def check_simulated_chromosomes(
    simulated_chromosomes: Dict[str, List[Dict[str, Any]]], 
    pre: int, 
    mid: int, 
    post: int, 
    ev_sequence: List[str]
) -> None:
    """
    Conduct several checks on the simulated chromosomes.

    Parameters:
        simulated_chromosomes: A dictionary where the values are lists of dictionaries representing chromosomes.
        pre: An integer representing the pre value.
        mid: An integer representing the mid value.
        post: An integer representing the post value.
        ev_sequence: A list of strings representing the ev sequence.

    Returns:
        None. Raises an error if any check fails.
    """
    assert pre + mid + post + 2 == len(ev_sequence), "Inconsistent input lengths"
    # some quick final sanity checks:
    if post == 0 or (mid == 0 and post == -1):
        assert ev_sequence[-1] == "G", "Expected 'G' at the end of ev sequence"
        # if a genome doubling round just occurred then the copy number of every chromosome will be even:
        for chrom_type in simulated_chromosomes:
            paternity_count = count_paternity(simulated_chromosomes[chrom_type], paternal=True)
            assert paternity_count % 2 == 0, f"Chromosomes: {simulated_chromosomes[chrom_type]}, Paternity count: {paternity_count}"

            paternity_count = count_paternity(simulated_chromosomes[chrom_type], paternal=False)
            assert paternity_count % 2 == 0, f"Chromosomes: {simulated_chromosomes[chrom_type]}, Paternity count: {paternity_count}"

    for chrom_type in simulated_chromosomes:
        assert len(simulated_chromosomes[chrom_type]) != 0, f"No chromosomes of type {chrom_type}"

    # some basic checks about the simulated chromosomes:
    try:
        assert check_all_chrs_are_unique(simulated_chromosomes), "Chromosomes are not unique"
        assert check_expected_keys_in_simulated_chromosomes_present(simulated_chromosomes), "Expected keys are missing in chromosomes"
    except AssertionError as error:
        logging.error(error)
