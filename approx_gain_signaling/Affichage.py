import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

from approx_gain_signaling.SignalingGame import *


class Affichage:
    

    def __init__(self, game):
        self.game = game

    
    def affichage(self, number_of_points, nb_simulation_par_point=6):

        if len(self.game.T) > 3:
            raise ValueError("Erreur, il y a trop d'états.")
        
        if len(self.game.T) == 3:
            self.affichage_3D(number_of_points, nb_simulation_par_point)

        if len(self.game.T) == 2:
            self.affichage_2D(number_of_points, nb_simulation_par_point)


    def affichage_2D(self, number_of_points,nb_simulation_par_point):

        fig, ax = plt.subplots()

        """ax.plot([0,0.5], [3,2.5], color='red')
        ax.plot([0.5,1], [1.5,1], color='red')

        ax.plot([0,0.5,1], [3,2.5,1], color='blue',linestyle='--')"""

        X = np.linspace(0, 1, number_of_points)

        Y = []
        i = 0
        for x in X:
            # On calcule max_gain(x)
            y, res = self.game.max_gain_CE([x, 1-x],number_initial_points = nb_simulation_par_point)
            Y.append(y)

            if i % 10 == 0:
                print(i)
            if res == False:
                print("Erreur en: " + str(i))
            i+=1

        ax.plot(X, Y, color='green')

        # Define custom legend patches
        #blue_patch = Patch(color='blue', label=r'Signaling with Commitment')
        #red_patch = Patch(color='red', label=r'PBE')
        green_patch = Patch(color='green', label=r'Communication equilibrium estimé avec python')

        # Add the custom legend
        plt.legend(handles=[ green_patch]) #red_patch,blue_patch,

        # Set plot limits
        ax.set_ylim([0, None])

        # Set labels
        ax.set_xlabel('P('+str(self.game.T[0])+')')
        ax.set_ylabel('Mean gain')

        plt.show()


    def affichage_3D(game, number_of_points):
        pass


    def detaille_equilibre(self,p):
        #Permet d'afficher les sigmas qui donnent la solution maximal
        def print_sigmas(vars):
            for t in [0,1]:
                print("s1("+self.game.S[0]+"|"+self.game.T[t]+")="+str(vars[t]))

            for t in [0,1]:
                for s in [0,1]:
                    for s1 in [0,1]:
                        print("s2("+self.game.A[0]+"|"+self.game.T[t]+","+self.game.S[s]+","+self.game.S[s1]+")="\
                              +str(vars[2 + 4*t+2*s+s1]))


        max, max_point, res = self.game.max_gainCE(p, get_mediator=True)

        if res == False:
            print("Erreur")
        else:
            print("Pour p(W)=" + str(p)+ ", le gain moyen maximum est " + str(max)+", il est atteint en:")
            print_sigmas(max_point)
