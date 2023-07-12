import code.utilities.utility as util

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


def remove_and_update(bit: set, l1: list, l2: list, significant = True):
    if significant:
        l = l2
    else:
        l = l1

    for w in range(1,len(l1)):
        changed = []
        for s in l1[w]:
            if bit <= s:
                changed.append(s)

        for s in changed:
            l1[w].remove(s)
            c = s-bit
            if c not in l[w-1]:
                l[w-1].append(c)


def compare_and_add(l1, l2, new):
        for a in l1:
            for b in l2:
                if a < b:
                    c = b - a
                    if c not in new:
                        new.append(c)

    
def get_parity_updates(measurements: dict, **kwargs)->list:
    n = len(measurements['errors'])-1
    to_update = measurements['errors'][1].copy()
    
    new_significant = measurements['errors'][1].copy()

    stop = False

    for significant in new_significant:
        remove_and_update(significant, measurements['errors'], measurements['corrects'], True)
        remove_and_update(significant, measurements['corrects'], measurements['errors'], True)

    not_significant = measurements['corrects'][1].copy()

    for n_s in not_significant:
        remove_and_update(n_s, measurements['errors'], measurements['corrects'], False)
        remove_and_update(n_s, measurements['corrects'], measurements['errors'], False)

    while not stop:
        new_significant = measurements['errors'][1].copy()

        if new_significant == []:
            for i in range(1, n):
                compare_and_add(measurements['errors'][i], measurements['corrects'][i+1], new_significant)
                if new_significant != []:
                    break

                compare_and_add(measurements['corrects'][i], measurements['errors'][i+1], new_significant)
                if new_significant != []:
                    break

        if new_significant != []:
            to_update += new_significant

            for significant in new_significant:
                remove_and_update(significant, measurements['errors'], measurements['corrects'], True)
                remove_and_update(significant, measurements['corrects'], measurements['errors'], True)

        else:
            stop = True

        not_significant = measurements['corrects'][1].copy() 

        for n_s in not_significant:
            remove_and_update(n_s, measurements['errors'], measurements['corrects'], False)
            remove_and_update(n_s, measurements['corrects'], measurements['errors'], False)
                
    return to_update

    

