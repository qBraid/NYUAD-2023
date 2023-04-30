### Parametrised quantum circuit for orthogonal graph state ###

# Import Pennylane 
import pennylane as qml
from pennylane.operation import Operation
import numpy as np

# Import parameters dataset to numpy array
# params = np.loadtxt('params.csv', delimiter=',')
params = np.zeros(28)

# Set the simulator
dev = qml.device("qiskit.aer", wires=2, shots=1000)

# Define the RBS gate function
class RBS(Operation):
    num_params = 1
    num_wires = 2
    par_domain = 'R'

    @staticmethod
    def decomposition(theta, wires):
        decomp = []

        decomp.append(
            qml.Hadamard(wires=wires[0]),
            qml.Hadamard(wires=wires[1]),
            qml.CZ(wires=wires),
            qml.RY(theta, wires=wires[0]),
            qml.RY(-theta, wires=wires[1]),
            qml.CZ(wires=wires),
            qml.Hadamard(wires=wires[0]),
            qml.Hadamard(wires=wires[1]),
        )

        return decomp



# Define the quantum circuit
@qml.qnode(dev)
def circuit(params):
    # Apply X gate1 to 1st and 2nd qubits
    qml.PauliX(wires=0)
    qml.PauliX(wires=1)
    # Apply RBS gate1 to 1st and 2nd qubit
    RBS(params[0], wires=[0, 1])
    # Apply X gate2 to 3rd qubits
    qml.PauliX(wires=2)
    # Apply RBS gate2 to 2nd and 3rd qubit
    # theta2
    RBS(params[1], wires=[1, 2])
    # Apply X gate3 to 4th qubits
    qml.PauliX(wires=3)
    # Apply RBS gate3 to 1st and 2nd qubit
    # theta3
    RBS(params[2], wires=[0, 1])
    # Apply X gate4 to 5th qubits
    qml.PauliX(wires=4)
    # Apply RBS gate4 to 3rd and 4th qubit
    # theta4
    RBS(params[3], wires=[2, 3])
    # Apply X gate5 to 6th qubits
    qml.PauliX(wires=5)
    # Apply RBS gate5 to 2nd and 3rd qubit
    # theta5
    RBS(params[4], wires=[1, 2])
    # Apply RBS gate7 to 4th and 5th qubit
    # theta7
    RBS(params[5], wires=[3, 4])
    # Apply X gate6 to 7th qubits
    qml.PauliX(wires=6)
    # Apply RBS gate6 to 1st and 2nd qubit
    # theta6
    RBS(params[6], wires=[0, 1])
    # Apply RBS gate8 to 3rd and 4th qubit
    # theta8
    RBS(params[7], wires=[2, 3])
    # Apply RBS gate11 to 5th and 6th qubit
    # theta11
    RBS(params[8], wires=[4, 5])

    # Apply RBS gate9 to 2nd and 3rd qubit
    # theta9
    RBS(params[9], wires=[1, 2])
    # Apply RBS gate12 to 4th and 5th qubit
    # theta12
    RBS(params[10], wires=[3, 4])
    # Apply RBS gate16 to 6th and 7th qubit
    # theta16
    RBS(params[11], wires=[5, 6])

    # Apply RBS gate10 to 1st and 2nd qubit
    # theta10
    RBS(params[12], wires=[0, 1])
    # Apply RBS gate13 to 3rd and 4th qubit
    # theta13
    RBS(params[13], wires=[2, 3])
    # Apply RBS gate17 to 5th and 6th qubit
    # theta17
    RBS(params[14], wires=[4, 5])
    # Apply RBS gate22  to 7th and 8th qubit
    # theta22
    RBS(params[15], wires=[6, 7])

    # Apply RBS gate14 to 2nd and 3rd qubit
    # theta14
    RBS(params[16], wires=[1, 2])
    # Apply RBS gate18 to 4th and 5th qubit
    # theta18
    RBS(params[17], wires=[3, 4])
    # Apply RBS gate23 to 6th and 7th qubit
    # theta23
    RBS(params[18], wires=[5, 6])

    # Apply RBS gate15 to 1st and 2nd qubit
    # theta15
    RBS(params[19], wires=[0, 1])
    # Apply RBS gate19 to 3rd and 4th qubit
    # theta19
    RBS(params[20], wires=[2, 3])

    # Apply RBS gate20 to 2nd and 3rd qubit
    # theta20
    RBS(params[21], wires=[1, 2])

    # Apply RBS gate21 to 1st and 2nd qubit
    # theta21
    RBS(params[22], wires=[0, 1])

    # Apply RBS gate26 to 3rd and 4th qubit
    # theta26
    RBS(params[23], wires=[2, 3])

    # Apply RBS gate27 to 2nd and 3rd qubit
    # theta27
    RBS(params[24], wires=[1, 2])

    # Apply RBS gate28 to 1st and 2nd qubit
    # theta28
    RBS(params[25], wires=[0, 1])

    return qml.probs(wires=[0, 1, 2, 3, 4, 5, 6, 7])


#Draw the circuit
print(qml.draw(circuit)(params))
