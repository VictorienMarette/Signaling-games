T = ["Weak", "Strong"]

S = ["Beer", "Quiche"]

A = ["Fight", "Cower"]

def U(a, s, t):
    res = 0

    if s == "Beer" and t == "Strong":
        res += 1

    if s == "Quiche" and t == "Weak":
        res += 1

    if a == "Cower":
        res += 2

    return res


def U_r(a, s, t):
    if a == "Fight" and t == "Weak":
        return 1
    
    if a == "Cower" and t == "Strong":
        return 1

    return 1