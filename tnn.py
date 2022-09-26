import numpy as np
from qiskit import QuantumCircuit


class TNN:

    def __init__(self, n: int, gates: dict={}):
        self.dim = n

        if gates == {}:
            gates = self.generate_gates()
        elif len(gates) != 2**n:
            raise ValueError(f"The length of gates is {len(gates)}, it should be {n}")
        self.gates = gates

        state = QuantumCircuit(n+1)
        self.network = state.to_gate(label="TNN")


    def generate_gates(self):
        gates = {}
        for i in range(2**(self.dim)):
            gates[np.binary_repr(i,self.dim)] = 0
        return(gates)


    def update_tnn(self, to_update: list):
        if "0"*self.dim in to_update:
            for k in self.gates:
                self.gates[k] = 0
        for g in to_update:
            if g not in self.gates:
                raise ValueError(f"{g} is not a gate")
            else:
                self.gates[g] = (self.gates[g]+1)%2


    def generate_network(self):
        qc = QuantumCircuit(self.dim+1)
        for g in self.gates:
            if self.gates[g] == 1:
                controls = []
                for i in range(self.dim):
                    if g[i] == "1":
                        controls.append(i)
                if controls == []:
                    qc.x(self.dim)
                else:
                    qc.mcx(controls, self.dim)
        self.network = qc.to_gate(label="TNN")
