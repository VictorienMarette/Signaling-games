import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

from approx_gain_signaling.SignalingGame import *


class Affichage:
    

    def __init__(self, game):
        self.game = game

    
    def affichage(self, number_of_points, jeux = ["PBE","Commit", "CE", "subCE"], nb_simulation_par_point=6, nb_simulation_si_pas_res = 6):

        if len(self.game.T) > 3:
            raise ValueError("Erreur, il y a trop d'états.")
        
        if len(self.game.T) == 3:
            self.affichage_3D(number_of_points, jeux, nb_simulation_par_point, nb_simulation_si_pas_res)

        if len(self.game.T) == 2:
            self.affichage_2D(number_of_points, jeux, nb_simulation_par_point, nb_simulation_si_pas_res)


    def affichage_2D(self, number_of_points, jeux, nb_simulation_par_point, nb_simulation_si_pas_res):

        fig, ax = plt.subplots()

        X = np.linspace(0, 1, number_of_points)

        handles=[]

        if "PBE" in jeux:
            YPBE = []

            print("Calcule pour le PBE")

            i = 0
            for x in X:
                # On calcule max_gain(x)
                y, res = self.game.max_gain_PBE([x, 1-x],number_initial_points = nb_simulation_par_point, \
                                            number_initial_points_if_no_res= nb_simulation_si_pas_res)
                YPBE.append(y)

                if i % 10 == 0:
                    print(i)
                if res == False:
                    print(str(i)+" Erreur en p("+self.game.T[0]+")="+str(x))
                i+=1

            ax.plot(X, YPBE, color='red')
            handles.append(Patch(color='red', label=r'PBE'))

        if "Commit" in jeux:
            Ycommit = []

            print("Calcule pour le commit")

            i = 0
            for x in X:
                # On calcule max_gain(x)
                y, res = self.game.max_gain_commit([x, 1-x],number_initial_points = nb_simulation_par_point, \
                                            number_initial_points_if_no_res= nb_simulation_si_pas_res)
                Ycommit.append(y)

                if i % 10 == 0:
                    print(i)
                if res == False:
                    print(str(i)+" Erreur en p("+self.game.T[0]+")="+str(x))
                i+=1

            ax.plot(X, Ycommit, color='blue')
            handles.append(Patch(color='blue', label=r'Signaling with Commitment'))

        if "CE" in jeux:
            YCE = []

            print("Calcule pour le CE")

            i = 0
            for x in X:
                # On calcule max_gain(x)
                y, res = self.game.max_gain_CE([x, 1-x],number_initial_points = nb_simulation_par_point, \
                                            number_initial_points_if_no_res= nb_simulation_si_pas_res)
                YCE.append(y)

                if i % 10 == 0:
                    print(i)
                if res == False:
                    print(str(i)+" Erreur en p("+self.game.T[0]+")="+str(x))
                i+=1

            ax.plot(X, YCE, color='green')
            handles.append(Patch(color='green', label=r'Communication equilibrium'))

        if "subCE" in jeux:
            YsubCE = []

            print("Calcule pour le subCE")

            i = 0
            for x in X:
                # On calcule max_gain(x)
                y, res = self.game.max_gain_CE_sub_perfect([x, 1-x],number_initial_points = nb_simulation_par_point, \
                                            number_initial_points_if_no_res= nb_simulation_si_pas_res)
                YsubCE.append(y)

                if i % 10 == 0:
                    print(i)
                if res == False:
                    print(str(i)+" Erreur en p("+self.game.T[0]+")="+str(x))
                i+=1

            ax.plot(X, YsubCE, color='yellow')
            handles.append(Patch(color='yellow', label=r'Sub perfect Communication equilibrium'))


        # Add the custom legend
        plt.legend(handles=handles) 

        # Set plot limits
        ax.set_ylim([0, None])

        # Set labels
        ax.set_xlabel('P('+str(self.game.T[0])+')')
        ax.set_ylabel('Mean gain')

        ax.set_title(self.game.name)

        plt.show()


    def affichage_3D(game, number_of_points,nb_simulation_si_pas_res):
        pass


    def detaille_equilibre_CE(self,p):
        len_T = len(self.game.T)
        len_S = len(self.game.S)
        len_A = len(self.game.A)

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

        #Permet d'afficher les sigmas qui donnent la solution maximal
        def print_sigmas(vars):
            for t in range(len_T):
                for s in range(len_S):
                    print("s1("+self.game.S[s]+"|"+self.game.T[t]+")="+str(selec_sigma_1(vars, s,t)), end=", ")
                print("")
            print("")

            for t in range(len_T):
                for s in range(len_S):
                    for s1 in range(len_S):
                        for a in range(len_A):
                            print("s2("+self.game.A[a]+"|"+self.game.T[t]+","+self.game.S[s]+","+self.game.S[s1]+")="\
                                +str(selec_sigma_2(vars, a,t,s,s1)), end=", ")
                        print("")


        max, max_point, res = self.game.max_gain_CE(p, get_mediator=True)

        if res == False:
            print("Erreur")
        else:
            print("Pour ", end="")
            for t in range(len_T):
                print("p("+self.game.T[t]+")=" + str(p[t]), end=", ")
            print(", le gain moyen maximum est " + str(max)+", il est atteint en:")
            print_sigmas(max_point)
