import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

from max_gain import max_gain_CE


def affichage(game, number_of_points, nb_simulation_par_point=6):
    if len(game.T) > 3:
        raise ValueError("Erreur, il y a trop d'états.")
    
    if len(game.T) == 3:
        affichage_3D(game, number_of_points, nb_simulation_par_point)

    if len(game.T) == 2:
        affichage_2D(game, number_of_points, nb_simulation_par_point)


def affichage_2D(game, number_of_points,nb_simulation_par_point):

    fig, ax = plt.subplots()

    """ax.plot([0,0.5], [3,2.5], color='red')
    ax.plot([0.5,1], [1.5,1], color='red')

    ax.plot([0,0.5,1], [3,2.5,1], color='blue',linestyle='--')"""

    X = np.linspace(0, 1, number_of_points)

    Y = []
    i = 0
    for x in X:
        # On calcule max_gain(x)
        y, res = max_gain_CE(game, [x, 1-x],number_initial_points = nb_simulation_par_point)
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
    ax.set_xlabel('P('+str(game.T[0])+')')
    ax.set_ylabel('Mean gain')

    plt.show()


def affichage_3D(game, number_of_points):
    pass