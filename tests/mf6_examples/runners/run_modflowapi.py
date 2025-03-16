"""Run modflowapi."""

from contextlib import redirect_stdout
import os

import modflowapi

from pymf6_tools.mf6examples.process_runner import run_func


def callback(sim, callback_step):
    """Empty."""


def run_model(sim_path, exe_path=None, dll_path=None):
    """Run modflowapi."""
    modflowapi.run_simulation(
        dll=dll_path, sim_path=sim_path, callback=callback
    )


if __name__ == '__main__':
    run_func(run_model)
