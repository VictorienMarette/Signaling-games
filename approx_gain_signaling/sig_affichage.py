import argparse
import importlib

import sys
sys.path.insert(1, '/home/victorien/Documents/recherche/HEC/Signaling-games/approx_gain_signaling')
from SignalingGame import *
from Affichage import *

if __name__ == "__main__":
    # Créer un parser avec RawTextHelpFormatter pour conserver le formatage du texte
    parser = argparse.ArgumentParser(
        description="Importer et exécuter un module Python dynamique avec des options",
        formatter_class=argparse.RawTextHelpFormatter
    )


    # Argument obligatoire : les deux nombres
    parser.add_argument("input", type=str, help="La source où le jeu est")
    
    parser.add_argument("nb_point", type=int, help="Nombres de point dans le graph")

    parser.add_argument("-e", "--equilibres",nargs='+', type=str, choices=["PBE","Commit", "CE", "subCE"]\
                        , help="Les équilibres qui nous intressents")
    
    parser.add_argument("-s", "--nb_simulation_par_point", type=int, help="Combient de simulation par point")
    parser.add_argument("-er", "--nb_simulation_si_erreur", type=int, help="Combient de simulation supplementaire par point si Erreur")

    # Analyser les arguments
    args = parser.parse_args()

    try:
        # Create a module spec from the file location
        spec = importlib.util.spec_from_file_location("jeux", args.input)

        # Create a new module based on the spec
        module = importlib.util.module_from_spec(spec)
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f"Erreur : Le jeux n'a pas été trouvé.")
    except Exception as e:
        raise Exception(f"Erreur lors de l'importation du jeux': {e}")

    # Load the module
    spec.loader.exec_module(module)

    for arg in ['A', 'S', 'T', 'U', 'U_r','name']:
        if not arg in dir(module):
            raise ValueError(f"La variable '{arg}' n'est pas dans {args.input}")
        
    if not isinstance(module.name, str):
        raise ValueError(f"La variable 'name' n'est pas une str")
    
    if not isinstance(module.T, list):
        raise ValueError(f"La variable 'T' n'est pas une list")
    if not isinstance(module.S, list):
        raise ValueError(f"La variable 'S' n'est pas une list")
    if not isinstance(module.A, list):
        raise ValueError(f"La variable 'A' n'est pas une list")
    
    try:
        for t in module.T:
            for s in module.S:
                for a in module.A:
                    if not isinstance(module.U(a,s,t), float)and not isinstance(module.U_r(a,s,t), int):
                        raise ValueError(f"La variable U({a},{s},{t}) n'est pas réelle")
    except ValueError as e:
        raise ValueError(e)
    except Exception:
        raise ValueError(f"La variable U ne marche pas pour tout les valeurs de T*S*A")
    
    try:
        for t in module.T:
            for s in module.S:
                for a in module.A:
                    if not isinstance(module.U_r(a,s,t), float) and not isinstance(module.U_r(a,s,t), int):
                        raise ValueError(f"La variable U_r({a},{s},{t}) n'est pas réelle")
    except ValueError as e:
        raise ValueError(e)
    except Exception:
        raise ValueError(f"La variable U_r ne marche pas pour tout les valeurs de T*S*A")
    
    nb_simulation_par_point=6
    nb_simulation_si_pas_res = 6
    eq =["PBE","Commit", "CE", "subCE"]

    if args.equilibres is not None:
        eq = args.equilibres
    if args.nb_simulation_par_point is not None:
        nb_simulation_par_point = args.nb_simulation_par_point
    if args.nb_simulation_si_erreur is not None:
        nb_simulation_si_pas_res = args.nb_simulation_si_erreur
    
    game = SignalingGame(module.name,module.T,module.S,module.A,module.U,module.U_r)
    a = Affichage(game)

    a.affichage(args.nb_point, jeux=eq,nb_simulation_par_point=nb_simulation_par_point, nb_simulation_si_pas_res = nb_simulation_si_pas_res)