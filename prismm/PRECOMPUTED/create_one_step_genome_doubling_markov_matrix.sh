#!/bin/bash
#SBATCH --job-name=genome_doubling_matrix
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00  # Adjust as needed
#SBATCH --output=logs/genome_doubling_matrix-%j.out
#SBATCH --error=logs/genome_doubling_matrix-%j.err

sage create_one_step_genome_doubling_markov_matrix.sage "$1"  # Assuming max_CN is passed as an argument

