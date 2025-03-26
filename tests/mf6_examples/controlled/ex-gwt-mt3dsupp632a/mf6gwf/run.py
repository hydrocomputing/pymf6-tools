"""Run ex-gwf-advtidal controlled."""

import sys

from pymf6.mf6 import MF6


def run(sim_path):
    """Run."""
    sim = MF6(sim_path=sim_path, do_solution_loop=False)
    gwf_models = sim.models['gwf6']
    gwf = gwf_models['flow']
    loop = sim.model_loop()
    for _ in loop:
        if gwf.kper > 0:
            break
    wel = gwf.packages.get_package('wel-1').as_mutable_bc()
    wel.q = 0.06
    for _ in loop:
        pass

if __name__ == '__main__':
    run(sys.argv[1])
