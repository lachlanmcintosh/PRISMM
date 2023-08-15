#!/usr/bin/bash
#SBATCH --job-name=steps_job
#SBATCH --ntasks=1
#SBATCH --mem=100G
#SBATCH --time=312:00:00
#SBATCH --partition=long
#SBATCH --output=steps-%j.out
#SBATCH --error=steps-%j.err

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <max_path_length>"
    exit 1
fi

# Activate sage before running this!

python steps.py $1
