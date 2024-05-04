"""
Stores and displays each of the Grover's Search Algorithm circuits used to
test the EA
"""
import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import ZGate, GroverOperator, MCMT, HGate, XGate, CZGate, CXGate, U3Gate, CCZGate, CCXGate, MCXGate
import qiskit.quantum_info as qi

def grovers_algorithm_oracle(states):
    """Builds an oracle for the Grover's Search algorithm that amplifies one or more marked states.

    It's assumed that all input marked states have the same number of bits.

    Args:
        states (str or list): The marked states of the oracle.

    Returns:
        circuit (QuantumCircuit): The quantum circuit representing the Grover oracle.
    """

    if not isinstance(states, list):
        states = [states]
    
    # Computes the number of qubits in the circuit
    num_qubits = len(states[0])

    circuit = QuantumCircuit(num_qubits)
    # Mark each target state in the list of input states
    for target_state in states:
        # Flips the target bit-string to match the Qiskit bit-ordering
        rev_target = target_state[::-1]
        # Find the indices of all the '0' elements in bit-string
        zero_individuals = [individuals for individuals in range(num_qubits) if rev_target.startswith("0", individuals)]

        # Adds a multi-controlled Z-Gate with pre- and post applied X-Gates (open-controls)
        # Where the target bit-string has a '0' entry
        circuit.x(zero_individuals)
        circuit.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
        circuit.x(zero_individuals)

    return circuit

def optimal_applications(num_qubits, num_marked_states):
    """ Returns the optimal number of applications of the diffusion operator 
    (required to successfully amplify the marked states). This is determined
    by the ratio of marked states to the total number of possible
    computational states.
    """
    return math.floor(math.pi / (4 * math.asin(math.sqrt(num_marked_states / 2**num_qubits))))

# A gate set which contains exactly all the circuits required to create a
# fully decomposed Grovers circuit
ggate_set1 = {1:HGate(), 2:XGate(), 3:CZGate(), 4:CXGate(), 5:U3Gate(math.pi/2, 0, math.pi), 10:"WIRE"}

ggate_set2 = {1:HGate(), 2:XGate(), 3:CCZGate(), 4:CCXGate(), 5:U3Gate(math.pi/2, 0, math.pi), 10:"WIRE"}
# Need to make a custom CZ gate to accommodate 3 or more control qubits
ggate_set3 = {1:HGate(), 2:XGate(), 3:MCMT('z', num_ctrl_qubits=3, num_target_qubits=1), 4:MCXGate(num_ctrl_qubits=3), 5:U3Gate(math.pi/2, 0, math.pi), 10:"WIRE"}

gpossible_gates_1 = [[1, [0]],
                   [1, [1]],
                   [2, [0]],
                   [2, [1]],
                   [3, [0,1]],
                #    [3, [1,0]],
                   [4, [0,1]],
                #    [4, [1,0]],
                   [5, [0]],
                   [5, [1]],
                   [10, [0]],
                   [10, [1]]]

# CCX Needs different configs, CCZ Does not
gpossible_gates_2 = [[1, [0]],
                    [1, [1]],
                    [1, [2]],
                    [2, [0]],
                    [2, [1]],
                    [2, [2]],
                    [3, [0,1,2]],
                    [4, [0,1,2]],
                    # [4, [0,2,1]],
                    # [4, [1,0,2]],
                    # [4, [1,2,0]],
                    # [4, [2,0,1]],
                    # [4, [2,1,0]],
                    [5, [0]],
                    [5, [1]],
                    [5, [2]],
                    [10, [0]],
                    [10, [1]],
                    [10, [2]]]

