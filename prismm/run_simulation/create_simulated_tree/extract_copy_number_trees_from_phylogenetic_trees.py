from typing import Dict, List, Tuple

from prismm.utils.make_left_heavy import make_left_heavy

def extract_copy_number_tree_from_phylogenetic_tree(phylogenetic_tree: Dict) -> List:
    """
    Extract a list representation of the copy number tree from the phylogenetic tree.

    :param phylo_tree: The input phylogenetic dict tree.
    :return: The resultant CN list tree.
    """
    CN_tree = [phylogenetic_tree.get("copy_number", 0)]
    
    for branch in ["child", "complement"]:
        if branch_tree := phylogenetic_tree.get(branch):
            CN_tree.append(extract_copy_number_tree_from_phylogenetic_tree(branch_tree))

    return CN_tree

def extract_copy_number_trees_from_phylogenetic_trees(phylogenetic_trees: Dict[str, Dict]) -> Dict[str, List]:
    """
    Convert phylogenetic_tree to copy number (CN) trees and make the trees left-heavy.

    :param phylo_trees: The input truth trees.
    :return: The resultant CN trees.
    """
    copy_number_trees = {}
    for chrom_type, tree in phylogenetic_trees.items(): # TODO, use keys here rather than .items
        copy_number_tree = extract_copy_number_tree_from_phylogenetic_tree(tree)
        copy_number_trees[chrom_type] = make_left_heavy(copy_number_tree)
        
    return copy_number_trees
