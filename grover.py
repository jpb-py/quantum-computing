from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def apply_oracle(qc, target):
    """
    Apply a two-qubit phase oracle for the specified target.

    target: a string such as '00', '01', '10' or '11'.
    Oracle flips phase of the target state
    """
    if target not in ('00', '01', '10', '11'):
        raise ValueError("Target must be a two-bit binary string")
    
    # Flip the string to get in Qiskit ordering
    target_reverse = target[::-1]
    for index, element in enumerate(target_reverse):
        if element == '0':
            qc.x(index)

    qc.cz(0,1)

    for index, element in enumerate(target_reverse):
        if element == '0':
            qc.x(index)

    print("Oracle applied on", target)

def apply_diffusion(qc):
    """
    Apply diffuser that reflects the amplitudes about their average - 
    increasing the target state's amplitude while decreasing others
    """
    qc.h([0, 1])
    qc.x([0,1])
    qc.cz(0,1)
    qc.x([0,1])
    qc.h([0,1])



targets = ['00', '01', '10', '11']

for target in targets:
    print("Building Grover circuit with target", target)
    qc = QuantumCircuit(2)

    # Initialise
    qc.h([0,1])

    #Oracle
    apply_oracle(qc,target)

    #Diffusion
    apply_diffusion(qc)

    #print(qc.draw())
    state = Statevector.from_instruction(qc)
    prob_target = state.probabilities_dict()[target]
    print("Target probability:", prob_target)

    assert abs(prob_target - 1.0) < 1e-10, (
        f"Grover failed for target {target}: P={prob_target}"
    )


