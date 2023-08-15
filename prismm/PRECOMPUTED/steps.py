#!/stornext/Home/data/allstaff/l/lmcintosh/mambaforge/envs/sage/bin/python

import subprocess
import time
import os
import sys
import math

def write_sbatch_script(cmd, detailed_job_name, max_path_length):
    """Create an sbatch script file and return its name."""
    slurm_dir = "slurm"
    os.makedirs(slurm_dir, exist_ok=True)  # make sure the directory exists
    mem_in_gb = math.ceil(2 ** (max_path_length - 6) * 1)
    print(mem_in_gb)

    script_content = (
        f"#!/bin/bash\n"
        f"#SBATCH --job-name={detailed_job_name}\n"
        f"#SBATCH --output=slurm/{detailed_job_name}.out\n"
        f"#SBATCH --error=slurm/{detailed_job_name}.err\n"
        f"#SBATCH --mem={mem_in_gb}GB\n"
        f"#SBATCH --requeue\n"
        f"\n"
        f"cd {os.path.abspath(os.getcwd())}\n"
        f"{cmd}\n"
    )
    script_filename = os.path.join(slurm_dir, f"{detailed_job_name}.sbatch")
    with open(script_filename, 'w') as script_file:
        script_file.write(script_content)

    return script_filename

def run_cmd_with_sbatch(cmd, detailed_job_name, max_path_length):
    """Run a command using sbatch and return the job ID."""
    sbatch_script = write_sbatch_script(cmd, detailed_job_name, max_path_length)  # <-- Pass the max_path_length
    print(f"\nSubmitting job with script '{sbatch_script}'")
    result = subprocess.run(["sbatch", "--parsable", sbatch_script], capture_output=True, text=True)
    job_id = result.stdout.strip()
    print(f"Job submitted successfully with job ID: {job_id}")
    return job_id

def run_cmd_with_sbatch(cmd, detailed_job_name, max_path_length):
    """Run a command using sbatch and return the job ID."""
    sbatch_script = write_sbatch_script(cmd, detailed_job_name, max_path_length)  # <-- Pass the max_path_length
    print(f"\nSubmitting job with script '{sbatch_script}'")
    result = subprocess.run(["sbatch", "--parsable", sbatch_script], capture_output=True, text=True)
    if result.returncode != 0:  # check if the sbatch command failed
        print(f"Error submitting job with script '{sbatch_script}'. Error: {result.stderr}")
        return None
    job_id = result.stdout.strip()
    print(f"The result is {result}")

    print(f"Job submitted successfully with job ID: {job_id}")
    return job_id



def generate_path_likelihoods(p_up, p_down, max_CN, max_path_length, path_description):
    cmd = f"./generate_path_likelihoods.sh {p_up} {p_down} {max_CN} {max_path_length} {path_description}"
    print(cmd)
    detailed_job_name = f"generate_path_likelihoods_{p_up:.2f}_{p_down:.2f}_{max_CN}_{path_description}"
    job_id = run_cmd_with_sbatch(cmd, detailed_job_name, max_path_length)  # <-- Pass the max_path_length
    return job_id

def wait_for_job(job_id: str, job_name: str):
    """Poll the status of a job until it completes."""
    while True:
        # Check the job's status using squeue
        result = subprocess.run(["squeue", "-j", job_id], capture_output=True, text=True)
        
        # If the job isn't listed, it has finished
        if job_id not in result.stdout:
            print(f"Job {job_name} ({job_id}) has completed.")
            break
        
        # Sleep for a short duration before checking again
        time.sleep(10) # 10 seconds, adjust as needed

def get_running_jobs_count() -> int:
    """Return the number of currently running jobs for the user."""
    result = subprocess.run(["squeue", "-u", "lmcintosh", "-h", "-o", "%i"], capture_output=True, text=True)
    job_ids = result.stdout.split()
    return len(job_ids)

from sage.all import load  # Import the Sage's load function
import glob

