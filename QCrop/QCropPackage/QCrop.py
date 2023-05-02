# -*- coding: utf-8 -*-
from hamiltonians import load_Molecule
import numpy as np
import matplotlib.pyplot as plt
import pylab
from typing import List 
import qutip as qt
from tqdm import tqdm
from qiskit.algorithms import VQE
from qiskit_nature.algorithms import GroundStateEigensolver,NumPyMinimumEigensolverFactory
from qiskit_nature.drivers import Molecule
from qiskit_nature.drivers.second_quantization import ElectronicStructureMoleculeDriver, ElectronicStructureDriverType
from qiskit_nature.transformers.second_quantization.electronic import ActiveSpaceTransformer
from qiskit_nature.problems.second_quantization import ElectronicStructureProblem
from qiskit_nature.converters.second_quantization import QubitConverter
from qiskit_nature.mappers.second_quantization import ParityMapper
from qiskit_nature.circuit.library import UCCSD, HartreeFock
from qiskit.circuit.library import EfficientSU2
from qiskit.opflow import TwoQubitReduction
from qiskit import BasicAer, Aer
from qiskit.utils import QuantumInstance
from qiskit.utils.mitigation import CompleteMeasFitter
from qiskit.providers.aer.noise import NoiseModel
from qiskit import Aer
from qiskit.utils import QuantumInstance, algorithm_globals
from qiskit.algorithms import VQE, NumPyMinimumEigensolver
from qiskit.algorithms.optimizers import COBYLA, L_BFGS_B, SLSQP,SPSA
from qiskit.circuit.library import TwoLocal
from qiskit.opflow import I, X, Z, Y
from qiskit.circuit import Parameter, ParameterVector, QuantumCircuit, QuantumRegister 
from numbers import Number
from qiskit.circuit import Gate, QuantumCircuit, QuantumRegister, ParameterExpression
from qiskit.quantum_info.operators.predicates import matrix_equal
from qiskit.quantum_info.operators.predicates import is_hermitian_matrix
from qiskit.extensions.exceptions import ExtensionError
from qiskit.circuit.exceptions import CircuitError
from qiskit.circuit import Parameter, QuantumCircuit, QuantumRegister 
from qiskit.extensions.unitary import UnitaryGate
import pylab
import matplotlib.pyplot as plt
from qiskit import Aer
from qiskit.utils import QuantumInstance, algorithm_globals
from qiskit.algorithms import VQE, NumPyMinimumEigensolver
from qiskit.algorithms.optimizers import SPSA
from qiskit.circuit.library import TwoLocal
from qiskit.opflow import I, X, Z

