T = ["Rock", "Paper", "Scissors"]

S = ["Rock s", "Paper s"]

A = ["Paper", "Scissors"]

def U(a, s, t):
    res = -U_r(a, s, t)

    if s == "Rock s" and t == "Scissors":
        res -= 2

    if s == "Paper s" and t == "Rock":
        res -= 2

    if s == "Rock s" and t == "Paper":
        res -= 1

    if s == "Paper s" and t == "Scissors":
        res -= 1

    return res


def U_r(a, s, t):
    res = 0

    if a == "Paper":
        if t == "Rock":
            res += 3
        if t == "Scissors":
            res += -3

    if a == "Scissors":
        if t == "Rock":
            res += -3
        if t == "Paper":
            res += 3

    return res

