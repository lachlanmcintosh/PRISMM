#!/bin/bash
#SBATCH --job-name=path_likelihoods
#SBATCH --ntasks=1
#SBATCH --mem=40G
#SBATCH --qos=bonus
#SBATCH --output=path_likelihoods-%j.out
#SBATCH --error=path_likelihoods-%j.err

sage generate_path_likelihoods.sage ${1} ${2} ${3} ${4} ${5}

