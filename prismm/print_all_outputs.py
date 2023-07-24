import os
import pickle
import glob
import math

# Initialising lists to store the results
results = []
total=0
# Use glob to find all matching file paths
for file_name in glob.glob('SIMULATIONS/simulation_*_smaller.pickle'):
    # Extract the number from the file name
    i = int(file_name.split('_')[1])
    

    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            print(f"Processing file: {file_name}")
            data = pickle.load(f)

            min_neg_loglik_correct = math.inf
            min_solution_correct = None

            min_neg_loglik_incorrect = math.inf
            min_solution_incorrect = None

            for solution in data["solutions"]:
                correct_path = solution["correct_path"]
                est_neg_loglik = solution["est_neg_loglik"]

                # If the path is correct and estimated negative log likelihood is less than
                # the current minimum, update the minimum and corresponding solution.
                if correct_path and est_neg_loglik < min_neg_loglik_correct:
                    min_neg_loglik_correct = est_neg_loglik
                    min_solution_correct = solution
                
                # If the path is not correct and estimated negative log likelihood is less than
                # the current minimum, update the minimum and corresponding solution.
                elif not correct_path and est_neg_loglik < min_neg_loglik_incorrect:
                    min_neg_loglik_incorrect = est_neg_loglik
                    min_solution_incorrect = solution
            
            # If a correct path solution is not found, print a message
            if min_solution_correct is None:
                total += 1
                print(f"No correct path solution found for file: {file_name}")
                print(f"{total} so far")
                continue

            # Build the correct path result
            result_correct = {
                "file": file_name,
                "i": i,
                "path_type": "correct",
                "correct_path": min_solution_correct["correct_path"],
                "est_neg_loglik": min_solution_correct["est_neg_loglik"],
                "pre": min_solution_correct["pre"],
                "mid": min_solution_correct["mid"],
                "post": min_solution_correct["post"],
                "p_up": min_solution_correct["p_up"],
                "p_down": min_solution_correct["p_down"]
            }

            # If there's an incorrect path solution, build its result
            if min_solution_incorrect is not None:
                result_incorrect = {
                    "file": file_name,
                    "i": i,
                    "path_type": "incorrect",
                    "correct_path": min_solution_incorrect["correct_path"],
                    "est_neg_loglik": min_solution_incorrect["est_neg_loglik"],
                    "pre": min_solution_incorrect["pre"],
                    "mid": min_solution_incorrect["mid"],
                    "post": min_solution_incorrect["post"],
                    "p_up": min_solution_incorrect["p_up"],
                    "p_down": min_solution_incorrect["p_down"]
                }
                results.append((result_correct, result_incorrect))
            else:
                results.append((result_correct, None))

# Pretty printing the results
for result_correct, result_incorrect in results:
    print("Correct path solution:")
    print(result_correct)
    if result_incorrect is not None:
        print("\nIncorrect path solution:")
        print(result_incorrect)
    else:
        print("\nNo incorrect path solution found.")
    print("\n" + "-"*50 + "\n")

