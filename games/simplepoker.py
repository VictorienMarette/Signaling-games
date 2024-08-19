name = "simple poker"

T = ["L","H"]

S = [0,2,4]

A = ["f","c"]

def U(a, s, t):
    if s == 0:
        return -1
    if a == "f":
        return 1
    if t == "L":
        return -1 -s
    if t == "H":
        return 1 + s

def U_r(a, s, t):
    return -U(a, s, t)