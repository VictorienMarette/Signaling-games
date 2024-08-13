import numpy as np
from scipy.optimize import minimize


def max_gain_CE_inital_point(game, p, initial_point):
    len_T = len(game.T)
    len_S = len(game.S)
    len_A = len(game.A)

    #Permet d'obtenir sigma1(s|t) avec vars
    def selec_sigma_1(vars, s,t):
        if s == 0:
            return vars[(len_S - 1)*t]
        
        sum = 0
        for i in range(s):
            sum += selec_sigma_1(vars, i,t)
        if s == len_S - 1:
            return (1 - sum)
        return (1 - sum)*vars[(len_S - 1)*t + s]

    #Permet d'obtenir sigma1(a|t,s,s1) avec vars
    def selec_sigma_2(vars, a,t,s,s1):
        if a == 0:
            return vars[(len_S - 1)*len_T + 4*t+2*s+s1]
        return 1- vars[(len_S - 1)*len_T + t*(len_A - 1)*len_S*len_S+s*(len_A - 1)*len_S+s1*(len_A - 1)]

    # Define the objective function to minimize 
    def objective(vars):
        sum = 0
        for t in range(len_T):
            for s in range(len_S):
                for a in range(len_A):
                    sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s)*p[t]*\
                        game.U(game.A[a],game.S[s],game.T[t])
        return -sum
    
    # Define the bounds for x and y
    bounds = [(0, 1) for i in initial_point] 

    # Define the constraints dictionary
    constraints = [] 

    #On definie une contraintes de l'emetteur en fonction de parametres
    def constraint_envoyeur(vars, t,t1,f_S_0,f_S_1):    
        def f(s):
            if s == 0:
                return f_S_0
            return f_S_1
        
        sum = 0

        for s in range(len_S):
            for a in range(len_A): 
                sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s)*game.U(game.A[a],game.S[s],game.T[t])
                sum -= selec_sigma_1(vars, s,t1)*selec_sigma_2(vars, a,t1,s,f(s))*game.U(game.A[a],game.S[f(s)],game.T[t])
        
        return sum
    
    #On ajoute toutes les contraintes de l'envoyeur
    for t in range(len_T):
        for t1 in range(len_T):
            for s in range(len_S):
                for s1 in range(len_S):
                    constraints.append({'type': 'ineq', \
                                        'fun': lambda vars, t=t,t1=t1,s=s,s1=s1: constraint_envoyeur(vars, t,t1,s,s1)})               

    #On definie une contraintes du receveur en fonction de parametres
    def constraint_receveur(vars, s,s1,f_A_0,f_A_1):
        def f(a):
            if a == 0:
                return f_A_0
            return f_A_1
        
        sum = 0

        for t in range(len_T):
            for a in range(len_A):
                sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s)*p[t]*game.U_r(game.A[a],game.S[s],game.T[t])
                sum -= selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s1)*p[t]*game.U_r(game.A[f(a)],game.S[s],game.T[t])
        
        return sum
    
    #On ajoute toutes les contraintes de l'envoyeur
    for s in range(len_S):
        for s1 in range(len_S):
            for a in range(len_A):
                for a1 in range(len_A):
                    constraints.append({'type': 'ineq', \
                                       'fun': lambda vars,s=s, s1=s1, a=a, a1=a1: constraint_receveur(vars, s,s1,a,a1)})

    # Perform the optimization
    result = minimize(objective, initial_point, bounds=bounds, constraints=constraints, method='SLSQP') 

    # Output the results
    return -result.fun, result.x, result.success