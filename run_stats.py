from code.stats.stats_parity import get_parallel_stats

if __name__ == '__main__':
    dims = range(4, 9)
    epsilons = [0.05]
    deltas = [0.4, 0.3, 0.2, 0.1, 0.075, 0.05, 0.02, 0.01]
    
    for n in dims:
        for epsilon in epsilons:
            for delta in deltas:
                get_parallel_stats(n, epsilon, delta, range(50), 16, 2)