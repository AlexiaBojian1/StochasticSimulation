#include <iostream>
#include <vector>
#include <random>
#include <iomanip>  

// Function to simulate a Markov chain for n steps, starting from state x0.
// p is the transition matrix, where p[i][j] = probability of going from state i to state j.
std::vector<int> simMarkovChain(const std::vector<std::vector<double>>& p, int x0, int n)
{
    // Create a random number generator (seeded by a random device).
    static std::random_device rd;
    static std::mt19937 gen(rd());

    // This will store the entire sequence of states (including the initial state).
    std::vector<int> x(n + 1);
    x[0] = x0;

    // Number of states = number of rows in p.
    int nrStates = static_cast<int>(p.size());

    for(int i = 1; i <= n; i++)
    {
        // Construct a discrete distribution based on the probabilities in row p[x[i-1]].
        // The next state is chosen according to those probabilities.
        std::discrete_distribution<int> dist(p[x[i - 1]].begin(), p[x[i - 1]].end());

        // Sample the next state.
        x[i] = dist(gen);
    }
    return x;
}

int main()
{
    // Define the transition matrix for a 3-state Markov chain.
    // p[i][j] = probability of transitioning from state i to state j.
    std::vector<std::vector<double>> p = {
        {0.2, 0.3, 0.5},  // from state 0
        {0.0, 0.3, 0.7},  // from state 1
        {0.5, 0.4, 0.1}   // from state 2
    };

    // Set the initial state and the number of steps to simulate.
    int initialState = 0;   // let's start in state 0
    int nSteps = 20;        // simulate 20 transitions

    // Run the simulation.
    std::vector<int> chain = simMarkovChain(p, initialState, nSteps);

    std::cout << "Simulated Markov chain states:\n";
    for (int i = 0; i < static_cast<int>(chain.size()); i++) {
        std::cout << chain[i] << (i + 1 < static_cast<int>(chain.size()) ? " -> " : "\n");
    }

    return 0;
}
