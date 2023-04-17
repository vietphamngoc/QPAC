set dim=4 6 8
set epsilon=0.1 0.05 0.01
set delta=0.1 0.05 0.02 0.01
set step=1 2

for %%n in (%dim%) do (
    for %%e in (%epsilon%) do (
        for %%d in (%delta%) do (
            for %%s in (%step%) do (
                python stats_parity.py %%n %%e %%d %%s 50 16

                python plot_figures.py parity %%n %%e %%d %%s mean
            )
        )
    )
)


PAUSE