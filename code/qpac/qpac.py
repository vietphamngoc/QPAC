import numpy as np
import types

import utilities.utility as util
import circuits.qaa as qaa

from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import QasmSimulator

from circuits.oracle import Oracle
from circuits.tnn import TNN


simulator = QasmSimulator()

def qpac_learn( epsilon: float, delta: float, ora: Oracle, tun_net: TNN,
                update_function: types.FunctionType, cut: int=100, step: int= 1):
    """
    Function performing the learning in the QPAC framework.

    Arguments:
        - epsilon: float, the error threshold
        - delta: float, the probability threshold
        - ora: Oracle, the query oracle for the target concept
        - tun_net: TNN, the network to be tuned
        - cut: int (default=100), the cut off threshold
        - step: int (default=1), the increment step size

    Returns:
        - The number of updates needed to reach the QPAC target
    """
    if step < 1:
        raise ValueError("step must be greater or equal to 1")

    n = ora.dim

    N = 2*(np.ceil(1/(np.pi*delta**2))//2)+2
    m_max = int(np.ceil(0.5*((np.pi/(4*np.arcsin(np.sqrt(epsilon/5)))) - 1)))

    # Setting the schedule for the number of oracle iterations
    if step == 1:
        schedule = range(m_max+1)
    else:
        schedule = [0]
        k = 0
        m = int(np.floor(step**k))
        while m < m_max:
            if m not in schedule:
                schedule.append(m)
            k += 1
            m = int(np.floor(step**k))
        schedule.append(m_max)

    i = -1
    s = 0
    n_update = 0
    m = 0
    measurements = {}
    measurements['errors'] = [[] for k in range(n+1)]
    measurements['corrects'] = [[] for k in range(n+1)]
    measured = []

    # Stops when m >= m_max and s <= N/2, that is when error less than epsilon
    while m < m_max or s > N/2:
        i += 1
        m = schedule[i]
        s = 0

        tun_net.generate_network()

        diffusion = qaa.get_diffusion_operator(ora, tun_net)

        # Creating the circuit
        qr = QuantumRegister(n, 'x')
        qar = QuantumRegister(2, 'a')
        cr = ClassicalRegister(n)
        car = ClassicalRegister(2)
        qc = QuantumCircuit(qr, qar, cr, car)

        # Applying the oracle, the network and scaling down
        qc.append(ora.gate, range(n+1))
        qc.append(tun_net.network, range(n+1))
        qc.cry(2*np.arcsin(1/np.sqrt(5)), qar[0], qar[1])

        # Applying amplitude amplification
        for k in range(m):
            qc.append(diffusion, range(n+2))

        # Measuring
        qc.measure(qr, cr)
        qc.measure(qar, car)

        # Running the circuit
        compiled_circuit = transpile(qc, simulator)
        job = simulator.run(compiled_circuit, shots=N)
        result = job.result()
        counts = result.get_counts(compiled_circuit)

        # Getting the errors and corrects and counting the errors
        for sample in counts:
            ones = util.str_to_ones(sample[3:][::-1])
            l = len(ones)
            if sample[0:2] == "11":
                s += counts[sample]
                if ones not in measured:
                    measurements["errors"][l].append(ones)
                    measured.append(ones)
            if sample[0:2] == "00":
                if ones not in measured:
                    measurements["corrects"][l].append(ones)
                    measured.append(ones)

        # If s > N/2 the error is greater than epsilon so update circuit and start new cycle 
        if s > N/2:
            to_update = update_function(measurements, network=tun_net, group=4)
            if to_update != []:
                tun_net.update_tnn(to_update)
                n_update += 1
                measurements = {}
                measurements['errors'] = [[] for k in range(n+1)]
                measurements['corrects'] = [[] for k in range(n+1)]
                measured = []
            i = -1

        if n_update==cut:
            return(-1)
    return(n_update)
