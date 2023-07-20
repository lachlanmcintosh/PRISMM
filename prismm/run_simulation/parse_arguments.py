import argparse
from prismm.script_args import add_base_args, add_simulation_args 
from argparse import Namespace

def parse_arguments() -> Namespace:
    """
    Parse command-line arguments used in the simulation process.
    """
    parser = argparse.ArgumentParser(
        description="Simulate a cancer genome and its phylogenetic trees."
    )

    # create the parser from prismm/script_args.py
    add_base_args(parser)
    add_simulation_args(parser)

    # read in the arguments
    args = parser.parse_args()
    assert isinstance(args, Namespace), "The parsed arguments should be of type 'Namespace'."

    return args


