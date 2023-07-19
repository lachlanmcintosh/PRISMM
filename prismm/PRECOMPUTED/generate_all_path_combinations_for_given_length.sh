#!/usr/bin/bash
#SBATCH --job-name=generate_all_paths
#SBATCH --ntasks=1
#SBATCH --mem=20G
#SBATCH --output=generate_all_paths-%j.out
#SBATCH --error=generate_all_paths-%j.err

# $1 refers to the first argument passed to the script
sage generate_all_path_combinations_for_given_length.sage "$1"

