from game import *
import numpy as np
from sympy import Matrix

def coef(s):
    vec = []

    for t in T:
        vec.append(U_r("war",s,t) - U_r("no war",s,t))

    return np.array([vec])

def cordonnes():
    return list(S)


# Définir la matrice augmentée (A|b)
A = np.column_stack( (np.vstack( (coef(S[0]), np.ones(4))), np.transpose(np.array([0, 1]) )))

# Calculer la forme réduite par lignes
rref_matrix, pivot_columns = Matrix(A).rref()

print(rref_matrix)



