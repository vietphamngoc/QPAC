import os
import pickle
import code.utilities.utility as util

from joblib import Parallel, delayed

from code.circuits.oracle import Parity_Oracle
from code.circuits.tnn import TNN
from code.qpac.qpac import qpac_learn
from code.qpac.update_strategy import get_parity_updates
from code.stats.error_rate import get_error_rate


def get_settings(n: int, number: int, epsilon: float, delta: float, step: int):
    script_directory = os.path.dirname(__file__)
    os.chdir(script_directory)
    os.chdir("../..")
    directory = f"{os.getcwd()}/results/parity"
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(directory)

    params = util.get_parameters(n)

    fcts = util.get_functions(n, number)

    run_directory = f"{os.getcwd()}/runs/{n}/{epsilon}_{delta}_{step}"

    if not os.path.exists(run_directory):
        os.makedirs(run_directory)

    return fcts, params, run_directory


def one_run(n: int, epsilon: float, delta: float, step: int, fcts: list, params: list, run_directory: str, j: int):
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

    for i in range(len(fcts)):
        if (i+1) % 5 == 0:
            print(f"run {j+1}: {i+1}/{len(fcts)}")
            with open(error_file, "wb") as f:
                pickle.dump(errors, f)
            with open(upd_file, "wb") as f:
                pickle.dump(ns_update, f)

        u = fcts[i]

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


def get_stats(n: int, epsilon: float, delta: float, runs: int, number: int=0, step: int=2):
    fcts, params, run_directory = get_settings(n, number, epsilon, delta, step)

    for j in range(runs):
        one_run(n, epsilon, delta, step, fcts, params, run_directory, j)


def get_parallel_stats(n: int, epsilon: float, delta: float, runs: int, number: int=0, step: int=2, n_jobs: int=5):
    fcts, params, run_directory = get_settings(n, number, epsilon, delta, step)

    Parallel(n_jobs=n_jobs)(delayed(one_run)(n, epsilon, delta, step, fcts, params, run_directory, j) for j in range(runs))

