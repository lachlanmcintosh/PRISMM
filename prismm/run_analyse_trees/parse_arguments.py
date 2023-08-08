import argparse
from prismm.script_args import add_base_args, add_analyse_trees_args

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run all processing scripts with the given test case and optional parameters."
    )

    # add the relevant arguments from clonal_trees/script_args.py
    add_base_args(parser)
    add_analyse_trees_args(parser)    

    return parser.parse_args()