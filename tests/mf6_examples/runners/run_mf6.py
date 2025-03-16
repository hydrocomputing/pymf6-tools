"""Run plain MODFLOW 6."""


from contextlib import chdir
from subprocess import run, CalledProcessError

from pymf6_tools.mf6examples.process_runner import run_func


def run_model(sim_path, exe_path='mf6', dll_path=None):
    """Run one MF6 model."""
    with chdir(sim_path):
        ret = run([exe_path], capture_output=True, encoding='utf-8')
    if ret.returncode != 0:
        raise Exception(ret.stderr + ret.stdout)

if __name__ == '__main__':
    run_func(run_model)