def count_lines_in_file(filename):
    if filename.endswith(".sobj"):
        data = load(filename)
        return len(data)

def count_lines_in_table(filename):
    with open(filename, 'r') as f:
        return sum(1 for line in f)

import sys
if __name__ == "__main__":

    max_path_length = int(sys.argv[1])
    max_jobs = 500
    max_CN = 2 ** max_path_length
    path_description = f"p{max_path_length}_v5"

    # Run the preliminary functions
    path_description = f"p{max_path_length}_v5"

    all_path_combinations_file = os.path.join("MATRICES", path_description, "all_path_combinations.sobj")
    gd_file = os.path.join("MATRICES", path_description, "GD.sobj")

    # Check if files exist and, if not, run the respective jobs
    if not os.path.exists(all_path_combinations_file):
        job_id1 = run_cmd_with_sbatch(f"./generate_all_path_combinations_for_given_length.sh {max_path_length}",
                                      f"generate_all_path_combinations_{max_path_length}", max_path_length)
        wait_for_job(job_id1, f"generate_all_path_combinations_{max_path_length}")

    if not os.path.exists(gd_file):
        job_id3 = run_cmd_with_sbatch(f"./create_one_step_genome_doubling_markov_matrix.sh {max_path_length}",
                                      f"create_one_step_genome_doubling_markov_matrix_{max_path_length}", max_path_length)
        wait_for_job(job_id3, f"create_one_step_genome_doubling_markov_matrix_{max_path_length}")


    job_ids = []  # list to collect job IDs
    submission_counter = 0  # Counter to keep track of submissions since the last check

    path_description = f"p{max_path_length}_v5"
    expected_line_count = count_lines_in_file(f"MATRICES/{path_description}/all_path_combinations.sobj") + 1

    for rep in range(1):
        for p_up in range(101):
            for p_down in range(101):
                if p_up + p_down <= 100:  # Fixed the condition to ensure it doesn't exceed 100%
                    p_up_rounded = round(p_up / 100.0, 2)
                    p_down_rounded = round(p_down / 100.0, 2)


                    table_file = f"MATRICES/{path_description}/table_u{p_up_rounded:.2f}_d{p_down_rounded:.2f}.csv"
                    file_prefix_to_delete = f"subbed_mat_u{p_up_rounded:.2f}_d{p_down_rounded:.2f}"


                    # Check if the table file exists and count its lines
                    if os.path.exists(table_file):
                        table_line_count = count_lines_in_table(table_file)
                        print(f"Table Filename: {table_file}, Line Count: {table_line_count}")

                        if table_line_count == expected_line_count:
                            continue  # Skip this iteration if the counts match
                    else:
                        print(f"Table file {table_file} does not exist.")

                    # If the execution reaches here, it means there's a mismatch. Delete relevant files and resubmit the job.
                    files_to_delete = [f for f in glob.glob(f"MATRICES/{path_description}/{file_prefix_to_delete}*")]

                    for file in files_to_delete:
                        print(f"Deleting file: {file}")
                        os.remove(file)


                    job_id = generate_path_likelihoods(p_up_rounded, p_down_rounded, max_CN, max_path_length, path_description)
                    job_ids.append((job_id, p_up_rounded, p_down_rounded))
                    submission_counter += 1

                    # Check the running jobs count every 50 submissions
                    if submission_counter == 50:
                        # If there are 500 jobs running, pause and wait until there's room
                        while get_running_jobs_count() >= max_jobs:
                            print(f"At least {max_jobs} jobs are currently running. Waiting for room to submit more...")
                            time.sleep(60)  # Wait for 1 minute before checking again
                        submission_counter = 0  # Reset the counter after the check

    # Wait for the remaining jobs to finish after all jobs have been submitted
    for job_id, p_up, p_down in job_ids:
        wait_for_job(job_id, f"generate_path_likelihoods_{p_up}_{p_down}")
