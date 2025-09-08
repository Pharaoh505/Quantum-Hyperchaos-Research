import numpy as np
from scipy.linalg import eigvals

def _clean_eigs(mat):
    vals = eigvals(mat)
    vals = np.real_if_close(vals)
    vals = np.clip(vals, 0, None)
    return vals

def von_neumann_entropy(rho, base=2.0):
    r = np.asarray(rho, dtype=complex)
    vals = _clean_eigs(r)
    vals = vals[vals > 1e-12]
    if vals.size == 0:
        return 0.0
    logs = np.log(vals)
    if base != np.e:
        logs = logs / np.log(base)
    return float(-np.sum(vals * logs))

def partial_trace_2qubit(rho4, subsystem=0):
    r = np.asarray(rho4, dtype=complex)
    if r.shape != (4,4):
        raise ValueError("needs 4x4")
    rsh = r.reshape(2,2,2,2)
    if subsystem == 0:
        return np.trace(rsh, axis1=0, axis2=2)
    if subsystem == 1:
        return np.trace(rsh, axis1=1, axis2=3)
    raise ValueError("subsystem must be 0 or 1")

def concurrence(rho4):
    rho = np.asarray(rho4, dtype=complex)
    sigma_y = np.array([[0, -1j],[1j,0]], dtype=complex)
    Y = np.kron(sigma_y, sigma_y)
    rho_t = Y @ rho.conj() @ Y
    R = rho @ rho_t
    vals = eigvals(R)
    vals = np.real_if_close(vals)
    vals = np.clip(vals, 0, None)
    s = np.sqrt(vals)
    s_sorted = np.sort(s)[::-1]
    s_padded = s_sorted
    if s_padded.size < 4:
        s_padded = np.pad(s_padded, (0, 4 - s_padded.size))
    C = max(0.0, float(s_padded[0] - s_padded[1] - s_padded[2] - s_padded[3]))
    return min(1.0, C)