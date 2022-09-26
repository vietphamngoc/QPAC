import numpy as np
import matplotlib.pyplot as plt
import random
import sys
import os
import pickle

import oracle
import tnn
import utility as util
from qpac import qpac_learn

from qiskit.providers.aer import QasmSimulator, StatevectorSimulator


def get_stats(n, epsilon, delta, runs, number=0, step=2):
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
                    ora = oracle.Oracle(n, logic, params=params)
                    network = tnn.TNN(n)

                    n_update = qpac_learn(epsilon, delta, ora, network, simulator, step=step)

                    ns_update[key] = n_update

                    if n_update != -1:
                        err = util.get_error_rate(ora, network, sv_simulator)
                        errors[key] = err
                    else:
                        print(key)
                        errors[key] = 0
        with open(error_file, "wb") as f:
            pickle.dump(errors, f)
        with open(upd_file, "wb") as f:
            pickle.dump(ns_update, f)


if __name__ == '__main__':
    n = int(sys.argv[1])
    epsilon = float(sys.argv[2])
    delta = float(sys.argv[3])
    run = int(sys.argv[4])

    if len(sys.argv) == 5:
        number = 0
    elif len(sys.argv) == 6:
        number = int(sys.argv[5])
    else:
        raise ValueError("Invalid number of arguments")


    simulator = QasmSimulator()
    sv_simulator = StatevectorSimulator()

    get_stats(n, epsilon, delta, run, number=number, step=2)
