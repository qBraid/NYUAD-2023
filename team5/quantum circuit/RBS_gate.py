### Create custom gate for Reconfigurable Beamsplitter (RBS) ###

from qiskit.circuit.gate import Gate
from qiskit.circuit.library.standard_gates import HGate, CZGate, RYGate

class RBSGate(Gate):

    def __init__(self, label=None, param=None):
        super().__init__(name='RBS', num_qubits=2, params=[param])
        
    def _define(self):
        from qiskit.circuit.quantumregister import QuantumRegister
        from qiskit.circuit.quantumcircuit import QuantumCircuit

        q = QuantumRegister(2, 'q')
        qc = QuantumCircuit(q, name=self.name)

        rules = [
            (HGate(), [q[0]], []),
            (HGate(), [q[1]], []),
            (CZGate(), [q[0], q[1]], []),
            (RYGate(self.params[0]), [q[0]], []),
            (RYGate(-self.params[0]), [q[1]], []),
            (CZGate(), [q[0], q[1]], []),
            (HGate(), [q[0]], []),
            (HGate(), [q[1]], [])
        ]

        qc._data = rules
        self.definition = qc