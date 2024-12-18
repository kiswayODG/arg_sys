import copy


def find_stable_extensions(Lab, arguments, attacks, Estable):
    while any(Lab[y] == "BLANK" for y in arguments):
        y = select_argument(Lab, arguments, attacks)

        Lab_prime = copy.deepcopy(Lab)
        Lab_prime[y] = "IN"
        for z in attacks[y]:
            Lab_prime[z] = "OUT"

        for z in [arg for arg in attacks if y in attacks[arg]]:
            if Lab_prime[z] == "BLANK":
                Lab_prime[z] = "MUST_OUT"
        
        find_stable_extensions(Lab_prime, arguments, attacks, Estable)

        if any(Lab[z] == "BLANK" for z in attacks[y]):
            Lab[y] = "MUST_OUT"
        else:
            Lab = Lab_prime

    if all(Lab[x] != "MUST_OUT" for x in arguments):
        extension = {x for x in arguments if Lab[x] == "IN"}
        if is_stable_extension(extension, arguments, attacks):
            Estable.append(extension)
            
            
def find_complete_extensions(Lab,arguments,attacks,Ecomplete):
    
        if not any(Lab[y] == "MUST_OUT" for y in arguments):
            if not any(Lab[x] in {"UNDEC", "BLANK"} and 
                       all(Lab[z] == "OUT" for z in attacks[x]) for x in arguments):
                # Construire l'extension actuelle
                S = {w for w in arguments if Lab[w] == "IN"}
                Ecomplete.append(S)

        while any(Lab[y] == "BLANK" for y in arguments):
            y = select_argument(Lab, arguments, attacks)

            # Créer une copie et propager IN et OUT
            Lab_prime = copy.deepcopy(Lab)
            Lab_prime[y] = "IN"
            for z in attacks[y]:
                Lab_prime[z] = "OUT"

            for z in [arg for arg in attacks if y in attacks[arg]]:
                if Lab_prime[z] in {"UNDEC", "BLANK"}:
                    Lab_prime[z] = "MUST_OUT"

                if not any(Lab_prime[w] == "BLANK" for w in attacks[z]):
                    Lab[y] = "UNDEC"

            find_complete_extensions(Lab_prime,arguments,attacks,Ecomplete)

            if any(Lab[z] in {"BLANK", "UNDEC"} for z in attacks[y]):
                Lab[y] = "UNDEC"
            else:
                Lab = Lab_prime


def select_argument(Lab, arguments, attacks):
    for y in arguments:
        if Lab[y] == "BLANK" and all(Lab[z] in {"OUT", "MUST_OUT"} for z in attacks[y]):
            return y
    return next(y for y in arguments if Lab[y] == "BLANK")

def is_stable_extension(extension, arguments, attacks):
    for arg in arguments:
        if arg not in extension:
            # Il doit être attaqué par au moins un argument IN
            if not any(attacker in extension for attacker in attacks[arg]):
                return False
    return True
