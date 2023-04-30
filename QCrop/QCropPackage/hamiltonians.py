
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

#Source: A. Kandala et. al., Nature volume 549, pages242–246 (2017)
#https://www.nature.com/articles/nature23879

def load_H2():
    H2_op = (-1.052373245772859 * I ^ I) + \
         (0.39793742484318045 * I ^ Z) + \
         (-0.39793742484318045 * Z ^ I) + \
         (-0.01128010425623538 * Z ^ Z) + \
         (0.18093119978423156 * X ^ X)
    return H2_op

# This Hamiltonian doesn't include the off-set I^I^I^I.
def load_LiH():
    LiH_op = (-0.096022*Z^I^I^I)+(-0.206128*Z^Z^I^I)+(0.364746*I^Z^I^I)+(0.096022*I^I^Z^I)+\
        (-0.206128*I^I^Z^Z)+(-0.364746*I^I^I^Z)+(-0.145438*Z^I^Z^I)+(0.056040*Z^I^Z^Z)+\
        (0.110811*Z^I^I^Z)+(-0.056040*Z^Z^Z^I)+(0.080334*Z^Z^Z^Z)+(0.063673*Z^Z^I^Z)+\
        (0.110811*I^Z^Z^I)+(-0.063673*I^Z^Z^Z)+(-0.095216*I^Z^I^Z)+(-0.012585*X^Z^I^I)+\
        (0.012585*X^I^I^I)+(0.012585*I^I^X^Z)+(0.012585*I^I^X^I)+(-0.002667*X^Z^X^Z)+\
        (-0.002667*X^Z^X^I)+(0.002667*X^I^X^Z)+(0.002667*X^I^X^I)+(0.007265*X^Z^I^Z)+\
        (-0.007265*X^I^I^Z)+(0.007265*I^Z^X^Z)+(0.007265*I^Z^X^I)+(-0.029640*X^X^I^I)+\
        (0.002792*I^X^I^I)+(-0.029640*I^I^X^X)+(0.002792*I^I^I^X)+(-0.008195*X^I^X^X)+\
        (-0.001271*X^I^I^X)+(-0.008195*X^X^X^I)+(0.028926*X^X^X^X)+(0.007499*X^X^I^X)+\
        (-0.001271*I^X^X^I)+(0.007499*I^X^X^X)+(0.009327*I^X^I^X)+(0.029640*Y^Y^I^I)+\
        (0.029640*I^I^Y^Y)+(0.028926*Y^Y^Y^Y)+(0.002792*Z^X^I^I)+(-0.002792*I^I^Z^X)+\
        (-0.016781*Z^I^Z^X)+(0.016781*Z^I^I^X)+(-0.016781*Z^X^Z^I)+(-0.016781*I^X^Z^I)+\
        (-0.009327*Z^X^Z^X)+(0.009327*Z^X^I^X)+(-0.009327*I^X^Z^X)+(-0.011962*Z^I^X^Z)+\
        (-0.011962*Z^I^X^I)+(0.000247*Z^Z^X^Z)+(0.000247*Z^Z^X^I)+(0.039155*Z^I^X^X)+\
        (-0.002895*Z^Z^X^X)+(-0.009769*Z^Z^I^X)+(-0.024280*I^Z^X^X)+(-0.008025*I^Z^I^X)+\
        (-0.039155*Z^I^Y^Y)+(0.002895*Z^Z^Y^Y)+(0.024280*I^Z^Y^Y)+(-0.011962*X^Z^Z^I)+\
        (0.011962*X^I^Z^I)+(-0.000247*X^Z^Z^Z)+(0.000247*X^I^Z^Z)+(0.008195*X^Z^X^X)+\
        (0.001271*X^Z^I^X)+(-0.008195*X^Z^Y^Y)+(0.008195*X^I^Y^Y)+(-0.001271*X^Z^Z^X)+\
        (0.001271*X^I^Z^X)+(0.008025*I^Z^Z^X)+(-0.039155*X^X^Z^I)+(-0.002895*X^X^Z^Z)+\
        (0.024280*X^X^I^Z)+(-0.009769*I^X^Z^Z)+(0.008025*I^X^I^Z)+(0.039155*Y^Y^Z^I)+\
        (0.002895*Y^Y^Z^Z)+(-0.024280*Y^Y^I^Z)+(-0.008195*X^X^X^Z)+(-0.001271*I^X^X^Z)+\
        (0.008195*Y^Y^X^Z)+(0.008195*Y^Y^X^I)+(-0.028926*X^X^Y^Y)+(-0.007499*I^X^Y^Y)+\
        (-0.028926*Y^Y^X^X)+(-0.007499*Y^Y^I^X)+(-0.007499*X^X^Z^X)+(0.007499*Y^Y^Z^X)+\
        (0.009769*Z^Z^Z^X)+(-0.001271*Z^X^X^Z)+(-0.001271*Z^X^X^I)+(0.008025*Z^X^I^Z)+\
        (0.007499*Z^X^X^X)+(-0.007499*Z^X^Y^Y)+(-0.009769*Z^X^Z^Z)
    return LiH_op
