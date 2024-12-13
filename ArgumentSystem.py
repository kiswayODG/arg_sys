from typing import List, Tuple
import itertools


class ArgumentSystem:

    arguments: List[str] = [] 
    all_ensemble_possible = [] 
    attaques: List[Tuple[str, str]] = []
    without_conflict: List[List[str]] = []
    admissible: List[List[str]] = []
    complete_ext: List[List[str]] = []



    def add_argument(arg: str) -> None:
        if not isinstance(arg, str):
        raise ValueError("L'argument doit être une chaîne de caractères.")
    arguments.append(arg)
    
    
    def generate_all_ensemble():
        ArgumentSystem.all_ensemble_possible = chain.from_iterable(combinations(arguments, ensemble_taille)\
        for r in range(len(arguments) + 1))
        

    def add_attaq(arg1: str, arg2: str) -> None:
    if not (isinstance(arg1, str) and isinstance(arg2, str)):
        raise ValueError("Les arguments d'une attaque doivent être des chaînes de caractères.")
    if arg1 not in arguments or arg2 not in arguments:
        raise ValueError("Les arguments d'une attaque doivent être déjà présents dans la liste des arguments.")
    attaques.append((arg1, arg2))
    

    def is_without_conflict(ensemble):
       for arg1 in ensemble:
            for arg2 in ensemble:
                if (arg1, arg2) in ArgumentSystem.attaques:
                    return False
        return True
    
    
    def is_admissible(ensemble):
        if not is_without_conflict(ensemble):
            return False
    
        for aj in ensemble:
            # les attaquants de aj
            attaquants = [ai for ai, cible in ArgumentSystem.attaques if cible == aj]

            for ai in attaquants:
                if not any((ak, ai) in ArgumentSystem.attaques for ak in ensemble):
                    return False

        return True
    
    def is_complete(ensemble):
        if not is_admissible(ensemble):
            return False
        
                 
    
    
