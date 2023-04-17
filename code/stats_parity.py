import sys
import os
import pickle

from oracle import Parity_Oracle
from tnn import TNN
from qpac import qpac_learn
from update_strategy import get_parity_updates
from error_rate import get_error_rate
import utility as util


def get_stats(  n: int, epsilon: float, delta: float, runs: int, number: int=0,
                step: int=1):
    print("Start")

    params = util.get_parameters(n)

    U = util.get_functions(n, number)

    run_directory = f"{os.getcwd()}/parity_runs/{n}/{epsilon}_{delta}_{step}"

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


if __name__ == '__main__':
    n = int(sys.argv[1])
    epsilon = float(sys.argv[2])
    delta = float(sys.argv[3])
    step = int(sys.argv[4])
    run = int(sys.argv[5])

    if len(sys.argv) == 6:
        number = 0
    elif len(sys.argv) == 7:
        number = int(sys.argv[6])
    else:
        raise ValueError("Invalid number of arguments")


    get_stats(n, epsilon, delta, run, number=number, step=step)
