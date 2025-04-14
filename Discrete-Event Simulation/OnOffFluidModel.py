import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def simBuffer(lam, mu, r1, r2, K, runLength, seed=None, trace=False):
    """
    Simulate the buffer system with two machines and return the average production rate.

    Parameters:
    - lam: failure rate of Machine 1 (1 / mean uptime)
    - mu: repair rate of Machine 1 (1 / mean downtime)
    - r1: production rate of Machine 1
    - r2: consumption rate of Machine 2
    - K: buffer size
    - runLength: total simulation time
    - seed: random seed for reproducibility
    - trace: if True, returns trace of buffer content

    Returns:
    - average production rate
    - (optional) buffer content time series (if trace=True)
    """
    if seed is not None:
        np.random.seed(seed)

    t = 0.0         # current time
    b = 0.0         # buffer content
    empty = 0.0     # total time buffer was empty

    upDist = stats.expon(scale=1 / lam)
    downDist = stats.expon(scale=1 / mu)

    time_trace = []
    buffer_trace = []

    while t < runLength:
        # Machine 1 is up
        u = upDist.rvs()
        u = min(u, runLength - t)  # don’t exceed total time
        t += u
        b = min(b + u * (r1 - r2), K)

        if trace:
            time_trace.append(t)
            buffer_trace.append(b)

        # Machine 1 goes down
        d = downDist.rvs()
        d = min(d, runLength - t)
        t += d
        b -= d * r2

        if b < 0:
            empty -= b / r2  # record how long Machine 2 was idle
            b = 0

        if trace:
            time_trace.append(t)
            buffer_trace.append(b)

    avg_rate = r2 * (1 - empty / t)
    if trace:
        return avg_rate, time_trace, buffer_trace
    return avg_rate

# Example usage:
if __name__ == "__main__":
    # Parameters
    lam = 1.0     # mean uptime = 1
    mu = 1.0      # mean downtime = 1
    r1 = 5.0      # production rate of machine 1
    r2 = 2.0      # consumption rate of machine 2
    K = 4.0       # buffer capacity
    runLength = 200.0  # total simulation time

    # Run simulation
    avg_rate, times, buffer = simBuffer(lam, mu, r1, r2, K, runLength, seed=42, trace=True)

    # Print result
    print(f"Estimated average production rate: {avg_rate:.3f}")

    # Plot buffer content over time
    plt.figure(figsize=(10, 5))
    plt.step(times, buffer, where='post')
    plt.xlabel("Time")
    plt.ylabel("Buffer content")
    plt.title("Buffer Content Over Time")
    plt.grid(True)
    plt.show()
