import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import pickle


def plot_run(n, epsilon, delta, concept="", run_id=1):
    if concept !="":
        run_root = concept + "_runs"
        figure_root = concept + "_figures"
    else:
        run_root = "runs"
        figure_root = "figures"
    run_directory = f"{os.getcwd()}/{run_root}/{n}/{epsilon}_{delta}"
    errors_directory = f"{os.getcwd()}/{figure_root}/{n}/{epsilon}_{delta}/errors"
    upds_directory = f"{os.getcwd()}/{figure_root}/{n}/{epsilon}_{delta}/updates"

    if not os.path.exists(errors_directory):
        os.makedirs(errors_directory)

    if not os.path.exists(upds_directory):
        os.makedirs(upds_directory)

    with open(f"{run_directory}/errors_{run_id}.txt", "rb") as f:
        errors = pickle.load(f)

    err_labels = []
    for key in errors:
        if errors[key] >= epsilon:
            err_labels.append(key)

    with open(f"{run_directory}/updates_{run_id}.txt", "rb") as f:
        upds = pickle.load(f)

    upd_labels = []
    for key in upds:
        if upds[key] == -1:
            upd_labels.append(key)

    plt.rc("font", size=15)

    error_fig = plt.figure(layout="tight")
    x, y = zip(*errors.items())
    plt.plot(x, [epsilon for i in x], color="r")
    plt.scatter(x, y, marker="+")
    c = 0
    for f in err_labels:
        plt.scatter(f, errors[f], marker="+", label=f)
        c += 1
    plt.xlabel("function")
    # plt.ylabel("error rate")
    plt.xticks([], rotation=45, ha="right")
    plt.legend(loc="upper right", bbox_to_anchor=(1,0.8))
    plt.savefig(f"{errors_directory}/run_{run_id}.png")

    upd_fig = plt.figure(layout="tight")
    x, y = zip(*upds.items())
    plt.rc("ytick", labelsize=10)
    plt.rc('legend', fontsize=12)
    plt.scatter(x, y, marker="+")
    c = 0
    for f in upd_labels:
        plt.scatter(f, -1, marker="+", label=f)
        c += 1
    # plt.xlabel("function")
    # plt.ylabel("N")
    plt.yticks([-1, 0, 1, max(y)])
    # plt.xticks(upd_labels, rotation=45, ha="right")
    if len(upd_labels) > 0:
        plt.legend(loc="upper right", bbox_to_anchor=(1,0.8))
    plt.xticks([], rotation=45, ha="right")
    plt.savefig(f"{upds_directory}/run_{run_id}.png")

if __name__ == '__main__':
    n = int(sys.argv[1])
    epsilon = float(sys.argv[2])
    delta = float(sys.argv[3])
    run_id = int(sys.argv[4])
    if len(sys.argv) == 6:
        concept = sys.argv[5]
    else:
        concept = ""
    
    plot_run(n, epsilon, delta, concept, run_id)
