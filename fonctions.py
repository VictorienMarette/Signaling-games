from wargame import *

def Y(s,p):
    res_war = 0
    res_no_war = 0
    for t in T:
        res_war += p(t)*U_r("war",s,t)
        res_no_war += p(t)*U_r("no war",s,t)

    if abs(res_no_war - res_war) < 0.01:
        return "M"
    if res_no_war < res_war:
        return "no war"
    return "war"

def E(s,p):
    if Y(s,p) == "war":
        dic = {}
        for t in T:
            dic[t] = U("war", s, t)
        return [dic]
    if Y(s,p) == "no war":
        dic = {}
        for t in T:
            dic[t] = U("no war", s, t)
        return [dic]
    else:
        dic1 = {}
        for t in T:
            dic1[t] = U("war", s, t)
    
        dic2 = {}
        for t in T:
            dic2[t] = U("no war", s, t)
        return [dic1, dic2]
    
def p(t):
    return 1/4

print(Y(('no military parade and excercices', 'comodites exports'), p))
print(E(('no military parade and excercices', 'comodites exports'), p))