# This Hamiltonian doesn't include the off-set I^I^I^I.
def load_BeH2():
    BeH2_op = (-0.143021*Z^I^I^I^I^I)+(0.104962*Z^Z^I^I^I^I)+(0.038195*I^Z^Z^I^I^I)+(-0.325651*I^I^Z^I^I^I)+\
        (-0.143021*I^I^I^Z^I^Z)+(0.104962*I^I^I^Z^Z^Z)+(0.038195*I^I^I^I^Z^I)+(-0.325651*I^I^I^I^I^I)+\
        (0.172191*I^Z^I^I^I^I)+(0.174763*Z^Z^Z^I^I^I)+(0.136055*Z^I^Z^I^I^I)+(0.116134*Z^I^I^Z^I^Z)+\
        (0.094064*Z^I^I^Z^Z^Z)+(0.099152*Z^I^I^I^Z^I)+(0.123367*Z^I^I^I^I^I)+(0.094064*Z^Z^I^Z^I^Z)+\
        (0.098003*Z^Z^I^Z^Z^Z)+(0.102525*Z^Z^I^I^Z^I)+(0.097795*Z^Z^I^I^I^I)+(0.099152*I^Z^Z^Z^I^Z)+\
        (0.102525*I^Z^Z^Z^Z^Z)+(0.112045*I^Z^Z^I^Z^I)+(0.105708*I^Z^Z^I^I^I)+(0.123367*I^I^Z^Z^I^Z)+\
        (0.097795*I^I^Z^Z^Z^Z)+(0.105708*I^I^Z^I^Z^I)+(0.133557*I^I^Z^I^I^I)+(0.172191*I^I^I^I^Z^I)+\
        (0.174763*I^I^I^Z^Z^Z)+(0.136055*I^I^I^Z^I^Z)+(0.059110*X^Z^I^I^I^I)+(-0.059110*X^I^I^I^I^I)+\
        (0.161019*I^Z^X^I^I^I)+(-0.161019*I^I^X^I^I^I)+(0.059110*I^I^I^X^Z^X)+(-0.059110*I^I^I^X^I^X)+\
        (0.161019*I^I^I^I^Z^I)+(-0.161019*I^I^I^I^I^I)+(-0.038098*X^I^X^I^I^I)+(-0.003300*X^Z^X^I^I^I)+\
        (0.013745*X^Z^I^X^Z^X)+(-0.013745*X^Z^I^X^I^X)+(-0.013745*X^I^I^X^Z^X)+(0.013745*X^I^I^X^I^X)+\
        (0.011986*X^Z^I^I^Z^I)+(-0.011986*X^Z^I^I^I^I)+(-0.011986*X^I^I^I^Z^I)+(0.011986*X^I^I^I^I^I)+\
        (0.011986*I^Z^X^X^Z^X)+(-0.011986*I^Z^X^X^I^X)+(-0.011986*I^I^X^X^Z^X)+(0.011986*I^I^X^X^I^X)+\
        (0.013836*I^Z^X^I^Z^I)+(-0.013836*I^Z^X^I^I^I)+(-0.013836*I^I^X^I^Z^I)+(0.013836*I^I^X^I^I^I)+\
        (-0.038098*I^I^I^X^I^X)+(-0.003300*I^I^I^X^Z^X)+(-0.002246*Z^Z^X^I^I^I)+(0.002246*Z^I^X^I^I^I)+\
        (0.014815*Z^I^I^X^Z^X)+(-0.014815*Z^I^I^X^I^X)+(0.009922*Z^I^I^I^Z^I)+(-0.009922*Z^I^I^I^I^I)+\
        (-0.002038*Z^Z^I^X^Z^X)+(0.002038*Z^Z^I^X^I^X)+(-0.007016*Z^Z^I^I^Z^I)+(0.007016*Z^Z^I^I^I^I)+\
        (-0.006154*X^I^Z^I^I^I)+(0.006154*X^Z^Z^I^I^I)+(0.014815*X^Z^I^Z^I^Z)+(-0.014815*X^I^I^Z^I^Z)+\
        (-0.002038*X^Z^I^Z^Z^Z)+(0.002038*X^I^I^Z^Z^Z)+(0.001124*X^Z^I^I^Z^I)+(-0.001124*X^I^I^I^Z^I)+\
        (0.017678*X^Z^I^I^I^I)+(-0.017678*X^I^I^I^I^I)+(-0.041398*Y^I^Y^I^I^I)+(0.011583*Y^Y^I^X^X^X)+\
        (-0.011094*Y^Y^I^I^X^I)+(0.010336*I^Y^Y^X^X^X)+(-0.005725*I^Y^Y^I^X^I)+(-0.006154*I^I^I^X^I^X)+\
        (0.011583*X^X^Z^X^X^X)+(-0.011094*X^X^Z^I^X^I)+(-0.011094*I^X^I^X^X^X)+(0.026631*I^X^I^I^X^I)+\
        (-0.017678*I^I^Z^X^I^X)+(0.011583*X^X^Z^Y^Y^Y)+(0.010336*X^X^Z^I^Y^I)+(-0.011094*I^X^I^Y^Y^Y)+\
        (-0.005725*I^X^I^I^Y^I)+(-0.041398*I^I^I^Y^I^Y)+(0.011583*Y^Y^I^Y^Y^Y)+(0.010336*Y^Y^I^I^Y^I)+\
        (0.010336*I^Y^Y^Y^Y^Y)+(0.010600*I^Y^Y^I^Y^I)+(0.024909*X^X^Z^X^X^X)+(-0.031035*I^X^I^X^X^X)+\
        (-0.010064*I^I^Z^I^I^I)+(0.024909*X^X^Z^Y^X^Y)+(-0.031035*I^X^I^Y^X^Y)+(0.024909*Y^Y^I^X^X^X)+\
        (0.021494*I^Y^Y^X^X^X)+(0.024909*Y^Y^I^Y^X^Y)+(0.021494*I^Y^Y^Y^X^Y)+(0.011094*X^X^Z^Z^X^Z)+\
        (-0.026631*I^X^I^Z^X^Z)+(0.011094*Y^Y^I^Z^X^Z)+(0.005725*I^Y^Y^Z^X^Z)+(0.010336*X^X^Z^Z^X^Z)+\
        (-0.005725*I^X^I^Z^X^Z)+(0.002246*I^I^I^Z^I^Z)+(0.010336*Y^Y^I^Z^X^Z)+(0.010600*I^Y^Y^Z^X^Z)+\
        (0.024909*X^X^X^X^X^X)+(-0.031035*X^X^X^I^X^I)+(-0.010064*I^I^X^I^I^I)+(0.024909*X^X^X^Y^Y^Y)+\
        (0.021494*X^X^X^I^Y^I)+(0.024909*Y^X^Y^X^X^X)+(-0.031035*Y^X^Y^I^X^I)+(0.024909*Y^X^Y^Y^Y^Y)+\
        (0.021494*Y^X^Y^I^Y^I)+(0.063207*X^X^X^X^X^X)+(0.063207*X^X^X^Y^X^Y)+(0.063207*Y^X^Y^X^X^X)+\
        (0.063207*Y^X^Y^Y^X^Y)+(0.031035*X^X^X^Z^X^Z)+(-0.009922*I^I^X^Z^I^Z)+(0.031035*Y^X^Y^Z^X^Z)+\
        (0.021494*X^X^X^Z^X^Z)+(0.021494*Y^X^Y^Z^X^Z)+(0.011094*Z^X^Z^X^X^X)+(-0.026631*Z^X^Z^I^X^I)+\
        (0.011094*Z^X^Z^Y^Y^Y)+(0.005725*Z^X^Z^I^Y^I)+(0.031035*Z^X^Z^X^X^X)+(0.031035*Z^X^Z^Y^X^Y)+\
        (0.026631*Z^X^Z^Z^X^Z)+(0.005725*Z^X^Z^Z^X^Z)+(0.010336*Z^X^X^X^X^X)+(-0.005725*Z^X^X^I^X^I)+\
        (0.010336*Z^X^X^Y^Y^Y)+(0.010600*Z^X^X^I^Y^I)+(0.021494*Z^X^X^X^X^X)+(0.021494*Z^X^X^Y^X^Y)+\
        (0.005725*Z^X^X^Z^X^Z)+(0.010600*Z^X^X^Z^X^Z)+(0.001124*I^Z^Z^X^Z^X)+(-0.001124*I^Z^Z^X^I^X)+\
        (-0.007952*I^Z^Z^I^Z^I)+(0.007952*I^Z^Z^I^I^I)+(0.017678*I^I^Z^X^Z^X)+(0.010064*I^I^Z^I^Z^I)+\
        (0.009922*I^Z^X^Z^I^Z)+(-0.007016*I^Z^X^Z^Z^Z)+(0.007016*I^I^X^Z^Z^Z)+(-0.007952*I^Z^X^I^Z^I)+\
        (0.007952*I^I^X^I^Z^I)+(0.010064*I^Z^X^I^I^I)+(-0.002246*I^I^I^Z^Z^Z)+(0.006154*I^I^I^X^Z^X)
    return BeH2_op


