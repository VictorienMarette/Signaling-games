from approx_gain_beerquiche.max_gain_CE import max_gain
import sys
sys.path.insert(1, '/home/victorien/Documents/recherche/HEC/Signaling-games/games')
from beerquiche import *

#Permet d'afficher les sigmas qui donnent la solution maximal
def print_sigmas(vars):
    for t in [0,1]:
        print("s1("+S[0]+"|"+T[t]+")="+str(vars[t]))

    for t in [0,1]:
        for s in [0,1]:
            for s1 in [0,1]:
                print("s2("+A[0]+"|"+T[t]+","+S[s]+","+S[s1]+")="+str(vars[2 + 4*t+2*s+s1]))


p_w = 0.75

max, max_point, res = max_gain(0.75, get_mediator=True)

if res == False:
    print("Erreur")
else:
    print("Pour p(W)=" + str(p_w)+ ", le gain moyen maximum est " + str(max)+", il est atteint en:")
    print_sigmas(max_point)