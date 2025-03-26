"""Run ex-gwf-advtidal controlled."""

import sys

from pymf6.mf6 import MF6


def run(sim_path):
    """Run."""
    for _ in MF6(sim_path=sim_path).model_loop():
        pass


if __name__ == '__main__':
    run(sys.argv[1])
