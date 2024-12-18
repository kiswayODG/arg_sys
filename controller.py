import sys
from computing_methods import find_stable_extensions,find_complete_extensions
from utilities import file_reader
import random


arguments = [] 
attaques = []


def process_se_co():
    
    lab = initialize_lab(arguments)
    completes = []
    find_complete_extensions(lab, arguments, attaques, completes)   
    ensemble_au_hasard = choose_random_extension(completes)
    if ensemble_au_hasard:
        print(ensemble_au_hasard)

def process_se_st():
    
    lab = initialize_lab(arguments)
    estables = []
    find_stable_extensions(lab, arguments, attaques, estables)   
    ensemble_au_hasard = choose_random_extension(estables)
    if ensemble_au_hasard:
        print(ensemble_au_hasard)

def process_dc_co(argument):
    
    lab = initialize_lab(arguments)
    completes = []
    find_complete_extensions(lab, arguments, attaques, completes)
    if check_argument_in_extensions(argument, completes):
        print('YES')
    else:
        print('No')

def process_ds_co(arg):
    
    lab = initialize_lab(arguments)
    completes = []
    find_stable_extensions(lab, arguments, attaques, completes)
   
    for comp in completes:
        if arg not in comp:
            print('YES')
            return
    print('No')

def process_dc_st(argument):
    
    lab = initialize_lab(arguments)
    estables = []
    find_stable_extensions(lab, arguments, attaques, estables)
    if check_argument_in_extensions(argument, estables):
        print('YES')
    else:
        print('No')
        

def process_ds_st(argument):
    
    lab = initialize_lab(arguments)
    estables = []
    find_stable_extensions(lab, arguments, attaques, estables) 
   
    for stable in estables:
        if argument not in stable:
            print('No')
            return
    print('Yes')


def handle_parameters(args):

    global arguments, attaques 
    arguments, attaques = file_reader(args.file)

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

        # Vérification si le paramètre existe dans le dictionnaire
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
    return {arg: "BLANK" for arg in arguments}

def check_argument_in_extensions(argument, extensions):
    for ext in extensions:
        if argument in ext:
            return True
    return False

def choose_random_extension(extensions):
    if len(extensions) > 0:
        return random.choice(extensions)
    return None