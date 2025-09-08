from simulations.theory.hyperchaos_model import integrate_driver, lorenz

def test_short():
    t, y = integrate_driver(lorenz, start=[1,1,1], span=(0,0.2), step=0.05)
    assert t.shape[0] == y.shape[1]
    assert y.shape[0] == 3