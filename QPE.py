import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate, UnitaryGate
from qiskit.quantum_info import Statevector


def apply_controlUs(qc, control_qubits, target_bit, U):
    """Apply controlled powers of a supplied unitary U."""
    for idx, qubit in enumerate(control_qubits):
        U_power = np.linalg.matrix_power(U, 2**idx)
        controlled_U = UnitaryGate(U_power).control(1)
        qc.append(controlled_U, [qubit, target_bit])

def print_control_probs(qc, control_qubits):
    probabilities = Statevector.from_instruction(qc).probabilities_dict(
        qargs=control_qubits
    )

    for state, probability in probabilities.items():
        print(f"{state}: {probability:.4f}")
    
def print_max_control_prob(qc, control_qubits):
    probabilities = Statevector.from_instruction(qc).probabilities_dict(
            qargs=control_qubits
    )

    key, value = max(probabilities.items(), key=lambda x: x[1])

    j = int(key, 2)

    print("Most likey phase estimate is:", f"{j}/{2**len(control_qubits)}")
    print("with probability", value)
    

# Specify inputs
control_qubit_counts = [3, 5, 8]
U = np.array([
    [1, 0],
    [0, np.exp(2j * np.pi / 3)]
], dtype=complex)

for num_control_qubits in control_qubit_counts:
    idx_target = num_control_qubits
    idx_controls = range(num_control_qubits)

    # Initialise circuit
    qc = QuantumCircuit(num_control_qubits+1)

    # Prepare target in |1>
    qc.x(idx_target)

    # Apply Hadamard to 3 control qubits
    qc.h(idx_controls)

    # Apply controlled-U, -U^2 and-U^4
    apply_controlUs(qc,idx_controls, idx_target, U)

    # Apply inverse QFT
    qft_gate = QFTGate(num_qubits=num_control_qubits)
    iqft_block = qft_gate.inverse()
    qc.append(iqft_block, idx_controls)


    # Print control probabilities
    #print_control_probs(qc, idx_controls)
    print_max_control_prob(qc, idx_controls)


