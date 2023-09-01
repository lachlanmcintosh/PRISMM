#!/bin/bash

# Initialize an empty array
declare -a paths=()

# Populate the array with values from p4_v5 to p10_v5
for i in {4..10}; do
    paths+=("p${i}_v5")
done

# Loop over each path and submit a job
for path in "${paths[@]}"; do
    sbatch --output=merge_and_split_${path}_%j.out --error=merge_and_split_${path}_%j.err merge_and_split_job.sh "$path"
done

