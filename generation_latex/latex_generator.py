T1 = ["W","S"]
T2 = ["W","S"]
S = ["Q","B"]

def U(a,s,t):
    res = 0
    if a == "C":
        res += 2
    if s == "Q" and t=="W":
        res += 1
    if s == "B" and t=="S":
        res += 1
    return res

def return_lignes_complete_avec_sigma(a,s,t):
    if U(a,s,t) == 0:
        return ""
    if U(a,s,t) == 1:
        return "\\sigma_1^M("+s+"|"+t+")\\sigma_2^M("+a+"|"+t+","+s+") \\ "
    return str(U(a,s,t))+"\\sigma_1^M("+s+"|"+t+")\\sigma_2^M("+a+"|"+t+","+s+") \\ "



latex = ""

cas = 1
subcas = 1

for t in T1:
    latex += "\\underline{Cas "+str(cas)+" :} "+ t + " \\\\ \n \n \\bigskip \n"
    for t2 in T2:
        for s in S:
            latex += "Cas "+str(cas) +"."+str(subcas) +": "+ t + ", suivre le médiateur plutôt que jouer "+ t2 + " "+ s  + "\\\\ \n "
            subcas +=1

            latex += "\\["
            for a in ["F","C"]:               
                latex += "\\sigma_2^M("+a+"|"+t+",\\sigma_1^M("+t+"))u("+a+",\\sigma_1^M("+t+"),"+t+") \\ "
                if a != "C":
                    latex += " + \\ "
            latex += " \\geq \\]\n"

            latex += "\\["
            for a in ["F","C"]:  
                latex += "\\sigma_2^M("+a+"|"+t2+","+s+")u("+a+","+s+","+t+") "
                if a != "C":
                    latex += " + \\ "
            latex += "\\] \n"

            latex += "\\[ \Leftrightarrow "

            for a in ["F","C"]:  
                for siter in S:
                    if return_lignes_complete_avec_sigma(a,siter,t) != "":
                        latex += return_lignes_complete_avec_sigma(a,siter,t)
                        latex += " + "
            latex = latex[:-2]
            latex += "\\geq \\]"
            

            latex += "\\["
            for a in ["F","C"]:  
                if U(a,s,t) == 1:
                    latex += "\\sigma_2^M("+a+"|"+t2+","+s+")\\ "
                elif U(a,s,t) != 0:
                    latex += str(U(a,s,t))+"\\sigma_2^M("+a+"|"+t2+","+s+")\\ "
                if a != "C" and U(a,s,t) != 0:
                    latex += " + \\ "
            latex += "\\] \n"



    cas+= 1
    subcas = 1

chemin_fichier = "generation_latex/output.txt"

with open(chemin_fichier, 'w', encoding='utf-8') as fichier:
    fichier.write(latex)
