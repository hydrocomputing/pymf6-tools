"""Run ex-gwf-advtidal controlled."""

import sys

from pymf6.mf6 import MF6


def run(sim_path):
    """Run."""
    adv = MF6(sim_path=sim_path, do_solution_loop=False)
    gwf_models = adv.models['gwf6']
    gwf = gwf_models['ex-gwf-advtidal']
    loop = adv.model_loop()
    for _ in loop:
        if gwf.kper > 2:
            break
    wel = gwf.packages.wel.as_mutable_bc()
    q = wel.q
    q.loc[4] = -40
    wel.q = q
    for _ in loop:
        pass


if __name__ == '__main__':
    run(sys.argv[1])
