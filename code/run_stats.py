import sys
import os

from stats.stats_parity import get_stats

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
    
    os.chdir(os.path.dirname(sys.argv[0]))
    os.chdir("../")
    
    get_stats(n, epsilon, delta, run, number=number, step=step)