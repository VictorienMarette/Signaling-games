import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.widgets import CheckButtons
import numpy as np

from SignalingGame import *


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


    def get_2D_multi_fig(self, number_of_points, jeux, nb_simulation_par_point, nb_simulation_si_pas_res):

        fig, ax = plt.subplots()

        X = np.linspace(0, 1, number_of_points)

        handles=[]
        Labels = []

        if "PBE" in jeux:
            YPBE = []

            print("Calcule pour le PBE")

            i = 0
            for x in X:
                # On calcule max_gain(x)
                y, res = self.game.max_gain_PBE([x, 1-x],number_initial_points = nb_simulation_par_point*5, \
                                            number_initial_points_if_no_res= nb_simulation_si_pas_res)

                if i % 10 == 0:
                    print(i)
                if res == False:
                    print(str(i)+" Erreur en p("+self.game.T[0]+")="+str(x))
                    YPBE.append(np.nan)
                else:
                    YPBE.append(y)
                i+=1

            line1, = ax.plot(X, YPBE, color='red')
            handles.append(Patch(color='red', label=r'PBE'))
            Labels.append('PBE')

        if "Commit" in jeux:
            Ycommit = []

            print("Calcule pour le commit")

            i = 0
            for x in X:
                # On calcule max_gain(x)
                y, res = self.game.max_gain_commit([x, 1-x],number_initial_points = nb_simulation_par_point*10, \
                                            number_initial_points_if_no_res= nb_simulation_si_pas_res)

                if i % 10 == 0:
                    print(i)
                if res == False:
                    print(str(i)+" Erreur en p("+self.game.T[0]+")="+str(x))
                    Ycommit.append(np.nan)
                else:
                    Ycommit.append(y)
                i+=1

            line2, = ax.plot(X, Ycommit, color='blue')
            handles.append(Patch(color='blue', label=r'Signaling with Commitment'))
            Labels.append('Commit')

        if "CE" in jeux:
            YCE = []

            print("Calcule pour le CE")

            i = 0
            for x in X:
                # On calcule max_gain(x)
                y, res = self.game.max_gain_CE([x, 1-x],number_initial_points = nb_simulation_par_point, \
                                            number_initial_points_if_no_res= nb_simulation_si_pas_res)

                if i % 10 == 0:
                    print(i)
                if res == False:
                    print(str(i)+" Erreur en p("+self.game.T[0]+")="+str(x))
                    YCE.append(np.nan)
                else:
                    YCE.append(y)
                i+=1

            line3, = ax.plot(X, YCE, color='green')
            handles.append(Patch(color='green', label=r'Communication equilibrium'))
            Labels.append('CE')

        if "subCE" in jeux:
            YsubCE = []

            print("Calcule pour le subCE")

            i = 0
            for x in X:
                # On calcule max_gain(x)
                y, res = self.game.max_gain_CE_sub_perfect([x, 1-x],number_initial_points = nb_simulation_par_point, \
                                            number_initial_points_if_no_res= nb_simulation_si_pas_res)

                if i % 10 == 0:
                    print(i)
                if res == False:
                    print(str(i)+" Erreur en p("+self.game.T[0]+")="+str(x))
                    YsubCE.append(np.nan)
                else:
                    YsubCE.append(y)
                i+=1

            line4, = ax.plot(X, YsubCE, color='yellow')
            handles.append(Patch(color='yellow', label=r'Sub perfect Communication equilibrium'))
            Labels.append('sub perfect CE')

        # Add the custom legend
        plt.legend(handles=handles) 

        # Set plot limits
        plt.ylim(bottom=0)

        # Set labels
        ax.set_xlabel('P('+str(self.game.T[0])+')')
        ax.set_ylabel('Mean gain')

        ax.set_title(self.game.name)

        def func(label):
            if label == 'PBE':
                line1.set_visible(not line1.get_visible())
            elif label == 'Commit':
                line2.set_visible(not line2.get_visible())
            elif label == 'CE':
                line3.set_visible(not line3.get_visible())
            elif label == 'sub perfect CE':
                line4.set_visible(not line4.get_visible())
            plt.draw()

        return fig, ax, func, Labels


    def affichage_2D(self, number_of_points, jeux, nb_simulation_par_point, nb_simulation_si_pas_res):
        fig, ax, func, Labels = self.get_2D_multi_fig(number_of_points, jeux, nb_simulation_par_point, nb_simulation_si_pas_res)

        plt.subplots_adjust(left=0.1, right=0.75, bottom=0.2, top=0.8)
        # Création de la zone pour les cases à cocher
        rax = plt.axes([0.8, 0.5, 0.15, 0.15])
        checkbox = CheckButtons(rax, Labels, [True for i in Labels])

        checkbox.on_clicked(func)

        plt.show()


    def affichage_3D(game, number_of_points,nb_simulation_si_pas_res):
        pass


    def detaille_equilibre_CE(self,p):
        len_T = len(self.game.T)
        len_S = len(self.game.S)
        len_A = len(self.game.A)

        #Permet d'afficher les sigmas qui donnent la solution maximal
        def print_sigmas(vars):
            for t in range(len_T):
                for s in range(len_S):
                    print("s1("+self.game.S[s]+"|"+self.game.T[t]+")="+str(SignalingGame.selec_sigma_1(vars, s,t, len_T, len_S, len_A)), end=", ")
                print("")
            print("")

            for t in range(len_T):
                for s in range(len_S):
                    for s1 in range(len_S):
                        for a in range(len_A):
                            print("s2("+self.game.A[a]+"|"+self.game.T[t]+","+self.game.S[s]+","+self.game.S[s1]+")="\
                                +str(SignalingGame.selec_sigma_2(vars, a,t,s,s1, len_T, len_S, len_A)), end=", ")
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
