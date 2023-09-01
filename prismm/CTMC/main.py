from aneuploidy import aneuploidy
from genome_doubling import genome_doubling
from likelihood_calculation import neg_log_likelihood, compute_best_likelihoods
from simulate_data import generate_observations, compute_transition_matrix

def pretty_print_results(results):
    for key in results:
        if "params" in key:
            model_name = key.split("_")[0]
            print(f"{model_name} Model Parameters:")
            for param, value in results[key].items():
                print(f"{param}: {value:.2f}")
            print()
        else:
            print(f"{key}: {results[key]:.2f}")
            print()

def main():
    # Simulated observations
    time = 0.2
    true_params_0 = [1, 1, time]    # Model 0 (no GD)
    true_params_1 = [1, 1, time, time] # Model 1 (1GD)
    true_params_2 = [1, 1, time, time, time]  # Model 2 (2GD)

    start_state = 1  # Starting state for simulation
    num_observations = 10  # Number of observations to simulate
    dimension = 32

    # Generate simulated observations
    simulated_observations_0 = generate_observations(compute_transition_matrix(true_params_0, dimension, model=0), start_state, num_observations)
    simulated_observations_1 = generate_observations(compute_transition_matrix(true_params_1, dimension, model=1), start_state, num_observations)
    simulated_observations_2 = generate_observations(compute_transition_matrix(true_params_2, dimension, model=2), start_state, num_observations)

    print("Simulated Observations for model 0:")
    print(simulated_observations_0)
    print()

    print("Simulated Observations for model 1:")
    print(simulated_observations_1)
    print()

    print("Simulated Observations for model 2:")
    print(simulated_observations_2)
    print()

    # Recover parameters
    recovered_results_0 = compute_best_likelihoods(simulated_observations_0, dimension=dimension)
    recovered_results_1 = compute_best_likelihoods(simulated_observations_1, dimension=dimension)
    recovered_results_2 = compute_best_likelihoods(simulated_observations_2, dimension=dimension)

    print("#"*20)
    print("Results for model 0:")
    pretty_print_results(recovered_results_0)

    print("#"*20)
    print("Results for model 1:")
    pretty_print_results(recovered_results_1)

    print("#"*20)
    print("Results for model 2:")
    pretty_print_results(recovered_results_2)

if __name__ == "__main__":
    main()
