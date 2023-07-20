import numpy as np
import matplotlib
matplotlib.use("Agg")  # Use the Agg backend to generate plot files
import matplotlib.pyplot as plt

def simulate_epochs(num_epochs, rate_lambda):
    # Generate exponentially distributed epoch lengths
    epoch_lengths = np.random.exponential(1/rate_lambda, num_epochs)

    events_per_epoch = []

    # For each epoch
    for epoch_length in epoch_lengths:
        # Generate Poisson distributed event count with rate=epoch length
        events = np.random.poisson(epoch_length)
        events_per_epoch.append(events)
    
    return epoch_lengths, events_per_epoch

def estimate_lambda_and_times(events_per_epoch):
    # Calculate total number of events and epochs
    total_events = sum(events_per_epoch)
    total_epochs = len(events_per_epoch)

    # Maximum likelihood estimate for λ is the sample mean
    lambda_estimate = total_events / total_epochs

    # Estimate time spent in each epoch as number of events divided by λ
    time_estimates = [events / lambda_estimate for events in events_per_epoch]

    # Return the estimates
    return lambda_estimate, time_estimates

def normalize(data):
    return data / np.sum(data)

def plot_cumulative_time(epoch_lengths, estimated_times):
    # Normalize the times
    epoch_lengths_norm = normalize(np.cumsum(epoch_lengths))
    estimated_times_norm = normalize(np.cumsum(estimated_times))

    # Plot the normalized cumulative times
    plt.plot(epoch_lengths_norm, label="Actual time")
    plt.plot(estimated_times_norm, label="Estimated time")
    plt.legend()
    plt.xlabel("Epoch")
    plt.ylabel("Normalized cumulative time")
    plt.savefig("cumulative_time.png")  # Save the plot as an image file

def summarize_epochs_and_estimates(epoch_lengths, events_per_epoch):
    # Calculate the total number of epochs and total event count
    total_epochs = len(epoch_lengths)
    total_events = sum(events_per_epoch)

    # Calculate total time spent
    total_time = sum(epoch_lengths)

    # Estimate λ and time spent in each epoch
    lambda_estimate, time_estimates = estimate_lambda_and_times(events_per_epoch)

    # Print the summary
    print(f"Total number of epochs: {total_epochs}")
    print(f"Total number of events: {total_events}")
    print(f"Total time spent: {total_time:.2f}")
    print(f"Estimated λ: {lambda_estimate:.2f}")

    # Print the number of events, time spent, and estimated time spent in each epoch
    for i in range(total_epochs):
        print(f"Epoch {i+1}: number of events = {events_per_epoch[i]}, time spent = {epoch_lengths[i]:.2f}, estimated time spent = {time_estimates[i]:.2f}")

    # Plot the normalized cumulative time spent and estimated time spent
    plot_cumulative_time(epoch_lengths, time_estimates)

num_epochs = 10
rate_lambda = 0.01

epoch_lengths, events_per_epoch = simulate_epochs(num_epochs, rate_lambda)
summarize_epochs_and_estimates(epoch_lengths, events_per_epoch)
