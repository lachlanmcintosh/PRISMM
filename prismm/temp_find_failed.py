import os
import pickle
import glob
from pprint import pprint

# Initialising lists to store the results
results = []

# Use glob to find all matching file paths
for file_name in glob.glob('SIMULATIONS/simulation_*_smaller.pickle'):
    # Extract the number from the file name
    i = int(file_name.split('_')[1])

    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            print("in")
            data = pickle.load(f)
            for solution in data["solutions"]:
                correct_path = solution["correct_path"]
                est_neg_loglik = solution["est_neg_loglik"]
                if est_neg_loglik == float('inf') and correct_path:
                    pre = solution["pre"]
                    mid = solution["mid"]
                    post = solution["post"]
                    p_up = solution["p_up"]
                    p_down = solution["p_down"]

                    result = {
                        "i": i,
                        "correct_path": correct_path,
                        "est_neg_loglik": est_neg_loglik,
                        "pre": pre,
                        "mid": mid,
                        "post": post,
                        "p_up": p_up,
                        "p_down": p_down
                    }

                    results.append(result)

# Pretty printing the results
for result in results:
    pprint(result)
    print("\n" + "-"*50 + "\n")

