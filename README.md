This project is an implementation of tunable neural network in the QPAC-learning framework. The theoretical details can be found in the following paper: https://arxiv.org/abs/2205.01514.

It contains 2 classes:
- Oracle in oracle.py which implements the query oracle.
- TNN in tnn.py which implements the tunable neural network.

The learning algorithm is implemented in qpac.py with the update strategy for the class of concept described in the paper being implemented in update_strategy.py.

delta.py, stats.py and plot_figures.py are scripts used to analyze the performances of the implementation.
