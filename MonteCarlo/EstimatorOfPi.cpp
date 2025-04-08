#include <iostream>
#include <random>
#include <cmath>

using namespace std;

int main() {
    const long long N = 100000000;

    //Initialize random generator and distribution
    mt19937_64 rng (12345);
    uniform_real_distribution<double> dist(-1.0, 1.0);

    long long pointsInsideCircle = 0;
    for (long long i = 0; i < N; i++) {
        double x = dist(rng);
        double y = dist(rng);
        if(x*x + y*y <= 1.0) {
            pointsInsideCircle++;
        }
    }

    double piEstimate = 4.0 * (static_cast<double>(pointsInsideCircle) / static_cast<double>(N));

    std::cout << "Estimated Pi = " << piEstimate << std::endl;

    return 0;
}