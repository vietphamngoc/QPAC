import utility as util

from tnn import TNN

def get_updates(measurements: dict, **kwargs)->list:
    """
    Function implementing the update strategy to learn the target concept.

    Arguments:
        - network: TNN, the network being tuned to learn the target concept
        - errors: list, the list of inputs measured as erroneous

    Returns:
        A list of gates to be switched
    """
    network = kwargs['network']
    n = network.dim
    errors = []
    for l in measurements['errors']:
        errors += l
    to_update = [errors[0]]
    active = [util.str_to_ones(k) for k,v in network.gates.items() if v == 1]

    if len(active) > 1 and ["0"*n] not in active:
        return(["0"*n])

    for error in errors:
        if error == set():
            return(["0"*n])
        all_empty = True
        for i in range(len(to_update)):
            inter = error & to_update[i]
            if inter != set():
                to_update[i] = inter
                all_empty = False
        if all_empty == True:
            to_update.append(errors)

    additional_gates = []
    for g in to_update:
        if network.gates[util.ones_to_str(g, n)] == 0:
            for a in active:
                if g.intersection(a) != set():
                    if g.intersection(a) == g:
                        if a not in additional_gates:
                            additional_gates.append(a)
                    else:
                        return(["0"*n])
    to_update = to_update + additional_gates

    return(to_update)


def get_parity_updates(measurements: dict, **kwargs)->list:
    number = kwargs['group']
    to_update = measurements['errors'][1]

    def compare_and_update(l1, l2):
        for a in l1:
            for b in l2:
                if a < b:
                    c = b - a
                    if c not in to_update:
                        to_update.append(c)

    for i in range(1, number):
        compare_and_update(measurements['errors'][i], measurements['corrects'][i+1])
        compare_and_update(measurements['errors'][-1-i], measurements['corrects'][-i])
        compare_and_update(measurements['corrects'][i], measurements['errors'][i+1])
        compare_and_update(measurements['corrects'][-1-i], measurements['errors'][-i])
    
    return(to_update)

    

