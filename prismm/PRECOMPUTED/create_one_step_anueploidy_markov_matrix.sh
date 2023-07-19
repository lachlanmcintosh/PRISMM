#!/bin/bash
#SBATCH --output=anueploidy_matrix-%j.out
#SBATCH --error=anueploidy_matrix-%j.err
#SBATCH --job-name=anueploidy_matrix
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --requeue

# $1 refers to the first argument passed to the script
sage create_one_step_anueploidy_markov_matrix.sage "$1"

