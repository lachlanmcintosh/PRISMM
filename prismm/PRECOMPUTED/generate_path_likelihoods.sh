#!/bin/bash
#SBATCH --job-name=path_likelihoods
#SBATCH --ntasks=1
#SBATCH --mem=40G
#SBATCH --qos=bonus
#SBATCH --output=logs/path_likelihoods-%j.out
#SBATCH --error=logs/path_likelihoods-%j.err

sage generate_path_likelihoods_functional.sage ${1} ${2} ${3} ${4} ${5}
