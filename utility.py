import numpy as np
import pickle
import random
import os

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info.operators import Operator


def ones_to_str(ones: set, n: int)->str:
    binary = ["0" for i in range(n)]
    for i in ones:
        binary[i] = "1"
    return("".join(binary))


def str_to_ones(string: str)->set:
    ones = [i for i in range(len(string)) if string[i] == "1"]
    return(set(ones))


def get_updates(tnn, errors: list, previous: list)->list:
    n = tnn.dim
    ones = str_to_ones(errors[0])
    to_update = [ones]
    active = [str_to_ones(k) for k,v in tnn.gates.items() if v == 1]

    for error in errors:
        ones = str_to_ones(error)
        if ones == set():
            return(["0"*n])
        all_empty = True
        for i in range(len(to_update)):
            inter = ones.intersection(to_update[i])
            if inter != set():
                to_update[i] = inter
                all_empty = False
        if all_empty == True:
            to_update.append(ones)

    gates = [ones_to_str(k, n) for k in to_update]

    for g in gates:
        if tnn.gates[g] == 0:
            ones_g = set([i for i in range(n) if g[i] == "1"])
            for a in active:
                if ones_g.intersection(a) != set() and ones_g.intersection(a) != ones_g:
                    gates = ["0"*n]
                    print("prout")
                    break
    # if set(gates).intersection(previous) != set():
    #     gates = ["0"*n]
    return(gates)


def get_diffusion_operator(oracle, tnn):
    n = tnn.dim
    qc = QuantumCircuit(n+2)
    # Chi_g
    qc.cz(n, n+1)
    # A^-1
    qc.cry(-2*np.arcsin(1/np.sqrt(5)), n, n+1)
    qc.append(tnn.network, range(n+1))
    qc.append(oracle.inv_gate, range(n+1))
    # -Chi_0
    mat = -np.eye(2**(n+2))
    mat[0,0] = 1
    op = Operator(mat)
    qc.unitary(op, range(n+2), label="Chi_0")
    # A
    qc.append(oracle.gate, range(n+1))
    qc.append(tnn.network, range(n+1))
    qc.cry(2*np.arcsin(1/np.sqrt(5)), n, n+1)
    return(qc.to_gate(label="Diffusion"))


def get_custom_params(n: int, u: str, angle)->list:
    if len(u) != n:
        raise ValueError(f"Length of u is not {n}")
    params = []
    for i in range(n):
        if u[i] == "1":
            params.append(angle)
        else:
            params.append(np.pi/2)
    return(params)


def get_error_rate(oracle, tnn, simulator):
    n = oracle.dim
    rate = 0
    qc = QuantumCircuit(n+1)
    qc.append(oracle.gate, range(n+1))
    qc.append(tnn.network, range(n+1))

    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    for s in counts:
        if s[0] == "1":
            rate += counts[s]
    return(rate)


def get_parameters(n):
    directory = f"{os.getcwd()}/parameters"

    if not os.path.exists(directory):
        os.makedirs(directory)

    file = f"{directory}/parameters_{n}.txt"

    if os.path.exists(file):
        with open(file, "rb") as f:
            params = pickle.load(f)

    else :
        params = []
        for i in range(n):
            params.append(random.random()*np.pi)
        with open(file, "wb") as f:
            pickle.dump(params, f)

    return(params)


def get_functions(n, number):
    if number > 2**n:
        raise ValueError(f"number should not be greater than {2**n}")

    directory = f"{os.getcwd()}/functions"

    if not os.path.exists(directory):
        os.makedirs(directory)

    file = f"{directory}/functions_{n}_{number}.txt"

    if os.path.exists(file):
        with open(file, "rb") as f:
            U = pickle.load(f)

    else:
        U = []
        if number == 0:
            for i in range(2**n):
                U.append(np.binary_repr(i, n))
        else:
            for i in range(number):
                u = random.randint(0, 2**n-1)
                while u in U:
                    u = random.randint(0, 2**n-1)
                U.append(np.binary_repr(u, n))

        with open(file, "wb") as f:
            pickle.dump(U, f)

    return(U)
