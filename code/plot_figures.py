import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import pickle


def plot_figure(data, save_directory, metric, mode="run"):
    x, y = zip(*data.items())

    plt.figure(layout="tight")

    if metric == "errors":
        plt.plot([epsilon for i in x], c="r")

    if mode == "run":
        plt.scatter(x, y, c="g", marker="o")

    else:
        plt.violinplot(y, positions=range(len(x)))

    plt.xlabel("function")

    if metric == "errors":
        plt.ylabel("error rate")
    else:
        plt.ylabel("number of updates")

    plt.xticks(range(len(x)), labels=x, rotation=45, fontsize='small', ha='center')

    plt.savefig(save_directory)


def collect(data_directory, metric):
    collection = {}
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
    
    return(collection)

def stats(data_directory, metric):
    collection = collect(data_directory, metric)
    mean = {}
    std = {}

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
        return(collect(data_directory, metric))
    

if __name__ == '__main__':
    concept = sys.argv[1]
    n = sys.argv[2]
    epsilon = float(sys.argv[3])
    delta = float(sys.argv[4])
    step = int(sys.argv[5])
    mode = sys.argv[6]
    if mode not in ["run", "mean"]:
        raise ValueError("6th argument must be either 'run' or 'mean'")
    
    os.chdir("../")

    data_directory = f"{os.getcwd()}/results/{concept}/runs/{n}/{epsilon}_{delta}_{step}"
    figure_directory = f"{os.getcwd()}/results/{concept}/figures/{n}/{epsilon}_{delta}_{step}"

    for metric in ["errors", "updates"]:
        save_directory = f"{figure_directory}/{metric}"
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        if mode == "run":
            run_id = sys.argv[7]
            data = get_data(data_directory, metric, mode, run_id=run_id)
            fig_file = f"{save_directory}/run_{run_id}.png"
        else:
            data = get_data(data_directory, metric, mode)
            fig_file = f"{save_directory}/mean.png"
        plot_figure(data, fig_file, metric, mode)

