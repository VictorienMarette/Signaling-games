import numpy as np

import sys
sys.path.insert(1, '/home/victorien/Documents/recherche/HEC/Signaling-games/games')
from beerquiche import *


#Calcule du gain maximum de l'émetteur à p_w fixe
def max_gain(p_w, print_mediator=False):

    def selection_sigma_1(s,t):
        vec = np.zeros(20)
        vec[2*t+s] = 1
        return vec

    def selection_sigma_2(a,t,sa,sb):
        vec = np.zeros(20)
        vec[3 + 8*sb+4*sa+2*t+a] = 1
        return vec

    def selection_sigma_1_x_2(s1,t1,a2,t2,sa2,sb2):
        mat = np.zeros((20,20))
        mat[3 + 8*sb2+4*sa2+2*t2+a2][2*t1+s1] = 1
        return mat
    
    def p_T(t):
        if t == 0:
            return p_w
        return 1- p_w

    # Define the problem data
    matrix_tp_maximise = np.zeros((20,20))
    for t in [0,1]:
        for s in [0,1]:
            for a in [0,1]:
                matrix_tp_maximise += selection_sigma_1_x_2(t,s,a,t,s,s)*p_T(t)*U(A[a],S[s],T[t])
    
    # Define the optimization variable
    x = cp.Variable(20)

    # Define the objective function
    objective = cp.Maximize(cp.quad_form(x, matrix_tp_maximise))

    # Define the constraints
    constraints = [x >= 0,  # Domain constraint: x_i >= 0
                   x <= 1   # Domain constraint: x_i <= 1
                  ]

    # Define and solve the problem
    prob = cp.Problem(objective, constraints)
    result = prob.solve(solver=cp.SCS)  # Use SCS solver which is open-source

    # Output the results
    print("Status:", prob.status)
    print("Optimal value:", prob.value)
    print("Optimal x:", x.value)


max_gain(0.5)