gpossible_gates_3 = [[1, [0]],
                    [1, [1]],
                    [1, [2]],
                    [1, [3]],
                    [2, [0]],
                    [2, [1]],
                    [2, [2]],
                    [2, [3]],
                    [3, [0,1,2,3]],
                    [4, [0,1,2,3]],
                    # [4, [0,1,3,2]],
                    # [4, [0,2,1,3]],
                    # [4, [0,2,3,1]],
                    # [4, [0,3,1,2]],
                    # [4, [0,3,2,1]],
                    # [4, [1,0,2,3]],
                    # [4, [1,0,3,2]],
                    # [4, [1,2,0,3]],
                    # [4, [1,2,3,0]],
                    # [4, [1,3,0,2]],
                    # [4, [1,3,2,0]],
                    # [4, [2,1,0,3]],
                    # [4, [2,1,3,0]],
                    # [4, [2,0,1,3]],
                    # [4, [2,0,3,1]],
                    # [4, [2,3,1,0]],
                    # [4, [2,3,0,1]],
                    # [4, [3,1,2,0]],
                    # [4, [3,1,0,2]],
                    # [4, [3,2,1,0]],
                    # [4, [3,2,0,1]],
                    # [4, [3,0,1,2]],
                    # [4, [3,0,2,1]],
                    [5, [0]],
                    [5, [1]],
                    [5, [2]],
                    [5, [3]],
                    [10, [0]],
                    [10, [1]],
                    [10, [2]],
                    [10, [3]]]

# The marked states for each of the three circuits respectively
marked_states1 = ["10"]
marked_states2 = ["011", "100"]
marked_states3 = ["0000", "1010"]

# Creates a base oracle circuit to be used to create each of the
# three circuits respectively
oracle1 = grovers_algorithm_oracle(marked_states1)
oracle2 = grovers_algorithm_oracle(marked_states2)
oracle3 = grovers_algorithm_oracle(marked_states3)

# Takes each of the three oracle circuits and returns a circuit that is
# composed of the oracle circuit and a circuit that amplifies the marked
# states
circuit1 = GroverOperator(oracle1)
circuit2 = GroverOperator(oracle2)
circuit3 = GroverOperator(oracle3)

# A 2-Qubit Grover's Search circuit, 'initialised' as an empty 2-qubit circuit
grover_circuit1 = QuantumCircuit(2)
# A 3-Qubit Grover's Search circuit, 'initialised' as an empty 3-qubit circuit
grover_circuit2 = QuantumCircuit(3)
# A 4-Qubit Grover's Search circuit, 'initialised' as an empty 4-qubit circuit
grover_circuit3 = QuantumCircuit(4)

# Complete Grover circuits start with a Hadamard gate to create an even
# superposition of all the basis states
# Therefore, Hadamard gates are added to the start of each of the circuits
grover_circuit1.h(range(circuit1.num_qubits))
grover_circuit2.h(range(circuit2.num_qubits))
grover_circuit3.h(range(circuit3.num_qubits))


# Applies the Grover operator the optimal number of times for each circuit
grover_circuit1.compose(circuit1.power(optimal_applications(2, len(marked_states1))), inplace=True)
grover_circuit2.compose(circuit2.power(optimal_applications(3, len(marked_states2))), inplace=True)
grover_circuit3.compose(circuit3.power(optimal_applications(4, len(marked_states3))), inplace=True)

# Gets the unitary matrix representing each of the circuits
grover_matrix1 = qi.Operator(grover_circuit1)
grover_matrix1 = grover_matrix1.data
grover_matrix2 = qi.Operator(grover_circuit2)
grover_matrix2 = grover_matrix2.data
grover_matrix3 = qi.Operator(grover_circuit3)
grover_matrix3 = grover_matrix3.data

# As this program is not being stored as a Jupyter Notebook, all images are
# stored in a specific directory instead of being displayed on screen

# Formats the matrix representing the first circuit and saves the example
# 2 qubit circuit to a file named "2qubit_circuit.pdf"
print(grover_circuit1.decompose().decompose().size())
grover_circuit1.decompose().decompose().draw(output="latex", filename="grover_circuits/2qubit_circuit.pdf", style="iqp")

# Formats the matrix representing the second circuit and saves the example
# 3 qubit circuit to a file named "3qubit_circuit.pdf"
print(grover_circuit2.decompose().decompose().size())
grover_circuit2.decompose().decompose().draw(output="latex", filename="grover_circuits/3qubit_circuit.pdf", style="iqp")

# Formats the matrix representing the third circuit and saves the example
# 4 qubit circuit to a file named "4qubit_circuit.pdf"
print(grover_circuit3.decompose().decompose().size())
grover_circuit3.decompose().decompose().draw(output="latex", filename="grover_circuits/4qubit_circuit.pdf", style="iqp")