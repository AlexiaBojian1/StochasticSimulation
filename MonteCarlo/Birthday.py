import random
import numpy as np

rng = np.random.default_rng()

def sameBirthday(birthdays):
    cal = [False] * 365
    for b in birthdays:
        if not cal[b]:
            cal[b] = True
        else: 
            
            return True
    return False

n = 50
nrRuns = 100000
counter = 0
for i in range(nrRuns) :
    birthdays = rng.integers(0,365, size = n)
    if sameBirthday(birthdays) :
        counter += 1      


estimated_probability = counter / nrRuns
print(f"Estimated probability (n={n}): {estimated_probability:.4f}")        
