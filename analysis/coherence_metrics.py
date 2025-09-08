import numpy as np

def purity(rho):
    r = np.asarray(rho, dtype=complex)
    return float(np.real_if_close(np.trace(r @ r)))

def l1_coherence(rho):
    a = np.asarray(rho, dtype=complex)
    off = a.copy()
    np.fill_diagonal(off, 0)
    return float(np.sum(np.abs(off)))

def coherence_half_time(times, coh):
    t = np.asarray(times)
    c = np.asarray(coh)
    if c.size == 0:
        return float('inf')
    half = c[0] / 2.0
    idx = np.where(c <= half)[0]
    return float(t[idx[0]]) if idx.size > 0 else float('inf')