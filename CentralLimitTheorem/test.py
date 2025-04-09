from numpy import std , mean , arange , zeros , sqrt
from scipy import stats
import matplotlib . pyplot as plt
from statsmodels . stats . weightstats import DescrStatsW

Zdist = stats . uniform (0 , 1) # Pick any distribution function here

z = Zdist . mean () # 1/2
sigma = Zdist . std () # 1/ sqrt (12)

n = 10
nrRuns = 100000

Ysim = zeros ( nrRuns )
for i in range ( nrRuns ) :
    Zsim = Zdist . rvs ( n)
    Yn = sqrt (n) * ( mean ( Zsim ) - z )/ sigma
    Ysim [i ] = Yn

plt.figure ()
plt.hist ( Ysim , bins =100 , rwidth =0.8 , density = True )
xs = arange ( min ( Ysim ) , max ( Ysim ) , 0.01)
ys = stats . norm (0 , 1). pdf ( xs )
