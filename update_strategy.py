import utility as util

from tnn import TNN

def get_updates(network: TNN, errors: list)->list:
    """
    Function implementing the update strategy to learn the target concept.

    Arguments:
        - network: TNN, the network being tuned to learn the target concept
        - errors: list, the list of inputs measured as erroneous

    Returns:
        A list of gates to be switched
    """
    n = network.dim
    ones = util.str_to_ones(errors[0])
    to_update = [ones]
    active = [util.str_to_ones(k) for k,v in network.gates.items() if v == 1]

    if len(active) > 1 and ["0"*n] not in active:
        return(["0"*n])

    for error in errors:
        ones = util.str_to_ones(error)
        if ones == set():
            return(["0"*n])
        all_empty = True
        for i in range(len(to_update)):
            inter = ones.intersection(to_update[i])
            if inter != set():
                to_update[i] = inter
                all_empty = False
        if all_empty == True:
            to_update.append(ones)

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

    return([util.ones_to_str(k, n) for k in to_update])
