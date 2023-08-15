#!/usr/bin/bash

# Step 1: Creating the jobid list
squeue -h -u lmcintosh -o "%i" > jobids.txt

# Step 2: Running scancel in the background for each job ID
while read -r jobid; do
    scancel $jobid &

    # Limit the number of background processes to 100
    while [[ $(jobs -r -p | wc -l) -ge 100 ]]; do
        sleep 1  # Sleep for 1 second before checking again
    done
done < jobids.txt

wait  # Wait for all background processes to complete

# Optional: Provide feedback
echo "All jobs for user 'lmcintosh' have been canceled."


