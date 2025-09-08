import numpy as np
from scipy.integrate import solve_ivp

sig_x = np.array([[0,1],[1,0]], dtype=complex)
sig_y = np.array([[0,-1j],[1j,0]], dtype=complex)
sig_z = np.array([[1,0],[0,-1]], dtype=complex)
sig_minus = np.array([[0,0],[1,0]], dtype=complex)

def _to_vec(rho):
    f = rho.ravel(order='C')
    return np.concatenate([f.real, f.imag])

def _to_rho(v):
    r = v[:4] + 1j * v[4:]
    return r.reshape((2,2), order='C')

def _comm(A,B):
    return A @ B - B @ A

def _lind(rho, ops, rates):
    L = np.zeros_like(rho, dtype=complex)
    for C,g in zip(ops, rates):
        if g == 0:
            continue
        CdC = C.conj().T @ C
        L += g * (C @ rho @ C.conj().T - 0.5 * (CdC @ rho + rho @ CdC))
    return L

def _rhs_maker(tarr, darr, H0, V, ops, rates):
    def f(tt, y):
        rho = _to_rho(y)
        A = np.interp(tt, tarr, darr)
        Ht = H0 + A * V
        dr = -1j * _comm(Ht, rho)
        if ops and any(rr > 0 for rr in rates):
            dr += _lind(rho, ops, rates)
        return _to_vec(dr)
    return f

def run_time_dependent_simulation(t_array, drive_array, H0=None, V=None, gamma_relax=0.0, gamma_dephase=0.0, rho0=None, rtol=1e-7, atol=1e-9):
    t_array = np.asarray(t_array)
    drive_array = np.asarray(drive_array)
    if H0 is None:
        H0 = 0.5 * sig_z
    if V is None:
        V = 0.7 * sig_x
    ops = []
    rates = []
    if gamma_relax > 0:
        ops.append(sig_minus)
        rates.append(gamma_relax)
    if gamma_dephase > 0:
        ops.append(sig_z)
        rates.append(gamma_dephase)
    if rho0 is None:
        rho0 = np.array([[1.0,0.0],[0.0,0.0]], dtype=complex)
    y0 = _to_vec(rho0)
    rhs = _rhs_maker(t_array, drive_array, H0, V, ops, rates)
    sol = solve_ivp(rhs, (t_array[0], t_array[-1]), y0, t_eval=t_array, method='RK45', rtol=rtol, atol=atol)
    if not sol.success:
        raise RuntimeError(sol.message)
    rhos = np.stack([_to_rho(col) for col in sol.y.T], axis=0)
    ex = np.real([np.trace(r @ sig_x) for r in rhos])
    ey = np.real([np.trace(r @ sig_y) for r in rhos])
    ez = np.real([np.trace(r @ sig_z) for r in rhos])
    purity = np.real([np.trace(r @ r) for r in rhos])
    l1 = [float(np.sum(np.abs(r - np.diag(np.diag(r))))) for r in rhos]
    return {"t": t_array, "rhos": rhos, "expect_x": np.array(ex), "expect_y": np.array(ey), "expect_z": np.array(ez), "purity": np.array(purity), "l1_coherence": np.array(l1)}