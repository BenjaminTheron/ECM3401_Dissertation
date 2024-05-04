"""
Stores and displays each of the Quantum Fourier Transform circuits used to
test the EA
"""
import numpy as np
import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT, HGate, SwapGate, CPhaseGate
import qiskit.quantum_info as qi

# Dynamically creates the gate set to be used as the rotation and number of
# possible p gates depends on the number of qubits being used (pi/2^N-1)

# a dictionary where the key value pair is the indexes and the Qiskit gate name
qgate_set1 = {1:HGate(), 2:SwapGate(), 3:CPhaseGate(math.pi/2), 10:"WIRE"}

qgate_set2 = {1:HGate(), 2:SwapGate(), 3:CPhaseGate(math.pi/2), 4:CPhaseGate(math.pi/4), 10:"WIRE"}

qgate_set3 = {1:HGate(), 2:SwapGate(), 3:CPhaseGate(math.pi/2), 4:CPhaseGate(math.pi/4), 5:CPhaseGate(math.pi/8), 10:"WIRE"}

# Creates sets of possible gates for 2qubit circuit
qpossible_gates_1 = [[1, [0]],
                    [1, [1]],
                    [2, [0,1]],
                    # [2, [1,0]],
                    [3, [0,1]],
                    # [3, [1,0]],
                    [10, [0]],
                    [10, [1]]]

# Creates the set of possible gates for the 3qubit circuit
qpossible_gates_2 = [[1, [0]],
                    [1, [1]],
                    [1, [2]],
                    # [2, [0,1]],
                    [2, [0,2]],
                    # [2, [1,0]],
                    # [2, [1,2]],
                    # [2, [2,0]],
                    # [2, [2,1]],
                    [3, [0,1]],
                    # [3, [0,2]],
                    # [3, [1,0]],
                    [3, [1,2]],
                    # [3, [2,0]],
                    # [3, [2,1]],
                    # [4, [0,1]],
                    [4, [0,2]],
                    # [4, [1,0]],
                    # [4, [1,2]],
                    # [4, [2,0]],
                    # [4, [2,1]],
                    [10, [0]],
                    [10, [1]],
                    [10, [2]]]

# Creates the set of possible gates for the 4qubit circuit
qpossible_gates_3 = [[1, [0]],
                    [1, [1]],
                    [1, [2]],
                    [1, [3]],
                    # [2, [0,1]],
                    # [2, [0,2]],
                    [2, [0,3]],
                    # [2, [1,0]],
                    [2, [1,2]],
                    # [2, [1,3]],
                    # [2, [2,0]],
                    # [2, [2,1]],
                    # [2, [2,3]],
                    # [2, [3,0]],
                    # [2, [3,1]],
                    # [2, [3,2]],
                    [3, [0,1]],
                    # [3, [0,2]],
                    # [3, [0,3]],
                    # [3, [1,0]],
                    [3, [1,2]],
                    # [3, [1,3]],
                    # [3, [2,0]],
                    # [3, [2,1]],
                    [3, [2,3]],
                    # [3, [3,0]],
                    # [3, [3,1]],
                    # [3, [3,2]],
                    # [4, [0,1]],
                    [4, [0,2]],
                    # [4, [0,3]],
                    # [4, [1,0]],
                    # [4, [1,2]],
                    [4, [1,3]],
                    # [4, [2,0]],
                    # [4, [2,1]],
                    # [4, [2,3]],
                    # [4, [3,0]],
                    # [4, [3,1]],
                    # [4, [3,2]],
                    # [5, [0,1]],
                    # [5, [0,2]],
                    [5, [0,3]],
                    # [5, [1,0]],
                    # [5, [1,2]],
                    # [5, [1,3]],
                    # [5, [2,0]],
                    # [5, [2,1]],
                    # [5, [2,3]],
                    # [5, [3,0]],
                    # [5, [3,1]],
                    # [5, [3,2]],
                    [10, [0]],
                    [10, [1]],
                    [10, [2]],
                    [10, [3]]]

# A 2-qubit QFT circuit which is initialised to an empty 2 qubit circuit
qft_circuit1 = QuantumCircuit(2)
# A 3-qubit QFT circuit which is initialised to an empty 3 qubit circuit
qft_circuit2 = QuantumCircuit(3)
# A 4-qubit QFT circuit which is initialised to an empty 4 qubit circuit
qft_circuit3 = QuantumCircuit(4)

# The Qiskit QFT method creates a complete QFT circuit with the specified parameters
qft_circuit1 = QFT(num_qubits=2, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name="qft2")

qft_circuit2 = QFT(num_qubits=3, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name="qft3")

qft_circuit3 = QFT(num_qubits=4, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name="qft4")

# Gets the unitary matrix representing each of the circuits
qft_matrix1 = qi.Operator(qft_circuit1)
qft_matrix1 = qft_matrix1.data
qft_matrix2 = qi.Operator(qft_circuit2)
qft_matrix2 = qft_matrix2.data
qft_matrix3 = qi.Operator(qft_circuit3)
qft_matrix3 = qft_matrix3.data

# As this program is not being stored as a Jupyter Notebook, all images are
# stored in a specific directory instead of being displayed on screen

# For each of the circuits, the pdf diagram is saved into the qft_circuits directory
# print(qft_circuit1)

qft_circuit1.decompose().draw(output="latex", filename="qft_circuits/2qubit_circuit.pdf", style="iqp")
print(qft_circuit1.decompose().data)

# print(qft_circuit2)
qft_circuit2.decompose().draw(output="latex", filename="qft_circuits/3qubit_circuit.pdf", style="iqp")

# print(qft_circuit3)
qft_circuit3.decompose().draw(output="latex", filename="qft_circuits/4qubit_circuit.pdf", style="iqp")