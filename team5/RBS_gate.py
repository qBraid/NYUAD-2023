from qiskit.circuit.gate import Gate
from qiskit.circuit.quantumregister import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit

# Create the RBS gate
def RBSGate(param, qubit1, qubit2):
    from qiskit.circuit.library.standard_gates.h import HGate, CZGate, RYGate

    # Create a quantum circuit with two qubits
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)

    # Apply hadamard on both qubits
    qc.append(HGate(), [qubit1])
    qc.append(HGate(), [qubit2])
    # Apply a two qubit CZ gate
    qc.append(CZGate(), [qubit1, qubit2])
    # Apply RY of pi.2 on both qubits
    qc.append(RYGate(param), [qubit1])
    qc.append(RYGate(-param), [qubit2])
    # Apply a two qubit CZ gate
    qc.append(CZGate(), [qubit1, qubit2])
    # Apply Hadamard on both qubits
    qc.append(HGate(), [qubit1])
    qc.append(HGate(), [qubit2])

