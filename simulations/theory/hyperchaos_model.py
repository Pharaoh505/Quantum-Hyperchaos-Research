import numpy as np

class HyperchaoticRossler:
    def __init__(self):
        self.params = {'a': 0.25, 'b': 3, 'c': 0.5, 'd': 0.05}
    
    def equations(self, t, state):
        x, y, z, w = state
        dx = -y - z
        dy = x + self.params['a']*y + w
        dz = self.params['b'] + x*z
        dw = -self.params['c']*z + self.params['d']*w
        return np.array([dx, dy, dz, dw])

if __name__ == "__main__":
    print("Testing hyperchaotic model...")
    model = HyperchaoticRossler()
    print("Derivatives at t=0:", model.equations(0, [0.1, 0, 0, 0]))