import numpy as np
import matplotlib.pyplot as plt

def simulate_brownian_motion_1d(T=1.0, M=1000):
    """
    Simulates a 1D standard Brownian motion B(t) for t in [0, T] using M steps.
    Returns:
        times: array of shape (M+1,)
        B:     array of shape (M+1,)
    """
    dt = T / M
    times = np.linspace(0, T, M + 1)
    increments = np.random.normal(loc=0.0, scale=np.sqrt(dt), size=M)
    B = np.zeros(M + 1)
    B[1:] = np.cumsum(increments)
    return times, B

def simulate_brownian_motion_2d(T=1.0, M=1000):
    """
    Simulates a 2D standard Brownian motion (X(t), Y(t)) for t in [0, T].
    Returns:
        times: array of shape (M+1,)
        X:     array of shape (M+1,)
        Y:     array of shape (M+1,)
    """
    dt = T / M
    times = np.linspace(0, T, M + 1)
    increments_x = np.random.normal(0.0, np.sqrt(dt), size=M)
    increments_y = np.random.normal(0.0, np.sqrt(dt), size=M)
    X = np.zeros(M + 1)
    Y = np.zeros(M + 1)
    X[1:] = np.cumsum(increments_x)
    Y[1:] = np.cumsum(increments_y)
    return times, X, Y

def plot_brownian_motion_1d(times, B):
    plt.figure()
    plt.plot(times, B, label="B(t)")
    plt.title("1D Standard Brownian Motion")
    plt.xlabel("Time t")
    plt.ylabel("B(t)")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_brownian_motion_2d(X, Y):
    plt.figure()
    plt.plot(X, Y, label="(X(t), Y(t)) path")
    plt.title("2D Standard Brownian Motion")
    plt.xlabel("X(t)")
    plt.ylabel("Y(t)")
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    T = 8.0    # Total time
    M = 1000   # Number of steps

    # Simulate and plot 1D Brownian motion
    times_1d, B = simulate_brownian_motion_1d(T, M)
    plot_brownian_motion_1d(times_1d, B)

    # Simulate and plot 2D Brownian motion
    times_2d, X, Y = simulate_brownian_motion_2d(T, M)
    plot_brownian_motion_2d(X, Y)
