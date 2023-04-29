# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 15:24:12 2023

@author: Team 5
"""

import numpy as np
import matplotlib.pyplot as plt

#import qiskit functionality
from qiskit.circuit.quantumregister import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.library.standard_gates import HGate, CZGate, RYGate

# Adding the transpiler to reduce the circuit to QASM instructions
# supported by the backend
from qiskit import transpile

# Use AerSimulator
from qiskit_aer import AerSimulator



RUN_BACKEND = 0 # 0 = simulator



# convert normalized vector to spherical variables
def angles(x, V = True):
    n = len(x)
    theta = np.zeros(n-1)
    
    for i in range(n-1):
        if i==0:
            theta[i] = np.arccos(x[i])
        else:
            tmp = x[i]
            for j in range(i):
                tmp *= 1/np.sin(theta[j])
            theta[i] = np.arccos(tmp)
            
    ### for checking correctness:
    if V:
        print("The following two should equal: ")
        print(x[-1])
        tmp = 1
        for i in range(n-1):
            tmp*=np.sin(theta[i])
        print(tmp)
        
    
    return theta






# # RBS gate -- TODO: replace by custom gate
# def apply_RBS(qc, qr, param):
#     # Apply hadamard on both qubits
#     qc.append(HGate(), [qr[0]])
#     qc.append(HGate(), [qr[1]])
#     # Apply a two qubit CZ gate
#     qc.append(CZGate(), [qr[0], qr[1]])
#     # Apply RY of pi.2 on both qubits
#     qc.append(RYGate(param/2), [qr[0]])
#     qc.append(RYGate(-param/2), [qr[1]])
#     # Apply a two qubit CZ gate
#     qc.append(CZGate(), [qr[0], qr[1]])
#     # Apply Hadamard on both qubits
#     qc.append(HGate(), [qr[0]])
#     qc.append(HGate(), [qr[1]])
    
#     qc.draw(output = 'mpl')
#     plt.show()
#     return qc



if __name__ == '__main__':
    n_q = 4
    n_shots = 10000
    
    # Create a quantum circuit with four qubits
    qr = QuantumRegister(n_q)
    qc = QuantumCircuit(qr)


    thetas = angles(np.ones(n_q)/np.sqrt(n_q), V = False)
    
    #prepares initial state: 1110 (corresponds to simple driangle)
    qc.x(0)
    #qc.x(1)
    #qc.x(2)
    
    
    #builds the circuit, fig. 2 from https://arxiv.org/pdf/2202.00054.pdf
    for ind, j in enumerate(range(2, n_q+1)):
        i = n_q-j
        qr_pair = [qr[i], qr[i+1]]
        
        #TODO - remove
        #qc = apply_RBS(qc, qr_pair, thetas[i])
    
        param = thetas[ind]
        
        qc.append(HGate(), [qr[i]])
        qc.append(HGate(), [qr[i+1]])
        # Apply a two qubit CZ gate
        qc.append(CZGate(), [qr[i], qr[i+1]])
        # Apply RY of pi.2 on both qubits
        qc.append(RYGate(param/2), [qr[i]])
        qc.append(RYGate(-param/2), [qr[i+1]])
        # Apply a two qubit CZ gate
        qc.append(CZGate(), [qr[i], qr[i+1]])
        # Apply Hadamard on both qubits
        qc.append(HGate(), [qr[i]])
        qc.append(HGate(), [qr[i+1]])
        
    
    qc.x(0)

    for ind, j in enumerate(range(2, n_q+1)):
        i = j-2
        qr_pair = [qr[i], qr[i+1]]
        
        #TODO - remove
        #qc = apply_RBS(qc, qr_pair, thetas[i])
    
        param = thetas[-ind]
        
        qc.append(HGate(), [qr[i]])
        qc.append(HGate(), [qr[i+1]])
        # Apply a two qubit CZ gate
        qc.append(CZGate(), [qr[i], qr[i+1]])
        # Apply RY of pi.2 on both qubits
        qc.append(RYGate(param/2), [qr[i]])
        qc.append(RYGate(-param/2), [qr[i+1]])
        # Apply a two qubit CZ gate
        qc.append(CZGate(), [qr[i], qr[i+1]])
        # Apply Hadamard on both qubits
        qc.append(HGate(), [qr[i]])
        qc.append(HGate(), [qr[i+1]])


    
    # Sample from the circuit
    meas = QuantumCircuit(n_q, n_q)
    meas.barrier(range(n_q))
    # map the quantum measurement to the classical bits
    meas.measure(range(n_q), range(n_q))
    
    # append the measurement to our circuit
    qc = meas.compose(qc, range(n_q), front=True)
    
    
        
    # Draw the circuit
    qc.draw(output='mpl')
    
    
    
    # Run the circuit
    if RUN_BACKEND == 0:
        backend = AerSimulator()
        
        # First we have to transpile the quantum circuit
        # to the low-level QASM instructions used by the
        # backend
        qc_compiled = transpile(qc, backend)
    
        
        # Execute the circuit on the qasm simulator.
        # We've set the number of repeats of the circuit
        # to be 1024, which is the default.
        job_sim = backend.run(qc_compiled, shots=n_shots)
        
        # Grab the results from the job.
        result_sim = job_sim.result()
        
        counts = result_sim.get_counts(qc_compiled)
        print(counts)
        
        from qiskit.visualization import plot_histogram
        plot_histogram(counts)
        plt.show()
    
    
    