import argparse
import logging
from argparse import Namespace
from prismm.script_args import add_base_args, add_simulation_args 

def parse_arguments() -> Namespace:
    """
    Parse command-line arguments used in the simulation process.
    
    This function initializes an ArgumentParser object, adds base and simulation-specific arguments,
    and then parses the command-line input. It returns the parsed arguments as an instance of Namespace.
    If the parsed arguments are not an instance of Namespace, an error is logged and the program is exited.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """

    # Initialize the parser with a description
    parser = argparse.ArgumentParser(
        description="Simulate a cancer genome and its phylogenetic trees."
    )

    # Add arguments to the parser from prismm/script_args.py
    add_base_args(parser)
    add_simulation_args(parser)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Validate the type of parsed arguments and log an error if they are not of type 'Namespace'
    if not isinstance(args, Namespace):
        logging.error("The parsed arguments should be of type 'Namespace'. Exiting the program.")
        exit(1)

    return args
