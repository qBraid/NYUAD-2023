#%%
from qiskit.circuit.gate import Gate
from qiskit.circuit.quantumregister import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.library.standard_gates import HGate, CZGate, RYGate

param = 0.5

# Create a quantum circuit with two qubits
qr = QuantumRegister(2)
qc = QuantumCircuit(qr)

# Apply hadamard on both qubits
qc.append(HGate(), [qr[0]])
qc.append(HGate(), [qr[1]])
# Apply a two qubit CZ gate
qc.append(CZGate(), [qr[0], qr[1]])
# Apply RY of pi.2 on both qubits
qc.append(RYGate(param), [qr[0]])
qc.append(RYGate(-param), [qr[1]])
# Apply a two qubit CZ gate
qc.append(CZGate(), [qr[0], qr[1]])
# Apply Hadamard on both qubits
qc.append(HGate(), [qr[0]])
qc.append(HGate(), [qr[1]])

# Draw the circuit
qc.draw(output='mpl')


# %%
