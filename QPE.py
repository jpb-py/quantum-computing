from numpy import pi
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit.quantum_info import Statevector
from fractions import Fraction



def apply_controlUs(qc, control_qubits, target_bit, theta):
    ''' Applies control-U operations on target_bit 
    given specified theta and control qubits, control qubits 
    must be supplied in least-significant-bit-first-order e.g [0, 1, 2]'''
    for idx, qubit in enumerate(control_qubits):
        qc.cp(2*pi*theta*2**idx, qubit, target_bit)

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

    key_reversed = key[::-1]
    j = 0
    for idx, char in enumerate(key_reversed):
        j += 2**(idx*float(char))*float(char)

    print("Most likey phase estimate is:", f"{j}/{2**len(control_qubits)}")
    print("with probability", value)
    
   
   
   
    

# Specify inputs
control_qubits = [3, 5, 8]
theta = 1/3

for num_control_qubits in control_qubits:
    idx_target = num_control_qubits
    idx_controls = range(num_control_qubits)

    # Initialise circuit
    qc = QuantumCircuit(num_control_qubits+1)

    # Prepare target in |1>
    qc.x(idx_target)

    # Apply Hadamard to 3 control qubits
    qc.h(idx_controls)

    # Apply controlled-U, -U^2 and-U^4
    apply_controlUs(qc,idx_controls, idx_target, theta)

    # Apply inverse QFT
    qft_gate = QFTGate(num_qubits=num_control_qubits)
    iqft_block = qft_gate.inverse()
    qc.append(iqft_block, idx_controls)


    # Print control probabilities
    #print_control_probs(qc, idx_controls)
    print_max_control_prob(qc, idx_controls)


