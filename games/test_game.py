T = ["Weak", "Strong"]

S = ["Beer", "Quiche", "caca"]

A = ["Fight", "Cower","SupaSayan"]

def U(a, s, t):
    res = 0

    if s == "Beer" and t == "Strong":
        res += 1

    if s == "Quiche" and t == "Weak":
        res += 1

    if s == "caca":
        res += 0.5

    if a == "Cower":
        res += 2

    if a == "SupaSayan":
        res += -0.5

    return res


def U_r(a, s, t):
    if a == "Fight" and t == "Weak":
        return 1
    
    if a == "Cower" and t == "Strong":
        return 1
    
    if a == "SupaSayan":
        return 0.5

    return 0