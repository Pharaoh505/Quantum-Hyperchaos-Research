import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from simulations.theory.hyperchaos_model import integrate_driver, normalize, lorenz
from simulations.qubit_dynamics import run_time_dependent_simulation
from analysis.plot import plot_summary, animate_bloch, animate_bloch_sphere

def demo_run(duration=8.0, dt=0.002, amp=1.0, gamma_relax=0.0, gamma_dephase=0.0, outdir='results'):
    t, y = integrate_driver(lorenz, start=[1.0, 1.0, 1.0], span=(0.0, duration), step=dt)
    drive = normalize(y[0]) * amp
    res = run_time_dependent_simulation(
        t, drive, gamma_relax=gamma_relax, gamma_dephase=gamma_dephase
    )
    os.makedirs(outdir, exist_ok=True)
    np.savez_compressed(
        os.path.join(outdir, 'demo.npz'),
        t=res['t'],
        drive=drive,
        expect_x=res['expect_x'],
        expect_y=res['expect_y'],
        expect_z=res['expect_z'],
        purity=res['purity'],
        l1=res['l1_coherence']
    )

 
    img = plot_summary(
        res['t'], drive, res['expect_x'], res['expect_y'], res['expect_z'],
        res['purity'], res['l1_coherence'], save_dir=outdir
    )
 
    animate_bloch(res['t'], res['expect_x'], res['expect_y'], res['expect_z'], save_dir=outdir)
    animate_bloch_sphere(res['expect_x'], res['expect_y'], res['expect_z'], save_dir=outdir)

    return os.path.join(outdir, 'demo.npz'), img

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--duration', type=float, default=8.0)
    p.add_argument('--dt', type=float, default=0.002)
    p.add_argument('--amp', type=float, default=1.0)
    p.add_argument('--gamma_relax', type=float, default=0.0)
    p.add_argument('--gamma_dephase', type=float, default=0.0)
    p.add_argument('--outdir', type=str, default='results')
    args = p.parse_args()
    demo_run(
        duration=args.duration, dt=args.dt, amp=args.amp,
        gamma_relax=args.gamma_relax, gamma_dephase=args.gamma_dephase,
        outdir=args.outdir
    )