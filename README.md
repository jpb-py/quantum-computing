# Quantum Computing — Python and Qiskit Projects

A collection of Python implementations exploring quantum computing concepts and algorithms, developed through independent study.

The focus is on understanding the underlying mathematics, implementing quantum circuits, and verifying their behaviour through simulation and comparison with theoretical or classical results.

## Projects

### Quantum Fundamentals and Introductory Algorithms (intro_algorithms.py)

Explores quantum superposition, entanglement, interference and introductory quantum algorithms through five small circuits:

Bell pair: Prepares the entangled state ((|00\rangle+|11\rangle)/\sqrt2).
Interference: Demonstrates how relative phase changes can produce deterministic measurement outcomes.
Second Bell state: Prepares the entangled state ((|01\rangle+|10\rangle)/\sqrt2).
Deutsch's algorithm: Implements a balanced oracle and demonstrates phase kickback.
Bernstein–Vazirani: Implements a simple hidden-bitstring oracle.

Each circuit is displayed and inspected using statevector amplitudes and simulated measurement counts.

### 2. Grover's Algorithm (`grover.py`)

Implements Grover's search algorithm for a two-qubit search space.
- Constructs a configurable phase oracle to mark any of the four computational-basis states.
- Implements the diffusion operator for amplitude amplification.
- Applies a single Grover iteration, sufficient to identify one marked state among four possibilities.
- Uses Qiskit's statevector simulator to verify the results, with automated assertions checking that the marked state has probability 1 for all four possible targets.

### 3. Quantum Phase Estimation (`QPE.py`)

Implements quantum phase estimation (QPE) to estimate the eigenphase of a unitary operator.

- Defines a single-qubit unitary matrix and constructs its controlled powers using Qiskit.
- Uses the target eigenstate \(|1\rangle\), with an expected eigenphase of \(1/4\).
- Applies Qiskit's inverse quantum Fourier transform to extract the phase estimate.
- Compares results using 3, 5 and 8 control qubits to investigate measurement precision.
- Reports the most probable phase estimate and its measurement probability using ideal statevector simulation.

### 4. QAOA for Max-Cut

Implements a single-layer (\(p=1\)) Quantum Approximate Optimisation Algorithm (QAOA) for a small Max-Cut problem.

**Method**

- Formulates Max-Cut as a quadratic binary optimisation problem.
- Constructs the corresponding cost Hamiltonian using Pauli-Z interactions.
- Implements parameterised cost and mixing unitaries in Qiskit.
- Uses SciPy's COBYLA optimiser to maximise the expected cut value.
- Compares results against exhaustive classical optimisation and random sampling.
- Investigates sensitivity to initial parameters and visualises the optimisation landscape.

**Results**

For a four-vertex graph with five edges:

| Metric | Result |
|---|---:|
| Exact maximum cut | 4 |
| Random sampling — expected cut | 2.500 |
| QAOA — best expected cut found | 3.237 |
| Random sampling — optimal-cut probability | 12.5% |
| QAOA — optimal-cut probability | 32.8% |

Multiple optimiser starting points converge to different local optima, demonstrating that classical parameter optimisation is an important part of the hybrid algorithm.

**Limitations**

The experiments use ideal statevector simulation without hardware noise or finite-shot sampling. The graph is small enough to solve trivially by exhaustive classical search.

The results illustrate QAOA's operation and its performance relative to random sampling.

## Tools

Python, Qiskit, NumPy, SciPy and Matplotlib.

