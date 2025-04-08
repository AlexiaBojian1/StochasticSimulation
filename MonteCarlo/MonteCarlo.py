from numpy import mean
from scipy import stats

expDist = stats.expon(scale = 1/10)
n = 10000
z = expDist.rvs(n)
est = mean(z)
print(est)