from collections import defaultdict
import sys
from enum import Enum
import argparse

class Label(Enum):
    BLANK = 0
    IN = 1
    OUT = 2
    UNDEC = 3
    MUST_OUT = 4
    
'''
class semantic(Enum):
    COMP='complete'
    ST='stable'
    PR='prefered'
    GR='Grounded'
''' 
    
def file_reader(file_path):
    arguments = set()
    attacks = defaultdict(set)
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('arg(') and line.endswith(').'):
                    arg = line[4:-2]
                    arguments.add(arg)
                elif line.startswith('att(') and line.endswith(').'):
                    att = line[4:-2].split(',')
                    attacks[att[0]].add(att[1])
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{file_path}' est introuvable.")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue : {str(e)}")
        sys.exit(1)

    return arguments, attacks

def parse_arguments():
    """
    Fonction dédiée pour parser les arguments depuis la ligne de commande.
    """
    parser = argparse.ArgumentParser(
        description="Programme de traitement pour différentes sémantiques d'Argumentation Framework (AF)"
    )
    
    parser.add_argument("-p", "--parameter", type=str, required=True,
                        help="Type de sémantique (SE-CO, SE-ST, DC-CO, DS-CO, DC-ST, DS-ST)")
    parser.add_argument("-f", "--file", type=str, required=True,
                        help="Chemin vers le fichier AF")
    parser.add_argument("-a", "--argument", type=str, required=False,
                        help="Nom de l'argument de la requête (obligatoire pour DC/DS)")

    return parser.parse_args()