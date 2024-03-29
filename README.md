This project is an implementation of tunable neural network in the QPAC-learning framework. The theoretical details can be found in the following paper: https://arxiv.org/abs/2205.01514.

The version of Qiskit used in this project is 0.34.2

It contains 2 classes:
- Oracle in circuits/oracle.py which implements the query oracle. Oracle has a subclass Parity_Oracle. The difference between the two is that for Parity_Oracle, the logic argument is a list of length 1, with the element of logic marking the significant bits of the function.
- TNN in circuits/tnn.py which implements the tunable neural network.

The learning algorithm is implemented in qpac/qpac.py.

The update strategy for the parity functions as well as another class of concepts have been implemented in qpac/update_strategy.py

circuits/qaa.py contains the quantum amplitude amplification algorithm, it takes as input the oracle and the TNN.

run_stats.py will run multiple experiments to train the TNN on the same set of randomly selected function of the class for different epsilon, delta and step size.




