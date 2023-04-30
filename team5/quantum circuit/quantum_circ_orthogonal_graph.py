# Import Qiskit libraries
from qiskit.circuit.quantumregister import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.library.standard_gates import XGate

# Import RBS gate
from RBS_gate import RBSGate

# Import Qiskit Aer simulator
from qiskit import Aer
from qiskit_aer import AerSimulator

# Create quantum register
qubit = QuantumRegister(8)
circ = QuantumCircuit (qubit)

# Apply X gate0,1 to 1st and 2nd qubits.
circ.append(XGate(), [qubit[0]]) 
circ.append(XGate(), [qubit[1]])

# Apply RBS gate1 to 1st and 2nd qubit
circ.append(RBSGate(param=0), [qubit[0], qubit[1]])

# Apply X gate2 to 3nd qubits.
circ.append(XGate(), [qubit[2]]) 
# Apply RBS gate2 to 2nd and 3rd qubit
# theta2
circ.append(RBSGate(param=0), [qubit[1], qubit[2]])

# Apply X gate3 to 4th qubits.
circ.append(XGate(), [qubit[3]]) 
# Apply RBS gate3 to 1st and 2nd qubit
# theta3
circ.append(RBSGate(param=0), [qubit[0], qubit[1]])

# Apply X gate4 to 5th qubits.
circ.append(XGate(), [qubit[4]]) 
# Apply RBS gate4 to 3rd and 4th qubit
# theta4
circ.append(RBSGate(param=0), [qubit[2], qubit[3]])

# Apply X gate5 to 6th qubits.
circ.append(XGate(), [qubit[5]]) 
# Apply RBS gate5 to 2nd and 3rd qubit
# theta5
circ.append(RBSGate(param=0), [qubit[1], qubit[2]])
# Apply RBS gate7 to 4th and 5th qubit
# theta7
circ.append(RBSGate(param=0), [qubit[3], qubit[4]])

# Apply X gate6 to 7th qubits.
circ.append(XGate(), [qubit[6]]) 
# Apply RBS gate6 to 1st and 2nd qubit
# theta6
circ.append(RBSGate(param=0), [qubit[0], qubit[1]])
# Apply RBS gate8 to 3rd and 4th qubit
# theta8
circ.append(RBSGate(param=0), [qubit[2], qubit[3]])
# Apply RBS gate11 to 5th and 6th qubit
# theta11
circ.append(RBSGate(param=0), [qubit[4], qubit[5]])

# Apply RBS gate9 to 2nd and 3rd qubit
# theta9
circ.append(RBSGate(param=0), [qubit[1], qubit[2]])
# Apply RBS gate12 to 4th and 5th qubit
# theta12
circ.append(RBSGate(param=0), [qubit[3], qubit[4]])
# Apply RBS gate16 to 6th and 7th qubit
# theta16
circ.append(RBSGate(param=0), [qubit[5], qubit[6]])

# Apply RBS gate10 to 1st and 2nd qubit
# theta10
circ.append(RBSGate(param=0), [qubit[0], qubit[1]])
# Apply RBS gate13 to 3rd and 4th qubit
# theta13
circ.append(RBSGate(param=0), [qubit[2], qubit[3]])
# Apply RBS gate17 to 5th and 6th qubit
# theta17
circ.append(RBSGate(param=0), [qubit[4], qubit[5]])
# Apply RBS gate22 to 7th and 8th qubit
# theta22
circ.append(RBSGate(param=0), [qubit[6], qubit[7]])

# Apply RBS gate14 to 2nd and 3rd qubit
# theta14
circ.append(RBSGate(param=0), [qubit[1], qubit[2]])
# Apply RBS gate18 to 4th and 5th qubit
# theta18
circ.append(RBSGate(param=0), [qubit[3], qubit[4]])
# Apply RBS gate23 to 6th and 7th qubit
# theta23
circ.append(RBSGate(param=0), [qubit[5], qubit[6]])

# Apply RBS gate15 to 1st and 2nd qubit
# theta15
circ.append(RBSGate(param=0), [qubit[0], qubit[1]])
# Apply RBS gate19 to 3th and 4th qubit
# theta19
circ.append(RBSGate(param=0), [qubit[2], qubit[3]])
# Apply RBS gate24 to 5th and 6th qubit
# theta24
circ.append(RBSGate(param=0), [qubit[4], qubit[5]])

# Apply RBS gate20 to 2nd and 3rd qubit
# theta20
circ.append(RBSGate(param=0), [qubit[1], qubit[2]])
# Apply RBS gate25 to 4th and 5th qubit
# theta25
circ.append(RBSGate(param=0), [qubit[3], qubit[4]])

# Apply RBS gate21 to 1st and 2nd qubit
# theta21
circ.append(RBSGate(param=0), [qubit[0], qubit[1]])
# Apply RBS gate26 to 3rd and 4th qubit
# theta26
circ.append(RBSGate(param=0), [qubit[2], qubit[3]])

# Apply RBS gate27 to 2nd and 3rd qubit
# theta27
circ.append(RBSGate(param=0), [qubit[1], qubit[2]])

# Apply RBS gate28 to 1st and 2nd qubit
# theta28
circ.append(RBSGate(param=0), [qubit[0], qubit[1]])

# Draw the circuit
circ.draw (output = 'mpl')

