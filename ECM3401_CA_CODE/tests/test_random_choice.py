"""A unit test module to validate the circuit_fitness function"""
import unittest
import math
from functions import circuit_fitness
from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, CZGate

class TestClass(unittest.TestCase):
    # A TestClass that stores each unit test for the circuit_fitness function

    # Boundary tests - testing the upper and lower bound
    def test_circuit_fitness_boundary1(self):
        """Tests circuit_fitness with a boundary circuit"""
        # Creates a valid 2 qubit circuit with an HGate on either qubit
        gate_set = {1: HGate()}
        test_circuit = QuantumCircuit(2)
        test_circuit.append(
            HGate(),
            [1]
        )
        test_circuit.append(
            HGate(),
            [2]
        )
        # Declares the goal matrix
        goal_matrix = [[math.inf, math.inf],
                       [math.inf, -math.inf]]
        
        # Asserts that the fitness (difference between the goal and created circuit)
        # is as expected
        fitness = circuit_fitness(test_circuit, gate_set, goal_matrix, 2)
        self.AssertRaises(TypeError)

    # Erroneous tests - testing the the fitness function against erroneous circuits
    def test_circuit_fitness_erroneous1(self):
        """Tests circuit_fitness with an invalid 2 qubit circuit"""
        # Creates a valid 2 qubit circuit with an HGate on either qubit
        gate_set = {1: HGate()}
        test_circuit = QuantumCircuit(2)
        test_circuit.append(
            HGate(),
            [1]
        )
        test_circuit.append(
            HGate(),
            [2]
        )
        # Declares the goal matrix
        goal_matrix = [[1, 1],
                       [1, 1]]
        
        # Asserts that the fitness (difference between the goal and created circuit)
        # is as expected
        fitness = circuit_fitness(test_circuit, gate_set, goal_matrix, 2)
        self.AssertRaises(TypeError)
    
    def test_circuit_fitness_erroneous1(self):
        """Tests circuit_fitness with an invalid circuit"""
        """Tests circuit_fitness with an invalid 2 qubit circuit"""
        # Creates a valid 2 qubit circuit with an HGate on either qubit
        gate_set = {1: HGate()}
        test_circuit = QuantumCircuit(2)
        test_circuit.append(
            HGate(),
            [1]
        )
        test_circuit.append(
            CZGate(),
            [2]
        )
        # Declares the goal matrix
        goal_matrix = [[math.inf() + 1, 1],
                       [1, 1]]
        
        # Asserts that the fitness (difference between the goal and created circuit)
        # is as expected
        fitness = circuit_fitness(test_circuit, gate_set, goal_matrix, 2)
        self.AssertRaises(TypeError)

    # Valid tests - testing all types of valid values
    def test_circuit_fitness_valid1(self):
        """Tests circuit_fitness with a valid 2 qubit circuit"""
        # Creates a valid 2 qubit circuit with an HGate on either qubit
        gate_set = {1: HGate()}
        test_circuit = QuantumCircuit(2)
        test_circuit.append(
            HGate(),
            [1]
        )
        test_circuit.append(
            HGate(),
            [2]
        )
        # Declares the goal matrix
        goal_matrix = [[1, 1],
                       [1, 1]]
        
        # Asserts that the fitness (difference between the goal and created circuit)
        # is as expected
        fitness = circuit_fitness(test_circuit, gate_set, goal_matrix, 2)
        self.AssertTrue(fitness==(2/math.sqrt(2)))

    def test_circuit_fitness_valid1(self):
        """Tests circuit_fitness with a valid 3 qubit circuit"""
        gate_set = {1: HGate()}
        test_circuit = QuantumCircuit(3)
        test_circuit.append(
            HGate(),
            [1]
        )
        test_circuit.append(
            HGate(),
            [2]
        )
        test_circuit.append(
            HGate(),
            [3]
        )

        # Declares the goal matrix
        goal_matrix = [[1,1,1],
                       [1,1,1],
                       [1,1,1]]
        
        # Asserts that the fitness value is as expected
        fitness = circuit_fitness(test_circuit, gate_set, goal_matrix, 3)
        self.AssertTrue(fitness==(2/math.sqrt(2)))

    def test_circuit_fitness_valid1(self):
        """Tests circuit_fitness with a valid 4 qubit circuit"""
        gate_set = {1: HGate()}
        test_circuit = QuantumCircuit(4)
        test_circuit.append(
            HGate(),
            [1]
        )
        test_circuit.append(
            HGate(),
            [2]
        )
        test_circuit.append(
            HGate(),
            [3]
        )
        test_circuit.append(
            HGate(),
            [4]
        )

        # Declares the goal matrix
        goal_matrix = [[1,1,1,1],
                       [1,1,1,1],
                       [1,1,1,1],
                       [1,1,1,1]]
        
        # Asserts that the fitness value is as expected
        fitness = circuit_fitness(test_circuit, gate_set, goal_matrix, 4)
        self.AssertTrue(fitness==(2/math.sqrt(2)))


def main_circuit_fitness():
    """Enables this test to be included in the test suite and to run each of the unit tests"""
    unittest.main()

if __name__ == "__main__":
    main_circuit_fitness()