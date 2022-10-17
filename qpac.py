import numpy as np

from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.providers.aer import QasmSimulator

import utility as util

def qpac_learn(epsilon, delta, oracle, tnn, simulator, cut=100, step = 1):
    if step < 1:
        raise ValueError("step must be greater or equal to 1")

    n = oracle.dim

    N = 2*(np.ceil(1/(np.pi*delta**2))//2)+2
    m_max = int(np.ceil(0.5*((np.pi/(4*np.arcsin(np.sqrt(epsilon/5)))) - 1)))

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
    errors = []

    while m < m_max or s > N/2:
        i += 1
        m = schedule[i]
        s = 0

        tnn.generate_network()

        diffusion = util.get_diffusion_operator(oracle, tnn)

        # Creating the circuit
        qr = QuantumRegister(n, 'x')
        qar = QuantumRegister(2, 'a')
        cr = ClassicalRegister(n)
        car = ClassicalRegister(2)
        qc = QuantumCircuit(qr, qar, cr, car)

        # Applying the oracle, the network and scaling down
        qc.append(oracle.gate, range(n+1))
        qc.append(tnn.network, range(n+1))
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

        # Getting and counting the errors
        # errors = []
        for sample in counts:
            if sample[0:2] == "11":
                s += counts[sample]
                rev = sample[3:][::-1]
                if rev not in errors:
                    errors.append(rev)

        if s > N/2:
            to_update = util.get_updates(tnn, errors)
            tnn.update_tnn(to_update)
            active = [k for k,v in tnn.gates.items() if v==1]
            n_update += 1
            i = -1
            errors = []

        if n_update==cut:
            return(-1)
    return(n_update)
