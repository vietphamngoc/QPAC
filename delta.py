import matplotlib.pyplot as plt
import sys
import os
import pickle

import oracle
import tnn
import utility as util
from qpac import qpac_learn

from qiskit.providers.aer import QasmSimulator, StatevectorSimulator


def retrieve_greater(n, epsilon, delta):
    directory = f"{os.getcwd()}/runs/{n}/{epsilon}_{delta}"
    aggregate = {}
    greater = {}
    i = 1
    while os.path.exists(f"{directory}/errors_{i}.txt"):
        with open(f"{directory}/errors_{i}.txt", "rb") as f:
            errors = pickle.load(f)
        for key in errors:
            err = errors[key]

            if key in aggregate:
                aggregate[key].append(err)
            else:
                aggregate[key] = [err]

            if err >= epsilon:
                greater[key] = []
        i += 1

    for key in greater:
        greater[key] = aggregate[key]

    return(greater)


def check_delta(greater, n, epsilon, delta, simulator, sv_simulator, step, runs=100):
    params = util.get_parameters(n)

    figure_directory = f"{os.getcwd()}/figures/{n}/{epsilon}_{delta}/greater"

    if not os.path.exists(figure_directory):
        os.makedirs(figure_directory)

    for key in greater:
        parts = key.split("+")
        x = bool(parts[0])
        u = parts[1]

        errors = []

        print(f"Start: {key}")

        for i in range(runs):
            if (i+1) % 10 == 0:
                print(f"{i+1}/{runs}")

            ora = oracle.Oracle(n, u, X=x, params=params)
            network = tnn.TNN(n)

            n_upd = qpac_learn(epsilon, delta, ora, network, simulator, step=step)

            if n_upd != -1:
                err = util.get_error_rate(ora, network, sv_simulator)
                errors.append(err)
            else:
                errors.append(0)

        runs_fig = plt.figure(layout="tight")
        plt.rc("font", size=15)
        plt.plot(range(runs), [epsilon for i in range(runs)], color="r")
        plt.scatter(range(runs), errors, marker="+")
        plt.xlabel("run")
        plt.xticks([])
        # plt.ylabel("error rate")
        # plt.title(f"Error rate for {key} over {runs} runs with d={delta}")
        # plt.legend(loc="upper right", bbox_to_anchor=(1,0.9))
        plt.savefig(f"{figure_directory}/{key}_{runs}runs.png")

if __name__ == '__main__':
    n = int(sys.argv[1])
    epsilon = float(sys.argv[2])
    delta = float(sys.argv[3])

    if len(sys.argv) == 5:
        runs = int(sys.argv[4])
    else:
        runs = 100

    simulator = QasmSimulator()
    sv_simulator = StatevectorSimulator()

    greater = retrieve_greater(n, epsilon, delta)

    if greater == {}:
        print("All good")
    else:
        print("Plotting")
        check_delta(greater, n, epsilon, delta, simulator, sv_simulator, step=1, runs=runs)
