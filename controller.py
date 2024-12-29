import sys
from computing_methods import find_stable_extensions,find_complete_extensions
from utilities import file_reader
import random
from argSys import ArgSys
from utilities import Label

'''
On fait des print et return dans nos methodes d'appel pour les raisons suivantes: 
   le print est fait pour l'affichage au console
   et le return est fait dans le but de recuperer le resultat et l'afficher dans le contexte visuel
   mis en place à cet effet
'''

def process_se_co():
    
    lab = initialize_lab(ArgSys.arguments)
    completes = []
    find_complete_extensions(lab,ArgSys.arguments, ArgSys.attaques, completes)  
    ensemble_au_hasard = choose_random_extension(completes)
  
    if ensemble_au_hasard:
        print('\n Extension complète: ',ensemble_au_hasard, end='\n')
        print('\n======Toutes les extensions complètes========', end='\n')
        print(completes, end='\n')      
        return completes       
                                        
def process_se_st():
    
    lab = initialize_lab(ArgSys.arguments)
    estables = []
    find_stable_extensions(lab,ArgSys.arguments, ArgSys.attaques, estables) 
   
    ensemble_au_hasard = choose_random_extension(estables)
    if ensemble_au_hasard:
        print('\n Extension stable: ',ensemble_au_hasard, end='\n')
        print('\n======Toutes les extensions stables========', end='\n')
        print(estables, end='\n')
        return estables

def process_dc_co(argument):
    
    lab = initialize_lab(ArgSys.arguments)
    completes = []
    find_complete_extensions(lab,ArgSys.arguments, ArgSys.attaques, completes)
    if check_argument_in_extensions(argument, completes):
        print('Yes')
        return 'YES'
    else:
        print('No')
        return 'No'

def process_ds_co(arg):
    
    lab = initialize_lab(ArgSys.arguments)
    completes = []
    find_stable_extensions(lab,ArgSys.arguments, ArgSys.attaques, completes)
   
    for comp in completes:
        if arg not in comp:
            print('Yes')
            return 'YES'
    print('No')
    return 'No'
    

def process_dc_st(argument):
    
    lab = initialize_lab(ArgSys.arguments)
    estables = []
    find_stable_extensions(lab,ArgSys.arguments, ArgSys.attaques, estables)
    if check_argument_in_extensions(argument, estables):
        print('Yes')
        return 'YES'
    else:
        print('No')
        return 'No'
        

def process_ds_st(argument):
    
    lab = initialize_lab(ArgSys.arguments)
    estables = []
    find_stable_extensions(lab,ArgSys.arguments, ArgSys.attaques, estables) 
   
    for stable in estables:
        if argument not in stable:
            print('No')
            return 'No'
    print('Yes')
    return 'Yes'

actions_ds = {
        "DC-CO": process_dc_co,
        "DS-CO": process_ds_co,
        "DC-ST": process_dc_st,
        "DS-ST": process_ds_st
        }
        
actions_se ={
        "SE-CO": process_se_co,
        "SE-ST": process_se_st,
        }

def handle_parameters(args):

    arguments, attaques = file_reader(args.file)
    ArgSys.set_arguments(arguments)
    ArgSys.set_attaques(attaques)
    
    if args.parameter in actions_ds:
        if not args.argument:
            print(f"Erreur : L'argument '-a' est requis pour {args.parameter}.")
            sys.exit(1)
        actions_ds[args.parameter](args.argument)
            
    elif args.parameter in actions_se:
        actions_se[args.parameter]()
            
    else:
        print(f"Erreur : Le paramètre '{args.parameter}' n'est pas reconnu.")
        sys.exit(1)
        
            

def initialize_lab(arguments):
    return {arg: Label.BLANK for arg in arguments}

def check_argument_in_extensions(argument, extensions):
    for ext in extensions:
        if argument in ext:
            return True
    return False

def choose_random_extension(extensions):
    if len(extensions) > 0:
        return random.choice(extensions)
    return None


def handle_semanticfrom_screen(semantic,arg=''):
    
    if semantic in actions_ds:
        if arg=='':
            print(f"Erreur :argument obligatoire pour {semantic}.")
            sys.exit(1)
        return actions_ds[semantic](arg)
            
    elif semantic in actions_se:
        return actions_se[semantic]()