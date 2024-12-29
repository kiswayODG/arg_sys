import copy
from utilities import Label


def find_stable_extensions(Lab, arguments, attacks, Estable):
    while any(Lab[y] == Label.BLANK for y in arguments):
        y = select_argument(Lab, arguments, attacks)

        Lab_prime = copy.deepcopy(Lab)
        Lab_prime[y] = Label.IN
        for z in attacks[y]:
            Lab_prime[z] = Label.OUT

        for z in [arg for arg in attacks if y in attacks[arg]]:
            if Lab_prime[z] == Label.BLANK:
                Lab_prime[z] = Label.MUST_OUT
                
            if not any(Lab_prime[w] == Label.BLANK for w in attacks[z]):
                    Lab[y] = Label.MUST_OUT
        find_stable_extensions(Lab_prime, arguments, attacks, Estable)

        if any(Lab[z] == Label.BLANK for z in find_attackers(y,attacks)):
            Lab[y] = Label.MUST_OUT
        else:
            Lab = Lab_prime

    if all(Lab[x] != Label.MUST_OUT for x in arguments):
        extension = {x for x in arguments if Lab[x] == Label.IN}
        if all(Lab[x] != Label.MUST_OUT for x in arguments):
            if extension not in Estable: Estable.append(extension)
            
            
      
def find_complete_extensions(Lab,arguments,attacks,Ecomplete):
    
        if not any(Lab[y] == Label.MUST_OUT for y in arguments):
          
            if not any(Lab[x] in {Label.UNDEC, Label.BLANK} and 
                       all(Lab[z] == Label.OUT for z in find_attackers(x, attacks)) for x in arguments):
                # Construire l'extension actuelle
                S = {w for w in arguments if Lab[w] == Label.IN}
                Ecomplete.append(S)

        while any(Lab[y] == Label.BLANK for y in arguments):
            y = select_argument(Lab, arguments, attacks)

            # Créer une copie et propager IN et OUT
            Lab_prime = copy.deepcopy(Lab)
            Lab_prime[y] = Label.IN
            for z in attacks[y]:
                Lab_prime[z] = Label.OUT

            for z in [arg for arg in attacks if y in attacks[arg]]:
                if Lab_prime[z] in {Label.UNDEC, Label.BLANK}:
                    Lab_prime[z] = Label.MUST_OUT

                if not any(Lab_prime[w] == Label.BLANK for w in attacks[z]):
                    Lab[y] = Label.UNDEC

            find_complete_extensions(Lab_prime,arguments,attacks,Ecomplete)

            if any(Lab[z] in {Label.BLANK, Label.UNDEC} for z in attacks[y]):
                Lab[y] = Label.UNDEC
            else:
                Lab = Lab_prime


def select_argument(Lab, arguments, attacks):
    """
    Sélectionner un argument y selon les règles données.
    """
    
    # Règle 1 : Trouver un argument y tel que Lab(y) = BLANK et ∀z ∈ {y}- Lab(z) ∈ {OUT, MUST_OUT}.
    for y in arguments:
        if Lab[y] == Label.BLANK:
            attackers = [z for z in attacks if y in attacks[z]]
            if all(Lab[z] in {Label.OUT, Label.MUST_OUT} for z in attackers):
                return y

    # Règle 2 : Si aucune règle 1 ne s'applique, sélectionner y avec Lab(y) = BLANK
    # tel que |{x : x ∈ {y}+ ∧ Lab(x) ≠ OUT}| est maximal.
    def count_non_out(y):
        return sum(1 for x in attacks.get(y, set()) if Lab[x] != Label.OUT)

    candidates = [y for y in arguments if Lab[y] == Label.BLANK]
    if candidates:
        return max(candidates, key=lambda y: count_non_out(y))


def find_attackers(x, attacks):
    attackers = {arg for arg, targets in attacks.items() if x in targets}
    return attackers