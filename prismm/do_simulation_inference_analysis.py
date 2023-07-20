import argparse
import prismm.script_args as script_args
from prismm.utils.set_logging import set_logging

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run all processing scripts with the given test case and optional parameters."
    )
    parser.add_argument(
        "--run",
        nargs='+',
        type=int,
        default=[1, 2, 3, 4],
        choices=[1, 2, 3, 4],
        help="Specify which scripts to run (1, 2, 3, or 4)"
    )

    # use the functions from script_args to add the arguments
    script_args.add_base_args(parser)
    script_args.add_simulation_args(parser)
    script_args.bp_search_args(parser)
    script_args.add_build_trees_args(parser)
    script_args.add_analyse_trees_args(parser)

    return parser.parse_args()

# Import the other scripts that are required to run the pipeline
from prismm.run_simulation.run_simulation import main as run_simulation
from prismm.run_summed_BP_search.run_summed_BP_search import main as run_summed_BP_search
from prismm.run_build_trees_and_timings.run_build_trees_and_timings import main as run_build_trees_and_timings
from prismm.run_analyse_trees.run_analyse_trees import main as run_analyse_trees

def main():
    args = parse_arguments()
    set_logging(args)

    if 1 in args.run:
        run_simulation(args)

    if 2 in args.run:
        run_summed_BP_search(args)

    if 3 in args.run:
        run_build_trees_and_timings(args)

    if 4 in args.run:
        run_analyse_trees(args)

if __name__ == "__main__":
    main()
