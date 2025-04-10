/************************************************************
 * Demonstrates:
 *  1) Homogeneous Poisson process simulation
 *  2) Non-homogeneous Poisson process simulation (thinning)
 *  3) Compound Poisson process simulation
 *
 * Compile example:
 *   g++ -std=c++17 poisson_all.cpp -o poisson_all
 * Run:
 *   ./poisson_all
 ************************************************************/
#include <iostream>
#include <random>
#include <vector>
#include <cmath>
#include <functional>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
 
 // 1) Homogeneous Poisson Process
 //    Returns a vector of arrival times that occur before time T.
 std::vector<double> simulateHomogeneousPoisson(double lambda, double T, std::mt19937 &rng)
 {
     std::vector<double> arrivalTimes;
     // exponential_distribution(rate) means average interarrival time = 1/lambda
     std::exponential_distribution<double> expDist(lambda);
 
     double t = 0.0;
     // Generate arrivals until time exceeds T
     while (true)
     {
         double dt = expDist(rng); // next interarrival time
         t += dt;
         if (t > T) break;
         arrivalTimes.push_back(t);
     }
     return arrivalTimes;
 }
 
 // 2) Non-Homogeneous Poisson Process (Thinning method)
 //    lambda(t) is a time-varying rate bounded above by lambdaMax.
 //    We first simulate a homogeneous Poisson with rate = lambdaMax,
 //    then accept each arrival with probability lambda(t)/lambdaMax.
 std::vector<double> simulateNonHomogeneousPoisson(
     std::function<double(double)> lambda_t, // user-supplied rate function
     double lambdaMax,
     double T,
     std::mt19937 &rng)
 {
     // Step 1: simulate homogeneous PP with rate = lambdaMax
     std::vector<double> candidateArrivals = simulateHomogeneousPoisson(lambdaMax, T, rng);
 
     // Step 2: thinning
     std::vector<double> acceptedArrivals;
     std::uniform_real_distribution<double> U(0.0, 1.0);
 
     for (double arrivalTime : candidateArrivals)
     {
         double acceptProb = lambda_t(arrivalTime) / lambdaMax;
         if (U(rng) < acceptProb)
         {
             acceptedArrivals.push_back(arrivalTime);
         }
     }
     return acceptedArrivals;
 }
 
 // 3) Compound Poisson Process
 //    Y(t) = sum_{i=1 to N(t)} of X_i, where N(t) is a Poisson process, and
 //    X_i are i.i.d. random jumps (independent of N(t)).
 //
 //    This function returns a vector of (time, process-value) pairs to
 //    illustrate how the compound process evolves over time.
 //
 //    - 'jumpGenerator(rng)' is a function/lambda that generates one random jump X_i.
 std::vector<std::pair<double,double>> simulateCompoundPoisson(
     double lambda,
     double T,
     std::mt19937 &rng,
     std::function<double(std::mt19937 &)> jumpGenerator)
 {
     std::vector<std::pair<double,double>> processPath;
 
     // First, get the arrival times from a homogeneous Poisson process
     std::vector<double> arrivalTimes = simulateHomogeneousPoisson(lambda, T, rng);
 
     // We'll keep track of the compound sum so far
     double compoundValue = 0.0;
 
     // For each arrival time, we "jump" by a random amount
     for (double t : arrivalTimes)
     {
         double jumpSize = jumpGenerator(rng);
         compoundValue += jumpSize;
         // Store the time and the new value of the process
         processPath.push_back({t, compoundValue});
     }
 
     return processPath;
 }
 
 // Example rate function for non-homogeneous process
 double exampleLambda(double t)
 {
     // For demonstration: lambda(t) = 2 + 2 sin(0.1 * pi * t)
     // which oscillates between 0 and 4.
     return 2.0 + 2.0 * std::sin(0.1 * M_PI * t);
 }
 
 int main()
 {
     // Initialize Mersenne Twister RNG with a seed
     std::random_device rd;
     std::mt19937 rng(rd());
 
     // ============ 1) Homogeneous Poisson Example =============
     double lambda = 1.0;
     double T = 10.0;
     std::vector<double> arrivalsHom = simulateHomogeneousPoisson(lambda, T, rng);
 
     std::cout << "Homogeneous Poisson (lambda=1, T=10) generated "
               << arrivalsHom.size() << " arrivals.\n";
 
     // ============ 2) Non-Homogeneous Poisson Example ==========
     double lambdaMax = 4.0;  // must be >= max of exampleLambda(t) over [0, T]
     std::vector<double> arrivalsNonHom =
         simulateNonHomogeneousPoisson(exampleLambda, lambdaMax, T, rng);
 
     std::cout << "Non-homogeneous Poisson generated "
               << arrivalsNonHom.size() << " arrivals.\n";
 
     // ============ 3) Compound Poisson Example =================
     // We'll use a uniform jump distribution in [0,1] just as an example.
     std::uniform_real_distribution<double> jumpDist(0.0, 1.0);
 
     // Make a lambda that draws from jumpDist
     auto jumpGen = [&](std::mt19937 &localRng){
         return jumpDist(localRng);
     };
 
     // Simulate a compound Poisson with rate=1 and time horizon=10
     std::vector<std::pair<double,double>> compoundPath =
         simulateCompoundPoisson(1.0, 10.0, rng, jumpGen);
 
     std::cout << "Compound Poisson process had "
               << compoundPath.size() << " jumps.\n";
     if (!compoundPath.empty())
     {
         std::cout << "Final value at time T=" << T
                   << " is " << compoundPath.back().second << "\n";
     }
 
     return 0;
 }
 