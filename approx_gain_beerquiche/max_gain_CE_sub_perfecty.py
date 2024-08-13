import numpy as np
from scipy.optimize import minimize


def max_gain_CE_sub_perfect_inital_point(game, p, initial_point):
    #Permet d'obtenir sigma1(s|t) avec vars
    def selec_sigma_1(vars, s,t):
        if s == 0:
            return vars[t]
        return 1- vars[t]

    #Permet d'obtenir sigma1(a|t,s,s1) avec vars
    def selec_sigma_2(vars, a,t,s,s1):
        if a == 0:
            return vars[2 + 4*t+2*s+s1]
        return 1- vars[2 + 4*t+2*s+s1]

    # Define the objective function to minimize 
    def objective(vars):
        sum = 0
        for t in [0,1]:
            for s in [0,1]:
                for a in [0,1]:
                    sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s)*p[t]*\
                        game.U(game.A[a],game.S[s],game.T[t])
        return -sum
    
    # Define the bounds for x and y
    bounds = [(0, 1) for i in range(10)] 

    # Define the constraints dictionary
    constraints = [] 

    #On definie une contraintes de l'emetteur en fonction de parametres
    def constraint_envoyeur(vars, t,t1,f_S_0,f_S_1):    
        def f(s):
            if s == 0:
                return f_S_0
            return f_S_1
        
        sum = 0

        for s in [0,1]:
            for a in [0,1]: 
                sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s)*game.U(game.A[a],game.S[s],game.T[t])
                sum -= selec_sigma_1(vars, s,t1)*selec_sigma_2(vars, a,t1,s,f(s))*game.U(game.A[a],game.S[f(s)],game.T[t])
        
        return sum
    
    #On ajoute toutes les contraintes de l'envoyeur
    for t in [0,1]:
        for t1 in [0,1]:
            for s in [0,1]:
                for s1 in [0,1]:
                    constraints.append({'type': 'ineq', \
                                        'fun': lambda vars, t=t,t1=t1,s=s,s1=s1: constraint_envoyeur(vars, t,t1,s,s1)})               

    #On definie une contraintes du receveur en fonction de parametres
    def constraint_receveur(vars, s,s1,f_A_0,f_A_1):
        def f(a):
            if a == 0:
                return f_A_0
            return f_A_1
        
        sum = 0

        for t in [0,1]:
            for a in [0,1]:
                sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s)*p[t]*game.U_r(game.A[a],game.S[s],game.T[t])
                sum -= selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s1)*p[t]*game.U_r(game.A[f(a)],game.S[s],game.T[t])
        
        return sum
    
    #On ajoute toutes les contraintes de l'envoyeur
    for s in [0,1]:
        for s1 in [0,1]:
            for a in [0,1]:
                for a1 in [0,1]:
                    constraints.append({'type': 'ineq', \
                                       'fun': lambda vars,s=s, s1=s1, a=a, a1=a1: constraint_receveur(vars, s,s1,a,a1)})

    # Perform the optimization
    result = minimize(objective, initial_point, bounds=bounds, constraints=constraints, method='SLSQP') 

    # Output the results
    return -result.fun, result.x, result.success