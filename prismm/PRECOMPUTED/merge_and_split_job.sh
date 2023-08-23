#!/bin/bash
#SBATCH --job-name=merge_and_split
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=25G  # Request 25GB of memory

# Path description from command line argument
path_description=$1

# Execute the Python script with the path description
python merge_and_split.py $path_description

