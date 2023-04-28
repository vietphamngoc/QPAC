import sys
import os

from figures.plot_figures import get_data, plot_figure

if __name__ == '__main__':
    concept = sys.argv[1]
    n = sys.argv[2]
    epsilon = float(sys.argv[3])
    delta = float(sys.argv[4])
    step = int(sys.argv[5])
    mode = sys.argv[6]
    if mode not in ["run", "all"]:
        raise ValueError("6th argument must be either 'run' or 'all'")
    
    script_directory = os.path.dirname(__file__)
    os.chdir(script_directory)
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
            fig_file = f"{save_directory}/all.png"
        plot_figure(data, fig_file, metric, mode=mode, epsilon=epsilon)