from itertools import product

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from scipy.optimize import minimize


def cut_value(bits, edges):
    """ Given bits and edges determine cut value"""
    cut = 0
    for edge in edges:
        xi = bits[edge[0]]
        xj = bits[edge[1]]
        cut += xi + xj - 2*xi*xj
    return cut

def brute_max_cut(edges, n):
    """Use brute force to determine max cut and optimal bit values
    given edges and number of vertices, n,"""
    max_cut = -1
    for bits in product([0,1], repeat=n):
        # Evaluate the cut
        cut = cut_value(bits,edges)
        if cut> max_cut:
            max_cut = cut
            best_bits = bits
        
    return max_cut, best_bits

def qaoa_circuit(gamma, beta, edges, n=4):
    """Create quantum circuit for QAOA where p=1 """
    qc = QuantumCircuit(n)
    qubits = range(n)

    # Apply Hadamard gates to obtain equal superposition of states
    qc.h(qubits)

    # Apply ZZ rotation for every edge
    for edge in edges:
        qc.rzz(-gamma, edge[0], edge[1])

    # Apply mixing operator to qubits
    qc.rx(2*beta, qubits)

    return qc

def bitstring_probabilities(gamma, beta, edges, n):
    """Given gamma, beta, edges, and number of vertices, n, 
    determine each bitstring probability"""
    qc = qaoa_circuit(gamma, beta, edges, n)
    sv = Statevector.from_instruction(qc)
    probabilities = sv.probabilities_dict()

    return probabilities

def expected_cut(bitstring_probabilities, edges):
    """ From cut probabilities calculate expected cut"""
    cut_count = 0
    for bitstring, prob in bitstring_probabilities.items():
        bits = [int(bit) for bit in bitstring[::-1]]
        cut = cut_value(bits, edges)
        cut_count += prob*cut

    return cut_count

def maxcut_probability(bitstring_probabilities, maxcut, edges):
    """From cut probabilities and maxcut determine
    probability of obtaining maxcut value"""
    maxcut_prob = 0
    for bitstring, prob in bitstring_probabilities.items():
        bits = [int(bit) for bit in bitstring[::-1]]
        cut = cut_value(bits, edges)
        if cut == maxcut:
            maxcut_prob += prob

    return maxcut_prob


def objective(params, edges, n):
    gamma, beta = params
    cut_probs = bitstring_probabilities(gamma, beta, edges, n)
    return -expected_cut(cut_probs, edges)

def run_tests():
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (0, 3)]
    n = 4

    bit_max = [0,1,1,0]
    assert cut_value(bit_max,edges) == 4, (
        f"For bits {bit_max} cut_value does not equal 4"
    )

    bit_zero = [0,0,0,0]
    assert cut_value(bit_zero,edges) == 0, (
            f"For bits {bit_zero} cut_value does not equal 0"
        )

    max_cut, best_bits = brute_max_cut(edges, n)
    assert max_cut == 4, (
        f"brute_max_cut does not return max_cut=4 for edges={edges} and n={4}"
    )
    assert cut_value(best_bits, edges) == 4, (
        "brute_max_cut does not return optimal bits")

    bit_probs = bitstring_probabilities(0.5, 0.3, edges, n)
    assert np.allclose(sum(bit_probs.values()),1), (
        "bitstring_probabilties do not sum to 1"
    )

    uniform_probs = bitstring_probabilities(0, 0, edges, n)
    assert np.allclose(expected_cut(uniform_probs, edges), 2.5), (
        "bitstring_probabilities failed with uniform baseline"
    )
    assert np.allclose(maxcut_probability(uniform_probs, max_cut, edges),0.125),(
        "maxcut_probability failed with uniform baseline"
    )

    qaoa_probs = bitstring_probabilities(0.5, 0.3, edges, n)
    assert expected_cut(qaoa_probs, edges) > 2.5, (
    "QAOA expected cut does not exceed random baseline"
    )

    print("All tests passed")


def main():
    # Inputs
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (0, 3)]
    n= 4

    
    max_cut, best_bits = brute_max_cut(edges, n)

    print("\n--- Max-Cut benchmark ---")
    print(f"Vertices: {n}")
    print(f"Edges: {len(edges)}")
    print(f"Exact maximum cut: {max_cut}")
    print(f"One optimal assignment: {best_bits}")
    print(f"Random baseline (expected cut): {len(edges)/2:.4f}")

    # Find max cut using QAOA
    result = minimize(objective, x0 = [0.5, 0.3], args=(edges,n), method="COBYLA")
    gamma_opt, beta_opt = result.x

    cut_prob_opt = bitstring_probabilities(gamma_opt, beta_opt, edges, n)
    cut_expect = expected_cut(cut_prob_opt, edges)
    maxcut_prob = maxcut_probability(cut_prob_opt, max_cut, edges)

    print("\n--- QAOA results (p=1) ---")
    print(f"Optimised gamma: {gamma_opt:.4f}")
    print(f"Optimised beta:  {beta_opt:.4f}")
    print(f"Expected cut: {cut_expect:.4f}")
    print(f"Probability of optimal cut: {maxcut_prob:.1%}")

    # Assess impact of starting position on output
    n_restarts = 10
    rng = np.random.default_rng(0)

    opt_output = []
    for i in range(n_restarts):
        gamma0 = rng.uniform(0, 2*pi)
        beta0 = rng.uniform(0, pi)

        result = minimize(objective, x0 = [gamma0, beta0], args=(edges,n), method="COBYLA")
        cut = -result.fun
        function_evals = result.nfev

        opt_output.append((cut, function_evals))

    print("\n--- Random restarts ---")
    for i, (cut, evaluations) in enumerate(opt_output, start=1):
        print(f"Run {i:2d}: Expected cut = {cut:.4f}, "
              f"Evaluations = {evaluations}")

    # Fully explore optimisation landscape
    gamma_points = np.linspace(0, 2*pi, num=50, endpoint=False)
    beta_points = np.linspace(0, pi, num=50, endpoint=False)

    cuts = []
    for gamma in gamma_points:
        for beta in beta_points:
            cut_probs = bitstring_probabilities(gamma, beta, edges, n)
            cut = expected_cut(cut_probs, edges)
            cuts.append(cut)


    # Plot heatmap
    gamma_grid, beta_grid = np.meshgrid(gamma_points, beta_points)
    cuts_2d = np.array(cuts).reshape(len(gamma_points), len(beta_points)).T
    plt.figure(figsize=(8, 6))


    heatmap = plt.pcolormesh(gamma_grid, beta_grid, cuts_2d, shading="auto", cmap="viridis")

    # Add visual aids
    plt.colorbar(heatmap, label="Expected cut value")
    plt.xlabel("Parameter gamma0")
    plt.ylabel("Parameter beta0")
    plt.title("2D Heatmap: Expected cut value")

    plt.show()

if __name__ == "__main__":
    run_tests()
    main()




