import numpy as np
from analysis.entanglement_metrics import concurrence, partial_trace_2qubit, von_neumann_entropy

def test_bell():
    psi = np.zeros((4,), dtype=complex)
    psi[0] = 1.0/np.sqrt(2)
    psi[3] = 1.0/np.sqrt(2)
    rho = np.outer(psi, psi.conj())
    C = concurrence(rho)
    assert C > 0.99
    rA = partial_trace_2qubit(rho, subsystem=1)
    S = von_neumann_entropy(rA, base=2.0)
    assert abs(S - 1.0) < 1e-6