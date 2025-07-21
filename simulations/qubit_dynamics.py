from qutip import basis, sigmaz, mesolve
from theory.hyperchaos_model import HyperchaoticRossler
from scipy.integrate import solve_ivp
import numpy as np

def simulate():
    model = HyperchaoticRossler()
    psi0 = basis(2, 0)
    times = np.linspace(0, 10, 1000)
    
    def H(t, args):
        sol = solve_ivp(model.equations, [t, t+0.1], [0.1, 0, 0, 0], t_eval=[t])
        return sigmaz() * sol.y[0][0] * 0.5
    
    result = mesolve(H, psi0, times, [], [])
    print("Simulation successful")
    return result.states

if __name__ == "__main__":
    simulate()