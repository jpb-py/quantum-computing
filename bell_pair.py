

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def test_circuit(name, circuit, shots=1000):
    """Display a circuit, statevector and measurement counts."""
    print(f"\n--- {name} ---")
    print(circuit.draw())

    state = Statevector.from_instruction(circuit)

    for basis, amplitude in state.to_dict().items():
        print(f"|{basis}>: {amplitude.real:.4f} {amplitude.imag:+.4f}j")

    print("Counts:", state.sample_counts(shots=shots))


# Circuit 1: Bell pair
qc1 = QuantumCircuit(2)
qc1.h(0)
qc1.cx(0, 1)

test_circuit("Bell pair", qc1)


# Circuit 2: Interference
qc2 = QuantumCircuit(2)
qc2.h(0)
qc2.z(0)
qc2.h(0)

test_circuit("Interference", qc2)


# Circuit 3: Bell state
qc3 = QuantumCircuit(2)
qc3.h(0)
qc3.x(1)
qc3.cx(0,1)

test_circuit("Bell states", qc3)

# Circuit 4: Deutsch's algorithm
qc4 = QuantumCircuit(2)
qc4.x(1)
qc4.h(0)
qc4.h(1)

qc4.cx(0,1)
qc4.h(0)

test_circuit("Deutsch algorithm", qc4)

# Circuit 5: Bernstein -Vazirani
qc5 = QuantumCircuit(3)
qc5.x(2)
qc5.h([0, 1, 2])
qc5.cx(1,2)
qc5.h(0)
qc5.h(1)

test_circuit("Bernstein-Vazirani", qc5)