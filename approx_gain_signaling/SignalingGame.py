import numpy as np
import random
from scipy.optimize import minimize
import itertools


class SignalingGame:

    def __init__(self, name, T, S, A, U, U_r):
        self.name = name
        self.T = T
        self.S = S
        self.A = A
        self.U = U
        self.U_r = U_r


    #Donne un point au hasard de taille n
    def random_initial_point(self, n):
        point = np.zeros(n)
        for s in range(n):
            point[s] = random.random()
        return point
    

    def max_gain_wrapper(self, f,n, get_mediator=False, number_initial_points = 4, number_initial_points_if_no_res = 6):
        max = 0
        max_point = np.zeros(20)
        res = False

        for i in range(number_initial_points):
            value, point, result = f(self.random_initial_point(n))
            if value > max and result:
                max = value
                max_point = point
                res =True

        if not res:
            while not res and number_initial_points_if_no_res > 0:
                value, point, result = f(self.random_initial_point(n))
                if value > max and result:
                    max = value
                    max_point = point
                    res =True
                number_initial_points_if_no_res -= 1

        if get_mediator:
            return max, max_point, res
        return max, res
    

    #Permet d'obtenir sigma_E(s|t) avec vars
    @classmethod
    def selec_sigma_E(cls,vars, s,t,len_T,len_S,len_A):
        if s == 0:
            return vars[(len_S - 1)*t]
        
        sum = 0
        for i in range(s):
            sum += SignalingGame.selec_sigma_E(vars, i,t,len_T,len_S,len_A)
        if s == len_S - 1:
            return (1 - sum)
        return (1 - sum)*vars[(len_S - 1)*t + s]


    #Permet d'obtenir sigma_R(a|s) avec vars
    @classmethod
    def selec_sigma_R(cls,vars, a,s,len_T,len_S,len_A):
        if a == 0:
            return vars[(len_S - 1)*len_T + s*(len_A - 1)]
        
        sum = 0
        for i in range(a):
            sum += SignalingGame.selec_sigma_R(vars, i,s, len_T,len_S,len_A)
        if a == len_A - 1:
            return (1 - sum)
        return (1 - sum)*vars[(len_S - 1)*len_T + s*(len_A - 1)+a]
    

    def max_gain_PBE_inital_point(self, p, initial_point):
        len_T = len(self.T)
        len_S = len(self.S)
        len_A = len(self.A)

        def selec_sigma_E(vars, s,t):
            return SignalingGame.selec_sigma_E(vars, s,t,len_T,len_S,len_A)
        
        def selec_sigma_R(vars, a,s):
            return SignalingGame.selec_sigma_R(vars, a,s,len_T,len_S,len_A)

        # Define the objective function to minimize 
        def objective(vars):
            sum = 0
            for t in range(len_T):
                for s in range(len_S):
                    for a in range(len_A):
                        sum += selec_sigma_E(vars, s,t)*selec_sigma_R(vars, a,s)*p[t]*\
                            self.U(self.A[a],self.S[s],self.T[t])
            return -sum
        
        # Define the bounds for x and y
        bounds = [(0, 1) for i in initial_point] 

        # Define the constraints dictionary
        constraints = [] 

        #On definie une contraintes de l'emetteur en fonction de parametres
        def constraint_envoyeur(vars, t,s1):    
            sum = 0
            for a in range(len_A): 
                for s in range(len_S):
                    sum += selec_sigma_E(vars, s,t)*selec_sigma_R(vars, a,s)*self.U(self.A[a],self.S[s],self.T[t])
                sum -= selec_sigma_R(vars, a,s1)*self.U(self.A[a],self.S[s1],self.T[t])
            return sum
        
        #On ajoute toutes les contraintes de l'envoyeur
        for t in range(len_T):
            for s1 in range(len_S):
                    constraints.append({'type': 'ineq', \
                                        'fun': lambda vars, t=t,s1=s1: constraint_envoyeur(vars, t,s1)})           

        #On definie une contraintes du receveur en fonction de parametres
        def constraint_receveur(vars, s,a1):
            sum = 0
            for t in range(len_T):
                for a in range(len_A):
                    sum += selec_sigma_E(vars, s,t)*selec_sigma_R(vars, a,s)*p[t]*self.U_r(self.A[a],self.S[s],self.T[t])
                sum -= selec_sigma_E(vars, s,t)*p[t]*self.U_r(self.A[a1],self.S[s],self.T[t])
            return sum
        
        #On ajoute toutes les contraintes de l'envoyeur
        for s in range(len_S):
            for a1 in range(len_A):
                constraints.append({'type': 'ineq', \
                                'fun': lambda vars,s=s, a1=a1: constraint_receveur(vars, s,a1)})

        # Perform the optimization
        result = minimize(objective, initial_point, bounds=bounds, constraints=constraints, method='SLSQP') 

        # Output the results
        return -result.fun, result.x, result.success


    def max_gain_PBE(self, p, get_mediator=False, number_initial_points = 4, number_initial_points_if_no_res = 6):
        taille_point = (len(self.S)-1)*(len(self.T))+(len(self.A)-1)*(len(self.S))
        return self.max_gain_wrapper((lambda initial_point,self=self, p=p: self.max_gain_PBE_inital_point(p, initial_point)) 
                                , taille_point, get_mediator=get_mediator, number_initial_points = number_initial_points, 
                                number_initial_points_if_no_res = number_initial_points_if_no_res)


    def max_gain_commit_inital_point(self, p, initial_point):
        len_T = len(self.T)
        len_S = len(self.S)
        len_A = len(self.A)

        def selec_sigma_E(vars, s,t):
            return SignalingGame.selec_sigma_E(vars, s,t,len_T,len_S,len_A)
        
        def selec_sigma_R(vars, a,s):
            return SignalingGame.selec_sigma_R(vars, a,s,len_T,len_S,len_A)

        # Define the objective function to minimize 
        def objective(vars):
            sum = 0
            for t in range(len_T):
                for s in range(len_S):
                    for a in range(len_A):
                        sum += selec_sigma_E(vars, s,t)*selec_sigma_R(vars, a,s)*p[t]*\
                            self.U(self.A[a],self.S[s],self.T[t])
            return -sum
        
        # Define the bounds for x and y
        bounds = [(0, 1) for i in initial_point] 

        # Define the constraints dictionary
        constraints = []          

        #On definie une contraintes du receveur en fonction de parametres
        def constraint_receveur(vars, s,a1):
            sum = 0
            for t in range(len_T):
                for a in range(len_A):
                    sum += selec_sigma_E(vars, s,t)*selec_sigma_R(vars, a,s)*p[t]*self.U_r(self.A[a],self.S[s],self.T[t])
                sum -= selec_sigma_E(vars, s,t)*p[t]*self.U_r(self.A[a1],self.S[s],self.T[t])
            return sum
        
        #On ajoute toutes les contraintes de l'envoyeur
        for s in range(len_S):
            for a1 in range(len_A):
                constraints.append({'type': 'ineq', \
                                'fun': lambda vars,s=s, a1=a1: constraint_receveur(vars, s,a1)})

        # Perform the optimization
        result = minimize(objective, initial_point, bounds=bounds, constraints=constraints, method='SLSQP') 

        # Output the results
        return -result.fun, result.x, result.success


    def max_gain_commit(self, p, get_mediator=False, number_initial_points = 4, number_initial_points_if_no_res = 6):
        taille_point = (len(self.S)-1)*(len(self.T))+(len(self.A)-1)*(len(self.S))
        return self.max_gain_wrapper((lambda initial_point,self=self, p=p: self.max_gain_commit_inital_point(p, initial_point)) 
                                , taille_point, get_mediator=get_mediator, number_initial_points = number_initial_points, 
                                number_initial_points_if_no_res = number_initial_points_if_no_res)
    

    #Permet d'obtenir sigma1(s|t) avec vars
    @classmethod
    def selec_sigma_1(cls,vars, s,t,len_T,len_S,len_A):
        if s == 0:
            return vars[(len_S - 1)*t]
        
        sum = 0
        for i in range(s):
            sum += SignalingGame.selec_sigma_1(vars, i,t,len_T,len_S,len_A)
        if s == len_S - 1:
            return (1 - sum)
        return (1 - sum)*vars[(len_S - 1)*t + s]


    #Permet d'obtenir sigma1(a|t,s,s1) avec vars
    @classmethod
    def selec_sigma_2(cls,vars, a,t,s,s1,len_T,len_S,len_A):
        if a == 0:
            return vars[(len_S - 1)*len_T + t*(len_A - 1)*len_S*len_S+s*(len_A - 1)*len_S+s1*(len_A - 1)]
        
        sum = 0
        for i in range(a):
            sum += SignalingGame.selec_sigma_2(vars, i,t,s,s1, len_T,len_S,len_A)
        if a == len_A - 1:
            return (1 - sum)
        return (1 - sum)*vars[(len_S - 1)*len_T + t*(len_A - 1)*len_S*len_S+s*(len_A - 1)*len_S+s1*(len_A - 1) + a]


    def max_gain_CE_inital_point(self, p, initial_point):
        len_T = len(self.T)
        len_S = len(self.S)
        len_A = len(self.A)

        def selec_sigma_1(vars, s,t):
            return SignalingGame.selec_sigma_1(vars, s,t,len_T,len_S,len_A)
        
        def selec_sigma_2(vars, a,t,s,s1):
            return SignalingGame.selec_sigma_2(vars, a,t,s,s1,len_T,len_S,len_A)

        # Define the objective function to minimize 
        def objective(vars):
            sum = 0
            for t in range(len_T):
                for s in range(len_S):
                    for a in range(len_A):
                        sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s)*p[t]*\
                            self.U(self.A[a],self.S[s],self.T[t])
            return -sum
        
        # Define the bounds for x and y
        bounds = [(0, 1) for i in initial_point] 

        # Define the constraints dictionary
        constraints = [] 

        #On definie une contraintes de l'emetteur en fonction de parametres
        def constraint_envoyeur(vars, t,t1,f):    
            sum = 0
            for s in range(len_S):
                for a in range(len_A): 
                    sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s)*self.U(self.A[a],self.S[s],self.T[t])
                    sum -= selec_sigma_1(vars, s,t1)*selec_sigma_2(vars, a,t1,s,f[s])*self.U(self.A[a],self.S[f[s]],self.T[t])
            return sum
        
        #On ajoute toutes les contraintes de l'envoyeur
        valeurs = list(range(len_S))
        for t in range(len_T):
            if p[t] > 0:
                for t1 in range(len_T):
                    for f in itertools.product(valeurs, repeat=len_S):
                        constraints.append({'type': 'ineq', \
                                            'fun': lambda vars, t=t,t1=t1,f=f: constraint_envoyeur(vars, t,t1,f)})               

        #On definie une contraintes du receveur en fonction de parametres
        def constraint_receveur(vars, s,s1,f):
            sum = 0
            for t in range(len_T):
                for a in range(len_A):
                    sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s)*p[t]*self.U_r(self.A[a],self.S[s],self.T[t])
                    sum -= selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s1)*p[t]*self.U_r(self.A[f[a]],self.S[s],self.T[t])
            return sum
        
        #On ajoute toutes les contraintes de l'envoyeur
        valeurs = list(range(len_A))
        for s in range(len_S):
            for s1 in range(len_S):
                for f in itertools.product(valeurs, repeat=len_A):
                    constraints.append({'type': 'ineq', \
                                    'fun': lambda vars,s=s, s1=s1, f=f: constraint_receveur(vars, s,s1,f)})

        # Perform the optimization
        result = minimize(objective, initial_point, bounds=bounds, constraints=constraints, method='SLSQP') 

        # Output the results
        return -result.fun, result.x, result.success


    def max_gain_CE(self, p, get_mediator=False, number_initial_points = 4, number_initial_points_if_no_res = 6):
        taille_point = (len(self.S)-1)*(len(self.T))+(len(self.A)-1)*(len(self.S))*(len(self.S))*(len(self.T))
        return self.max_gain_wrapper((lambda initial_point,self=self, p=p: self.max_gain_CE_inital_point(p, initial_point)) 
                                , taille_point, get_mediator=get_mediator, number_initial_points = number_initial_points, 
                                number_initial_points_if_no_res = number_initial_points_if_no_res)


    def max_gain_CE_sub_inital_point(self, p, initial_point):
        len_T = len(self.T)
        len_S = len(self.S)
        len_A = len(self.A)

        def selec_sigma_1(vars, s,t):
            return SignalingGame.selec_sigma_1(vars, s,t,len_T,len_S,len_A)
        
        def selec_sigma_2(vars, a,t,s,s1):
            return SignalingGame.selec_sigma_2(vars, a,t,s,s1,len_T,len_S,len_A)

        # Define the objective function to minimize 
        def objective(vars):
            sum = 0
            for t in range(len_T):
                for s in range(len_S):
                    for a in range(len_A):
                        sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s)*p[t]*\
                            self.U(self.A[a],self.S[s],self.T[t])
            return -sum
        
        # Define the bounds for x and y
        bounds = [(0, 1) for i in initial_point] 

        # Define the constraints dictionary
        constraints = [] 

        #On definie une contraintes de l'emetteur dans un premier temps
        def constraint_envoyeur(vars, t,t1):    
            sum = 0
            for s in range(len_S):
                for a in range(len_A): 
                    sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s)*self.U(self.A[a],self.S[s],self.T[t])
                    sum -= selec_sigma_1(vars, s,t1)*selec_sigma_2(vars, a,t1,s,s)*self.U(self.A[a],self.S[s],self.T[t])
            return sum
        
        #On ajoute toutes les contraintes de l'envoyeur
        for t in range(len_T):
            if p[t] > 0:
                for t1 in range(len_T):
                    constraints.append({'type': 'ineq', \
                                        'fun': lambda vars, t=t,t1=t1: constraint_envoyeur(vars, t,t1)})

        #On definie une contraintes de l'emetteur dans un deuxieme temps
        def constraint_envoyeur2(vars, t,t1,s,s1):    
            sum = 0
            for a in range(len_A): 
                sum += selec_sigma_2(vars, a,t1,s,s)*self.U(self.A[a],self.S[s],self.T[t])
                sum -= selec_sigma_2(vars, a,t1,s,s1)*self.U(self.A[a],self.S[s1],self.T[t])
            return sum
        
        #On ajoute toutes les contraintes de l'envoyeur
        for t in range(len_T):
            if p[t] > 0:
                for t1 in range(len_T):
                    for s in range(len_S):
                        for s1 in range(len_S):
                            constraints.append({'type': 'ineq', \
                                                'fun': lambda vars, t=t,t1=t1,s=s,s1=s1: constraint_envoyeur2(vars, t,t1,s,s1)})                 

        #On definie une contraintes du receveur dans un premier temps
        def constraint_receveur(vars, s,s1):
            sum = 0
            for t in range(len_T):
                for a in range(len_A):
                    sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s)*p[t]*self.U_r(self.A[a],self.S[s],self.T[t])
                    sum -= selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s1)*p[t]*self.U_r(self.A[a],self.S[s],self.T[t])
            return sum
        
        #On ajoute toutes les contraintes de l'envoyeur
        for s in range(len_S):
            for s1 in range(len_S):
                constraints.append({'type': 'ineq', \
                                'fun': lambda vars,s=s, s1=s1: constraint_receveur(vars, s,s1)})
                
        #On definie une contraintes du receveur dans un deuxieme temps
        def constraint_receveur2(vars, s,s1,a,a1):
            sum = 0
            for t in range(len_T):
                sum += selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s1)*p[t]*self.U_r(self.A[a],self.S[s],self.T[t])
                sum -= selec_sigma_1(vars, s,t)*selec_sigma_2(vars, a,t,s,s1)*p[t]*self.U_r(self.A[a1],self.S[s],self.T[t])
            return sum
        
        #On ajoute toutes les contraintes de l'envoyeur
        for s in range(len_S):
            for s1 in range(len_S):
                    for a in range(len_A):
                        for a1 in range(len_A):
                            constraints.append({'type': 'ineq', \
                                            'fun': lambda vars,s=s, s1=s1,a=a,a1=a1: constraint_receveur2(vars, s,s1,a,a1)})

        # Perform the optimization
        result = minimize(objective, initial_point, bounds=bounds, constraints=constraints, method='SLSQP') 

        # Output the results
        return -result.fun, result.x, result.success
    

    def max_gain_CE_sub_perfect(self, p, get_mediator=False, number_initial_points = 4, number_initial_points_if_no_res = 6):
        taille_point = (len(self.S)-1)*(len(self.T))+(len(self.A)-1)*(len(self.S))*(len(self.S))*(len(self.T))
        return self.max_gain_wrapper((lambda initial_point,self=self, p=p: self.max_gain_CE_sub_inital_point(p, initial_point)) 
                                , taille_point, get_mediator=get_mediator, number_initial_points = number_initial_points, 
                                number_initial_points_if_no_res = number_initial_points_if_no_res)