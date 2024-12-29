from collections import defaultdict
import sys
from enum import Enum
import argparse
import random

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

class Semantic(Enum):
    SE_CO = "SE-CO"
    SE_ST = "SE-ST"
    DC_CO = "DC-CO"
    DS_CO = "DS-CO"
    DC_ST = "DC-ST"
    DS_ST = "DS-ST"
    
from collections import defaultdict
import sys

def file_reader(file_path):
    arguments = []
    attacks = defaultdict(set)
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('arg(') and (line.endswith(').') or line.endswith(')')):
                    arg = line[4:].rstrip(').')  
                    arguments.append(arg)
                elif line.startswith('att(') and (line.endswith(').') or line.endswith(')')):
                    att = line[4:].rstrip(').').split(',')
                    if len(att) == 2:  
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

def choose_random_extension(extensions):
    type(extensions)
    try:
        if len(extensions) > 0:
            return random.choice(extensions)
    except :
        return "Reessayer inhabituelle, une erreur survenu!"

