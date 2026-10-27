import numpy as np

# Create computational basis vectors
psi_zero = np.array([1, 0])
psi_one = np.array([0, 1])

# Define Hadamard & Pauli-X matrices
hadamard = 1/np.sqrt(2)*np.array([[1, 1], [1, -1]])
pauli_X = np.array([[0, 1], [1, 0]])

# Test on psi_zero
H0 = hadamard@psi_zero
X0 = pauli_X@psi_zero
HH0 = hadamard@hadamard@psi_zero

#Verify HH0
print(np.allclose(HH0,psi_zero))

# Two qubits
psi_00 = np.kron(psi_zero, psi_zero)
psi_10 = np.kron(psi_one, psi_zero)

# Construct H tensor product I
HI = np.kron(hadamard, np.identity(2))

HI00 = HI@psi_00
probs = np.abs(HI00)**2

# Complex amplitudes
psi = 1/np.sqrt(2)*np.array([1, 0, 0, 1j])

psi_probs = np.abs(psi)**2
print(np.allclose(1, np.sum(psi_probs)))
print(psi_probs)


