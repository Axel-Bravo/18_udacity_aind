import numpy as np
from math import log

# Write a function that takes as input two lists Y, P,
# and returns the float corresponding to their cross-entropy.
def cross_entropy(Y, P):
    return  - sum([Y[i]*log(P[i]) if Y[i] == 1 else (1-Y[i])*log(1-P[i]) for i in range(len(Y))])