#Interatomic distance H2: 0.735Å, LiH: 1.545Å, BeH2: 1.3Å
def load_Molecule(molecule_name, distance = None):
    if molecule_name == "LiH":
        if distance == None:
            distance = 1.545
            print("The atomic distance is ",distance,"Å")
        molecule = Molecule(
            # Coordinates in Angstrom
            geometry=[["Li", [0.0, 0.0, 0.0] ], ["H", [0.0, 0.0, distance]]],multiplicity=1, charge=0,)
        driver = ElectronicStructureMoleculeDriver(molecule=molecule, basis="sto3g", driver_type=ElectronicStructureDriverType.PYSCF)
        properties = driver.run()

        num_particles = (properties.get_property("ParticleNumber").num_particles)
        num_spin_orbitals = int(properties.get_property("ParticleNumber").num_spin_orbitals)

        # Define Problem, Use ActiveSpaceTransformer.
        active_space_trafo = ActiveSpaceTransformer(num_electrons=num_particles, num_molecular_orbitals=3)
        problem = ElectronicStructureProblem(driver, transformers=[active_space_trafo])

        second_q_ops = problem.second_q_ops()  # Get 2nd Quant OP
        num_spin_orbitals = problem.num_spin_orbitals
        num_particles = problem.num_particles
        mapper = ParityMapper()  # Set Mapper
        hamiltonian = second_q_ops[0]  # Set Hamiltonian
        # Do two qubit reduction
        converter = QubitConverter(mapper,two_qubit_reduction=True)
        reducer = TwoQubitReduction(num_particles)
        qubit_op = converter.convert(hamiltonian)
        qubit_op = reducer.convert(qubit_op)
        return qubit_op, problem, converter
    elif molecule_name == "H2":
        if distance == None:
            distance =0.735
            print("The atomic distance is ",distance,"Å")
        molecule = Molecule(geometry=[ ["H", [0.0, 0.0, 0.0] ],["H", [distance, 0.0, 0.0] ]],multiplicity=1,charge=0)
        driver = ElectronicStructureMoleculeDriver(molecule=molecule,basis="sto3g",driver_type=ElectronicStructureDriverType.PYSCF)
        problem = ElectronicStructureProblem(driver)
        second_q_ops = problem.second_q_ops()  # Get 2nd Quant OP
        num_spin_orbitals = problem.num_spin_orbitals
        num_particles = problem.num_particles

        mapper = ParityMapper()  # Set Mapper

        hamiltonian = second_q_ops[0]  # Set Hamiltonian

        # Do two qubit reduction
        converter = QubitConverter(mapper,two_qubit_reduction=True)
        reducer = TwoQubitReduction(num_particles)
        qubit_op = converter.convert(hamiltonian)
        qubit_op = reducer.convert(qubit_op)
        return qubit_op, problem, converter

    elif molecule_name == "BeH2":
        if distance == None:
            distance = 1.3
            print("The atomic distance is ",distance,"Å")
        molecule = Molecule(
            # Coordinates in Angstrom
            geometry=[["Be", [0.0, 0.0, 0.0] ], ["H", [distance, 0.0, 0.0]],["H", [-distance, 0.0, 0.0]]],multiplicity=1, charge=0,)
        driver = ElectronicStructureMoleculeDriver(molecule=molecule, basis="sto3g", driver_type=ElectronicStructureDriverType.PYSCF)
        properties = driver.run()
        num_particles = (properties.get_property("ParticleNumber").num_particles)
        num_spin_orbitals = int(properties.get_property("ParticleNumber").num_spin_orbitals)

        # Define Problem, Use ActiveSpaceTransformer.
        active_space_trafo = ActiveSpaceTransformer(num_electrons=num_particles, num_molecular_orbitals=4)
        problem = ElectronicStructureProblem(driver, transformers=[active_space_trafo])
        second_q_ops = problem.second_q_ops()  # Get 2nd Quant OP
        num_spin_orbitals = problem.num_spin_orbitals
        num_particles = problem.num_particles
        mapper = ParityMapper()  # Set Mapper
        hamiltonian = second_q_ops[0]  # Set Hamiltonian
        # Do two qubit reduction
        converter = QubitConverter(mapper,two_qubit_reduction=True)
        reducer = TwoQubitReduction(num_particles)
        qubit_op = converter.convert(hamiltonian)
        qubit_op = reducer.convert(qubit_op)
        return qubit_op, problem, converter
    else:
        print("Error: We only support H2, LiH, and BeH2")
        return 

def total_energy_solver(problem, converter):
    solver = NumPyMinimumEigensolverFactory()
    calc = GroundStateEigensolver(converter, solver)
    result = calc.solve(problem)
    return result.total_energies[0].real

def energy_solver(operator):
    npme = NumPyMinimumEigensolver()
    result = npme.compute_minimum_eigenvalue(operator=operator)
    return result.eigenvalue.real




