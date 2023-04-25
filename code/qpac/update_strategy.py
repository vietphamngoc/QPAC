import utilities.utility as util

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
    
    active = [util.str_to_ones(k) for k,v in network.gates.items() if v == 1]

    def get_intersections(meas):
        collection = []
        for l in meas:
            collection += l

        if collection != []:
            intersections = [collection[0]]
            for s in collection[1:]:
                all_empty = True
                for i in range(len(intersections)):
                    inter = s & intersections[i]
                    if inter != set():
                        intersections[i] = inter
                        all_empty = False
                if all_empty:
                    intersections.append(s)
            return(intersections)
        else:
            return []
    
    errors_inter = get_intersections(measurements['errors'])
    corrects_inter = get_intersections(measurements['corrects'])

    to_update = []
    add_0 = False

    if len(errors_inter) == 1:
        to_update = errors_inter
    elif len(corrects_inter) == 1:
        to_update = corrects_inter
        add_0 = True
    
    if to_update != []:
        for g in active:
            if g != set():
                inter = to_update[0] & g
                if inter != g:
                    to_update[0] = inter
                    to_update.append(g)
                else:
                    to_update = []

    if add_0:    
        to_update.append(set())
    
    return to_update
    

def get_parity_updates(measurements: dict, **kwargs)->list:
    l = len(measurements['errors'])
    to_update = measurements['errors'][1]

    def compare_and_update(l1, l2):
        for a in l1:
            for b in l2:
                if a < b:
                    c = b - a
                    if c not in to_update:
                        to_update.append(c)

    for i in range(1, l-1):
        compare_and_update(measurements['errors'][i], measurements['corrects'][i+1])
        compare_and_update(measurements['corrects'][i], measurements['errors'][i+1])
    
    return to_update

    

