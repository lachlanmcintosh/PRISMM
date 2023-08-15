import subprocess
import time
import os

def run_cmd_with_sbatch(cmd_list, job_name: str) -> str:
    print(f"\nSubmitting job '{job_name}' with command '{' '.join(cmd_list)}'")
    result = subprocess.run(["sbatch", "--parsable", "--wrap"] + cmd_list, capture_output=True, text=True)
    job_id = result.stdout.strip()
    print(f"Job '{job_name}' submitted successfully with job ID: {job_id}")
    return job_id

def wait_for_job(job_id: str, job_name: str):
    print(f"Waiting for job '{job_name}' with job ID: {job_id} to finish...")
    while True:
        result = subprocess.run(["squeue", "-j", job_id], capture_output=True, text=True)
        if job_id not in result.stdout:
            print(f"Job '{job_name}' with job ID: {job_id} has finished.")
            break
        time.sleep(10)

def generate_all_path_combinations(max_path_length):
    cmd_list = ["./generate_all_path_combinations_for_given_length.sh", str(max_path_length)]
    job_id = run_cmd_with_sbatch(cmd_list, "generate_all_path_combinations")
    wait_for_job(job_id, "generate_all_path_combinations")

def create_one_step_anueploidy_markov_matrix(max_CN):
    cmd_list = ["./create_one_step_anueploidy_markov_matrix.sh", str(max_CN)]
    job_id = run_cmd_with_sbatch(cmd_list, "create_one_step_anueploidy_markov_matrix")
    wait_for_job(job_id, "create_one_step_anueploidy_markov_matrix")

def create_one_step_genome_doubling_markov_matrix(max_CN):
    cmd_list = ["./create_one_step_genome_doubling_markov_matrix.sh", str(max_CN)]
    job_id = run_cmd_with_sbatch(cmd_list, "create_one_step_genome_doubling_markov_matrix")
    wait_for_job(job_id, "create_one_step_genome_doubling_markov_matrix")

def generate_path_likelihoods(p_up, p_down, max_CN, max_path_length, path_description):
    cmd_list = ["./generate_path_likelihoods.sh", str(p_up), str(p_down), str(max_CN), str(max_path_length), path_description]
    job_name = f"generate_path_likelihoods_{p_up}_{p_down}"
    job_id = run_cmd_with_sbatch(cmd_list, job_name)
    return job_id

import sys


if __name__ == "__main__":
    max_path_length = 8
    max_CN = 2 ** max_path_length
    path_description = f"p{max_path_length}_v4"

    generate_all_path_combinations(max_path_length)
    sys.exit()
    create_one_step_anueploidy_markov_matrix(max_path_length)
    create_one_step_genome_doubling_markov_matrix(max_path_length)

    job_ids = []
    for rep in range(1):
        for p_up in range(101):
            for p_down in range(101):
                if p_up + p_down < 101:
                    FILE = f"MATRICES/subbed_u{p_up}_d{p_down}_{path_description}.csv"
                    if not os.path.exists(FILE):
                        job_id = generate_path_likelihoods(p_up, p_down, max_CN, max_path_length, path_description)
                        job_ids.append(job_id)

    for job_id in job_ids:
        wait_for_job(job_id, f"generate_path_likelihoods_{p_up}_{p_down}")

    os.system("python check_all_files_exist.py")

