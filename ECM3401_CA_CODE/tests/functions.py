import random
import math
import numpy as np
import qiskit.quantum_info as qi
import matplotlib.pyplot as plt
from deap import base, creator, tools
from qiskit import QuantumCircuit
from qft_circuits import *
from grover_circuits import *

def random_gate() -> [int, [int,int]]:
    """ 
    Selects and returns a random gate from the gate set of the
    specified gate.

    Returns:
        [int, [int, int]]: Returns a random gate from the gate set of the
            specified circuit. This enables the initial population to be
            created and has a format which matches the built in qiskit
            representation.
    """
    return random.choice(qpossible_gates_2)

def circuit_fitness(current_circuit: [[int, [int, int]]],
                   gate_set: [[int, [int, int]]],
                   target_matrix: [[float]],
                   num_qubits: int) -> (float,):
    """
    Converts the provided circuit into a Quantum Circuit object that Qiskit can
    operate on and then calculates the fitness of the circuit (the element to element
    difference between it's matrix and the target circuit's matrix).

    Args:
        current_circuit ([int, [[int, [int, int]]]): This typecasting is not absolute
            as some gates only affect one qubit or represent a wire. The current circuit
            being evaluated by the algorithm, stored in a format that can easily be
            converted into a Qiskit represntation.
        gate_set ([int, [[int, [int, int]]]): This typecasting is not aboslute for the
            same aforementioned reasons. This is the complete gate set for the current
            algorithm and number of qubits, again stored in a format that enables them
            to be added and removed from circuits with ease.
        target_matrix ([[float]]): The array of imaginary float values representing the
            goal circuit, which enables the difference between elements in the matrix
            to be calculated.
        num_qubits (int): The number of qubits being used by the circuit, stored
            as an integer as this value is a whole number.

    Returns:
        (fitness,): The Deap library requires all evaluation functions to return
            a tuple (single objective is treated as a special case of multi-objective).
            The float representing the difference between the current circuit and the
            goal is returned in the desired format.
    """
    # Converts the representation of the current circuit into a QuantumCircuit object
    qiskit_representation = convert_circuit(current_circuit, num_qubits, gate_set)
    # Finds the matrix representing the current quantum circuit
    circuit_unitary_matrix = qi.Operator(qiskit_representation)
    circuit_unitary_matrix = circuit_unitary_matrix.data
    # The circuit's fitness is the sum of the absolute element to element difference
    fitness = 0
    for i in range(0, len(circuit_unitary_matrix)):
        for j in range(0, len(circuit_unitary_matrix[i])):
            fitness += abs(circuit_unitary_matrix[i][j] - target_matrix[i][j])

    return (fitness,)

def circuit_size(current_circuit: [[int, [int, int]]]) -> int:
    """
    Calculates and returns the number of gates within a quantum circuit,
    using my proprietary (non-qiskit) representation.

    Args:
        current_circuit ([int, [[int, [int, int]]]): This typecasting is not absolute
            as some gates only affect one qubit or represent a wire. The current circuit
            being evaluated by the algorithm, stored in a format that can easily be
            converted into a Qiskit represntation.
    
    Returns:
        size (int): The size of the circuit, as an integer as this value is a whole
            number.
    """
    size = 0
    # Loops through each index in the circuit representation
    # The size counter is incremented for each index that isn't a wire
    for gate in current_circuit:
        if gate[0] != 10:
            size += 1

    return size

