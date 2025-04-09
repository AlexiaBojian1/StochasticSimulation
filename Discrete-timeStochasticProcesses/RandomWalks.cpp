#include <iostream>
#include <vector>
#include <random>

// Function to simulate a simple random walk with prob p of stepping +1
//Return a vector of positions s_0 s_1 s_2...

std::vector<int> simRandomWalk(double p, int n) {

    static std::random_device rd; //non-det seed source
    static std::mt19937 gen(rd()); //random number generator
    std::bernoulli_distribution dist(p); //will return true with prob p

    //create a vectro to hold the position
    std::vector<int> positions(n+1, 0);

    for(int i = 1 ; i <= n; i++) {
        int step = dist(gen) ? +1 : -1;
        positions[i] = positions[i-1] + step;
    }

    return positions;
}

int main() {
    double p = 0.5;
    int n = 100;

    std::vector<int> path = simRandomWalk(p,n);
    for (int i = 0; i <= n; ++i)
    {
        std::cout << "Step " << i << ": " << path[i] << std::endl;
    }

    return 0;

}