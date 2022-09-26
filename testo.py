import oracle
import tnn
from utility import *
from qpac import qpac_learn

from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator, StatevectorSimulator

n = 8
epsilon = 0.001
delta = 0.3

simulator = QasmSimulator()
sv_simulator = StatevectorSimulator()

params = get_parameters(n)

ora = oracle.Oracle(n, ["11011001", "00000000"], params)

tun_network = tnn.TNN(n)

n = qpac_learn(epsilon, delta, ora, tun_network, simulator)
err = get_error_rate(ora, tun_network, sv_simulator)

print(f"gates:{[k for k,v in tun_network.gates.items() if v == 1]}, error:{err}, updates:{n}")