def convert_circuit(current_circuit: [[int, [int, int]]],
                    num_qubits: int,
                    gate_set: [[int, [int, int]]]) -> QuantumCircuit(int):
    """
    Converts a list based representation of a quantum circuit into a Qiskit compatible
    QuantumCircuit object which can be modified and read with Qiskit's methods.

    Args:
        current_circuit ([int, [[int, [int, int]]]): This typecasting is not absolute
            as some gates only affect one qubit or represent a wire. The current circuit
            being evaluated by the algorithm, stored in a format that can easily be
            converted into a Qiskit represntation.
        num_qubits (int): The number of qubits being used by the circuit, stored
            as an integer as this value is a whole number.
        gate_set ([int, [[int, [int, int]]]): This typecasting is not aboslute for the
            same aforementioned reasons. This is the complete gate set for the current
            algorithm and number of qubits, again stored in a format that enables them
            to be added and removed from circuits with ease.

    Returns:
        circuit (QuantumCircuit(int)): The Qiskit QuantumCircuit representation of the
            circuit being evaluated by the algorithm.
    """
    # Creates a new QuantumCircuit object to add the gates to
    circuit = QuantumCircuit(num_qubits)
    for gate in current_circuit:
        # If the current gate is anything but a wire, decompose the gate and
        # add it to the QuantumCircuit object
        if gate_set[gate[0]] != 'WIRE':
            circuit.append(
                gate_set[gate[0]],
                gate[1]
            )

    return circuit

def mutate(circuit: [[int, [int, int]]]) -> [[int, [int, int]]]:
    """
    Mutates a random gate in the provided circuit by changing it to another gate
    from the gate set at random (this gate set is the one being used by the algorithm being
    evaluated at the given size). 

    Args:
        circuit ([int, [[int, [int, int]]]): This typecasting is not absolute
            as some gates only affect one qubit or represent a wire. The current circuit
            which is about to be mutated, stored in a format that can easily be
            converted into a Qiskit represntation.

    Returns:
        circuit ([int, [[int, [int, int]]]): This typecasting is not absolute
            as some gates only affect one qubit or represent a wire. The current circuit
            which has now been mutated by the algorithm (contains one gate which has
            potentially changed), stored in a format that can easily be converted into a
            Qiskit represntation.
    """
    # The current gate can be mutated to any other gate in the gate set
    possible_gates = qpossible_gates_2
    
    # Choose a random gate in the circuit via index to mutate
    mutation_index = random.randint(0, len(circuit) - 1)
    # Choose a random gate from the gate set to replace said gate
    circuit[mutation_index] = random.choice(possible_gates)

    # Deletes the mutated individuals fitness values as they are no
    # longer related to the individual
    del circuit.fitness.values

    return circuit    

def crossover(circuit1: [[int, [int, int]]],
              circuit2: [[int, [int, int]]]
             ) -> ([[int, [int, int]]], [[int, [int, int]]]):
    """
    Executes a two point crossover between two provided circuits by selecting
    two indexes (gates) at random and swapping all the indexes (gates)
    between them.

    Args:
        circuit1 ([[int, [int, int]]]): This typecasting is not absolute
            as some gates only affect one qubit or represent a wire. The first circuit
            to be crossed over with the circuit below, stored in a format that can
            easily be converted into a Qiskit represntation.
        circuit2 ([[int, [int, int]]]): Akin to the other circuit this typecasting is not
            absolute. The second parent circuit to be crossed over with the above circuit.
            stored in a format that can easily be converted into a Qiskit represntation.

    Returns:
        ([[int, [int, int]]], [[int, [int, int]]])
    """
    # Specifies that two point crossover is to be used
    # (more points can be used)
    num_points = 2
    # Chooses num_points random indicies to swap
    # If there is an odd number of points selected, the end of the list is
    # chosen as the end point for the second crossover
    if num_points%2 != 0:
        indicies = []
        indicies.append(len(circuit1) - 1)
    else:
        indicies = []
    
    # Validates that no two crossover points are the same
    for i in range(0, num_points):
        temp_index = random.randint(0, len(circuit1) - 1)
        while temp_index in indicies:
            temp_index = random.randint(0, len(circuit1) - 1)

        indicies.append(temp_index)

    # Sorts the list of indexes so that the crossover can be performed correctly
    indicies.sort()

    # Performs the crossover in place, swapping all values between the crossover points
    for i in range(0, len(indicies), 2):
        temp_values = circuit1[indicies[i]:indicies[i+1]]
        circuit1[indicies[i]: indicies[i+1]] = circuit2[indicies[i]: indicies[i+1]]
        circuit2[indicies[i]: indicies[i+1]] = temp_values

    # Deletes the fitness values associated with the "mated" circuits
    # As they are no longer related to the individual
    del circuit1.fitness.values
    del circuit2.fitness.values

    return (circuit1, circuit2)  