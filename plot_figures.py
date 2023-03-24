import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import pickle


def plot_figure(data, save_directory, metric, mode="run", **kwargs):
    x, y = zip(*data.items())

    plt.figure(layout="tight")

    if metric == "errors":
        plt.plot(x, [epsilon for i in x], c="r")

    plt.scatter(x, y, c="g", marker="o")

    if mode == "mean":
        xe, ye = zip(*kwargs['std'].items())
        plt.errorbar(x, y, yerr=ye, ecolor="black", fmt="o", mfc="g", capsize=5)

    plt.xlabel("function")

    if metric == "errors":
        plt.ylabel("error rate")
    else:
        plt.ylabel("number of updates")

    plt.xticks(x, rotation=45, fontsize='small', ha='center')

    plt.savefig(save_directory)


def stats(data_directory, metric):
    collection = {}
    mean = {}
    std = {}
    files = []

    for f in os.listdir(data_directory):
        if metric in f:
            files.append(f)

    with open(f"{data_directory}/{files[0]}", "rb") as f:
        data = pickle.load(f)
    for k in data:
        collection[k] = [data[k]]

    for i in range(1,len(files)):
        with open(f"{data_directory}/{files[i]}", "rb") as f:
            data = pickle.load(f)
        for k in data:
            collection[k].append(data[k])

    for k in collection:
        mean[k] = np.mean(collection[k])
        std[k] = np.std(collection[k])
    
    return(mean, std)


def get_data(data_directory, metric, mode, **kwargs):
    if mode == "run":
        run_id = kwargs["run_id"]
        with open(f"{data_directory}/{metric}_{run_id}.txt", "rb") as f:
            data = pickle.load(f)
        return(data)
    else:
        return(stats(data_directory, metric))
    

if __name__ == '__main__':
    concept = sys.argv[1]
    n = sys.argv[2]
    epsilon = float(sys.argv[3])
    delta = float(sys.argv[4])
    mode = sys.argv[5]
    if mode not in ["run", "mean"]:
        raise ValueError("5th argument must be either 'run' or 'mean'")

    data_directory = f"{os.getcwd()}/{concept}_runs/{n}/{epsilon}_{delta}"
    figure_directory = f"{os.getcwd()}/{concept}_figures/{n}/{epsilon}_{delta}"


    if mode == "run":
        run_id = sys.argv[6]

        for metric in ["errors", "updates"]:
            data = get_data(data_directory, metric, mode, run_id=run_id)
            directory = f"{figure_directory}/{metric}"
            if not os.path.exists(directory):
                os.makedirs(directory)
            fig_file = f"{directory}/run_{run_id}.png"
            plot_figure(data, fig_file, metric, mode)

    else:
        for metric in ["errors", "updates"]:
            mean, std = get_data(data_directory, metric, mode)
            directory = f"{figure_directory}/{metric}"
            if not os.path.exists(directory):
                os.makedirs(directory)
            fig_file = f"{directory}/mean.png"
            plot_figure(mean, fig_file, metric, mode, std=std)
