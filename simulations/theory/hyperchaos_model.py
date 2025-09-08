import numpy as np
from scipy.integrate import solve_ivp

def lorenz(t, vec, s=10.0, r=28.0, b=8.0/3.0):
    x, y, z = vec
    return [s * (y - x), x * (r - z) - y, x * y - b * z]

def rossler(t, vec, a=0.2, b=0.2, c=5.7):
    x, y, z = vec
    return [-y - z, x + a * y, b + z * (x - c)]

def integrate_driver(fn, start, span, step, args=()):
    tgrid = np.arange(span[0], span[1] + 1e-12, step)
    sol = solve_ivp(lambda tt, yy: fn(tt, yy, *args), span, start, t_eval=tgrid, method='RK45', rtol=1e-8)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.t, sol.y

def normalize(s):
    arr = np.asarray(s, dtype=float)
    m = arr.mean()
    sd = arr.std()
    if sd == 0:
        return arr - m
    return (arr - m) / (sd + 1e-12)