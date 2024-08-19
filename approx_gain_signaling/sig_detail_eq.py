#!/usr/bin/env python3

import argparse
import importlib
import sys

if __name__ == "__main__":
    # Créer un parser avec RawTextHelpFormatter pour conserver le formatage du texte
    parser = argparse.ArgumentParser(
        description="Importer et exécuter un module Python dynamique avec des options",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Description multi-lignes avec chaînes de caractères triples
    description = """
    L'opération à effectuer :
    - 'affichage' : Permet un affichage interactif 
    - 'multi' : Soustraction
    - 'detailed' : Multiplication
    Choisissez parmi ces options pour spécifier l'opération désirée.
        """
    
    # Argument obligatoire : l'opération
    parser.add_argument(
        "operation",
        choices=["affichage", "multi", "detailed"],
        help=description
    )

    # Argument obligatoire : les deux nombres
    parser.add_argument("input", type=str, help="La source où le ou les jeux sont")

    """# Argument optionnel : activer le mode verbeux
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Activer le mode verbeux pour afficher des informations détaillées sur l'exécution."
    )"""

    parser.add_argument("-e", "--equilibres",nargs='+', type=str, choices=["PBE","Commit", "CE", "subCE"]\
                        , help="Les équilibres qui nous intressents")
    
    parser.add_argument("-o", "--output",type=str, help="Outupt directory")

    #Pour le calcule de graphiques

    # Analyser les arguments
    args = parser.parse_args()

    # Sélectionner l'opération en fonction de l'argument
    if args.operation == "affichage":
        result = args.nombre1 + args.nombre2
        operation = "addition"
    elif args.operation == "multi":
        result = args.nombre1 - args.nombre2
        operation = "soustraction"
    elif args.operation == "detailed":
        result = args.nombre1 * args.nombre2
        operation = "multiplication"
    else:
        print("Opération non reconnue.")
        sys.exit(1)

    # Afficher le résultat
    if args.verbose:
        print(f"Opération : {operation} ({args.nombre1}, {args.nombre2}) = {result}")
    else:
        print(f"Résultat : {result}")

    # Importer le module dynamique
    module_name = args.module
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"Erreur : Le module '{module_name}' n'a pas été trouvé.")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur lors de l'importation du module '{module_name}': {e}")
        sys.exit(1)

    # Préparer les arguments à passer au module
    params = {
        'param': args.param,
        'file': args.file
    }

    # Appeler une fonction 'main' dans le module, si elle existe
    if hasattr(module, "main"):
        if args.verbose:
            print(f"Exécution du module '{module_name}' avec les paramètres : {params}")
        module.main(**params)
    else:
        print(f"Le module '{module_name}' n'a pas de fonction 'main' à exécuter.")