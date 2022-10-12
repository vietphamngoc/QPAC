import numpy as np
import random

from qiskit import QuantumCircuit

class Oracle:

    def __init__(self, n: int, logic: list, params: list=[]):

        if params == []:
            for i in range(n):
                params.append(random.random()*np.pi)

        if len(params) != n:
            raise ValueError(f"The length of param is {len(params)}, it should be {n}")

        self.dim = n
        self.params = params
        self.logic = logic

        qc = QuantumCircuit(n+1)
        self.apply_amplitude(qc, inverse=False)
        self.apply_function(qc)

        qc_inv = QuantumCircuit(n+1)
        self.apply_function(qc_inv)
        self.apply_amplitude(qc_inv, inverse=True)

        self.gate = qc.to_gate(label="Oracle")
        self.inv_gate = qc_inv.to_gate(label="Oracle^-1")


    def apply_amplitude(self, qc, inverse):
        for i in range(self.dim):
            qc.ry((-1)**(inverse)*self.params[i],i)


    def apply_function(self, qc):
        for u in self.logic:
            if len(u) != self.dim:
                raise ValueError(f"The length of {u} should be {self.dim}")
            if u == "0"*self.dim:
                qc.x(self.dim)
            else:
                controls = []
                for i in range(self.dim):
                    if u[i] == "1":
                        controls.append(i)
                qc.mcx(controls, self.dim)
