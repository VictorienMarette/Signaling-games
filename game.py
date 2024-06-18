import itertools

T1 = {"stronger army", "weak army"}
T2 = {"abundance of resources", "no abundance of resources"}

T = list(itertools.product(T1, T2))

S1 = {"military parade and excercices", "no military parade and excercices"}
S2 = {"comodites exports", "no comodites exports"}

S = list(itertools.product(S1, S2))

A = {"war", "no war"}

def U(a, s, t):
    cost_of_war_if_strong = 4
    cost_military_if_weak = 2
    gain_of_commodites_export_if_resources = 3
    gain_of_commodites_export_if_no_resources = -1

    if a == "war" and t[0] == "weak army":
        return 0
    
    res = 5 #base gain
    if a == "war":
        res += - cost_of_war_if_strong
    if t[0] == "weak army" and s[0] == "military parade and excercices":
        res += - cost_military_if_weak 
    if s[1] == "comodites exports":
        if t[1] == "abundance of resources":
            res += gain_of_commodites_export_if_resources
        else:
            res += gain_of_commodites_export_if_no_resources
    
    return res


def U_r(a, s, t):
    base_gain = 7
    gain_comodites_exp = 1
    gain_of_war_if_no_ressources = 3
    gain_of_war_if_ressources = 7
    cost_war_if_weak = 2
    cost_war_if_strong = 6

    res = base_gain
    if s[1] == "comodites exports":
        res += gain_comodites_exp
    if a == "war":
        if t[1] == "abundance of resources":
            res += gain_of_war_if_ressources
        else:
            res += gain_of_war_if_no_ressources
        if t[0] == "stronger army":
            res -= cost_war_if_strong
        else:
            res -= cost_war_if_weak
    return res