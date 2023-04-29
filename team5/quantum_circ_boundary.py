# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 15:24:12 2023

@author: Team 5
"""

import numpy as np
import matplotlib.pyplot as plt

#import qiskit functionality
from qiskit.circuit.gate import Gate
from qiskit.circuit.quantumregister import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.library.standard_gates import HGate, CZGate, RYGate





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
    
    
    # Create a quantum circuit with four qubits
    qr = QuantumRegister(n_q)
    qc = QuantumCircuit(qr)


    thetas = angles(np.ones(n_q)/np.sqrt(n_q), V = False)
    
    #prepares initial state: 1110 (corresponds to simple driangle)
    
    
    
    #builds the circuit, fig. 2 from https://arxiv.org/pdf/2202.00054.pdf
    for j in range(2, n_q+1):
        i = n_q-j
        qr_pair = [qr[i], qr[i+1]]
        
        #TODO - remove
        #qc = apply_RBS(qc, qr_pair, thetas[i])
    
        param = thetas[i]
        
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

    for j in range(2, n_q+1):
        i = j-2
        qr_pair = [qr[i], qr[i+1]]
        
        #TODO - remove
        #qc = apply_RBS(qc, qr_pair, thetas[i])
    
        param = thetas[i]
        
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
    qc.measure(range(n_q), range(n_q))
    
    
    
    
        
    # Draw the circuit
    qc.draw(output='mpl')
    