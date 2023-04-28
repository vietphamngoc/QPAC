import os
import pickle

import utilities.utility as util

from circuits.oracle import Parity_Oracle
from circuits.tnn import TNN
from qpac.qpac import qpac_learn
from qpac.update_strategy import get_parity_updates
from stats.error_rate import get_error_rate


def get_stats(  n: int, epsilon: float, delta: float, runs: int, number: int=0,
                step: int=1):

    script_directory = os.path.dirname(__file__)
    os.chdir(script_directory)
    os.chdir("../..")
    directory = f"{os.getcwd()}/results"
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)

    print(f"Saving results to: {os.getcwd()}")

    params = util.get_parameters(n)

    U = util.get_functions(n, number)

    run_directory = f"{os.getcwd()}/runs/{n}/{epsilon}_{delta}_{step}"

    if not os.path.exists(run_directory):
        os.makedirs(run_directory)

    for j in range(runs):
        print(f"Run {j+1}")

        error_file = f"{run_directory}/errors_{j+1}.txt"
        upd_file = f"{run_directory}/updates_{j+1}.txt"

        if not os.path.exists(error_file) or not os.path.exists(upd_file):
            errors = {}
            ns_update = {}

        else:
            with open(error_file, "rb") as f:
                errors = pickle.load(f)
            with open(upd_file, "rb") as f:
                ns_update = pickle.load(f)

        for i in range(len(U)):
            if (i+1) % 5 == 0:
                print(f"{i+1}/{len(U)}")
                with open(error_file, "wb") as f:
                    pickle.dump(errors, f)
                with open(upd_file, "wb") as f:
                    pickle.dump(ns_update, f)

            u = U[i]

            if u not in errors or u not in ns_update:
                ora = Parity_Oracle(n, [u], params=params)
                tun_net = TNN(n)

                n_update = qpac_learn(epsilon, delta, ora, tun_net, get_parity_updates, step=step)

                ns_update[u] = n_update


                err = get_error_rate(ora, tun_net)
                errors[u] = err

        with open(error_file, "wb") as f:
            pickle.dump(errors, f)
        with open(upd_file, "wb") as f:
            pickle.dump(ns_update, f)
