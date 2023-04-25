import sys
import os
import pickle

import utilities.utility as util

from circuits.oracle import Oracle
from circuits.tnn import TNN
from qpac.qpac import qpac_learn


def get_stats(  n: int, epsilon: float, delta: float, runs: int, number: int=0,
                step: int=1):
    print("Start")

    params = util.get_parameters(n)

    U = util.get_functions(n, number)

    run_directory = f"{os.getcwd()}/runs/{n}/{epsilon}_{delta}"

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
            for x in [False, True]:
                key = f"{int(x)}+{u}"
                logic = [u]
                if x:
                    logic.append("0"*n)

                if key not in errors or key not in ns_update:
                    # print(f"Function: {key}")
                    ora = Oracle(n, logic, params=params)
                    tun_net = TNN(n)

                    n_update = qpac_learn(  epsilon, delta, ora, tun_net,
                                            step=step)

                    ns_update[key] = n_update

                    # active = [k for k,v in tun_net.gates.items() if v==1]
                    # print(f"Final gates: {active}\n")

                    if n_update != -1:
                        err = util.get_error_rate(ora, tun_net)
                        errors[key] = err
                    else:
                        print(key)
                        errors[key] = 0
        with open(error_file, "wb") as f:
            pickle.dump(errors, f)
        with open(upd_file, "wb") as f:
            pickle.dump(ns_update, f)