class QCrop:
    def __init__(self):
        # Assumes the user has installed all from requirements.txt
        pass
        
    def generateGraph(self,molecule,lower_bound,upper_bound,step):
        '''
        Generates the graph for the given molecule by testing the interatomic distance going from lower_bound to upper_bound by step.

        Parameters
        ----------
        molecule : str
            Name of the molecule (eg: H2).
        lower_bound : float
            Starting interatomic distance to begin.
        upper_bound : float
            Ending interatomic distance.
        step : float
            Step for varying interactomic distance.

        Returns
        -------
        None.
        '''
        # quantum setup - choose simulator and optimiser
        self.atom=molecule
        backend = BasicAer.get_backend("statevector_simulator")
        slsqp = SLSQP(5)
        spsa = SPSA(100)
        
        self.ia_dist = np.arange(lower_bound,upper_bound,step)
        self.reference_e0 = []
        self.vqe_spsa_e0 = []
        
        for dist in self.ia_dist:
            BeH2 = load_Molecule(molecule, dist)
            c_solver = NumPyMinimumEigensolverFactory()
            calc1 = GroundStateEigensolver(BeH2[2], c_solver)
            ref_result = calc1.solve(BeH2[1])
            
            qubit_ham = BeH2[0]
            problem = BeH2[1]
            converter = BeH2[2]
            
            self.reference_e0.append(ref_result.total_energies[0].real)
            init_state = HartreeFock(problem.num_spin_orbitals, problem.num_particles, converter)
            var_form = UCCSD(converter, problem.num_particles, problem.num_spin_orbitals, initial_state=init_state)
            # run VQE with SPSA
            vqe_spsa = VQE(var_form, spsa, quantum_instance=backend)
            vqe_spsa_calc = vqe_spsa.compute_minimum_eigenvalue(qubit_ham)
            vqe_spsa_result = problem.interpret(vqe_spsa_calc).total_energies[0].real
            self.vqe_spsa_e0.append(vqe_spsa_result)
    
    def plotGraph(self):
        plt.plot(self.ia_dist, self.reference_e0, color = 'green', label="Reference ground state energies")
        plt.scatter(self.ia_dist, self.vqe_spsa_e0, label="VQE energies using SPSA")
        #plt.plot(ia_distances, vqe_slsqp_e0, color = 'yellow', label="VQE energies using SLSQP")
        plt.xlabel('Interatomic distance')
        plt.title("Energy vs Interatomic Distance for "+self.atom)
        plt.ylabel('Energy')
        plt.legend()
        plt.show()
        
    def getHam(self,molecule, dist):
        #from qiskit_nature.units import DistanceUnit
        #from qiskit_nature.second_q.drivers import PySCFDriver
        #from qiskit_nature.second_q.mappers.qubit_converter import QubitConverter
        #from qiskit_nature.second_q.mappers import ParityMapper
        #from qiskit.opflow import TwoQubitReduction
        BeH2 = load_Molecule(molecule, dist)
        qubitham = BeH2[0]
        allcoef=[float(''.join(x.split('*')[0].split())) for x in str(qubitham).split('\n')]
        allops=[''.join(x.split('*')[1].split()) for x in str(qubitham).split('\n')]
        return allcoef,allops    
        
    
    def readOutVQE(self.coeffs,op_strings):
        import numpy as np
        import scipy.optimize as opt
        from qiskit import transpile,QuantumCircuit
        from qiskit.circuit.library import TwoLocal
        from qiskit.providers.fake_provider import FakeAthens
        import mthree
        def opstr_to_meas_circ(op_str):
            num_qubits = len(op_str[0])
            circs = []
            for op in op_str:
                qc = QuantumCircuit(num_qubits)
                for idx, item in enumerate(op):
                    if item == 'X':
                        qc.h(num_qubits-idx-1)
                    elif item == 'Y':
                        qc.sdg(num_qubits-idx-1)
                        qc.h(num_qubits-idx-1)
                circs.append(qc)
            return circs
        ansatz = TwoLocal(2, rotation_blocks='ry', entanglement_blocks='cx')
        meas_circs = opstr_to_meas_circ(op_strings)
        full_circs = [ansatz.compose(meas_circs[kk]).measure_all(inplace=False) for kk in range(len(meas_circs))]
        meas_strings = [string.replace('X', 'Z').replace('Y', 'Z') for string in op_strings]
        backend = FakeAthens()
        trans_circs = transpile(full_circs, backend)  
        num_params = ansatz.num_parameters
        #params = np.random.uniform(0,5,num_params) #np.array([1.22253725, 0.39053752, 0.21462153, 5.48308027,2.06984514, 3.65227416, 4.01911194, 0.35749589])
        params = np.array([1.22253725, 0.39053752, 0.21462153, 5.48308027,
                       2.06984514, 3.65227416, 4.01911194, 0.35749589])
        params += 0.05*(np.random.random(params.shape[0])-0.5)
        mit = mthree.M3Mitigation(backend)
        mit.cals_from_system([0,1])
        def vqe_func(params, *args):
            bound_circs = [circ.bind_parameters(params) for circ in trans_circs]
            counts = backend.run(bound_circs, shots=4096).result().get_counts()
            quasis = mit.apply_correction(counts, [0,1])
            energy = np.sum(coeffs*quasis.expval(meas_strings))
            return energy
    
        res = opt.minimize(vqe_func, params, method = 'COBYLA')
        return res.fun
        
    def ErrorMitigatedCircuit(self, molecule,distance):
        '''
        Using the error mitigated circuit using Measurement Error Mitigation.
        
        Parameters
        ----------
        molecule : str
            Name of molecule (eg: H2).
        distance : float
            Intermolecular distance.

        Returns
        -------
        float
            Total energy of the configuration.

        '''
        coefs,ops=self.getHam(molecule,distance)
        return self.readOutVQE(coefs,ops)
        
        
                
        