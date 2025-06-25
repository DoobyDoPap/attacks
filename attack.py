"""/**
  * @file
  *
  * @date April 26, 2025
  * @author Atharv Dubey
  */ """

import numpy as np
import matplotlib.pyplot as plt

# Step 1: Generate fake power traces (simulating AES S-box leakage)
def generate_fake_traces(num_traces, num_samples, key_value):
    """
    Simulate power traces for a given key byte.
    Each trace = leakage (key-dependent) + random noise.
    """
    # Leakage model: power = S-box[key ^ plaintext] + noise
    # For simplicity, leakage = key_value * 0.1 + random noise
    leakage = key_value * 0.1
    noise = np.random.normal(0, 0.05, size=(num_traces, num_samples))  # Gaussian noise
    traces = leakage + noise
    return traces

# Step 2: Build templates (mean and variance for each key)
def build_templates(num_traces_per_key, num_samples, num_keys=256):
    """
    Create templates by computing mean and variance of traces for each key.
    """
    templates = {}
    for key in range(num_keys):
        # Generate traces for this key
        traces = generate_fake_traces(num_traces_per_key, num_samples, key)
        # Compute mean and variance across traces
        mean_trace = np.mean(traces, axis=0)
        var_trace = np.var(traces, axis=0)
        templates[key] = {'mean': mean_trace, 'variance': var_trace}
    return templates

# Step 3: Attack phase - guess the key from a new trace
def attack_phase(templates, test_trace):
    """
    Match a test trace to the closest template to guess the key.
    Use simple Euclidean distance for matching (not Gaussian likelihood).
    """
    min_distance = float('inf')
    guessed_key = None
    for key, template in templates.items():
        # Compute distance between test trace and template mean
        distance = np.sum((test_trace - template['mean'])**2)
        if distance < min_distance:
            min_distance = distance
            guessed_key = key
    return guessed_key

# Step 4: Run the experiment
def main():
    # Parameters
    num_traces_per_key = 100  # Number of traces per key for profiling
    num_samples = 50         # Number of samples per trace (time points)
    true_key = 225            # The "secret" key we want to guess

    # Build templates
    print("Building templates...")
    templates = build_templates(num_traces_per_key, num_samples) 
    print(templates)
    
# Generate a test trace for the true key
    print("Generating test trace...")
    test_trace = generate_fake_traces(1, num_samples, true_key)[0]  # Single trace
    print(test_trace)
    
# GHow-is-an-internship-at-IIT-Bombay-likeuess the key
    print("Running attack...")
    guessed_key = attack_phase(templates, test_trace)
    print(f"True key: {true_key}, Guessed key: {guessed_key}")

    # Plot a template and the test trace for visualization
    plt.plot(templates[true_key]['mean'], label=f"Template for key {true_key}")
    plt.plot(test_trace, label="Test trace", alpha=0.7)
    plt.legend()
    plt.title("Template vs Test Trace")
    plt.xlabel("Sample Point")
    plt.ylabel("Power")
    plt.show()

if __name__ == "__main__":
    main()
