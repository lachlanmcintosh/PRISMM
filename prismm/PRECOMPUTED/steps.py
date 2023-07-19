import subprocess
import time
import os

def run_cmd_with_sbatch(cmd: str, job_name: str) -> str:
    """Run a command using sbatch and return the job ID."""
    print(f"\nSubmitting job '{job_name}' with command '{cmd}'")
    result = subprocess.run(["sbatch", "--parsable", "--wrap", cmd], capture_output=True, text=True)
    job_id = result.stdout.strip()  # job ID is the output of the sbatch command
    print(f"Job '{job_name}' submitted successfully with job ID: {job_id}")
    return job_id

def get_job_id_from_file(filename: str):
    with open(filename, 'r') as f:
        job_id = f.read().strip()
    return job_id

def wait_for_job(job_id: str, job_name: str):
    """Wait for the job with the given ID to finish."""
    print(f"Waiting for job '{job_name}' with job ID: {job_id} to finish...")
    while True:
        result = subprocess.run(["squeue", "-j", job_id], capture_output=True, text=True)
        if job_id not in result.stdout:
            print(f"Job '{job_name}' with job ID: {job_id} has finished.")
            break  # job has finished
        time.sleep(10)  # wait before checking again

def generate_all_path_combinations():
    cmd = "./generate_all_path_combinations_for_given_length.sh {}".format(max_path_length)
    job_id = run_cmd_with_sbatch(cmd, "generate_all_path_combinations")
    wait_for_job(job_id, "generate_all_path_combinations")

def create_one_step_anueploidy_markov_matrix():
    cmd = "./create_one_step_anueploidy_markov_matrix.sh {}".format(max_path_length)
    job_id = run_cmd_with_sbatch(cmd, "create_one_step_anueploidy_markov_matrix")
    wait_for_job(job_id, "create_one_step_anueploidy_markov_matrix")

def create_one_step_genome_doubling_markov_matrix():
    cmd = "./create_one_step_genome_doubling_markov_matrix.sh {}".format(max_path_length)
    job_id = run_cmd_with_sbatch(cmd, "create_one_step_genome_doubling_markov_matrix")
    wait_for_job(job_id, "create_one_step_genome_doubling_markov_matrix")

def generate_path_likelihoods(p_up, p_down):
    cmd = "./generate_path_likelihoods.sh {} {} {} {} {}".format(p_up, p_down, max_CN, max_path_length, path_description)
    job_name = f"generate_path_likelihoods_{p_up}_{p_down}"
    job_id = run_cmd_with_sbatch(cmd, job_name)
    return job_id  # return job_id instead of waiting here

if __name__ == "__main__":
    max_path_length = 8
    max_jobs = 400
    max_CN = 2 ** max_path_length
    path_description = "p{}_v4".format(max_path_length)

    generate_all_path_combinations()
    create_one_step_anueploidy_markov_matrix()
    create_one_step_genome_doubling_markov_matrix()

    job_ids = []  # list to collect job IDs
    for rep in range(1):
        for p_up in range(101):
            for p_down in range(101):
                if p_up + p_down < 101:
                    FILE = "MATRICES/subbed_u{}_d{}_{}.csv".format(p_up, p_down, path_description)
                    if not os.path.exists(FILE):
                        job_id = generate_path_likelihoods(p_up, p_down)
                        job_ids.append(job_id)  # add job_id to the list

    # Wait for all jobs to finish
    for job_id in job_ids:
        wait_for_job(job_id, f"generate_path_likelihoods_{p_up}_{p_down}")

    # Check if all files exist
    os.system("python check_all_files_exist.py")
