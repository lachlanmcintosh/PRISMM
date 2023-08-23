#!/bin/bash

# List of paths to submit jobs for
paths=("p10_v5" "p4_v5" "p6_v5" "p8_v5")

# Loop over each path and submit a job
for path in "${paths[@]}"; do
    sbatch --output=merge_and_split_${path}_%j.out --error=merge_and_split_${path}_%j.err merge_and_split_job.sh "$path"
done

