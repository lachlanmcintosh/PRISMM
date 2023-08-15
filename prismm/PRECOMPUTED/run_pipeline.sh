# to run the pipeline just write

# sbatch steps.sh path_length where path length is an integer

sbatch steps.sh 5
sbatch steps.sh 8
sbatch steps.sh 10

# next we need to do a check to see if all the files exist
# then we need to check that collated files are all of the right length (if not delete and do again)
# it might need to be rerun several times to make sure that all files exist in the end as they can be preempted. 
# you can check that all the files exist with 
# python check_all_files_exists.py
