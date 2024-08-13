import numpy as np
import random

from max_gain_CE import *


#Donne un point au hasard de taille n
def random_initial_point(n):
    point = np.zeros(n)
    for s in range(n):
        point[s] = random.random()
    return point


def max_gain_wrapper(f,n, get_mediator=False, number_initial_points = 4, number_initial_points_if_no_res = 6):
    max = 0
    max_point = np.zeros(20)
    res = False

    for i in range(number_initial_points):
        value, point, result = f(random_initial_point(n))
        if value > max and result:
            max = value
            max_point = point
            res =True

    if not res:
        while not res and number_initial_points_if_no_res > 0:
            value, point, result = f(random_initial_point(n))
            if value > max and result:
                max = value
                max_point = point
                res =True
            number_initial_points_if_no_res -= 1

    if get_mediator:
        return max, max_point, res
    return max, res


def max_gain_CE(game, p, get_mediator=False, number_initial_points = 4, number_initial_points_if_no_res = 6):
    taille_point = (len(game.S)-1)*(len(game.T))+(len(game.A)-1)*(len(game.S))*(len(game.S))*(len(game.T))
    return max_gain_wrapper((lambda initial_point,game=game, p=p: max_gain_CE_inital_point(game,p, initial_point)) 
                            , taille_point, get_mediator=get_mediator, number_initial_points = number_initial_points, 
                            number_initial_points_if_no_res = number_initial_points_if_no_res)