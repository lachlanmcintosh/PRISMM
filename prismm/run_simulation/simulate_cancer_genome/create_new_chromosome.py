import copy
from typing import Dict, Any

def create_new_chromosome(
    old_chromosome: Dict[str, Any], 
    chrom_count: int, 
    epoch: int
) -> Dict[str, Any]:
    """
    Create a new chromosome by deep copying an old chromosome and updating
    its unique identifier, epoch created, and parent details.

    Args:
        old_chromosome (Dict[str, Any]): The chromosome to be copied.
        chrom_count (int): The current chromosome count.
        epoch (int): The current epoch.

    Returns:
        new_chromosome (Dict[str, Any]): The newly created chromosome.

    Raises:
        AssertionError: If the input types do not match the expected types.
    """
    assert isinstance(old_chromosome, dict), "old_chromosome must be of type dict"
    assert isinstance(chrom_count, int), "chrom_count must be of type int"
    assert isinstance(epoch, int), "epoch must be of type int"

    # Deep copy the old chromosome to create the new chromosome
    new_chromosome = copy.deepcopy(old_chromosome)

    # Update the unique identifier, epoch created, and parent details
    new_chromosome.update({
        "unique_identifier": chrom_count,
        "epoch_created": epoch,
        "parent": old_chromosome.get("unique_identifier")
    })

    new_chromosome["sibling"] = old_chromosome["unique_identifier"]
    old_chromosome["sibling"] = new_chromosome["unique_identifier"]

    return new_chromosome
